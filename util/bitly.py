import json
from base64 import encodestring
from urllib import urlencode

import local

from google.appengine.api import urlfetch

def test():
  import stubs
  stubs.all()
  # canonical test
  cred = credentials()
  longUrl = "http://google.com"
  response = shorten(longUrl=longUrl, **cred)
  if 'http://bit.ly/' in response:
    print 'ok'
  else:
    print 'failed, got "%s"' % response

def credentials():
  config = local.config()
  if config:
    return config['bitly']

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
    try:
      data = json.read(response.content)
      if data['errorCode'] == 0:
        return data['results'][longUrl]['shortUrl']
    except json.ReadException:
      pass

if __name__ == '__main__':
  test();
