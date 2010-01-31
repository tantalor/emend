import yaml
import os

from env import branch

from google.appengine.api import memcache


def config(filename='local.yaml', cachekey='local_config'):
  config = memcache.get(cachekey)
  if config:
    return config
  if os.path.exists(filename):
    config = yaml.load(file(filename).read())
    # branch each value by environment
    config = dict([(key, branch(value)) for key, value in config.iteritems()])
    memcache.set(cachekey, config)
    return config
  return dict()

def config_get(key):
  return config()[key]

def test():
  import stubs
  stubs.memcache()
  # canonical test
  c = config()
  if c:
    print 'ok'
  else:
    print 'failed'

if __name__ == '__main__':
  test()
