from test.mocks.model_mock import MockModel
from model.site import Site


class MockSite(Site, MockModel):
  def __init__(self, domain="test.com", key_name="test", **kwargs):
    super(MockSite, self).__init__(
      domain=domain,
      key_name=key_name,
      **kwargs
    )
