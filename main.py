from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from util import EmendHandler, handler

import app.default
import app.sites.default
import app.sites.detail
import app.sites.edits.detail
import app.sites.edits.delete

def main():
  run_wsgi_app(webapp.WSGIApplication(
    [
      (r'/?',
        EmendHandler.factory(page=app.default)),
      (r'/sites/?',
        EmendHandler.factory(page=app.sites.default)),
      (r'/sites/([^/]+)/?',
        EmendHandler.factory(page=app.sites.detail)),
      (r'/sites/([^/]+)/edits/([^/]+)',
        EmendHandler.factory(page=app.sites.edits.detail)),
      (r'/sites/([^/]+)/edits/([^/]+)/delete',
        EmendHandler.factory(page=app.sites.edits.delete)),
    ],
    debug=True))

if __name__ == "__main__":
  main()
