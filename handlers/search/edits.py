import re
from emend import Edit

PAGE_SIZE = 10


def get(handler, response):
  query = handler.request.get('q')
  status = handler.request.get('status')
  response.query = query
  # from edit
  from_key = handler.request.get('from')
  if from_key:
    from_edit = Edit.get(from_key)
  else:
    from_edit = None
  # get some edits
  if re.match('^http://', query):
    edits = search_by_url(query, from_edit=from_edit, status=status)
  else:
    edits = search_by_query(query, from_edit=from_edit, status=status)
  # for output
  response.edits = edits[:PAGE_SIZE]
  # check for more results  
  if len(edits) > PAGE_SIZE:
    response.has_next = 1
    response.next_from = edits[PAGE_SIZE].key()


def search(query, from_edit=None, status=None):
  if status:
    query = query.filter('status =', status)
  if from_edit:
    query = query.order('-created').\
      filter('created <=', from_edit.created)
  else:
    query = query.order('-created')
  return query.fetch(PAGE_SIZE+1)


def search_by_query(query, **kwargs):
  return search(Edit.all().search(query), **kwargs)


def search_by_url(url, **kwargs):
  return search(Edit.all().filter('url =', url), **kwargs)
