from megaera import local
from oauth import signed_url

from google.appengine.api import urlfetch


def tweet(status, **credentials):
  if not credentials:
    # shortcut for no-credentials case
    credentials = local.config_get('twitter')
  update_url = "http://twitter.com/statuses/update.xml"
  fetch_url = signed_url(url=update_url, method='POST', status=status, **credentials)
  response = urlfetch.fetch(fetch_url, method=urlfetch.POST)
  if response:
    return response.content
