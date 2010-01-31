import sys

from util.emend import Emend
from util.megaera.megaera import NotFoundException

from google.appengine.ext.webapp import Request, Response


def mock_handler(page, request='/', **response):
  handler = Emend.with_page(page=page)()
  handler.initialize(Request.blank(request), Response())
  handler.response_dict(**response)
  handler.logout_url = lambda self: None
  handler.login_url = lambda self: None
  def mock_not_found():
    raise NotFoundException()
  handler.not_found = mock_not_found
  def mock_handle_error():
    (error_type, error, tb) = sys.exc_info()
    raise error
  handler.handle_error = mock_handle_error
  return handler
