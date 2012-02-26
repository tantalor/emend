from emend import Edit

PAGE_SIZE=5

def get(handler, response):
  user = handler.get_user(required=True)
  # get some open edits
  open_edits = Edit.all().\
    filter('author =', user).\
    filter('status =', 'open').\
    order('-created').\
    fetch(PAGE_SIZE+1)
  response.open = open_edits[:PAGE_SIZE]
  if len(open_edits) == PAGE_SIZE+1:
    response.next.open.url = handler.urlize("%s/open" % user.permalink())+"?from=%s" % open_edits[PAGE_SIZE].key()
  # get some closed edits
  closed_edits = Edit.all().\
    filter('author =', user).\
    filter('status =', 'closed').\
    order('-created').\
    fetch(PAGE_SIZE+1)
  response.closed = closed_edits[:PAGE_SIZE]
  if len(closed_edits) == PAGE_SIZE+1:
    response.next.closed.url = handler.urlize("%s/open" % user.permalink())+"?from=%s" % closed_edits[PAGE_SIZE].key()
