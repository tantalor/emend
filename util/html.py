import re
import htmlentitydefs
import html5lib
from html5lib import treebuilders, treewalkers
from html5lib.tokenizer import HTMLTokenizer
from html5lib.serializer.htmlserializer import HTMLSerializer

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

class StripTags(HTMLTokenizer):
  def __iter__(self):
    for token in super(StripTags, self).__iter__():
      if token["type"] not in ["StartTag", "EndTag", "EmptyTag"]:
        yield token

def strip_tags(html):
  if html:
    builder = treebuilders.getTreeBuilder("dom")
    parser = html5lib.HTMLParser(tree=builder, tokenizer=StripTags)
    tree = parser.parseFragment(html)
    walker = treewalkers.getTreeWalker("dom")
    stream = walker(tree)
    serializer = HTMLSerializer()
    return serializer.render(stream)

def clean(html):
  """Decodes html entities and strips tags"""
  return decode_entities(strip_tags(html))
