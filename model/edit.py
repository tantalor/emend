from util.levenshtein import describe

from site import Site
from user import User

from google.appengine.ext import db, search
from google.appengine.api import users
from util import bitly, twitter, env
from util.warn import warn

class Edit(search.SearchableModel):
  index = db.IntegerProperty(required=True)
  url = db.StringProperty(required=True)
  author = db.ReferenceProperty(required=True, reference_class=User)
  datetime = db.DateTimeProperty(auto_now_add=True)
  original = db.StringProperty(required=True, multiline=True)
  proposal = db.StringProperty(required=True, multiline=True)
  closed = db.BooleanProperty(required=True, default=False)
  
  site = property(fget=lambda self: self.parent())
  short_date = property(fget=lambda self: self.datetime.strftime('%A, %b %d, %Y'))
  long_date = property(fget=lambda self: self.datetime.strftime('%a, %b %d at %I:%M %p'))
  original_utf8 = property(fget=lambda self: self.original.encode('utf8'))
  proposal_utf8 = property(fget=lambda self: self.proposal.encode('utf8'))
  original_desc = property(fget=lambda self: self.describe()[0])
  proposal_desc = property(fget=lambda self: self.describe()[1])
  
  def can_edit(self):
    user = users.get_current_user()
    if users.is_current_user_admin():
      return True
    if user and user == self.author.user:
      return True
  
  def permalink(self):
    return "%s/edits/%s" % (self.site.permalink(), self.index)
  
  _describe = None
  def describe(self):
    if not self._describe:
      self._describe = describe(self.original, self.proposal)
    return self._describe
  
  def as_tweet(self):
    as_tweet = '"%s" should be "%s" on #%s' % (\
        self.original_utf8,\
        self.proposal_utf8,\
        self.site.domain.encode('utf8'))
    # try to append a short url if we can
    short_url = self.short_url()
    if short_url:
      as_tweet = "%s %s" % (as_tweet, short_url)
    return as_tweet
  
  def short_url(self):
    """Try to shorten the url, but suppress errors."""
    credentials = env.branch(bitly.credentials())
    if credentials:
      try:
        return bitly.shorten(self.permalink(), **credentials)
      except DownloadError, e:
        warn("failed to shorten", e)
    else:
      warn("could not find bitly credentials")
  
  def tweet(self):
    """Try to tweet this edit, but suppress errors."""
    status = self.as_tweet()
    if status:
      credentials = env.branch(twitter.credentials())
      if credentials:
        try:
          return twitter.tweet(self.status(), **credentials)
        except DownloadError, e:
          warn("failed to tweet", e)
      else:
        warn("could not find twitter credentials")
    
  def sanitize(self):
    return dict(
      original=self.original,
      proposal=self.proposal,
      closed=self.closed,
      site=self.site.sanitize(),
      author=self.author.sanitize(),
    )
  
  def open(self):
    def open_edit():
      if not self.closed:
        return
      self.closed = False
      self.put()
      # fiddle site counts
      self.site.closed -= 1
      self.site.open += 1
      self.site.put()
      return True
    if (db.run_in_transaction(open_edit)):
      # fiddle user counts
      self.author.closed -= 1
      self.author.open += 1
      self.author.put()
  
  def close(self):
    def close_edit():
      if self.closed:
        return
      self.closed = True
      self.put()
      # fiddle site counts
      self.site.open -= 1
      self.site.closed += 1
      self.site.put()
      return True
    if (db.run_in_transaction(close_edit)):
      # fiddle user counts
      self.author.open -= 1
      self.author.closed += 1
      self.author.put()
