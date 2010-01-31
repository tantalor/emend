from test.mocks.model_mock import MockModel
from model.user import User

from google.appengine.api import users


class MockUser(User, MockModel):
  def __init__(self, email="foo@bar.com", **kwargs):
    super(MockUser, self).__init__(
      key_name="test",
      user=users.User(
        email=email,
        _auth_domain="test",
      ),
      **kwargs
    )
