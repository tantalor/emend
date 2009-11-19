from model.user import User

def get(handler, response):
  response.users = User.all().\
    filter('open >', 0).\
    order('-open').\
    fetch(10)
  response.users += User.all().\
    filter('open =', 0).\
    filter('closed >', 0).\
    order('-closed').\
    fetch(10)
