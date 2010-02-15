from google.appengine.api import urlfetch, memcache

import re

__canonical_re__ = re.compile('<link rel=["\']canonical["\'][^>]*href=["\']([^\'"]*)["\']')


def canonical_url(url):
  # check cache
  cache_key = "canonical_url(%s)"
  cached = memcache.get(cache_key % url)
  if cached:
    return cached
  # fetch conent
  response = urlfetch.fetch(url.replace(' ', '%20'))
  if response:
    # decode content
    html = unicode(response.content, 'iso-8859-1')
    # extract canonical url
    _url = canonical_url_in_html(html)
    if _url:
      # cache for posterity
      memcache.set(cache_key, _url)
      return _url

def canonical_url_in_html(html):
  match = __canonical_re__.search(html)
  if match:
    return match.group(1)


if __name__ == '__main__':
  import stubs
  import sys
  stubs.urlfetch()
  stubs.memcache()
  print canonical_url(sys.argv[1])
