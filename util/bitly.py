import os
import sys
import yaml
import json
from time import time
from base64 import encodestring
from urllib import urlencode

from google.appengine.api import urlfetch, memcache, apiproxy_stub_map, urlfetch_stub
from google.appengine.api.memcache import memcache_stub

def test():
  if len(sys.argv) != 3:
    print "usage: python %s bitly.yaml dev" % sys.argv[0]
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
  longUrl = "http://google.com"
  response = shorten(longUrl=longUrl, **cred[sys.argv[2]])
  if 'http://bit.ly/' in response:
    print 'ok'
  else:
    print 'failed, got "%s"' % response

def credentials(filename='config/bitly.yaml'):
  credentials = memcache.get('bitly_credentials')
  if credentials:
    return credentials
  if os.path.exists(filename):
    credentials = yaml.load(file(filename).read())
    memcache.set('bitly_credentials', credentials)
    return credentials

def shorten(longUrl, login, apiKey):
  payload = urlencode(dict(
    longUrl=longUrl,
    login=login,
    apiKey=apiKey,
    version="2.0.1",
    format="json"))
  url = "http://api.bit.ly/shorten"
  response = urlfetch.fetch("%s?%s" % (url, payload))
  if response:
    data = json.read(response.content)
    if data['errorCode'] == 0:
      return data['results'][longUrl]['shortUrl']
    else:
      return data['errorMessage']
    # return response.content

if __name__ == '__main__':
  test();
