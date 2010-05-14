from os import environ
from hashlib import md5

from google.appengine.ext import db
from google.appengine.api import users, memcache

from emend.const import DATE_SHORT
from pretty_timedelta import pretty_datetime_from_now

class User(db.Model):
  user = db.UserProperty(required=True)
  nickname = db.StringProperty()
  open = db.IntegerProperty(required=True, default=0)
  closed = db.IntegerProperty(required=True, default=0)
  created = db.DateTimeProperty(auto_now_add=True)
  
  created_short = property(fget=lambda self: self.created.strftime(DATE_SHORT))
  
  def __str__(self):
    return self.nickname or self.user.nickname()
  
  def can_edit(self):
    user = users.get_current_user()
    if users.is_current_user_admin():
      return True
    if self.user == user:
      return True
  
  def permalink(self, shareable=False):
    host = environ.get('HTTP_HOST')
    if self.can_edit() and not shareable:
      key = self.user.email()
    else:
      key = self.key()
    return "http://%s/users/%s" % (host, key)
  
  def shareable_permalink(self):
    return self.permalink(shareable=True)
  
  def put(self):
    super(User, self).put()
    self.invalidate()
  
  def invalidate(self):
    memcache.set(self.key().name(), self)
  
  def gravatar(self):
    gravatar = "http://www.gravatar.com/avatar"
    email_hash = md5(self.user.email())
    return "%s/%s" % (gravatar, email_hash.hexdigest())
  
  def created_pretty_timedelta(self):
    return pretty_datetime_from_now(self.created)
  
  @staticmethod
  def key_name_from_email(email, prefix="user"):
    """Accepts google.appengine.api.users.User object."""
    return '%s:%s' % (prefix, email)
  
  def sanitize(self):
    return dict(
      nickname=unicode(self)
    )
