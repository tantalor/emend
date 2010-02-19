from collections import defaultdict

class recursivedefaultdict(defaultdict):
  """Due to Kent S Johnson."""
  def __init__(self, *args, **kwargs):
    super(recursivedefaultdict, self).__init__(type(self), *args, **kwargs)
  
  def __getattr__(self, name):
    return self[name]
  
  def __setattr__(self, name, value):
    self[name] = value
  
  def __delattr__(self, name):
    del self[name]
