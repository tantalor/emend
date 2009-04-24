from model.edit import Edit

def get(handler, response):
  if not handler.is_admin():
    return handler.not_found(status=403)
  for edit in Edit.all():
    if hasattr(edit, 'closed'):
      if edit.closed:
        edit.status = 'closed'
      else:
        edit.status = 'open'
      delattr(edit, 'closed')
    edit.put()
