import logging
import os
import re
import sys
import traceback
import yaml

from sanitize import sanitize
from recursivedefaultdict import recursivedefaultdict
import env
import json
import local
from to_xml import to_xml

from google.appengine.api import users, memcache
from google.appengine.api.datastore_errors import NeedIndexError
from google.appengine.ext.webapp import template, RequestHandler


class NotFoundException(Exception):
  pass


class MegaeraRequestHandler(RequestHandler):
  # These constants are used to locate the default templates.
  HANDLERS_BASE = 'handlers'
  TEMPLATES_BASE = 'templates'
  
  def __init__(self):
    self.__response_dict__ = recursivedefaultdict()
  
  @classmethod
  def with_page(cls, page):
    if isinstance(page, str):
      __import__(page)
      page = sys.modules[page]
    return type(page.__file__, (cls,), dict(page=page))
  
  def response_dict(self, **kwargs):
    """Returns the response dictionary and sets the given values."""
    if kwargs:
      self.__response_dict__.update(**kwargs)
    return self.__response_dict__
  
  def url_args(self):
    """Returns the URL arguments in the WSGI paths."""
    return self.__url_args__
  
  def url_arg(self, index):
    """Returns the URL arg at the given index or None."""
    args = self.url_args()
    if args and 0 <= index < len(args):
       return args[index]
    
  def get(self, *args):
    """Responds to GET requests from WSGIApplication."""
    if self.has_param('post'):
      return self.post(*args)
    # check for trailing slashes
    match = re.compile('^(/.*[^/])/+$').search(self.request.path)
    if match and match.groups(1):
      # strip trailing slashes and redirect
      return self.redirect(match.group(1))
    # check if we can respond
    if hasattr(self.page, 'get'):
      # run the handler and get the template path
      path = self.handle(self.page.get, *args)
    else:
      # return with 405
      path = self.not_found(status=405)
    # render the template
    if self.is_atom():
      # for atom
      self.response.headers['Content-Type'] = "application/atom+xml; charset=UTF-8"
      self.render(path, 'atom')
    else:
      # for html
      self.render(path)
  
  def post(self, *args):
    """Responds to POST requests from WSGIApplication"""
    self.__url_args__ = args
    # check if we can post
    if hasattr(self.page, 'post'):
      # run the handler and get the template path
      path = self.handle(self.page.post, *args)
    else:
      # return with 405
      path = self.not_found(status=405)
    # if we encountered errors, run the get handler
    if self.has_errors():
      self.get(*args)
    else:
      # otherwise render the template
      self.render(path)
  
  def has_errors(self):
    """Returns if the response dictionary contains form errors."""
    return 'errors' in self.response_dict()
  
  def is_admin(self):
    """Returns if the current user is an admin."""
    return users.is_current_user_admin()
  
  def has_param(self, param):
    return len(self.request.get_all(param)) > 0
  
  def is_json(self):
    """Returns if the current request is for JSON."""
    return self.has_param('json')
  
  def is_yaml(self):
    """Returns if the current request is for YAML."""
    return self.has_param('yaml')
  
  def is_xml(self):
    """Returns if the current request is for XML."""
    return self.has_param('xml')
  
  def is_atom(self):
    """Returns if the current request is for Atom."""
    return self.has_param('atom')
  
  def logout_url(self):
    """Returns the logout URL of the current request."""
    return users.create_logout_url(self.request.uri)
  
  def login_url(self):
    """Returns the login URL of the current request."""
    return users.create_login_url(self.request.uri)
  
  def host(self):
    """Returns the current host's name."""
    return os.environ.get('HTTP_HOST')
  
  def cache_key(self, page=None, vary=None):
    page_name = self.page_name(page=page)
    return '-'.join([str(x) for x in (page_name, vary) if x])
  
  def cached(self, vary=None):
    """Returns if the current page is cached and updates the response dict with the cached values."""
    if self.has_param('no_cache'):
      return
    cached = memcache.get(
      key=self.cache_key(vary=vary),
      namespace="handler-cache")
    if cached:
      # update the response
      self.response_dict(**cached)
      return True
  
  def cache(self, time=0, vary=None, **kwargs):
    """Caches and updates the response dict with the given values for the current page."""
    memcache.set(
      key=self.cache_key(vary=vary),
      value=kwargs,
      time=time,
      namespace="handler-cache")
    # update the response
    self.response_dict(**kwargs)
  
  def invalidate(self, page=None, vary=None):
    """Invalidates the cache for given page or the current page."""
    memcache.delete(
      key=self.cache_key(vary=vary, page=page),
      namespace="handler-cache")
  
  def page_name(self, page=None):
    """Returns the name of the given page or the current page."""
    if not page:
      page = self.page
    match = re.compile("%s/([^.]*)" % self.HANDLERS_BASE).search(page.__file__)
    if match:
      return match.group(1)
  
  def default_template(self, ext="html"):
    """Returns the path for the current page's default template."""
    name = self.page_name()
    if name:
      return "%s.%s" % (name, ext)
    raise Exception("failed to build default template for %s" % page)
  
  def handle(self, method, *args):
    """Invokes the given method and return the template path to render."""
    self.__url_args__ = args
    try:
      return method(self, self.response_dict())
    except NotFoundException:
      return self.not_found()
    except NeedIndexError:
      return self.not_found(status=503)
    except:
      return self.handle_error()
  
  def handle_error(self):
    """Prepares a traceback for 500 errors, returns error template path."""
    (error_type, error, tb) = sys.exc_info()
    tb_formatted = traceback.format_tb(tb)
    error_type = error_type.mro()[0].__name__
    self.response_dict(
      error=error,
      error_type=error_type,
      tb_formatted=tb_formatted)
    logging.error("%s: %s", error_type, error)
    self.response.set_status(code=500)
    return 'error.html'
  
  def render(self, path, base="html"):
    """Renders the given template or the default template, or JSON(P)/YAML."""
    if self.is_json():
      sanitized = sanitize(self.response_dict())
      json_str = json.write(sanitized)
      callback = self.request.get('callback')
      if re.match("^[_a-z]([_a-z0-9])*$", callback, re.IGNORECASE):
        json_str = "%s(%s)" % (callback, json_str) # jsonp
      self.response.headers['Content-Type'] = "text/javascript; charset=UTF-8"
      self.response.out.write(json_str)
      return
    if self.is_yaml():
      sanitized = sanitize(self.response_dict())
      yaml_str = yaml.safe_dump(sanitized, default_flow_style=False)
      self.response.headers['Content-Type'] = "text/plain; charset=UTF-8"
      self.response.out.write(yaml_str)
      return;
    if self.is_xml():
      sanitized = sanitize(self.response_dict())
      xml_str = to_xml(obj=sanitized, tag="response")
      self.response.headers['Content-Type'] = "text/xml; charset=UTF-8"
      self.response.out.write(xml_str)
      return;
    if not path:
      path = self.default_template(ext=base)
    path = os.path.join(self.TEMPLATES_BASE, path)
    if self.file_exists(path):
      try:
        # the template might find these handy
        self.response_dict(
          handler=self,
          is_dev=env.is_dev()
        )
        rendered = template.render(path, self.response_dict())
        self.response.out.write(rendered)
      except template.django.template.TemplateSyntaxError, error:
        self.response.headers['Content-Type'] = 'text/plain'
        message = "Template syntax error: %s" % error
        logging.critical(message)
        self.response.out.write(message)
    else:
      self.response.headers['Content-Type'] = 'text/plain'
      message = "Template not found: %s" % path
      logging.critical(message)
      self.response.out.write(message)
  
  def file_exists(self, path):
    return os.path.exists(path)
  
  def redirect(self, *args):
    """Redirects to the given location (unless in JSON/YAML mode)."""
    if not self.is_json() and not self.is_yaml():
      super(MegaeraRequestHandler, self).redirect(*args)
  
  def not_found(self, status=404):
    """Returns generic not-found template (see images/errors/ for supported status codes)."""
    self.response_dict(status=status)
    self.response.set_status(code=status)
    return 'not_found.html'
  
  def form_error(self, **kwargs):
    """Set the given form errors."""
    response = self.response_dict()
    for key, value in kwargs.iteritems():
      response.errors[key] = value
    
  def config(self):
    """Returns the local configuration."""
    return local.config()
