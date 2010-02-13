from model import Site, Edit

def get(handler, response):
  """Enforce key_name_from_domain compatibility 
  on all sites and edits."""
  if not handler.is_admin():
    return handler.not_found(status=403)
  for site in Site.all():
    key_name = Site.key_name_from_domain(site.domain)
    if not site.key().name() == key_name:
      copy = Site(
        key_name = key_name,
        domain = site.domain
      )
      copy.put()
      for edit in Edit.all().ancestor(site):
        Edit(
          index = edit.index,
          author = edit.author,
          original = edit.original,
          proposal = edit.proposal,
          url = edit.url,
          parent = copy,
          datetime = edit.datetime
        ).put()
        edit.delete()
      site.delete()
