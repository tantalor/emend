from google.appengine.ext.webapp import WSGIApplication
from google.appengine.ext.webapp.util import run_wsgi_app

from megaera import MegaeraRequestHandler

def application():
  return WSGIApplication([
    ('/', MegaeraRequestHandler.with_page('handlers.default'))
  ], debug=True)

def main():
  run_wsgi_app(application())

if __name__ == "__main__":
  main()
