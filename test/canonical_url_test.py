import unittest

from emend import stubs
from emend.canonical_url import canonical_url_in_html


class TestCanonicalURL(unittest.TestCase):
  def setUp(self):
    stubs.urlfetch()

  def test_canonical_url_in_html(self):
    expected = 'http://example.com'
    html = '<link rel="canonical" href="%s" />' % expected
    canonical_url = canonical_url_in_html(html)
    self.assertEquals(canonical_url, expected)

  def test_canonical_url_in_html_with_single_quotes(self):
    expected = 'http://example.com'
    html = '<link rel=\'canonical\' href=\'%s\' />' % expected
    canonical_url = canonical_url_in_html(html)
    self.assertEquals(canonical_url, expected)


if __name__ == "__main__":
  unittest.main()
