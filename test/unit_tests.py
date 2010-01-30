# -*- coding: utf-8 -*-

import unittest
import sys
from urllib import urlencode

from util.megaera.megaera import NotFoundException
from util.emend import Emend
from model.site import Site
from model.edit import Edit
from model.user import User

from google.appengine.api import users
from google.appengine.ext.webapp import Request, Response
from google.appengine.ext import db

class MockModel(db.Model):
  def put(self):
    pass
  def delete(self):
    pass

class MockUser(User, MockModel):
  def __init__(self, email="foo@bar.com", **kwargs):
    super(MockUser, self).__init__(
      key_name="test",
      user=users.User(
        email=email,
        _auth_domain="test",
      ),
      **kwargs
    )

class MockSite(Site, MockModel):
  def __init__(self, domain="test.com", key_name="test", **kwargs):
    super(MockSite, self).__init__(
      domain=domain,
      key_name=key_name,
      **kwargs
    )

class MockEdit(Edit, MockModel):
  def __init__(self, original="test", proposal="test", url="http://test.com", **kwargs):
    super(MockEdit, self).__init__(
      index=0,
      url=url,
      original=original,
      proposal=proposal,
      author=MockUser(),
      parent=MockSite(),
      **kwargs
    )
    if self.is_open:
      self.site.open += 1
      self.author.open += 1
    if self.is_closed:
      self.site.closed += 1
      self.author.closed += 1

def mock_handler(page, request='/', **response):
  handler = Emend.with_page(page=page)()
  handler.initialize(Request.blank(request), Response())
  handler.response_dict(**response)
  handler.logout_url = lambda self: None
  handler.login_url = lambda self: None
  def mock_not_found():
    raise NotFoundException()
  handler.not_found = mock_not_found
  def mock_handle_error():
    (error_type, error, tb) = sys.exc_info()
    raise error
  handler.handle_error = mock_handle_error
  return handler

class SiteTest(unittest.TestCase):
  def testDomainKey(self):
    """foo.com and www.foo.com should map to foo.com"""
    prefix = "test_prefix"
    self.assertEquals(
      Site.key_name_from_domain("foo.com", prefix=prefix),
      "%s:foo.com" % prefix)
    self.assertEquals(
      Site.key_name_from_domain("www.foo.com", prefix=prefix),
      "%s:foo.com" % prefix)

class EditTest(unittest.TestCase):
  def testUnicodeOriginal(self):
    """An edit with unicode characters"""
    # mock edit
    original = u"Don’t judge a proggie by it’s UI"
    edit = MockEdit(original=original, proposal=original)
    # mock handler
    import handlers.sites.edits.detail
    handler = mock_handler(page=handlers.sites.edits.detail, edit=edit)
    # execute handler
    try:
      handler.get()
    except UnicodeDecodeError:
      self.fail("failed to decode unicode")
    except UnicodeEncodeError:
      self.fail("failed to encode unicode")
  
  def testUnicodeURL(self):
    """A URL with unicode characters"""
    # mock edit
    url = u"http://test.com/“tell-your-girl”/"
    edit = MockEdit(url=url)
    # mock handler
    import handlers.sites.edits.detail
    handler = mock_handler(page=handlers.sites.edits.detail, edit=edit)
    # execute handler
    try:
      handler.get()
    except UnicodeEncodeError:
      self.fail("failed to encode unicode")
  
  def testAsTweet(self):
    """Tweets of various lengths"""
    original = ("Lorem ipsum dolor sit amet, consectetur adipisicing elit, "
                "sed do eiusmod tempor incididunt ut labore et dolore magna "
                "aliqua. Ut enim ad minim veniam, quis nostrud exercitation "
                "ullamco laboris nisi ut aliquip ex ea commodo consequat.")
    proposal = ("Duis aute irure dolor in reprehenderit in voluptate velit "
                "esse cillum dolore eu fugiat nulla pariatur. Excepteur sint "
                "occaecat cupidatat non proident, sunt in culpa qui officia "
                "deserunt mollit anim id est laborum.")
    edit = MockEdit(original=original, proposal=proposal)
    for max_len in (100, 120, 140, 160, 180):
      tweet = edit.as_tweet(max_len=max_len)
      if len(tweet) > max_len:
        self.fail("tweet is too long")
  
  def testClose(self):
    edit = MockEdit()
    site = edit.site
    author = edit.author
    site_open, site_closed = site.open, site.closed
    author_open, author_closed = author.open, author.closed
    edit.close()
    self.assertEquals(site_open - 1, site.open)
    self.assertEquals(site_closed + 1, site.closed)
    self.assertEquals(author_open - 1, author.open)
    self.assertEquals(author_closed + 1, author.closed)
  
  def testOpen(self):
    edit = MockEdit(status="closed")
    site = edit.site
    author = edit.author
    site_open, site_closed = site.open, site.closed
    author_open, author_closed = author.open, author.closed
    edit.open()
    self.assertEquals(site_open + 1, site.open)
    self.assertEquals(site_closed - 1, site.closed)
    self.assertEquals(author_open + 1, author.open)
    self.assertEquals(author_closed - 1, author.closed)
  
  def testDeleteOpen(self):
    edit = MockEdit()
    site = edit.site
    author = edit.author
    site_open = site.open
    author_open = author.open
    edit.delete()
    self.assertEquals(site_open - 1, site.open)
    self.assertEquals(author_open - 1, author.open)
  
  def testDeleteClosed(self):
    edit = MockEdit(status="closed")
    site = edit.site
    author = edit.author
    site_closed = site.closed
    author_closed = author.closed
    edit.delete()
    self.assertEquals(site_closed - 1, site.closed)
    self.assertEquals(author_closed - 1, author.closed)

class HomePageTest(unittest.TestCase):
  def testUnicodeSuggest(self):
    original = u"the original design"
    request = '/?%s' % urlencode(dict(original=original.encode('utf8')))
    # mock handler
    import handlers.default
    handler = mock_handler(page=handlers.default, request=request)
    # execute handler
    try:
      handler.get()
    except UnicodeEncodeError:
      self.fail('failed to encode unicode')
