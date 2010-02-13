from google.appengine.api import memcache

def get(handler, response):
  if not handler.is_admin():
    return handler.not_found(status=403)
  key = handler.request.get('key')
  namespace = handler.request.get('namespace') or None
  response.old = memcache.get(key=key, namespace=namespace)
  response.new = memcache.delete(key=key, namespace=namespace)
