import re
from emend import Edit


PAGE_SIZE = 10
URL_SHA1_QUERY = re.compile('^url_sha1:(\w+)$')


def get(handler, response):
  query = handler.request.get('q')
  status = handler.request.get('status')
  url_sha1 = handler.request.get('url_sha1')
  response.query = query
  response.status = status
  search_args = dict(status=status)
  # default heading
  if status == "open":
    heading = "Open edits"
  elif status == "closed":
    heading = "Closed edits"
  else:
    heading = "All edits"
  # from edit
  from_key = handler.request.get('from')
  if from_key:
    response.to_key = from_key
    search_args['from_edit'] = Edit.get(from_key)
  # to edit
  to_key = handler.request.get('to')
  if to_key:
    search_args['to_edit'] = Edit.get(to_key)
  # search edits
  if not url_sha1:
    url_sha1_match = URL_SHA1_QUERY.match(query)
    if url_sha1_match:
      (url_sha1,) = url_sha1_match.groups()
  if url_sha1:
    edits = search_by_url_sha1(url_sha1, **search_args)
    heading = "sha1(url) = %s..." % (url_sha1[:6])
  else:
    edits = search_by_query(query, **search_args)
    if query:
      heading = query
  # check for next/prev
  if to_key:
    if len(edits) > PAGE_SIZE + 1:
      response.to_key = edits[1].key()
      edits = edits[1:]
  if len(edits) > PAGE_SIZE:
    response.from_key = edits[PAGE_SIZE].key()
  elif to_key:
    response.from_key = edits[-1].key()
    edits = edits[:-1]
  # for output
  response.edits = edits[:PAGE_SIZE]
  response.heading = heading


def search(query, from_edit=None, to_edit=None, status=None):
  # filter
  if status:
    query = query.filter('status =', status)
  # order
  if to_edit:
    query = query.\
      order('created').\
      filter('created >=', to_edit.created)
    edits = query.fetch(PAGE_SIZE+2)
    # reverse so we get descending order
    return edits[::-1]
  if from_edit:
    query = query.\
      order('-created').\
      filter('created <=', from_edit.created)
  else:
    query = query.order('-created')
  return query.fetch(PAGE_SIZE+1)


def search_by_query(query, **kwargs):
  return search(Edit.all().search(query), **kwargs)


def search_by_url(url, **kwargs):
  return search(Edit.all().filter('url =', url), **kwargs)


def search_by_url_sha1(url_sha1, **kwargs):
  return search(Edit.all().filter('url_sha1 =', url_sha1), **kwargs)
