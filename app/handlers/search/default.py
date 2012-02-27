def get(handler, response):
  search_url = handler.urlize("/search/edits")
  response.search.by_query.url = search_url+"?query=%s"
  response.search.by_url.url = search_url+"?url=%s"
  response.search.by_url_sha1.url = search_url+"?url_sha1=%s"
