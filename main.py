import yaml

from google.appengine.ext.webapp import WSGIApplication, template
from google.appengine.ext.webapp.util import run_wsgi_app

from util.request_handler import EmendRequestHandler

def routes():
  return yaml.load(file('routes.yaml'))

def application():
  return WSGIApplication([
    (path, EmendRequestHandler.with_page(page))
    for (path, page) in routes()
  ], debug=True)

def run():
  template.register_template_library('template')
  run_wsgi_app(application())

def main():
  run()

if __name__ == "__main__":
  main()
