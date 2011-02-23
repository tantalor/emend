from google.appengine.ext import db

class Counts():
  def pretty_counts(self):
    counts = []
    if self.open:
      plural = ''
      if self.open > 1:
        plural = 's'
      counts.append('%s open edit%s' % (self.open, plural))
    if self.closed:
      counts.append('%s fixed' % self.closed)
    if counts:
      return "(%s)" % ', '.join(counts)
    else:
      return ''
