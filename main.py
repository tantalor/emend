import yaml

from google.appengine.ext.webapp import WSGIApplication
from google.appengine.ext.webapp.util import run_wsgi_app

from emend import EmendRequestHandler, template

def routes():
  return yaml.load(file('routes.yaml'))

def application():
  return WSGIApplication([
    (path, EmendRequestHandler.with_page(page))
    for (path, page) in routes()
  ], debug=True)

def main():
  template.install()
  run_wsgi_app(application())

if __name__ == "__main__":
  main()
