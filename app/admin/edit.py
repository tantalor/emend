from model.edit import Edit

def get(handler, response):
  if not handler.is_admin():
    return handler.not_found(status=403)
  for edit in Edit.all():
    edit.created = edit.datetime
    edit.save()
