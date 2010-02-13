from model import Edit

PAGE_SIZE = 5

def get(handler, response):
  site = handler.get_site(create_if_missing=True)
  if not site.is_saved():
    return
  # get some open edits
  open_edits = Edit.all().\
    ancestor(site).\
    filter('status =', 'open').\
    order('-index').\
    fetch(PAGE_SIZE+1)
  response.open = open_edits[:PAGE_SIZE]
  if len(open_edits) == PAGE_SIZE+1:
    response.has_next_open = 1
    response.next_open_from = open_edits[PAGE_SIZE].index
  # get some closed edits
  closed_edits = Edit.all().\
    ancestor(site).\
    filter('status =', 'closed').\
    order('-index').\
    fetch(PAGE_SIZE+1)
  response.closed = closed_edits[:PAGE_SIZE]
  if len(closed_edits) == PAGE_SIZE+1:
    response.has_next_closed = 1
    response.next_closed_from = closed_edits[PAGE_SIZE].index
