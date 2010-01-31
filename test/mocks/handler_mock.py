from emend.request_handler import EmendRequestHandler

from google.appengine.ext.webapp import Request, Response


def mock_handler(page, request='/', **response):
  handler = EmendRequestHandler.with_page(page=page)()
  handler.initialize(Request.blank(request), Response())
  handler.response_dict(**response)
  handler.logout_url = lambda self: None
  handler.login_url = lambda self: None
  return handler
