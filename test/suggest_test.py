# -*- coding: utf-8 -*-


import unittest

from emend import stubs, suggest


class TestSuggest(unittest.TestCase):
  def setUp(self):
    stubs.urlfetch()
    stubs.memcache()
  
  def test_ascii_fails(self):
    self.failUnlessRaises(TypeError, lambda: suggest('ascii'))
  
  def test_spelling(self):
    query = u"Lunar Reconnoissance Orbiter"
    expected = u"Lunar Reconnaissance Orbiter"
    suggestion = suggest(query=query)
    self.assertEquals(suggestion, expected)
  
  def test_apostrophe_s(self):
    query = u"in my 20's"
    expected = u"in my 20s"
    suggestion = suggest(query=query)
    self.assertEquals(suggestion, expected)
  
  def test_apostrophe_s_unicode(self):
    query = u"in my 20’s"
    expected = u"in my 20s"
    suggestion = suggest(query=query)
    self.assertEquals(suggestion, expected)


if __name__ == "__main__":
  unittest.main()
