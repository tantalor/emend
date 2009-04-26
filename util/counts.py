class Counts:
  """Abstract base class to present something with counts."""
  def counts(self):
    """Needs an 'open' and 'closed' attribute or property."""
    counts = []
    if self.open:
      plural = ''
      if self.open > 1:
        plural = 's'
      counts.append('%s open edit%s' % (self.open, plural))
    if self.closed:
      counts.append('%s fixed' % self.closed)
    if counts:
      return ', '.join(counts)
