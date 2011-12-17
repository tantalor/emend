# -*- coding: utf-8 -*-

import logging
from datetime import datetime

from site import Site
from user import User

from google.appengine.ext import db, search
from google.appengine.api import users, memcache
from google.appengine.api.urlfetch_errors import DownloadError
import hashlib

import emend
from emend.const import DATE_SHORT
from pretty_timedelta import pretty_datetime_from_now
from megaera.fetch import fetch_decode

from bloom import BloomFilter
import pickle


class Edit(search.SearchableModel):
  index = db.IntegerProperty(required=True)
  url = db.StringProperty(required=True)
  url_sha1 = db.StringProperty()
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
  
  def put(self):
    self.url_sha1 = hashlib.sha1(self.url.encode('utf8')).hexdigest()
    super(Edit, self).put()
  
  def can_edit(self):
    user = users.get_current_user()
    if users.is_current_user_admin():
      return True
    if user and user == self.author.user:
      if not self.author.banned:
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
      return emend.bitly.shorten(self.permalink())
    except DownloadError, e:
      logging.error("failed to shorten: %s", e)
    except KeyError, e:
      logging.warn('missing credentials: %s', e)
  
  def tweet(self):
    """Try to tweet this edit, but suppress errors."""
    status = self.as_tweet().encode('utf8')
    if status:
      try:
        return emend.twitter.tweet(status)
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
      url_sha1=self.url_sha1,
      permalink=self.permalink(),
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
    content = fetch_decode(self.url)
    if content:
      # decode html entities, strip tags
      return emend.html.clean(content)
  
  def created_pretty_timedelta(self):
    return pretty_datetime_from_now(self.created)
  
  def modified_pretty_timedelta(self):
    return pretty_datetime_from_now(self.modified)
  
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


class Bloom(db.Model):
  pickled = db.BlobProperty()
  
  def get_filter(self):
    if hasattr(self, '_filter'):
      return getattr(self, '_filter')
    if self.pickled:
      _filter = pickle.loads(self.pickled)
    else:
      _filter = BloomFilter(m=10000, k=2)
    setattr(self, '_filter', _filter)
    return _filter
  
  def reset(self):
    self.pickled = None
    if hasattr(self, '_filter'):
      delattr(self, '_filter')
  
  def put(self):
    self.pickled = pickle.dumps(self.get_filter())
    memcache.set(key=self.key().name(), namespace='bloom', value=self)
    return super(Bloom, self).put()
  
  @classmethod
  def get_by_key_name(cls, key_name):
    bloom = memcache.get(key=key_name, namespace='bloom')
    if bloom:
      return bloom
    return super(Bloom, cls).get_by_key_name(key_name)
  
  def add(self, k):
    self.get_filter().add(k)
  
  def __contains__(self, k):
    if k in self.get_filter():
      return 1


def get_url_sha1_bloom():
  key_name = 'edits-url-sha1'
  return Bloom.get_by_key_name(key_name) or Bloom(key_name=key_name)
