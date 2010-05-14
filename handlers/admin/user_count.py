from emend import Edit, User

def get(handler, response):
  if not handler.is_admin():
    return handler.not_found(status=403)
  # reset counts
  for user in User.all():
    user.open = Edit.all().\
      filter('author =', user).\
      filter('status =', 'open').\
      count()
    user.closed = Edit.all().\
      filter('author =', user).\
      filter('status =', 'closed').\
      count()
    user.put()
