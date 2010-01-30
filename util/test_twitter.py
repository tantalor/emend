import unittest
from time import time

import stubs
from twitter import tweet


class TestTwitter(unittest.TestCase):
  def setUp(self):
    stubs.all()

  def testTweet(self):
    status = "test %s" % int(time())
    response = tweet(status=status)
    expected = '<text>%s</text>' % status
    self.assertTrue(expected in response)


if __name__ == "__main__":
  unittest.main()
