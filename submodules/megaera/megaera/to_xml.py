from xml.dom.minidom import Document


def to_xml(obj, tag="data"):
  """Returns XML from dicts or seqs."""
  doc = Document()
  body = doc.createElement(tag)
  add(doc, body, obj)
  doc.appendChild(body)
  return doc.toprettyxml(indent='  ')

def add(doc, elem, obj):
  """Adds object to document at element."""
  if isinstance(obj, dict):
    # dictionary
    add_dict(doc, elem, obj)
  elif hasattr(obj, '__iter__'):
    # sequence
    add_seq(doc, elem, obj)
  else:
    # default: text node
    child = doc.createTextNode(str(obj))
    elem.appendChild(child)

def add_dict(doc, elem, d):
  """Adds dictionary to document at element."""
  for key, value in d.iteritems():
    child = doc.createElement(key)
    add(doc, child, value)
    elem.appendChild(child)

def add_seq(doc, elem, seq, tag="value"):
  """Adds sequence to document at element."""
  for value in seq:
    child = doc.createElement(tag)
    add(doc, child, value)
    elem.appendChild(child)
