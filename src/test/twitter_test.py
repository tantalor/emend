import unittest
from time import time

from emend import stubs
from emend.twitter import tweet, untweet


class TestTwitter(unittest.TestCase):
  def setUp(self):
    stubs.all()

  def test_tweet_untweet(self):
    status = "test %s" % int(time())
    status_id = tweet(status=status)
    self.assertTrue(status_id > 0, "tweet() returns new status id")
    if status_id > 0:
      destroyed_status_id = untweet(status_id=status_id)
      self.assertEqual(status_id, destroyed_status_id, "untweet() destroys status id")


if __name__ == "__main__":
  unittest.main()
