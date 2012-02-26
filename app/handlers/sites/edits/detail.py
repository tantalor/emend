from emend import Edit

def get(handler, response):
  edit = handler.get_edit(required=True)
  
  # next
  next = Edit.all().\
    ancestor(edit.site).\
    filter('index >', edit.index).\
    filter('status =', 'open').\
    order('index').\
    get()
  if next:
    response.next.edit = next
    response.next.url = handler.urlize(next.permalink())
  
  # prev  
  prev = Edit.all().\
    ancestor(edit.site).\
    filter('index <', edit.index).\
    filter('status =', 'open').\
    order('-index').\
    get()
  if prev:
    response.previous.edit = prev
    response.previous.url = handler.urlize(prev.permalink())
