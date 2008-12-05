def get(handler, response):
  edit = handler.get_edit()
  if not edit:
    return handler.redirect('/sites')
