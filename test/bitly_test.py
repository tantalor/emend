import unittest

from util import stubs
from util.bitly import shorten


class TestBitly(unittest.TestCase):
  def setUp(self):
    stubs.all()

  def testShorten(self):
    longUrl = "http://google.com"
    response = shorten(longUrl=longUrl)
    expected = "http://bit.ly/1BArVh"
    self.assertEquals(expected, response)


if __name__ == "__main__":
  unittest.main()
