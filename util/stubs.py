from google.appengine.api import apiproxy_stub_map, urlfetch_stub
from google.appengine.api.memcache import memcache_stub

def urlfetch():
  apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap() 
  apiproxy_stub_map.apiproxy.RegisterStub('urlfetch', 
    urlfetch_stub.URLFetchServiceStub())
  
def memcache():
  apiproxy_stub_map.apiproxy.RegisterStub('memcache', 
    memcache_stub.MemcacheServiceStub())

def all():
  try:
    urlfetch()
    memcache()
    return True
  except:
    pass

def test():
  if all():
    print 'ok'
  else:
    print 'failed'

if __name__ == '__main__':
  test()