from model_mock import MockModel
from site_mock import MockSite
from user_mock import MockUser
from model.edit import Edit


class MockEdit(Edit, MockModel):
  def __init__(self, original="test", proposal="test", url="http://test.com", **kwargs):
    super(MockEdit, self).__init__(
      index=0,
      url=url,
      original=original,
      proposal=proposal,
      author=MockUser(),
      parent=MockSite(),
      **kwargs
    )
    if self.is_open:
      self.site.open += 1
      self.author.open += 1
    if self.is_closed:
      self.site.closed += 1
      self.author.closed += 1
