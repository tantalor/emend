from emend import Edit

def get(handler, response):
  edit = handler.get_edit(required=True)
  
  edit.author.gravatar72 = edit.author.gravatar(size=72)
  
  # next
  next = Edit.all().\
    ancestor(edit.site).\
    filter('index >', edit.index).\
    filter('status =', 'open').\
    order('index').\
    fetch(1)
  if next:
    response.next = next[0]
  
  # prev  
  prev = Edit.all().\
    ancestor(edit.site).\
    filter('index <', edit.index).\
    filter('status =', 'open').\
    order('-index').\
    fetch(1)
  if prev:
    response.prev = prev[0]
  
