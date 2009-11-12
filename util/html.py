import re

# by no means exhaustive
entities = {
  u'&quot;':   u'\u0022', # double quotation mark
  u'&ldquo;':  u'\u201c', # left double quotation mark
  u'&rdquo;':  u'\u201d', # right double quotation mark
  u'&amp;':    u'\u0026', # ampersand
  u'&apos;':   u'\u0027', # apostrophe
  u'&lt;':     u'\u003C', # less-than sign
  u'&gt;':     u'\u003E', # greater-than sign
}

def decode_entities(html):
  # numeric entities
  matches = re.findall("(&\#(x?)([0-9a-f]+);)", html, re.IGNORECASE)
  for match, is_hex, entity in matches:
    base = 10
    if is_hex:
      base = 16
    html = html.replace(match, unichr(int(entity, base)))
  # predefined entities
  for entity, codepoint in entities.iteritems():
    html = html.replace(entity, codepoint)
  return html
