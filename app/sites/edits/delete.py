def post(handler, response):
  if not handler.user():
    return handler.redirect('/')
  # get site
  edit = handler.get_edit()
  if edit and edit.can_edit():
    edit.delete()
  # redirect
  redirect = handler.request.get('continue')
  handler.redirect(redirect or '/')
