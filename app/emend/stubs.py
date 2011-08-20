from google.appengine.api import apiproxy_stub_map, urlfetch_stub
from google.appengine.api.memcache import memcache_stub

from megaera import env

def urlfetch():
  if env.server_software():
    return
  apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap() 
  apiproxy_stub_map.apiproxy.RegisterStub('urlfetch', 
    urlfetch_stub.URLFetchServiceStub())

def memcache():
  if env.server_software():
    return
  apiproxy_stub_map.apiproxy.RegisterStub('memcache', 
    memcache_stub.MemcacheServiceStub())

def all():
  if env.server_software():
    return
  from google.appengine.tools import dev_appserver_main, dev_appserver
  dev_appserver.SetupStubs('emend', **dev_appserver_main.DEFAULT_ARGS)
