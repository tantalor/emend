from emend import User


PAGE_SIZE = 10


def get(handler, response):
  from_key = handler.request.get('from')
  if from_key:
    from_user = User.get(from_key)
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
  else:
    users = User.all().\
      order('-open').\
      order('-closed').\
      fetch(PAGE_SIZE+1)
  
  response.users = users[:PAGE_SIZE]
  if len(users) > PAGE_SIZE:
    response.next.user = users[PAGE_SIZE]
    response.next.url = "http://%s/users?from=%s" % (handler.host(), response.next.user.key())
