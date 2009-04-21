from os import environ

from google.appengine.ext import db
from google.appengine.api import users, memcache

class User(db.Model):
  user = db.UserProperty(required=True)
  nickname = db.StringProperty()
  open = db.IntegerProperty(required=True, default=0)
  closed = db.IntegerProperty(required=True, default=0)
  
  def __str__(self):
    return self.nickname or self.user.nickname()
  
  def can_edit(self):
    user = users.get_current_user()
    if users.is_current_user_admin():
      return True
    if self.user == user:
      return True
  
  def permalink(self, shareable=False):
    host = environ['HTTP_HOST']
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
  
  @staticmethod
  def key_name_from_email(email, prefix="user"):
    """Accepts google.appengine.api.users.User object."""
    return '%s:%s' % (prefix, email)
  
  def counts(self):
    counts = []
    if self.open:
      plural = ''
      if self.open > 1:
        plural = 's'
      counts.append('%s edit%s' % (self.open, plural))
    if self.closed:
      counts.append('%s fixed' % self.closed)
    if counts:
      return ', '.join(counts)
  
  def sanitize(self):
    return dict(
      nickname=str(self)
    )
