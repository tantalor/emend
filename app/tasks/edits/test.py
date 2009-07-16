from model.edit import Edit

FETCH_COUNT = 10

def get(handler, response):
  if not handler.is_admin():
    return handler.not_found(status=403)
  # get edits in need of testing
  edits = Edit.all()\
    .filter('status =', 'open')\
    .order('tested')\
    .fetch(FETCH_COUNT)
  # test them
  response.edits = []
  for edit in edits:
    status = edit.test()
    response.edits.append(dict(edit=edit, status=status))
