import re
import os
import cgi
import urllib
from emend import Edit


PAGE_SIZE = 10


def get(handler, response):
  q = handler.request.get('q')
  status = handler.request.get('status')
  url_sha1 = handler.request.get('url_sha1')
  cursor = handler.request.get('cursor')
  
  if url_sha1:
    response.heading = "sha1(url) = %s..." % (url_sha1[:6])
  if status == "open":
    response.heading = "Open edits"
  elif status == "closed":
    response.heading = "Closed edits"
  else:
    response.heading = "All edits"
  
  query = Edit.all()
  
  # filter
  if url_sha1:
    query = query.filter('url_sha1 =', url_sha1)
  if status:
    query = query.filter('status =', status)
  if q:
    query = query.search(q)
  
  # sort
  query = query.order('-created')
  
  # cursor
  if cursor:
    query = query.with_cursor(cursor)
  
  edits = query.fetch(PAGE_SIZE)
  cursor = query.cursor()
  
  if len(edits) == PAGE_SIZE:
    response.next.cursor = cursor
    # build next url
    query_dict = cgi.parse_qs(os.environ.get('QUERY_STRING'), keep_blank_values=True)
    query_dict['cursor'] = cursor
    response.next.cursor = cursor
    response.next.url = 'http://%s/search/edits?%s' % (handler.host(), urllib.urlencode(query_dict, doseq=True))
  
  # for output
  response.edits = edits[:PAGE_SIZE]
