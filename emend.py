import re

from google.appengine.ext import db
from google.appengine.api import users

class Site(db.Model):
  domain = db.StringProperty(required=True)
  owner = db.UserProperty()
  index = db.IntegerProperty(required=True, default=0)
  
  @staticmethod
  def key_name_from_domain(domain):
    match = re.compile('^www\.(.*)$').search(domain)
    if match:
      # remove "www."
      return match.group(1)
    return domain

class Edit(db.Model):
  index = db.IntegerProperty(required=True)
  site = db.ReferenceProperty(required=True)
  url = db.StringProperty(required=True)
  author = db.UserProperty(required=True)
  datetime = db.DateTimeProperty(auto_now_add=True)
  original = db.StringProperty(required=True, multiline=True)
  proposal = db.StringProperty(required=True, multiline=True)
  
  def can_edit(self):
    user = users.get_current_user()
    if users.is_current_user_admin():
      return True
    if user and (user == self.author or user == self.site.owner):
      return True
