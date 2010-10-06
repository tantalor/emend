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
  
  def test_a_vowel_sound(self):
    query = u"a ant"
    expected = u"an ant"
    suggestion = suggest(query=query)
    self.assertEquals(suggestion, expected)
  
  def test_combination(self):
    query = u"it's a ant"
    expected = u"its an ant"
    suggestion = suggest(query=query)
    self.assertEquals(suggestion, expected)


if __name__ == "__main__":
  unittest.main()
