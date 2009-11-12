import sys
import yaml

from google.appengine.ext.webapp import WSGIApplication
from google.appengine.ext.webapp.util import run_wsgi_app

from util.handler import Handler

def routes():
  return yaml.load(file('routes.yaml'))

def module(name):
  __import__(name)
  return sys.modules[name]

def handler(**kwargs):
  return type(str(kwargs), (Handler,), kwargs)

def application():
  return WSGIApplication([
    (path, handler(page=module(handler_module)))
    for (path, handler_module) in routes()
  ], debug=True)

def main():
  run()

def run():
  run_wsgi_app(application())

if __name__ == "__main__":
  main()
