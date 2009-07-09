# -*- coding: utf-8 -*-

import unittest

from util.handler import Handler, NotFoundException
from model.site import Site
from model.edit import Edit
from model.user import User

from google.appengine.api import users
from google.appengine.ext.webapp import Request, Response

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

def mock_user(email="foo@bar.com"):
  return User(key_name="test",
    user=users.User(email=email, _auth_domain="test"))

def mock_site(domain="test.com", key_name="test"):
  return Site(domain=domain, key_name=key_name)

def mock_edit(original="test", proposal="test", url="http://test.com"):
  return Edit(
    index=0,
    url=url,
    original=original,
    proposal=proposal,
    author=mock_user(),
    parent=mock_site(),
  )

def mock_handler(page, **response):
  handler = Handler.factory(page=page)()
  handler.initialize(Request(environ=dict()), Response())
  handler.response_dict(**response)
  handler.logout_url = lambda self: None
  handler.login_url = lambda self: None
  def mock_not_found():
    raise NotFoundException()
  handler.not_found = mock_not_found
  return handler

class EditTest(unittest.TestCase):
  def testUnicodeOriginal(self):
    """An edit with unicode characters"""
    # mock edit
    original = u"Don’t judge a proggie by it’s UI"
    edit = mock_edit(original=original, proposal=original)
    # mock handler
    import app.sites.edits.detail
    handler = mock_handler(page=app.sites.edits.detail, edit=edit)
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
    edit = mock_edit(url=url)
    # mock handler
    import app.sites.edits.detail
    handler = Handler.factory(page=app.sites.edits.detail)()
    handler.initialize(Request(environ=dict()), Response())
    handler.response_dict(edit=edit)
    handler.get_edit = lambda **kwargs: edit
    handler.logout_url = lambda self: None
    handler.login_url = lambda self: None
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
    edit = mock_edit(original=original, proposal=proposal)
    for max_len in (100, 120, 140, 160, 180):
      tweet = edit.as_tweet(max_len=max_len)
      if len(tweet) > max_len:
        self.fail("tweet is too long")
