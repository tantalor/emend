def sanitize(obj):
  """Sanitize for json or yaml output."""
  if isinstance(obj, dict):
    # a dictionary
    return dict([(key, sanitize(value)) for key, value in obj.iteritems()])
  if hasattr(obj, '__iter__'):
    # a iterable sequence
    return [sanitize(v) for v in obj]
  if hasattr(obj, 'sanitize'):
    # a sanitizeable object
    return obj.sanitize()
  if isinstance(obj, BaseException):
    # an exception
    return str(obj)
  return obj
