from urllib import urlencode

from megaera import local, json

from google.appengine.api import urlfetch

def test():
  import stubs
  stubs.all()
  # canonical test
  query = "Lunar Reconnoissance Orbiter"
  response = suggest(query=query)
  if response == 'Lunar Reconnaissance Orbiter':
    print 'passed'
  elif response:
    print 'failed, got "%s"' % response
  else:
    print 'failed, got no suggestion'

def suggest(query, appid=None):
  """query should be utf8 encoded"""
  if appid is None:
    # shortcut for no-credentials case
    credentials = local.credentials('yahoo')
    return suggest(query, **credentials)
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
