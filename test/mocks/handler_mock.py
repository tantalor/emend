from emend import RequestHandler

from google.appengine.ext.webapp import Request, Response


def mock_handler(page, request='/', **response):
  handler = RequestHandler.with_page(page=page)()
  handler.initialize(Request.blank(request), Response())
  handler.response_dict(**response)
  handler.logout_url = lambda: None
  handler.login_url = lambda: None
  return handler
