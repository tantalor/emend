from model.site import Site
from model.edit import Edit

def get(handler, response):
  if not handler.is_admin():
    return handler.redirect('/')
  # unclose unclosed edits
  for edit in Edit.all():
    if not edit.closed:
      edit.closed = False
      edit.put()
  for site in Site.all():
    open = Edit.all().ancestor(site).filter('closed =', False)
    closed = Edit.all().ancestor(site).filter('closed =', True)
    site.open = open.count()
    site.closed = closed.count()
    site.put()
