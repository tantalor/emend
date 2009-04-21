from google.appengine.ext.webapp import template
from util.warn import warn

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
def describe(parser, token):
  (_, string_key, desc_key) = token.split_contents()
  return DescribeNode(string_key, desc_key)

class DescribeNode(template.django.template.Node):
  """Annotate a string with a description of string operations."""
  def __init__(self, string_key, desc_key):
    self.string_key = string_key
    self.desc_key = desc_key
  
  def render(self, context):
    try:
      string = template.django.template.resolve_variable(self.string_key, context)
      desc = template.django.template.resolve_variable(self.desc_key, context)
      return ''.join(map(DescribeNode.span, zip(string, desc)))
    except template.django.template.VariableDoesNotExist:
      pass
    return ''
  
  @staticmethod
  def span(pair):
    c, op = pair
    c = c.encode('utf8')
    if c == '\r':
      return ''
    if c == '\n':
      return '<br>'
    if op == 'p':
      return c
    return '<span class="%s">%s</span>' % (op, c)
