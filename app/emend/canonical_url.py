from google.appengine.api import urlfetch, memcache

import re
from urlparse import urlparse, urljoin

from megaera.fetch import fetch_decode


__canonical_re__ = re.compile('<link rel=["\']canonical["\'][^>]*href=["\']([^\'"]*)["\']')


def canonical_url(url):
  # check cache
  cache_key = "canonical_url(%s)"
  cached = memcache.get(cache_key % url)
  if cached:
    return cached
  # fetch conent
  html = fetch_decode(url)
  if html:
    # extract canonical url
    _url = canonical_url_in_html(html, url)
    if _url:
      # cache for posterity
      memcache.set(cache_key, _url)
      return _url

def canonical_url_in_html(html, url):
  match = __canonical_re__.search(html)
  if match:
    return urljoin(url, match.group(1))

if __name__ == '__main__':
  import stubs
  import sys
  stubs.urlfetch()
  stubs.memcache()
  print canonical_url(sys.argv[1])
