import unittest

from emend import stubs
from emend.canonical_url import canonical_url_in_html


class TestCanonicalURL(unittest.TestCase):
  def setUp(self):
    stubs.urlfetch()

  def test_canonical_url_in_html(self):
    url = 'http://example.com'
    canonical_url = url
    expected = url
    html = '<link rel="canonical" href="%s" />' % canonical_url
    canonical_url = canonical_url_in_html(html, url)
    self.assertEquals(canonical_url, expected)

  def test_canonical_url_in_html_with_single_quotes(self):
    url = 'http://example.com'
    canonical_url = url
    expected = url
    html = '<link rel=\'canonical\' href=\'%s\' />' % canonical_url
    canonical_url = canonical_url_in_html(html, url)
    self.assertEquals(canonical_url, expected)

  def test_relative_path(self):
    url = 'http://example.com'
    canonical_url = "/index.html"
    expected = url+canonical_url
    html = '<link rel="canonical" href="%s" />' % canonical_url
    canonical_url = canonical_url_in_html(html, url)
    self.assertEquals(canonical_url, expected)


if __name__ == "__main__":
  unittest.main()
