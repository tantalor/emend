import unittest

import stubs
from blogsearch import ping


class TestBlogsearch(unittest.TestCase):
  def setUp(self):
    stubs.all()

  def testPing(self):
    response = ping(
      name='Official Google Blog',
      url='http://googleblog.blogspot.com',
      changesURL='http://googleblog.blogspot.com/atom.xml')
    expected = 'Thanks for the ping.'
    self.assertEquals(response, expected)


if __name__ == "__main__":
  unittest.main()
