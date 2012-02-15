from datetime import datetime

from emend import Edit

PAGE_SIZE=10

import logging

def get(handler, response):
  user = handler.get_user(required=True)
  # get some edits
  from_key = handler.request.get('from')
  if from_key:
    from_edit = Edit.get(from_key)
  else:
    from_edit = None
  if from_edit:
    edits = Edit.all().\
      filter('author =', user).\
      filter('status =', 'closed').\
      filter('created <=', from_edit.created).\
      order('-created').\
      fetch(PAGE_SIZE+1)
  else:
    edits = Edit.all().\
      filter('author =', user).\
      filter('status =', 'closed').\
      order('-created').\
      fetch(PAGE_SIZE+1)
  # for output
  response.edits = edits[:PAGE_SIZE]
  
  if len(edits) > PAGE_SIZE:
    response.next.url = "%s?from=%s" % (handler.base_path(), edits[PAGE_SIZE].key())
