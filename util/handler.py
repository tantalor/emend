import cgi
import os
import sys
import re
import urllib
import traceback
import logging
from types import InstanceType

from google.appengine.api import users, memcache
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
from google.appengine.api.datastore_errors import BadKeyError

import twitter
import blogsearch
import json
import yaml
import bitly
import env
import local
from model.site import Site
from model.edit import Edit
from model.user import User
from recursivedefaultdict import recursivedefaultdict
from sanitize import sanitize

template.register_template_library('template')

class NotFoundException(Exception):
  pass

class Handler(webapp.RequestHandler):
  
  @staticmethod
  def factory(**kwargs):
    """Convenience method for subclasses of Handler."""
    return type(str(kwargs), (Handler,), kwargs)
  
  def __init__(self):
    self._response_dict = recursivedefaultdict()
    self._url_args = None
  
  def response_dict(self, **kwargs):
    if kwargs:
      self._response_dict.update(**kwargs)
    return self._response_dict
    
  def get(self, *args):
    # remove expiration from ACSID cookie, set ACSID-reset=1
    if 'ACSID' in self.request.cookies and\
       'ACSID-reset' not in self.request.cookies:
      acsid = self.request.cookies['ACSID']
      self.response.headers.add_header('Set-Cookie', "ACSID=%s" % acsid, path='/')
      self.response.headers.add_header('Set-Cookie', "ACSID-reset=1", path='/')
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
  
  def current_user(self):
    """Returns the current user"""
    user = users.get_current_user()
    if user:
      key_name = User.key_name_from_email(user.email())
      cached = memcache.get(key_name)
      if cached:
        return cached
      # User models are keyed by user email
      uncached = User.get_or_insert(key_name=key_name, user=user)
      uncached.invalidate() # cache it
      return uncached
  
  def get_site(self, required=False, create_if_missing=False):
    if self._url_args:
      # based on the regexp in main.py
      domain = self._url_args[0]
      key_name = Site.key_name_from_domain(domain)
      site = Site.get_by_key_name(key_name)
      if not site and create_if_missing:
        # create a site (but don't save it)
        site = Site(key_name=key_name, domain=domain)
      if site:
        self.response_dict(site = site) # for the template
        return site
    if required:
      raise NotFoundException("site not found")
  
  def get_edit(self, required=False):
    site = self.get_site()
    if site and self._url_args:
      # based on the regexp in main.py
      index = int(self._url_args[1])
      edits = Edit.all().\
        ancestor(site).\
        filter('index =', index).\
        fetch(1)
      if edits:
        edit = edits[0]
        self.response_dict(edit = edit) # for the template
        return edit
    if required:
      raise NotFoundException("edit not found")
  
  def get_user(self, required=False):
    if self._url_args:
      # based on the regexp in main.py
      key = self._url_args[0]
      email = urllib.unquote(key)
      key_name = User.key_name_from_email(email)
      user = None
      try:
        user = User.get(key)
      except BadKeyError:
        pass
      if not user:
        user = User.get_by_key_name(key_name)
      if user:
        self.response_dict(user = user) # for the template
        return user
    if required:
      raise NotFoundException("user not found")
  
  def host(self):
    return os.environ['HTTP_HOST']
  
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
  
  def twitter_credentials(self):
    return env.branch(twitter.credentials())
  
  def ping_blogsearch(self):
    name = 'Emend: Edit the Interwebs'
    url = 'http://%s' % self.host()
    changesURL = '%s?atom' % url
    return blogsearch.ping(name=name, url=url, changesURL=changesURL)
  
  def config(self):
    return local.config()
