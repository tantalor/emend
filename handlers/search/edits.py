import re
from emend import Edit

PAGE_SIZE = 10


def get(handler, response):
  query = handler.request.get('q')
  response.query = query
  # from edit
  from_key = handler.request.get('from')
  if from_key:
    from_edit = Edit.get(from_key)
  else:
    from_edit = None
  # get some edits
  if re.match('^http://', query):
    edits = search_by_url(query, from_edit)
  else:
    edits = []#search_by_query(query, from_edit)
  # for output
  response.edits = edits[:PAGE_SIZE]
  # check for more results  
  if len(edits) > PAGE_SIZE:
    response.has_next = 1
    response.next_from = edits[PAGE_SIZE].key()


def search_by_query(query, from_edit):
  if from_edit:
    return Edit.all().\
      search(query).\
      order('-created').\
      filter('created <=', from_edit.created).\
      fetch(PAGE_SIZE+1)
  else:
    return Edit.all().\
      search(query).\
      order('-created').\
      fetch(PAGE_SIZE+1)


def search_by_url(url, from_edit):
  if from_edit:
    return Edit.all().\
      filter('url =', url).\
      filter('created <=', from_edit.created).\
      order('-created').\
      fetch(PAGE_SIZE+1)
  else:
    return Edit.all().\
      filter('url =', url).\
      order('-created').\
      fetch(PAGE_SIZE+1)
