from model.edit import Edit

from google.appengine.api.urlfetch_errors import DownloadError

FETCH_COUNT = 10

def get(handler, response):
  # get edits in need of testing
  edits = Edit.all()\
    .filter('status =', 'open')\
    .order('tested')\
    .fetch(FETCH_COUNT)
  # test them
  response.edits = []
  for edit in edits:
    try:
      status = edit.test()
      response.edits.append(dict(edit=edit, status=status))
    except DownloadError:
      response.edits.append(dict(edit=edit, status="error"))
