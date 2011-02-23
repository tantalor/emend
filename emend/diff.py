from difflib import SequenceMatcher

def diff(src, dst):
  def ops():
    seq = SequenceMatcher(None, src, dst)
    for (op, i1, i2, j1, j2) in seq.get_opcodes():
      if op[0] == 'd':
        yield '<span style="background-color:#faa">%s</span>' % src[i1:i2]
      elif op[0] == 'i':
        yield '<span style="background-color:#ada">%s</span>' % dst[j1:j2]
      elif op[0] == 'r':
        yield '<span style="background-color:#faa">%s</span>'\
              '<span style="background-color:#ada">%s</span>'\
              % (src[i1:i2], dst[j1:j2])
      else:
        yield src[i1:i2]
  return ''.join(s for s in ops())

def diff_src(src, dst):
  return direct_diff(src, dst)

def diff_dst(src, dst):
  return direct_diff(src, dst, invert=True)

def direct_diff(src, dst, invert=False):
  def ops(src, dst):
    seq = SequenceMatcher(None, src, dst)
    if invert:
      return dst, [(op, j1, j2) for (op, i1, i2, j1, j2) in seq.get_opcodes() if op != 'd']
    else:
      return src, [(op, i1, i2) for (op, i1, i2, j1, j2) in seq.get_opcodes() if op != 'i']
  def span(subject, op, i, j):
    if op == 'equal':
      return subject[i:j]
    else:
      return '<span style="background-color:#%s">%s</span>' % (
        'ada' if invert else 'faa',
        subject[i:j])
  # get opcodes and subject string (src or dst)
  subject, opcodes = ops(src, dst)
  # map opcodes to a list of spans (.same or .different)
  spans = [span(subject, op, i, j) for (op, i, j) in opcodes]
  return ''.join(spans)

