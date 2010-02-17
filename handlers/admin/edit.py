from emend import Edit

import logging

def get(handler, response):
  if not handler.is_admin():
    return handler.not_found(status=403)
  for edit in Edit.all():
    if not edit.tested:
      edit.tested = None
      edit.put()
