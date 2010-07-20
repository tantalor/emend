from urllib import urlencode

from megaera import local, json

from google.appengine.api import urlfetch

def suggest(query, **kwargs):
  return yahoo_suggest(query, **kwargs) or\
    apostrophe_s_suggest(query)

def apostrophe_s_suggest(query):
  removed_apostrophe = query.replace("'s", 's')
  if len(removed_apostrophe) != len(query):
    return removed_apostrophe

def yahoo_suggest(query, appid=None):
  """query should be utf8 encoded"""
  if appid is None:
    # shortcut for no-credentials case
    credentials = local.config_get('yahoo')
    return suggest(query, **credentials)
  url = "http://search.yahooapis.com/WebSearchService/V1/spellingSuggestion"
  payload = urlencode(dict(output='json', query=query, appid=appid))
  response = urlfetch.fetch('%s?%s' % (url, payload))
  if response:
    try:
      data = json.read(response.content)
      if data and data['ResultSet']:
        result = data['ResultSet']['Result']
        if result != 'None':
          return result
    except json.ReadException:
      pass
