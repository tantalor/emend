def post(handler, response):
  if not handler.current_user():
    return handler.redirect('/')
  edit = handler.get_edit(required=True)
  if edit.can_edit():
    edit.open()
  # redirect
  handler.redirect(handler.request.get('continue') or edit.permalink())
