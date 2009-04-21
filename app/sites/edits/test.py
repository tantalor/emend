from google.appengine.api.urlfetch import fetch

from util.warn import warn

def post(handler, response):
  edit = handler.get_edit(required=True)
  page = fetch(edit.url)
  content = unicode(page.content, 'iso-8859-1')
  if edit.proposal in content:
    edit.close()
    response.status = 'fixed'
  elif edit.original in content:
    response.status = 'unfixed'
  else:
    response.status = 'uncertain'
  