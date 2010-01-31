import unittest

from util import stubs
from util.suggest import suggest


class TestSuggest(unittest.TestCase):
  def setUp(self):
    stubs.all()
  
  def test_suggest(self):
    query = "Lunar Reconnoissance Orbiter"
    expected = "Lunar Reconnaissance Orbiter"
    suggestion = suggest(query=query)
    self.assertEquals(suggestion, expected)


if __name__ == "__main__":
  unittest.main()
