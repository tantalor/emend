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
  suggestion = query
  for function in suggest_functions:
    suggestion = function(suggestion, **kwargs) or query
  if suggestion != query:
    return suggestion

def apostrophe_s_suggest(query, **kwargs):
  return __APOSTROPHE_S_RE_.sub('s', query)

def a_vowel_sound_suggest(query, **kwargs):
  def repl(m):
    return ' '.join(['an', m.group(1)])
  return __A_VOWEL_SOUND__.sub(repl, query)

def yahoo_suggest(query, **kwargs):
  url = "http://query.yahooapis.com/v1/public/yql"
  yql = "select * from search.spelling where query='%s'" % query.replace("'", "\\'").encode('utf8')
  response = urlfetch.fetch('%s?%s' % (url, urlencode(dict(format='json', q=yql))))
  if response:
    try:
      data = json.read(response.content)
      if data and 'query' in data and data['query']['results']:
        return data['query']['results']['suggestion']
    except json.ReadException:
      pass
