import logging

def post(handler, response):
  if handler.is_admin():
    user = handler.get_user(required=True)
    user.banned = False
    user.put()
    response.success = 1
