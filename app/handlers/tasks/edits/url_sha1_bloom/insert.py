from emend.model.edit import get_url_sha1_bloom

def post(handler, response):
  url_sha1 = handler.request.get('url_sha1');
  bloom = get_url_sha1_bloom()
  if url_sha1 and bloom:
    bloom.add(url_sha1)
    bloom.put()
    response.status = "ok"
  else:
    return handler.not_found()
