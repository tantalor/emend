from emend import Edit, User

def get(handler, response):
  if not handler.is_admin():
    return handler.not_found(status=403)
  # reset counts
  for user in User.all():
    user.open = 0
    user.closed = 0
    user.put()
  # count up open and closed
  for edit in Edit.all():
    if edit.closed:
      edit.author.closed += 1
    else:
      edit.author.open += 1
    edit.author.put()
