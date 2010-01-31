from util.emend import Emend

from google.appengine.ext.webapp import Request, Response


def mock_handler(page, request='/', **response):
  handler = Emend.with_page(page=page)()
  handler.initialize(Request.blank(request), Response())
  handler.response_dict(**response)
  handler.logout_url = lambda self: None
  handler.login_url = lambda self: None
  return handler
