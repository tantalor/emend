import cgi
import os
import sys
import re
import base64
import urllib
import yaml

from urlparse import urlparse
from collections import defaultdict

from google.appengine.ext import webapp
from google.appengine.api import users, urlfetch, memcache
from google.appengine.ext.webapp import template

from emend import Site, Edit

class recursivedefaultdict(defaultdict):
  """Due to Kent S Johnson."""
  def __init__(self, *args, **kwargs):
    super(recursivedefaultdict, self).__init__(type(self), *args, **kwargs)
  
  def __getattr__(self, name):
    return self[name]
  
  def __setattr__(self, name, value):
    self[name] = value
  
  def __delattr__(self, name):
    del self[name]

def twitter_credentials(filename='twitter.yaml'):
  credentials = memcache.get('twitter_credentials')
  if credentials:
    return credentials
  if os.path.exists(filename):
    credentials = yaml.load(file(filename).read())
    memcache.set('twitter_credentials', credentials)
    return credentials

def send_tweet(status, username, password):
  payload = {'status' : status, 'source' : 'Emend'}
  payload = urllib.urlencode(payload)
  auth = base64.encodestring('%s:%s' % (username, password))[:-1]
  headers = {'Authorization': "Basic %s" % auth}
  url = "http://twitter.com/statuses/update.xml"
  return urlfetch.fetch(url, payload=payload, method=urlfetch.POST, headers=headers)

def handler(page):
  """Returns an EmendHandler(webapp.RequestHandler) subclass
  bound to the given page.
  """
  # returns a subclass of EmendHandler with the given page
  return type(str(page), (EmendHandler,), {'page': page})


class EmendHandler(webapp.RequestHandler):
  _response_dict = None
  _url_args = None
  
  @staticmethod
  def factory(**kwargs):
    return type(str(kwargs), (EmendHandler,), kwargs)
  
  def response_dict(self, **kwargs):
    if self._response_dict:
      return self._response_dict.update(**kwargs)
    # defaults the template might find handy
    self._response_dict = recursivedefaultdict(
      handler = self,
      **kwargs
    )
    return self._response_dict
  
  def get(self, *args):
    self._url_args = args
    self.handle(self.page.get)
  
  def post(self, *args):
    self._url_args = args
    self.handle(self.page.post)
  
  def is_dev(self):
    if os.environ['SERVER_SOFTWARE'].find('Development') >= 0:
      return True
  
  def logout_url(self):
    return users.create_logout_url(self.request.uri)
  
  def login_url(self):
    return users.create_login_url(self.request.uri)
  
  def user(self):
    user = users.get_current_user()
    if users.is_current_user_admin():
      user.is_admin = 1
    elif user:
      user.is_admin = 0
    return user
  
  def get_site(self):
    if self._url_args:
      # based on the regexp in main.py
      domain = self._url_args[0]
      key_name = Site.key_name_from_domain(domain)
      site = Site.get_by_key_name(key_name)
      if site:
        self.response_dict(site = site) # for the template
        return site
  
  def get_edit(self):
    site = self.get_site()
    if site and self._url_args:
      # based on the regexp in main.py
      edit = Edit.get_by_id(int(self._url_args[1]), site)
      if edit:
        self.response_dict(edit = edit) # for the template
        return edit
  
  def default_template(self):
    base = os.path.dirname(__file__)
    page = self.page.__file__
    match = re.compile(base+'/app/([^.]*)').match(page)
    return "%s.html" % match.group(1)
  
  def handle(self, method):
    response = self.response_dict()
    try:
      template_path = method(self, response)
    except:
      (error, value, tb) = sys.exc_info()
      template_path = 'error.html'
      response.value = value
    if not template_path:
      template_path = self.default_template()
    template_path = os.path.join(
      os.path.dirname(__file__), 'html', template_path)
    if os.path.exists(template_path):
      self.response.out.write(template.render(template_path, response))
  
  def warn(self, *args, **kwargs):
    if kwargs:
      self.warn(*["%s: %s" % (k, v) for k, v in kwargs.iteritems()])
    if args:
      sys.stderr.write(">>> %s\n" % ', '.join([str(s) for s in args]))

  def tweet(self, status):
    credentials = twitter_credentials()
    if credentials:
      if self.is_dev() and 'dev' in credentials:
        return send_tweet(status, **credentials['dev'])
      elif 'prod' in credentials:
        return send_tweet(status, **credentials['prod'])
    self.warn("could not find twitter credentials")
