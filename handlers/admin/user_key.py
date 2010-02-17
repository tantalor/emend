from emend import Edit, User

def get(handler, response):
  if not handler.is_admin():
    return handler.not_found(status=403)
  for user in User.all():
    key_name = User.key_name_from_email(user.user.email())
    if not user.key().name() == key_name:
      copy = User(key_name=key_name, user=user.user)
      copy.put()
      # fix edits
      for edit in Edit.all().filter('author =', user):
        edit.author = copy
        edit.put()
      user.delete()
