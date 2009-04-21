import os
import sys
import yaml
from time import time
from base64 import encodestring
from urllib import urlencode

from google.appengine.api import urlfetch, memcache, apiproxy_stub_map, urlfetch_stub
from google.appengine.api.memcache import memcache_stub

def test():
  if len(sys.argv) != 3:
    print "usage: python %s twitter.yaml dev" % sys.argv[0]
    return
  # setup urlfetch stub
  apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap() 
  apiproxy_stub_map.apiproxy.RegisterStub('urlfetch', 
    urlfetch_stub.URLFetchServiceStub())
  # setup memcache stub
  apiproxy_stub_map.apiproxy.RegisterStub('memcache', 
    memcache_stub.MemcacheServiceStub())
  # canonical test
  cred = credentials(sys.argv[1])
  status = "test %s" % int(time())
  response = tweet(status=status, **cred[sys.argv[2]])
  if '<id>' in response:
    print 'ok'
  else:
    print 'failed, got "%s"' % response

def credentials(filename='config/twitter.yaml'):
  credentials = memcache.get('twitter_credentials')
  if credentials:
    return credentials
  if os.path.exists(filename):
    credentials = yaml.load(file(filename).read())
    memcache.set('twitter_credentials', credentials)
    return credentials

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
  test();
