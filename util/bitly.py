from base64 import encodestring
from urllib import urlencode

from megaera import local, json

from google.appengine.api import urlfetch


def shorten(longUrl, login=None, apiKey=None):
  if login is None and apiKey is None:
    # shortcut for no-credentials case
    credentials = local.config_get('bitly')
    return shorten(longUrl, **credentials)
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
