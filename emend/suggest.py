# -*- coding: utf-8 -*-


from urllib import urlencode
import re

from megaera import local, json

from google.appengine.api import urlfetch


__APOSTROPHE_S_RE_ = re.compile(u"['’]s")

__A_VOWEL_SOUND__ = re.compile(u"a ([aeiouh])")


def suggest(query, **kwargs):
  """accepts unicode, returns unicode"""
  if type(query) is not unicode:
    raise TypeError
  suggest_functions = [
    yahoo_suggest,
    apostrophe_s_suggest,
    a_vowel_sound_suggest,
  ]
  for function in suggest_functions:
    query = function(query, **kwargs) or query
  return query

def apostrophe_s_suggest(query, **kwargs):
  return __APOSTROPHE_S_RE_.sub('s', query)

def a_vowel_sound_suggest(query, **kwargs):
  def repl(m):
    return ' '.join(['an', m.group(1)])
  return __A_VOWEL_SOUND__.sub(repl, query)

def yahoo_suggest(query, appid=None, **kwargs):
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
