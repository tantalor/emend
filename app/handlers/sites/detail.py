from emend import Edit

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
    response.next.open.url = handler.urlize("%s/open" % site.permalink())+"?from=%s" % open_edits[PAGE_SIZE].index
  # get some closed edits
  closed_edits = Edit.all().\
    ancestor(site).\
    filter('status =', 'closed').\
    order('-index').\
    fetch(PAGE_SIZE+1)
  response.closed = closed_edits[:PAGE_SIZE]
  if len(closed_edits) == PAGE_SIZE+1:
    response.next.closed.url = handler.urlize("%s/closed" % site.permalink())+"?from=%s" % closed_edits[PAGE_SIZE].index
