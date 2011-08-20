import unittest

from mocks import MockUser


class TestUser(unittest.TestCase):
  def testEmailNickname(self):
    user = MockUser(email="foo@example.com")
    self.assertEquals(str(user), "foo")
  
  def testNicknameOverride(self):
    user = MockUser(email="foo@example.com", nickname="bar")
    self.assertEquals(str(user), "bar")
    

if __name__ == "__main__":
  unittest.main()
