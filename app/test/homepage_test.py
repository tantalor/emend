# -*- coding: utf-8 -*-


import unittest
from urllib import urlencode

from mocks import mock_handler
from emend import stubs


class TestHomepage(unittest.TestCase):
  def setUp(self):
    stubs.all()
    
  def test_unicode_suggest(self):
    original = u"the original design"
    request = '/?%s' % urlencode(dict(original=original.encode('utf8')))
    # mock handler
    import handlers.default
    handler = mock_handler(page=handlers.default, request=request)
    # execute handlers  
    try:
      handler.get()
    except UnicodeEncodeError:
      self.fail('failed to encode unicode')


if __name__ == "__main__":
  unittest.main()
