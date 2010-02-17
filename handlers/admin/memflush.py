from google.appengine.api import memcache

def get(handler, response):
  if not handler.is_admin():
    return handler.not_found(status=403)
  response.status = memcache.flush_all()
