import unittest

from emend import stubs
from emend.bitly import shorten


class TestBitly(unittest.TestCase):
  def setUp(self):
    stubs.all()

  def test_shorten(self):
    longUrl = "http://google.com"
    response = shorten(longUrl=longUrl)
    self.assertTrue(response.startswith('http://bit.ly/'))


if __name__ == "__main__":
  unittest.main()
