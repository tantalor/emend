import re
import os
import cgi
import urllib
import logging

from emend import Edit
from emend.model.edit import get_url_sha1_bloom

PAGE_SIZE = 10


def get(handler, response):
  q = handler.request.get('q')
  status = handler.request.get('status')
  url_sha1 = handler.request.get('url_sha1')
  from_key = handler.request.get('from')
  to_key = handler.request.get('to')
  
  from_edit, to_edit = None, None
  
  if from_key:
    from_edit = Edit.get(from_key)
  if to_key:
    to_edit = Edit.get(to_key)
  
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
    # check bloom first
    if not url_sha1 in get_url_sha1_bloom():
      return
    # continue with query
    query = query.filter('url_sha1 =', url_sha1)
  if status:
    query = query.filter('status =', status)
  if q:
    query = query.search(q)
  if from_edit:
    query = query.filter('created <=', from_edit.created)
  if to_edit:
    query = query.filter('created >', to_edit.created)
  
  # sort
  if to_edit:
    query = query.order('created')
  else:
    query = query.order('-created')
  
  # output
  edits = query.fetch(PAGE_SIZE+1)
  response.edits = edits[:PAGE_SIZE]
  if to_edit:
    response.edits.reverse()
  
  if url_sha1 and not edits:
    logging.error('bloom false positive %s', url_sha1)
  
  # pagination
  query_dict = cgi.parse_qs(os.environ.get('QUERY_STRING'), keep_blank_values=True)
  if to_edit: # backward
    next_query_dict = query_dict.copy()
    next_query_dict.pop("to", None)
    next_query_dict["from"] = to_edit.key() # first on next page
    response.next.url = '%s?%s' % (handler.base_path(), urllib.urlencode(next_query_dict, doseq=True))
    
    if len(edits) > PAGE_SIZE:
      previous_query_dict = query_dict.copy()
      previous_query_dict.pop("from", None)
      previous_query_dict["to"] = response.edits[0].key() # first on this page
      response.previous.url = '%s?%s' % (handler.base_path(), urllib.urlencode(previous_query_dict, doseq=True))
      
  else: # forward
    if len(edits) > PAGE_SIZE:
      next_query_dict = query_dict.copy()
      next_query_dict.pop("to", None)
      next_query_dict["from"] = edits[-1].key() # first on next page
      response.next.url = '%s?%s' % (handler.base_path(), urllib.urlencode(next_query_dict, doseq=True))
    
    if response.edits and from_edit:
      previous_query_dict = query_dict.copy()
      previous_query_dict.pop("from", None)
      previous_query_dict["to"] = response.edits[0].key() # first on this page
      response.previous.url = '%s?%s' % (handler.base_path(), urllib.urlencode(previous_query_dict, doseq=True))
