import re
from emend import Edit


PAGE_SIZE = 10


def get(handler, response):
  query = handler.request.get('q')
  status = handler.request.get('status')
  response.query = query
  response.status = status
  search_args = dict(status=status)
  # default heading
  if status == "open":
    response.default_heading = "Open edits"
  elif status == "closed":
    response.default_heading = "Closed edits"
  else:
    response.default_heading = "All edits"
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
  if re.match('^http://', query):
    edits = search_by_url(query, **search_args)
  else:
    edits = search_by_query(query, **search_args)
  # check for next/prev
  if to_key:
    if len(edits) > PAGE_SIZE + 1:
      response.to_key = edits[1].key()
      edits = edits[1:]
  if len(edits) > PAGE_SIZE:
    response.from_key = edits[PAGE_SIZE].key()
  # for output
  response.edits = edits[:PAGE_SIZE]


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
