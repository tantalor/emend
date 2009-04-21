from sys import stderr
  
def warn(*args, **kwargs):
  if kwargs:
    warn(*["%s: %s" % (k, v) for k, v in kwargs.iteritems()])
  if args:
    stderr.write(">>> %s\n" % ', '.join([str(s) for s in args]))
