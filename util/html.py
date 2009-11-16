import re
import htmlentitydefs
import HTMLParser

def decode_entities(html):
  # numeric entities
  matches = re.findall("(&\#(x?)([0-9a-f]+);)", html, re.IGNORECASE)
  for match, is_hex, entity in matches:
    base = 10
    if is_hex:
      base = 16
    html = html.replace(match, unichr(int(entity, base)))
  # predefined entities
  for entity, codepoint in htmlentitydefs.name2codepoint.iteritems():
    html = html.replace('&%s;' % entity, unichr(codepoint))
  return html

class StripTags(HTMLParser.HTMLParser):
  def __init__(self):
    self.reset()
    self.data = []
  def handle_data(self, d):
    self.data.append(d)
  def get_text(self):
    return ''.join(self.data)

def strip_tags(html):
  parser = StripTags()
  parser.feed(html)
  return parser.get_text()

def clean(html):
  """Decodes html entities and strips tags"""
  return decode_entities(strip_tags(html))
