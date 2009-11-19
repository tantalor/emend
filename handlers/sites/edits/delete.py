import handlers.default

def post(handler, response):
  edit = handler.get_edit(required=True)
  if not edit.can_edit():
    return handler.redirect(edit.permalink())
  # update site open/closed count
  if edit.is_open:
    edit.site.open -= 1
    edit.site.put()
  elif edit.is_closed:
    edit.site.closed -= 1
    edit.site.put()
  # remove it
  edit.delete()
  # clear homepage cache
  handler.invalidate(page=app.default)
  # redirect
  handler.redirect(edit.site.permalink())
