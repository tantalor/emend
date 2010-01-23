from html import decode_entities, strip_tags, clean
import unittest


class HTMLTest(unittest.TestCase):
  def testDecodeNumericEntities(self):
    """Decode numeric entities to unicode code points."""
    encoded = 'It&#8217;s my birthday'
    decoded = u'It\u2019s my birthday'
    self.assertEquals(decode_entities(encoded), decoded)
  
  def testStripTags(self):
    """Strip all tags."""
    encoded = '<p>This</table> <script>is <foo>bad</html> html.<body>'
    decoded = u'This is bad html.'
    self.assertEquals(strip_tags(encoded), decoded)
  
  def testClean(self):
    """Strip all tags and decode html entities to unicode code points."""
    encoded = '<p>From the Latin <i>emendare</i>, &#x201c;to free from fault.&rdquo;</p>'
    decoded = u'From the Latin emendare, \u201cto free from fault.\u201d'
    self.assertEquals(clean(encoded), decoded)


if __name__ == "__main__":
  unittest.main()
