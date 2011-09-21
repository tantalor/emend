from emend import User


PAGE_SIZE = 10


def get(handler, response):
  from_key = handler.request.get('from')
  to_key = handler.request.get('to')
  
  from_user, to_user = None, None
  
  if from_key:
    from_user = User.get(from_key)
  
  if to_key:
    to_user = User.get(to_key)
    
  # get users
  if to_user:
    users = User.all().\
      filter('open =', to_user.open).\
      filter('closed =', to_user.closed).\
      filter('__key__ <=', to_user.key()).\
      order('-__key__').\
      fetch(PAGE_SIZE+2)
    users.reverse()
    if len(users) < PAGE_SIZE+2:
      pad = User.all().\
        filter('open =', to_user.open).\
        filter('closed >', to_user.closed).\
        order('closed').\
        order('-__key__').\
        fetch(PAGE_SIZE+2-len(users))
      pad.reverse()
      users = pad+users
    if len(users) < PAGE_SIZE+2:
      pad = User.all().\
        filter('open >', to_user.open).\
        order('open').\
        order('closed').\
        order('-__key__').\
        fetch(PAGE_SIZE+2-len(users))
      pad.reverse()
      users = pad+users
    if len(users) > PAGE_SIZE+1:
      response.users = users[1:PAGE_SIZE+1]
    else:
      response.users = users[:PAGE_SIZE]
  elif from_key:
    # get users with same open & closed count, order by key
    users = User.all().\
      filter('open =', from_user.open).\
      filter('closed =', from_user.closed).\
      filter('__key__ >=', from_user.key()).\
      order('__key__').\
      fetch(PAGE_SIZE+1)
    # get more users with same open count and lower closed count,
    # order by closed count
    if len(users) < PAGE_SIZE+1:
      users += User.all().\
        filter('open =', from_user.open).\
        filter('closed <', from_user.closed).\
        order('-closed').\
        fetch(PAGE_SIZE+1-len(users))
    # get more users with lower open count,
    # order by open & closed count
    if len(users) < PAGE_SIZE+1:
      users += User.all().\
        filter('open <', from_user.open).\
        order('-open').\
        order('-closed').\
        fetch(PAGE_SIZE+1-len(users))
    response.users = users[:PAGE_SIZE]
  else:
    users = User.all().\
      order('-open').\
      order('-closed').\
      fetch(PAGE_SIZE+1)
    response.users = users[:PAGE_SIZE]
  
  # pagination
  if to_user:
    response.next.user = to_user
    response.next.url = "http://%s/users?from=%s" % (handler.host(), response.next.user.key())
    
    if len(users) > PAGE_SIZE+1:
      response.previous.user = users[1]
      response.previous.url = "http://%s/users?to=%s" % (handler.host(), response.previous.user.key())
  else:
    if from_user:
      response.previous.user = users[0]
      response.previous.url = "http://%s/users?to=%s" % (handler.host(), response.previous.user.key())
        
    if len(users) > PAGE_SIZE:
      response.next.user = users[PAGE_SIZE]
      response.next.url = "http://%s/users?from=%s" % (handler.host(), response.next.user.key())
