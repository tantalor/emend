import unittest

import megaera
from megaera import MegaeraRequestHandler

from google.appengine.ext.webapp import Request, Response
from google.appengine.api import apiproxy_stub_map
from google.appengine.api.memcache import memcache_stub


class MockTemplate:
  def render(self, path, vars):
    self.path = path
    self.vars = vars


def mock_handler(file='handlers/mock.py', request='/mock', **response):
  class MockPage: __file__ = file
  handler = MegaeraRequestHandler.with_page(MockPage())()
  handler.initialize(Request.blank(request), Response())
  handler.response_dict(**response)
  return handler


def stub_memcache():
  try:
    apiproxy_stub_map.apiproxy.RegisterStub('memcache', 
      memcache_stub.MemcacheServiceStub())
  except AssertionError:
    pass

class TestMegaera(unittest.TestCase):
  def setUp(self):
    self.mock_template = megaera.request_handler.template = MockTemplate()
    stub_memcache()
  
  def test_with_page(self):
    class MockPage: __file__ = ''
    page = MockPage()
    handler = MegaeraRequestHandler.with_page(page)()
    self.assertEquals(handler.page, page)
  
  def test_default_template(self):
    handler = mock_handler(file='handlers/foo/bar.py')
    template = handler.default_template()
    self.assertEquals(template, 'foo/bar.html')
  
  def test_atom_template(self):
    handler = mock_handler(file='handlers/foo/bar.py')
    template = handler.default_template(ext='atom')
    self.assertEquals(template, 'foo/bar.atom')
  
  def test_is_atom(self):
    handler = mock_handler()
    self.assertFalse(handler.is_atom())
    atom_handler = mock_handler(request='/?atom')
    self.assertTrue(atom_handler.is_atom())
  
  def test_is_json(self):
    handler = mock_handler()
    self.assertFalse(handler.is_json())
    json_handler = mock_handler(request='/?json')
    self.assertTrue(json_handler.is_json())
  
  def test_post_override(self):
    class PostClosure():
      is_post = False
      def post(self): self.is_post = True
    handler = mock_handler(request='/?post')
    post_closure = PostClosure()
    handler.post = post_closure.post
    handler.get()
    self.assertTrue(post_closure.is_post)
  
  def test_render(self):
    handler = mock_handler(file='handlers/foo/bar.py')
    handler.file_exists = lambda self: True
    handler.render(None)
    self.assertEquals(self.mock_template.path, 'templates/foo/bar.html')
  
  def test_atom_render(self):
    handler = mock_handler(file='handlers/foo/bar.py', request='/?atom')
    handler.file_exists = lambda self: True
    handler.render(None)
    self.assertTrue(handler.is_atom())
    self.assertEquals(self.mock_template.path, 'templates/foo/bar.html')
  
  def test_cache(self):
    handler = mock_handler()
    handler.cache(foo='foo')
    handler = mock_handler()
    self.assertTrue(handler.cached())
    self.assertEquals(handler.response_dict().foo, 'foo')
  
  def test_cache_vary(self):
    handler = mock_handler()
    handler.cache(foo='foo', vary='bar')
    handler = mock_handler()
    self.assertTrue(handler.cached(vary='bar'))
    self.assertEquals(handler.response_dict().foo, 'foo')
  
  def test_cache_invalidate(self):
    handler = mock_handler()
    handler.cache(foo='foo')
    handler = mock_handler()
    handler.invalidate()
    self.assertFalse(handler.cached())
  
  def test_cache_vary_invalidate(self):
    handler = mock_handler()
    handler.cache(foo='foo', vary='bar')
    handler = mock_handler()
    handler.invalidate(vary='bar')
    self.assertFalse(handler.cached())
  

if __name__ == '__main__':
  unittest.main()
