import yaml

from google.appengine.ext.webapp import WSGIApplication, template
from google.appengine.ext.webapp.util import run_wsgi_app

from emend import EmendRequestHandler

def routes():
  return yaml.load(file('routes.yaml'))

def application():
  return WSGIApplication([
    (path, EmendRequestHandler.with_page(page))
    for (path, page) in routes()
  ], debug=True)

def main():
  template.register_template_library('emend.template')
  run_wsgi_app(application())

if __name__ == "__main__":
  main()
