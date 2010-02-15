from google.appengine.api import urlfetch

import re

__canonical_re__ = re.compile('<link rel=["\']canonical["\'][^>]*href=["\']([^\'"]*)["\']')


def canonical_url(url):
  response = urlfetch.fetch(url.replace(' ', '%20'))
  if response:
    # print response.content
    # decode content
    html = unicode(response.content, 'iso-8859-1')
    return canonical_url_in_html(html)

def canonical_url_in_html(html):
  match = __canonical_re__.search(html)
  if match:
    return match.group(1)



if __name__ == '__main__':
  import stubs
  import sys
  stubs.urlfetch()
  print canonical_url(sys.argv[1])
