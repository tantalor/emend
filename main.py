from google.appengine.ext.webapp import WSGIApplication
from google.appengine.ext.webapp.util import run_wsgi_app

from util.handler import Handler

import app.iphone
import app.about
import app.admin.edit
import app.admin.memclear
import app.admin.site_count
import app.admin.site_key
import app.admin.user_count
import app.admin.user_key
import app.default
import app.search.default
import app.search.edits
import app.sites.default
import app.sites.detail
import app.sites.edits.close
import app.sites.edits.detail
import app.sites.edits.open
import app.sites.edits.pingback
import app.sites.edits.test
import app.sites.edits.trackback
import app.sites.edits.update
import app.users.default
import app.users.detail
import app.users.closed
import app.users.open
import app.users.nickname
import app.not_found

def application():
  return WSGIApplication([
    (r'/iphone',
      Handler.factory(page=app.iphone)),
    (r'/about',
      Handler.factory(page=app.about)),
    (r'/admin/edit',
      Handler.factory(page=app.admin.edit)),
    (r'/admin/memclear',
      Handler.factory(page=app.admin.memclear)),
    (r'/admin/site_count',
      Handler.factory(page=app.admin.site_count)),
    (r'/admin/site_key',
      Handler.factory(page=app.admin.site_key)),
    (r'/admin/user_count',
      Handler.factory(page=app.admin.user_count)),
    (r'/admin/user_key',
      Handler.factory(page=app.admin.user_key)),
    (r'/search/edits',
      Handler.factory(page=app.search.edits)),
    (r'/search',
      Handler.factory(page=app.search.default)),
    (r'/sites',
      Handler.factory(page=app.sites.default)),
    (r'/sites/([^/]+)',
      Handler.factory(page=app.sites.detail)),
    (r'/sites/([^/]+)/edits/([^/]+)/close',
      Handler.factory(page=app.sites.edits.close)),
    (r'/sites/([^/]+)/edits/([^/]+)',
      Handler.factory(page=app.sites.edits.detail)),
    (r'/sites/([^/]+)/edits/([^/]+)/open',
      Handler.factory(page=app.sites.edits.open)),
    (r'/sites/([^/]+)/edits/([^/]+)/pingback',
      Handler.factory(page=app.sites.edits.pingback)),
    (r'/sites/([^/]+)/edits/([^/]+)/test',
      Handler.factory(page=app.sites.edits.test)),
    (r'/sites/([^/]+)/edits/([^/]+)/trackback',
      Handler.factory(page=app.sites.edits.trackback)),
    (r'/sites/([^/]+)/edits/([^/]+)/update',
      Handler.factory(page=app.sites.edits.update)),
    (r'/users',
      Handler.factory(page=app.users.default)),
    (r'/users/([^/]+)',
      Handler.factory(page=app.users.detail)),
    (r'/users/([^/]+)/closed',
      Handler.factory(page=app.users.closed)),
    (r'/users/([^/]+)/open',
      Handler.factory(page=app.users.open)),
    (r'/users/([^/]+)/nickname',
      Handler.factory(page=app.users.nickname)),
    (r'/*',
      Handler.factory(page=app.default)),
    (r'/.*',
      Handler.factory(page=app.not_found)),
  ], debug=True)

def main():
  run()

def run():
  run_wsgi_app(application())

if __name__ == "__main__":
  main()
