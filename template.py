from difflib import SequenceMatcher

from google.appengine.ext.webapp import template

register = template.create_template_register()


@register.filter
def truncate(value, length, suffix='&hellip;'):
  length = int(length)
  value = str(value)
  if len(value) > length:
    return value[:length]+suffix
  else:
    return value


@register.filter
def strip(value):
  return value.strip()


@register.filter
def utf8(value):
  return value.encode('utf8')


@register.tag
def form_error(parser, token):
  (_, key) = token.split_contents()
  return FormErrorNode(key)

class FormErrorNode(template.django.template.Node):
  """Add <span class="error">...</span> elements to bad fields."""
  def __init__(self, key):
    self.key = key
  
  def render(self, context):
    variable = "errors.%s" % self.key
    try:
      error = template.django.template.resolve_variable(variable, context)
      if error:
        return '<span class="error">%s</span>' % error
    except template.django.template.VariableDoesNotExist:
      pass
    return ''


@register.tag
def diff(parser, token):
  (_, src_key, dst_key) = token.split_contents()
  return DiffNode(src_key, dst_key)

class DiffNode(template.django.template.Node):
  """Annotate a string with a description of string operations."""
  def __init__(self, src_key, dst_key):
    self.src_key = src_key
    self.dst_key = dst_key
  
  def render(self, context):
    try:
      src = template.django.template.resolve_variable(self.src_key, context)
      dst = template.django.template.resolve_variable(self.dst_key, context)
      # utf8 encode
      src = src.encode('utf8')
      dst = dst.encode('utf8')
      # sequence matcher (sensitive to spaces)
      seq = SequenceMatcher(None, src, dst)
      # map opcodes to a list of spans (.same or .different)
      spans = [DiffNode.span(src, op) for op in seq.get_opcodes()]
      return ''.join(spans)
    except template.django.template.VariableDoesNotExist:
      pass
    return ''
  
  @staticmethod
  def span(src, (op, i1, i2, j1, j2)):
    if i1 == i2:
      return ''
    elif op == 'equal':
      return '<span class="same">%s</span>' % src[i1:i2]
    else:
      return '<span class="different">%s</span>' % src[i1:i2]


@register.tag
def counts(parser, token):
  (_, string_key) = token.split_contents()
  return CountsNode(string_key)

class CountsNode(template.django.template.Node):
  """Describe the counts of an object."""
  def __init__(self, string_key):
    self.string_key = string_key
  
  def render(self, context):
    try:
      obj = template.django.template.resolve_variable(self.string_key, context)
      counts = []
      if obj.open:
        plural = ''
        if obj.open > 1:
          plural = 's'
        counts.append('%s open edit%s' % (obj.open, plural))
      if obj.closed:
        counts.append('%s fixed' % obj.closed)
      if counts:
        return "(%s)" % ', '.join(counts)
    except template.django.template.VariableDoesNotExist:
      pass
