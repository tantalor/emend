import handlers.default

def post(handler, response):
  edit = handler.get_edit(required=True)
  if not edit.can_edit():
    return handler.redirect(edit.permalink())
  # remove it
  edit.delete()
  # clear homepage cache
  handler.invalidate(page=handlers.default)
  # redirect
  handler.redirect(edit.site.permalink())
