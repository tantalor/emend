from google.appengine.api import memcache

def get(handler, response):
  if not handler.is_admin():
    return handler.not_found(status=403)
  key = handler.request.get('key')
  response.old = memcache.get(key)
  response.new = memcache.delete(key)
