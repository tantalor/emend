from base64 import encodestring
from urllib import urlencode

from megaera import local

from oauth import signed_url

from google.appengine.api import urlfetch

def test():
  import stubs
  stubs.all()
  # canonical test
  from time import time
  status = "test %s" % int(time())
  response = tweet(status=status)
  if '<text>%s</text>' % status in response:
    print 'passed'
  else:
    print 'failed, got "%s"' % response

def tweet(status, **credentials):
  if not credentials:
    # shortcut for no-credentials case
    credentials = local.credentials('twitter')
  update_url = "http://twitter.com/statuses/update.xml"
  fetch_url = signed_url(url=update_url, method='POST', status=status, **credentials)
  response = urlfetch.fetch(fetch_url, method=urlfetch.POST)
  if response:
    return response.content

if __name__ == '__main__':
  test()
