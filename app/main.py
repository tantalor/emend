import yaml

from google.appengine.ext.webapp import WSGIApplication
from google.appengine.ext.webapp.util import run_wsgi_app

from emend import RequestHandler
from emend.diff import diff, diff_src, diff_dst
from rfc3339 import datetimetostr as rfc3339
from urllib import quote
from megaera import get_jinja2_env

jinja2_env = get_jinja2_env()
jinja2_env.filters['quote'] = lambda s: quote(s.encode('utf8'))
jinja2_env.globals['diff'] = diff
jinja2_env.globals['diff_src'] = diff_src
jinja2_env.globals['diff_dst'] = diff_dst
jinja2_env.filters['rfc3339'] = rfc3339

def routes():
  return yaml.load(file('routes.yaml'))

def handlers():
  return [(path, handler) for (path, handler) in [
    RequestHandler.path_with_page(path, page)
    for (path, page) in routes()
  ] if handler]

application = WSGIApplication(handlers(), debug=True)
