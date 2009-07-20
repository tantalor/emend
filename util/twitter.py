from base64 import encodestring
from urllib import urlencode

import local

from google.appengine.api import urlfetch

def test():
  import stubs
  stubs.all()
  # canonical test
  from time import time
  status = "test %s" % int(time())
  response = tweet(status=status)
  if '<id>' in response:
    print 'ok'
  else:
    print 'failed, got "%s"' % response

def tweet(status, username=None, password=None, source='Emend'):
  if username is None and password is None:
    # shortcut for no-credentials case
    return tweet(status, **local.credentials('twitter'))
  payload = urlencode(dict(status=status, source=source))
  auth = encodestring('%s:%s' % (username, password))
  auth = auth.rstrip() # remove trailing newline
  headers = {'Authorization': "Basic %s" % auth}
  url = "http://twitter.com/statuses/update.xml"
  response = urlfetch.fetch(url,
    payload=payload, method=urlfetch.POST, headers=headers)
  if response:
    return response.content

if __name__ == '__main__':
  test()
