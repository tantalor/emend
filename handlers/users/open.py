from datetime import datetime

from model import Edit

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
      filter('status =', 'open').\
      filter('created <=', from_edit.created).\
      order('-created').\
      fetch(PAGE_SIZE+1)
  else:
    edits = Edit.all().\
      filter('author =', user).\
      filter('status =', 'open').\
      order('-created').\
      fetch(PAGE_SIZE+1)
  # for output
  response.edits = edits[:PAGE_SIZE]
  
  if len(edits) > PAGE_SIZE:
    response.has_next = 1
    response.next_from = edits[PAGE_SIZE].key()
