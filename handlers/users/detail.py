from emend import Edit

PAGE_SIZE=5

def get(handler, response):
  user = handler.get_user(required=True)
  user.gravatar72 = user.gravatar(size=72)
  # get some open edits
  open_edits = Edit.all().\
    filter('author =', user).\
    filter('status =', 'open').\
    order('-created').\
    fetch(PAGE_SIZE+1)
  response.open = open_edits[:PAGE_SIZE]
  if len(open_edits) == PAGE_SIZE+1:
    response.has_next_open = 1
    response.next_open_from = open_edits[PAGE_SIZE].key()
  # get some closed edits
  closed_edits = Edit.all().\
    filter('author =', user).\
    filter('status =', 'closed').\
    order('-created').\
    fetch(PAGE_SIZE+1)
  response.closed = closed_edits[:PAGE_SIZE]
  if len(closed_edits) == PAGE_SIZE+1:
    response.has_next_closed = 1
    response.next_closed_from = closed_edits[PAGE_SIZE].key()
