from emend import Edit
from emend.model.edit import get_url_sha1_bloom

def get(handler, response):
  if not handler.is_admin():
    return handler.not_found(status=403)
  query = Edit.all()
  bloom = get_url_sha1_bloom()
  bloom.reset()
  count = 0
  while 1:
    edits = query.fetch(1000)
    if not edits:
      break
    count += len(edits)
    for edit in edits:
      bloom.add(edit.url_sha1)
    query = Edit.all().with_cursor(query.cursor())
  bloom.put()
  response.count = count
