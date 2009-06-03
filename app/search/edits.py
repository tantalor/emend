from model.edit import Edit

PAGE_SIZE = 10

def get(handler, response):
  query = handler.request.get('q')
  response.query = query
  # get some edits
  from_key = handler.request.get('from')
  if from_key:
    from_edit = Edit.get(from_key)
  else:
    from_edit = None
  if from_edit:
    edits = Edit.all().\
      search(query).\
      order('-created').\
      filter('created <=', from_edit.created).\
      fetch(PAGE_SIZE+1)
  else:
    edits = Edit.all().\
      search(query).\
      order('-created').\
      fetch(PAGE_SIZE+1)
  # for output
  response.edits = edits[:PAGE_SIZE]
  
  if len(edits) > PAGE_SIZE:
    response.has_next = 1
    response.next_from = edits[PAGE_SIZE].key()
