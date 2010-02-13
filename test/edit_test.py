# -*- coding: utf-8 -*-

import unittest

import handlers.sites.edits.detail
from mocks.edit_mock import MockEdit
from mocks.handler_mock import mock_handler
from emend import stubs

class TestEdit(unittest.TestCase):
  def setUp(self):
    stubs.all()
  
  def test_unicode_original(self):
    """An edit with unicode characters"""
    # mock edit
    original = u"Don’t judge a proggie by it’s UI"
    edit = MockEdit(original=original, proposal=original)
    # mock handler
    handler = mock_handler(page=handlers.sites.edits.detail, edit=edit)
    # execute handler
    try:
      handler.get()
    except UnicodeDecodeError:
      self.fail("failed to decode unicode")
    except UnicodeEncodeError:
      self.fail("failed to encode unicode")
  
  def test_unicode_url(self):
    """A URL with unicode characters"""
    # mock edit
    url = u"http://test.com/“tell-your-girl”/"
    edit = MockEdit(url=url)
    # mock handler
    handler = mock_handler(page=handlers.sites.edits.detail, edit=edit)
    # execute handler
    try:
      handler.get()
    except UnicodeEncodeError:
      self.fail("failed to encode unicode")
  
  def test_as_tweet(self):
    """Tweets of various lengths"""
    original = ("Lorem ipsum dolor sit amet, consectetur adipisicing elit, "
                "sed do eiusmod tempor incididunt ut labore et dolore magna "
                "aliqua. Ut enim ad minim veniam, quis nostrud exercitation "
                "ullamco laboris nisi ut aliquip ex ea commodo consequat.")
    proposal = ("Duis aute irure dolor in reprehenderit in voluptate velit "
                "esse cillum dolore eu fugiat nulla pariatur. Excepteur sint "
                "occaecat cupidatat non proident, sunt in culpa qui officia "
                "deserunt mollit anim id est laborum.")
    edit = MockEdit(original=original, proposal=proposal)
    for max_len in (100, 120, 140, 160, 180):
      tweet = edit.as_tweet(max_len=max_len)
      if len(tweet) > max_len:
        self.fail("tweet is too long")
  
  def test_close(self):
    edit = MockEdit()
    site = edit.site
    author = edit.author
    site_open, site_closed = site.open, site.closed
    author_open, author_closed = author.open, author.closed
    edit.close()
    self.assertEquals(site_open - 1, site.open)
    self.assertEquals(site_closed + 1, site.closed)
    self.assertEquals(author_open - 1, author.open)
    self.assertEquals(author_closed + 1, author.closed)
  
  def test_open(self):
    edit = MockEdit(status="closed")
    site = edit.site
    author = edit.author
    site_open, site_closed = site.open, site.closed
    author_open, author_closed = author.open, author.closed
    edit.open()
    self.assertEquals(site_open + 1, site.open)
    self.assertEquals(site_closed - 1, site.closed)
    self.assertEquals(author_open + 1, author.open)
    self.assertEquals(author_closed - 1, author.closed)
  
  def test_delete_open(self):
    edit = MockEdit()
    site = edit.site
    author = edit.author
    site_open = site.open
    author_open = author.open
    edit.delete()
    self.assertEquals(site_open - 1, site.open)
    self.assertEquals(author_open - 1, author.open)
  
  def test_delete_closed(self):
    edit = MockEdit(status="closed")
    site = edit.site
    author = edit.author
    site_closed = site.closed
    author_closed = author.closed
    edit.delete()
    self.assertEquals(site_closed - 1, site.closed)
    self.assertEquals(author_closed - 1, author.closed)
  
  def test_fixed(self):
    edit = MockEdit(original="zombie", proposal="ninja")
    def mock_content():
      return "pirate ninja robot"
    edit.page_content = mock_content
    self.assertEquals(edit.test(), "fixed")
  
  def test_unfixed(self):
    edit = MockEdit(original="ninja", proposal="zombie")
    def mock_content():
      return "pirate ninja robot"
    edit.page_content = mock_content
    self.assertEquals(edit.test(), "unfixed")
  
  def test_uncertain(self):
    edit = MockEdit(original="spam", proposal="eggs")
    def mock_content():
      return "pirate ninja robot"
    edit.page_content = mock_content
    self.assertEquals(edit.test(), "uncertain")
  
  def test_substring_fixed(self):
    edit = MockEdit(original="ninja robot", proposal="ninja")
    def mock_content():
      return "pirate ninja"
    edit.page_content = mock_content
    self.assertEquals(edit.test(), "fixed")
  
  def test_substring_unfixed(self):
    edit = MockEdit(original="ninja robot", proposal="ninja")
    def mock_content():
      return "pirate ninja robot"
    edit.page_content = mock_content
    self.assertEquals(edit.test(), "unfixed")
  
  def test_substring_uncertain(self):
    edit = MockEdit(original="ninja robot", proposal="ninja")
    def mock_content():
      return "spam eggs"
    edit.page_content = mock_content
    self.assertEquals(edit.test(), "uncertain")


if __name__ == "__main__":
  unittest.main()
