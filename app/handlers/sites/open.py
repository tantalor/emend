from emend import Edit

PAGE_SIZE = 10

def get(handler, response):
  site = handler.get_site(required=True)
  # get some edits
  from_index = handler.request.get('from')
  if from_index:
    from_index = int(from_index)
    edits = Edit.all().\
      ancestor(site).\
      filter('index <=', from_index).\
      filter('status =', 'open').\
      order('-index').\
      fetch(PAGE_SIZE+1)
    # get top edit for comparison
    top_edit = Edit.all().\
      ancestor(site).\
      order('-index').\
      fetch(1)
    if top_edit[0].index != edits[0].index:
      response.previous.index = from_index + PAGE_SIZE
      response.previous.url = "%s?from=%s" % (handler.base_path(), response.previous.index)
  else:
    edits = Edit.all().\
      ancestor(site).\
      filter('status =', 'open').\
      order('-index').\
      fetch(PAGE_SIZE+1)
  response.edits = edits[:PAGE_SIZE]
  if len(edits) > PAGE_SIZE:
    response.next.index = edits[-1].index
    response.next.url = "%s?from=%s" % (handler.base_path(), response.next.index)
