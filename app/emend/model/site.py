import re

from counts import Counts

from google.appengine.ext import db

class Site(db.Model, Counts):
  domain = db.StringProperty(required=True)
  index = db.IntegerProperty(required=True, default=0)
  open = db.IntegerProperty(required=True, default=0)
  closed = db.IntegerProperty(required=True, default=0)
  
  @staticmethod
  def key_name_from_domain(domain, prefix="site"):
    # remove "www."
    match = re.compile('^www\.(.*)$').search(domain)
    if match:
      domain = match.group(1)
    # prefix required because key names may not begin with a digit
    return "%s:%s" % (prefix, domain)
  
  def __str__(self):
    return self.domain
  
  def permalink(self):
    return "/sites/%s" % self.domain
  
  def sanitize(self, urlize):
    json = dict(
      domain=self.domain,
      open=self.open,
      closed=self.closed,
      permalink=urlize(self.permalink()),
    )
    return json
