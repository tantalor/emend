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

from google.appengine.api import users, memcache
from google.appengine.ext.webapp import template, RequestHandler

class NotFoundException(Exception):
  pass

class Handler(RequestHandler):
  
  def __init__(self):
    self._response_dict = recursivedefaultdict()
    self._url_args = None
  
  def response_dict(self, **kwargs):
    if kwargs:
      self._response_dict.update(**kwargs)
    return self._response_dict
    
  def get(self, *args):
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
    self._url_args = args
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
    return 'errors' in self.response_dict()
  
  def is_admin(self):
    return users.is_current_user_admin()
  
  def is_json(self):
    return len(self.request.get_all('json')) > 0
  
  def is_yaml(self):
    return len(self.request.get_all('yaml')) > 0
  
  def is_atom(self):
    return len(self.request.get_all('atom')) > 0
  
  def logout_url(self):
    return users.create_logout_url(self.request.uri)
  
  def login_url(self):
    return users.create_login_url(self.request.uri)
  
  def host(self):
    return os.environ['HTTP_HOST']
  
  def cache_key(self, page=None):
    if not page:
      page = self.page
    if page:
      return page.__file__
  
  def cached(self):
    cached = memcache.get(
      key=self.cache_key(),
      namespace="handler-cache")
    if cached:
      # update the response
      self.response_dict(**cached)
      return True
  
  def cache(self, time=0, **kwargs):
    memcache.set(
      key=self.cache_key(),
      value=kwargs,
      time=time,
      namespace="handler-cache")
    # update the response
    self.response_dict(**kwargs)
  
  def invalidate(self, page=None):
    memcache.delete(
      key=self.cache_key(page),
      namespace="handler-cache")
  
  def default_template(self, ext="html", base="/app"):
    page = self.page.__file__
    match = re.compile("%s/([^.]*)" % base).search(page)
    if match and match.group(1):
      return "%s.%s" % (match.group(1), ext)
    raise Exception("failed to build default template for %s" % page)
  
  def handle(self, method, *args):
    """Invoke the given method and return the template path to render."""
    self._url_args = args
    try:
      return method(self, self.response_dict())
    except NotFoundException:
      return self.not_found()
    except:
      return self.handle_error()
  
  def handle_error(self):
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
    """Render the given template or the default template."""
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
      yaml_str = yaml.dump(sanitized, default_flow_style=False)
      self.response.headers['Content-Type'] = "text/plain; charset=UTF-8"
      self.response.out.write(yaml_str)
      return;
    if not path:
      path = self.default_template(ext=base)
    path = os.path.join(base, path)
    if os.path.exists(path):
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
  
  def redirect(self, *args):
    if not self.is_json() and not self.is_yaml():
      super(Handler, self).redirect(*args)
  
  def not_found(self, status=404):
    self.response_dict(status=status)
    self.response.set_status(code=status)
    return 'not_found.html'
  
  def form_error(self, **kwargs):
    response = self.response_dict()
    for key, value in kwargs.iteritems():
      response.errors[key] = value
    
  def config(self):
    return local.config()
