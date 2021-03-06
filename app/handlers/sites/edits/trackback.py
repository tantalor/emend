import logging

from tblib import TrackBack
from emend import site_name

from google.appengine.api import urlfetch


def post(handler, response):
  edit = handler.get_edit(required=True)
  try:
    title = 'Emend > Sites > %s > %s' % (edit.site.domain, edit.original)
    excerpt = edit.as_tweet().encode('utf8')
    url = edit.permalink()
    tb = TrackBack(title=title, excerpt=excerpt, url=url, blog_name=site_name())
    tb.autodiscover(edit.url)
    if tb.ping() == 1:
      response.error = "Didn't find a trackback URI."
    else:
      response.success = 1
  except urlfetch.DownloadError, e:
    logging.error("trackback failed: %s", e);
    response.error = e.message
  # redirect
  handler.redirect(handler.request.get('continue') or edit.permalink())
