from model.edit import Edit

def get(handler, response):
  user = handler.get_user(required=True)
  # get some open edits
  response.open = Edit.all().\
    filter('author =', user).\
    filter('closed = ', False).\
    order('-created').\
    fetch(10)
  # get some closed edits
  response.closed = Edit.all().\
    filter('author =', user).\
    filter('closed = ', True).\
    order('-created').\
    fetch(10)
