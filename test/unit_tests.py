import unittest

from model.site import Site
from model.edit import Edit
from model.user import User

from google.appengine.api import users

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
