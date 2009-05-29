import os
import yaml
from time import time
from base64 import encodestring
from urllib import urlencode

import local
import stubs

from google.appengine.api import urlfetch, memcache, apiproxy_stub_map, urlfetch_stub
from google.appengine.api.memcache import memcache_stub

def test():
  stubs.all()
  # canonical test
  cred = credentials()
  status = "test %s" % int(time())
  response = tweet(status=status, **cred)
  if '<id>' in response:
    print 'ok'
  else:
    print 'failed, got "%s"' % response

def credentials():
  config = local.config()
  if config:
    return config['twitter']

def tweet(status, username, password, source='Emend'):
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
