import urllib
import logging

from model import Edit, Site, User

from megaera import local
from megaera.request_handler import MegaeraRequestHandler, NotFoundException

from google.appengine.api import users, memcache
from google.appengine.ext import db

class EmendRequestHandler(MegaeraRequestHandler):
  
  def current_user(self):
    """Returns the logged-in User object."""
    user = users.get_current_user()
    if user:
      key_name = User.key_name_from_email(user.email())
      cached = memcache.get(key_name)
      if cached:
        return cached
      try:
        # User models are keyed by user email
        uncached = User.get_or_insert(key_name=key_name, user=user)
        uncached.invalidate() # cache it
        return uncached
      except CapabilityDisabledError:
        pass
  
  def get_site(self, required=False, create_if_missing=False):
    """Returns the Site object given by the URL."""
    if self.response_dict().site:
      return self.response_dict().site
    domain = self.url_arg(0)
    if domain:
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
    """Returns the Edit object given by the URL."""
    if self.response_dict().edit:
      return self.response_dict().edit
    site = self.get_site()
    index = self.url_arg(1)
    if site and index:
      index = int(index)
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
    """Returns the User object given by the URL."""
    if self.response_dict().user:
      return self.response_dict().user
    key = self.url_arg(0)
    if key:
      user = None
      try:
        user = User.get(key)
      except db.BadKeyError:
        pass
      if not user:
        email = urllib.unquote(key)
        key_name = User.key_name_from_email(email)
        user = User.get_by_key_name(key_name)
      if user:
        self.response_dict(user = user) # for the template
        return user
    if required:
      raise NotFoundException("user not found")
    
  def twitter_credentials(self):
    """Returns Emend's twitter credentials, if any."""
    try:
      return local.config_get('twitter')
    except KeyError, e:
      logging.warn('missing credentials: %s', e)
