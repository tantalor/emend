from emend import Site, Edit

def get(handler, response):
  if not handler.is_admin():
    return handler.not_found(status=403)
  # unclose unclosed edits
  for edit in Edit.all():
    if not edit.closed:
      edit.closed = False
      edit.put()
  for site in Site.all():
    open = Edit.all().ancestor(site).filter('status =', 'open')
    closed = Edit.all().ancestor(site).filter('status =', 'closed')
    site.open = open.count()
    site.closed = closed.count()
    site.put()
