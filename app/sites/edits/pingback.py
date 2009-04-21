from util.pingback import pingback
import xmlrpclib
from google.appengine.api import urlfetch

from util.warn import warn

def post(handler, response):
  edit = handler.get_edit(required=True)
  try:
    sourceURI = edit.permalink()
    targetURI = edit.url
    if pingback(sourceURI=sourceURI, targetURI=targetURI):
      response.success = 1
    else:
      response.error = "Didn't find a pingback URI."
  except xmlrpclib.Fault, e:
    response.error = e.faultString
    warn("pingback XMLRPC failed", e);
  except urlfetch.DownloadError, e:
    response.error = e.message
    warn("pingback failed", e);
  # redirect
  handler.redirect(handler.request.get('continue') or edit.permalink())