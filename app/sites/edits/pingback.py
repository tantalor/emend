import logging
import xmlrpclib

from util.pingback import pingback

from google.appengine.api import urlfetch

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
    logging.error("pingback XMLRPC failed: %s", e);
  except xmlrpclib.ProtocolError, e:
    response.error = e.errmsg
    logging.error("pingback XMLRPC failed: %s", e);
  except urlfetch.DownloadError, e:
    response.error = e.message
    logging.error("pingback failed: %s", e);
  # redirect
  handler.redirect(handler.request.get('continue') or edit.permalink())
