import unittest

from emend import stubs, suggest


class TestSuggest(unittest.TestCase):
  def setUp(self):
    stubs.all()
  
  def test_spelling(self):
    query = "Lunar Reconnoissance Orbiter"
    expected = "Lunar Reconnaissance Orbiter"
    suggestion = suggest(query=query)
    self.assertEquals(suggestion, expected)
  
  def test_apostrophe_s(self):
    query = "in my 20's"
    expected = "in my 20s"
    suggestion = suggest(query=query)
    self.assertEquals(suggestion, expected)


if __name__ == "__main__":
  unittest.main()
