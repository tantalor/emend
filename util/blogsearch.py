from google.appengine.api import urlfetch, apiproxy_stub_map, urlfetch_stub

from urllib import urlencode

def test():
  # setup urlfetch stub
  apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap() 
  apiproxy_stub_map.apiproxy.RegisterStub('urlfetch', 
    urlfetch_stub.URLFetchServiceStub())
  # canonical test 
  response = ping(
    name='Official Google Blog',
    url='http://googleblog.blogspot.com',
    changesURL='http://googleblog.blogspot.com/atom.xml')
  if response == 'Thanks for the ping.':
    print 'ok'
  else:
    print 'failed, got "%s"' % response

def ping(name, url, changesURL, ping_url='http://blogsearch.google.com/ping'):
  payload = urlencode(dict(name=name, url=url, changesURL=changesURL))
  response = urlfetch.fetch('%s?%s' % (ping_url, payload))
  if response:
    return response.content

if __name__ == '__main__':
  test();
