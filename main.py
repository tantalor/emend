import yaml

from google.appengine.ext.webapp import WSGIApplication, template
from google.appengine.ext.webapp.util import run_wsgi_app

from emend import RequestHandler

def routes():
  return yaml.load(file('routes.yaml'))

def handlers():
  return [(path, handler) for (path, handler) in [
    (path, RequestHandler.with_page(page))
    for (path, page) in routes()
  ] if handler]

def application():
  return WSGIApplication(handlers(), debug=True)

def main():
  template.register_template_library('emend.template')
  run_wsgi_app(application())

if __name__ == "__main__":
  main()
