from model.edit import Edit

def get(handler, response):
  if not handler.is_admin():
    return handler.redirect('/')
  for edit in Edit.all():
    edit.proposal = edit.proposal.strip()
    edit.original = edit.original.strip()
    edit.save()
