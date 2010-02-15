from google.appengine.api import urlfetch

from urllib import urlencode


def ping(name, url, changesURL, ping_url='http://blogsearch.google.com/ping'):
  payload = urlencode(dict(name=name, url=url, changesURL=changesURL))
  response = urlfetch.fetch('%s?%s' % (ping_url, payload))
  if response:
    return response.content
