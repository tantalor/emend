import json
from urllib import urlencode

import local

from google.appengine.api import urlfetch

def test():
  import stubs
  stubs.all()
  # canonical test
  cred = credentials()
  query = "Lunar Reconnoissance Orbiter"
  response = suggest(query=query, **cred)
  if response == 'Lunar Reconnaissance Orbiter':
    print 'ok'
  elif response:
    print 'failed, got "%s"' % response
  else:
    print 'failed, got no suggestion'

def credentials():
  config = local.config()
  if config:
    return config['yahoo']

def suggest(query, appid):
  url = "http://search.yahooapis.com/WebSearchService/V1/spellingSuggestion"
  payload = urlencode(dict(output='json', query=query, appid=appid))
  response = urlfetch.fetch('%s?%s' % (url, payload))
  if response:
    try:
      data = json.read(response.content)
      if data['ResultSet']:
        result = data['ResultSet']['Result']
        if result != 'None':
          return result
    except json.ReadException:
      pass

if __name__ == '__main__':
  test()
