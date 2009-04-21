from model.edit import Edit

from util.warn import warn

def get(handler, response):
  edit = handler.get_edit(required=True)
  
  # next
  next = Edit.all().\
    ancestor(edit.site).\
    filter('index >', edit.index).\
    order('index').\
    fetch(1)
  if next:
    response.next = next[0]
  
  # prev  
  prev = Edit.all().\
    ancestor(edit.site).\
    filter('index <', edit.index).\
    order('-index').\
    fetch(1)
  if prev:
    response.prev = prev[0]
  
