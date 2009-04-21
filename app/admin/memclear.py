from google.appengine.api import memcache

def get(handler, response):
  key = handler.request.get('key')
  response.old = memcache.get(key)
  response.new = memcache.delete(key)
