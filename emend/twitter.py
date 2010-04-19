from megaera import local, json
from oauth import signed_url

from google.appengine.api import urlfetch


__TWITTER_API__ = "http://api.twitter.com/1"


def tweet(status, **credentials):
  if not credentials:
    # shortcut for no-credentials case
    credentials = local.config_get('twitter')
    if not credentials:
      return
  update_url = "%s/statuses/update.json" % __TWITTER_API__
  fetch_url = signed_url(url=update_url, method='POST', status=status, **credentials)
  response = urlfetch.fetch(fetch_url, method=urlfetch.POST)
  try:
    content = json.read(response.content)
    return content.get('id')
  except json.ReadException:
    pass

def untweet(status_id, **credentials):
  if not credentials:
    # shortcut for no-credentials case
    credentials = local.config_get('twitter')
    if not credentials:
      return
  destroy_url = "%s/statuses/destroy.json" % __TWITTER_API__
  fetch_url = signed_url(url=destroy_url, method='POST', id=status_id, **credentials)
  response = urlfetch.fetch(fetch_url, method=urlfetch.POST)
  try:
    content = json.read(response.content)
    return content.get('id')
  except json.ReadException:
    pass
