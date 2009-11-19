from urlparse import urlparse
from model.site import Site

def get(handler, response):
  edit = handler.get_edit(required=True)
  if not edit.can_edit():
    return handler.redirect(edit.permalink())
  # don't override user input
  if not handler.has_errors():
    response.url = edit.url
    response.original = edit.original
    response.proposal = edit.proposal

def post(handler, response):
  edit = handler.get_edit(required=True)
  if not edit.can_edit():
    return handler.redirect(edit.permalink())
  # post params
  url = handler.request.get('url').strip()
  original = handler.request.get('original').strip()
  proposal = handler.request.get('proposal').strip()
  # copy params for error case
  response.url = url
  response.original = original
  response.proposal = proposal
  # parse url
  domain = urlparse(url).netloc
  if not domain:
    # fix URL by prefixing with default scheme
    url = "http://%s" % url
    domain = urlparse(url).netloc
  # error cases
  if not domain:
    handler.form_error(url="Invalid URL")
  if not original:
    handler.form_error(original="Original required")
  if not proposal:
    handler.form_error(proposal="Proposal required")
  # check that the site didn't change
  key_name = Site.key_name_from_domain(domain)
  if edit.site.key().name() != key_name:
    handler.form_error(url="Cannot change domain")
  # exit if errors occured
  if handler.has_errors():
    return
  # update the edit
  edit.url = url
  edit.original = original
  edit.proposal = proposal
  edit.put()
  # redirect
  handler.redirect(edit.permalink())
