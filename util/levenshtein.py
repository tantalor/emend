_op_rp_ = {0: 'p', 1: 'r'}

def levenshtein(src, dst):
  lsrc, ldst = len(src), len(dst)
  d = []; # len(src) x len(dst) -> (int, p|r|i|d)
  for i in xrange(lsrc+1):
    d.append([0] * (ldst+1))
    d[i][0] = (i, 'i')
  for j in xrange(1, ldst+1):
    d[0][j] = (j, 'd')
  d[0][0] = (0, 'p')
  for i in xrange(0, lsrc):
    for j in xrange(0, ldst):
      cost = int(src[i] != dst[j])
      choices = {
        d[i][j][0]+cost: _op_rp_[cost],
        d[i][j+1][0]+1: 'd',
        d[i+1][j][0]+1: 'i'
      }
      best = min(choices)
      d[i+1][j+1] = (best, choices[best])
  return d

def levenshtein(src, dst):
  lsrc, ldst = len(src), len(dst)
  d = []; # len(dst) x len(src) -> (int, p|r|i|d)
  for i in xrange(ldst+1):
    d.append([0] * (lsrc+1))
    d[i][0] = (i, 'i')
  for j in xrange(1, lsrc+1):
    d[0][j] = (j, 'd')
  d[0][0] = (0, 'p')
  for i in xrange(0, ldst):
    for j in xrange(0, lsrc):
      cost = int(dst[i] != src[j])
      choices = {
        d[i][j][0]+cost: _op_rp_[cost],
        d[i][j+1][0]+1: 'i',
        d[i+1][j][0]+1: 'd'
      }
      best = min(choices)
      d[i+1][j+1] = (best, choices[best])
  return d

def distance(src, dst):
  lev = levenshtein(src, dst)
  return lev[len(dst)][len(src)][0]

def sequence(src, dst):
  lev = levenshtein(src, dst)
  seq = []
  i, j = len(dst), len(src)
  while i or j:
    op = lev[i][j][1]
    seq.insert(0, op)
    if not op == 'd':
      i = i-1
    if not op == 'i':
      j = j-1
  return seq

def describe(src, dst):
  seq = sequence(src, dst)
  def map_op(op1, op2):
    if op1 == 'r':
      return op2
    return op1
  # map r to d and filter out i
  src_seq = [map_op(op, 'd') for op in seq if op != 'i']
  # map r to i and filter out d
  src_dst = [map_op(op, 'i') for op in seq if op != 'd']
  return src_seq, src_dst

def test():
  args = "sunday", "saturday"
  desc = describe(*args)
  if distance(*args) == 3 and\
    ''.join(sequence(*args)) == 'piiprppp' and\
    ''.join(desc[0]) == 'ppdppp' and\
    ''.join(desc[1]) == 'piipippp':
    return "ok"

if __name__ == '__main__':
  print test()
