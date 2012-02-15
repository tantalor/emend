from emend import User
from google.appengine.datastore import datastore_query


PAGE_SIZE = 1

def get(handler, response):
  # parameters
  from_cursor = handler.request.get('from')
  to_cursor = handler.request.get('to')
  
  # setup query
  if to_cursor:
    query = backward_query().with_cursor(to_cursor)
  elif from_cursor:
    query = forward_query().with_cursor(from_cursor)
  else:
    query = forward_query()
  
  # fetch results
  response.users = query.fetch(PAGE_SIZE)
  if to_cursor:
    response.users.reverse()
  
  # pagination
  if to_cursor:
    response.next.cursor = reverse(to_cursor)
    response.next.url = "%s?from=%s" % (handler.base_path(), response.next.cursor)
    
    response.previous.cursor = query.cursor()
    response.previous.url = "%s?to=%s" % (handler.base_path(), response.previous.cursor)
  else:
    if from_cursor:
      response.previous.cursor = reverse(from_cursor)
      response.previous.url = "%s?to=%s" % (handler.base_path(), response.previous.cursor)
    
    if len(response.users) >= PAGE_SIZE:
      response.next.cursor = query.cursor()
      response.next.url = "%s?from=%s" % (handler.base_path(), response.next.cursor)

def forward_query():
  return User.all().order('-open').order('-closed').order('-__key__')

def backward_query():
  return User.all().order('open').order('closed').order('__key__')
  
def reverse(cursor):
  return datastore_query.Cursor.from_websafe_string(cursor).reversed().to_websafe_string()
