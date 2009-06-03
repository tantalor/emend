# -*- coding: utf-8 -*-

import unittest

from util.handler import Handler
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

def mock_edit(original, proposal="test", url="http://test.com"):
  return Edit(
    index=0,
    url=url,
    original=original,
    proposal=proposal,
    author=mock_user(),
    parent=mock_site(),
  )

class EditTest(unittest.TestCase):
  def testUnicode(self):
    """An edit with unicode characters should not raise UnicodeDecodeError"""
    # mock edit
    original = u"Don’t judge a proggie by it’s UI"
    edit = mock_edit(original=original)
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
    except UnicodeDecodeError:
      self.fail("failed to decode unicode")    
