from emend import User

def post(handler, response):
  user = handler.get_user(required=True)
  nickname = handler.request.get('nickname')
  if user.can_edit() and nickname:
    user.nickname = nickname
    user.put()
  # redirect
  handler.redirect(handler.request.get('continue') or '/')
