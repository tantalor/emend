# -*- coding: utf-8 -*-

from difflib import SequenceMatcher
from os import environ
from urllib import quote
import cgi
from rfc3339 import datetimetostr as datetime_to_rfc3339

from google.appengine.ext.webapp import template

register = template.create_template_register()

def escape(s):
  return quote(str(s), safe='~')

from logging import warn

@register.filter
def truncate(value, length, suffix=u'…'):
  length = int(length)
  if len(value) > length:
    return value[:length]+suffix
  else:
    return value


@register.filter
def strip(value):
  return value.strip()


@register.filter
def utf8(value):
  return unicode(value).encode('utf8')


@register.filter
def rfc3339(datetime):
  return datetime_to_rfc3339(datetime)


@register.filter
def on_path(value):
  query_string = environ.get('QUERY_STRING')
  if query_string:
    path_info = environ.get('PATH_INFO')
    escaped_query = query_string.replace('&', '&amp;')
    return "%s?%s&amp;%s" % (path_info, escaped_query, escape(value))
  else:
    return "?%s" % value


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

@register.filter
def diff(src, dst):
  def ops():
    seq = SequenceMatcher(None, src, dst)
    for (op, i1, i2, j1, j2) in seq.get_opcodes():
      if op[0] == 'd':
        yield '<span style="background-color:#faa">%s</span>' % src[i1:i2]
      elif op[0] == 'i':
        yield '<span style="background-color:#ada">%s</span>' % dst[j1:j2]
      else:
        yield src[i1:i2]
  return ''.join(s.encode('utf8') for s in ops())

@register.tag
def diff_src(parser, token):
  (_, src_key, dst_key) = token.split_contents()
  return DiffNode(src_key, dst_key)

@register.tag
def diff_dst(parser, token):
  (_, src_key, dst_key) = token.split_contents()
  return DiffNode(src_key, dst_key, invert=True)

class DiffNode(template.django.template.Node):
  """Annotate a string with a description of string operations."""
  def __init__(self, src_key, dst_key, invert=False):
    self.src_key = src_key
    self.dst_key = dst_key
    self.invert = invert
  
  def render(self, context):
    try:
      src = cgi.escape(template.django.template.resolve_variable(self.src_key, context))
      dst = cgi.escape(template.django.template.resolve_variable(self.dst_key, context))
      # get opcodes and subject string (src or dst)
      subject, opcodes = self.opcodes(src, dst)
      # map opcodes to a list of spans (.same or .different)
      spans = [self.span(subject, op, i, j) for (op, i, j) in opcodes]
      return ''.join(spans)
    except template.django.template.VariableDoesNotExist:
      pass
    return ''
  
  def opcodes(self, src, dst):
    # sequence matcher (sensitive to spaces)
    seq = SequenceMatcher(None, src, dst)
    if self.invert:
      return dst, [(op, j1, j2) for (op, i1, i2, j1, j2) in seq.get_opcodes() if op != 'd']
    else:
      return src, [(op, i1, i2) for (op, i1, i2, j1, j2) in seq.get_opcodes() if op != 'i']
  
  def span(self, subject, op, i, j):
    if op == 'equal':
      return subject[i:j].encode('utf8')
    else:
      return '<span style="background-color:#%s">%s</span>' % (
        'ada' if self.invert else 'faa',
        subject[i:j].encode('utf8'))


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
      else:
        return ''
    except template.django.template.VariableDoesNotExist:
      pass
