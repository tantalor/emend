# -*- coding: utf-8 -*-

import logging
from datetime import datetime

from site import Site
from user import User

from google.appengine.ext import db, search
from google.appengine.api import users
from google.appengine.api.urlfetch import fetch
from google.appengine.api.urlfetch_errors import DownloadError

from emend import bitly, twitter, html
from emend.const import DATE_SHORT
from pretty_timedelta import pretty_datetime_from_now

class Edit(search.SearchableModel):
  index = db.IntegerProperty(required=True)
  url = db.StringProperty(required=True)
  author = db.ReferenceProperty(required=True, reference_class=User)
  created = db.DateTimeProperty(auto_now_add=True)
  modified = db.DateTimeProperty()
  tested = db.DateTimeProperty()
  original = db.StringProperty(required=True, multiline=True)
  proposal = db.StringProperty(required=True, multiline=True)
  status = db.StringProperty(default="open", required=True)
  
  site = property(fget=lambda self: self.parent())
  is_open = property(fget=lambda self: self.status == 'open')
  is_closed = property(fget=lambda self: self.status == 'closed')
  created_short = property(fget=lambda self: self.created.strftime(DATE_SHORT))
  modified_short = property(fget=lambda self: self.modified.strftime(DATE_SHORT))
  
  def can_edit(self):
    user = users.get_current_user()
    if users.is_current_user_admin():
      return True
    if user and user == self.author.user:
      return True
  
  def permalink(self):
    return "%s/edits/%s" % (self.site.permalink(), self.index)
  
  def as_tweet(self, max_len=140):
    """This edit as a tweet (unicode)."""
    short_url = self.short_url()
    original = self.original
    proposal = self.proposal
    # compute limit, i.e. maximum lenth of original+proposal
    template = u'"%s" should be "%s" on %s'
    limit = max_len - len(template % ('', '', '')) - len(self.site.domain)
    if short_url:
      limit = limit - len(short_url) - 1 # for the short url and space
    # cut down to limit
    if len(original)+len(proposal) > limit:
      sub_limit = limit/2-3 # leave space for ellipses
      if len(original) > sub_limit:
        original = original[:sub_limit]+"..."
      if len(proposal) > sub_limit:
        proposal = proposal[:sub_limit]+"..."
    # compose tweet
    as_tweet = template % (original, proposal, self.site.domain)
    # try to append a short url if we can
    if short_url:
      as_tweet = "%s %s" % (as_tweet, short_url)
    return as_tweet
  
  def short_url(self):
    """Try to shorten the url, but suppress errors."""
    try:
      return bitly.shorten(self.permalink())
    except DownloadError, e:
      logging.error("failed to shorten: %s", e)
    except KeyError, e:
      logging.warn('missing credentials: %s', e)
  
  def tweet(self):
    """Try to tweet this edit, but suppress errors."""
    status = self.as_tweet().encode('utf8')
    if status:
      try:
        return twitter.tweet(status)
      except DownloadError, e:
        logging.error("failed to tweet: %s", e)
      except KeyError, e:
        logging.warn('missing credentials: %s', e)
  
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
  
  def delete(self):  
    # fiddle site/author open/closed counts
    if self.is_open:
      self.site.open -= 1
      self.author.open -= 1
    elif self.is_closed:
      self.site.closed -= 1
      self.author.closed -= 1
    self.site.put()
    self.author.put()
    super(Edit, self).delete()
  
  def page_content(self):
    page = fetch(self.url.replace(' ', '%20'))
    if page:
      # decode content
      content = unicode(page.content, 'utf8')
      # decode html entities, strip tags
      content = html.clean(content)
      return content
  
  def created_pretty_timedelta(self):
    return pretty_datetime_from_now(self.created)
  
  def test(self):
    # record test
    self.tested = datetime.now()
    self.put()
    # fetch page
    content = self.page_content()
    if content:
      # remove comments
      comment = u"“%s” should be “%s”" % (self.original, self.proposal)
      content = content.replace(comment, '')
      # test page
      if self.proposal in self.original:
        if self.original in content:
          return 'unfixed'
        elif self.proposal in content:
          return 'fixed'
        else:
          return 'uncertain'
      else:
        if self.proposal in content:
          self.close()
          return 'fixed'
        elif self.original in content:
          return 'unfixed'
        else:
          return 'uncertain'
