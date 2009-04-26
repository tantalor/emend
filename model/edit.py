import logging
from datetime import datetime

from util.levenshtein import describe

from site import Site
from user import User

from google.appengine.ext import db, search
from google.appengine.api import users
from google.appengine.api.urlfetch_errors import DownloadError
from util import bitly, twitter, env
from util.const import DATE_SHORT

class Edit(search.SearchableModel):
  index = db.IntegerProperty(required=True)
  url = db.StringProperty(required=True)
  author = db.ReferenceProperty(required=True, reference_class=User)
  created = db.DateTimeProperty(auto_now_add=True)
  modified = db.DateTimeProperty()
  original = db.StringProperty(required=True, multiline=True)
  proposal = db.StringProperty(required=True, multiline=True)
  status = db.StringProperty(default="open", required=True)
  
  site = property(fget=lambda self: self.parent())
  is_open = property(fget=lambda self: self.status == 'open')
  is_closed = property(fget=lambda self: self.status == 'closed')
  created_short = property(fget=lambda self: self.created.strftime(DATE_SHORT))
  modified_short = property(fget=lambda self: self.modified.strftime(DATE_SHORT))
  original_utf8 = property(fget=lambda self: self.original.encode('utf8'))
  proposal_utf8 = property(fget=lambda self: self.proposal.encode('utf8'))
  original_desc = property(fget=lambda self: self.__describe_once()[0])
  proposal_desc = property(fget=lambda self: self.__describe_once()[1])
  
  def can_edit(self):
    user = users.get_current_user()
    if users.is_current_user_admin():
      return True
    if user and user == self.author.user:
      return True
  
  def permalink(self):
    return "%s/edits/%s" % (self.site.permalink(), self.index)
  
  def describe(self):
    return describe(self.original, self.proposal)
  
  def __describe_once(self):
    """Save the results of self.describe() locally."""
    attr = '__description__'
    if not hasattr('self', attr):
      setattr(self, attr, self.describe())
    return getattr(self, attr)
  
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
        logging.error("failed to shorten: %s", e)
    else:
      logging.info("could not find bitly credentials")
  
  def tweet(self):
    """Try to tweet this edit, but suppress errors."""
    status = self.as_tweet()
    if status:
      credentials = env.branch(twitter.credentials())
      if credentials:
        try:
          return twitter.tweet(status, **credentials)
        except DownloadError, e:
          logging.error("failed to tweet: %s", e)
      else:
        logging.info("could not find twitter credentials")
    
  def sanitize(self):
    return dict(
      original=self.original,
      proposal=self.proposal,
      status=self.status,
      site=self.site.sanitize(),
      url=self.url,
      author=self.author.sanitize(),
    )
  
  def open(self):
    def open_txn():
      if self.is_open:
        return
      self.status = 'open'
      self.modified = datetime.now()
      self.put()
      # fiddle site counts
      self.site.closed -= 1
      self.site.open += 1
      self.site.put()
      return True
    if (db.run_in_transaction(open_txn)):
      # fiddle user counts
      self.author.closed -= 1
      self.author.open += 1
      self.author.put()
  
  def close(self):
    def close_txn():
      if self.is_closed:
        return
      self.status = 'closed'
      self.modified = datetime.now()
      self.put()
      # fiddle site counts
      self.site.open -= 1
      self.site.closed += 1
      self.site.put()
      return True
    if (db.run_in_transaction(close_txn)):
      # fiddle user counts
      self.author.open -= 1
      self.author.closed += 1
      self.author.put()
