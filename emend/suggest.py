# -*- coding: utf-8 -*-


from urllib import urlencode
import re

from megaera import local, json

from google.appengine.api import urlfetch


__APOSTROPHE_S_RE_ = re.compile(u"['’]s")


def suggest(query, **kwargs):
  """accepts unicode, returns unicode"""
  if type(query) is not unicode:
    raise TypeError
  return yahoo_suggest(query, **kwargs) or\
    apostrophe_s_suggest(query)

def apostrophe_s_suggest(query):
  """query should be unicode"""
  if __APOSTROPHE_S_RE_.search(query):
    return __APOSTROPHE_S_RE_.sub('s', query)

def yahoo_suggest(query, appid=None):
  if appid is None:
    # shortcut for no-credentials case
    credentials = local.config_get('yahoo')
    return suggest(query, **credentials)
  url = "http://search.yahooapis.com/WebSearchService/V1/spellingSuggestion"
  payload = urlencode(dict(output='json', query=query.encode('utf8'), appid=appid))
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
