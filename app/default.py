import re
import os

from urlparse import urlparse

from emend import Site, Edit
from google.appengine.ext import db

def get(handler, response):
  # get params
  response.url = handler.request.get('url');
  response.original = handler.request.get('original')
  # build bookmarklet
  bookmarklet = ''.join(file('js/bookmarklet.js').readlines())
  bookmarklet = re.compile('\s').sub('', bookmarklet)
  response.bookmarklet = bookmarklet
  # get latest edits
  response.edits = set(Edit.all().order('-datetime').fetch(3))

def post(handler, response):
  if not handler.user():
    return handler.redirect('/')
  # post params
  url = handler.request.get('url');
  original = handler.request.get('original')
  proposal = handler.request.get('proposal')
  # parse url
  domain = urlparse(url).netloc
  if not domain:
    # fix URL by prefixing with default scheme
    url = "http://%s" % url
    domain = urlparse(url).netloc
  if not domain:
    # error case
    response.errors.url = "Invalid URL."
    return
  # get site
  key_name = Site.key_name_from_domain(domain)
  site = Site.get_or_insert(key_name, domain=domain)
  
  def put_edit():
    Edit(
      index = site.index,
      site = site,
      author = handler.user(),
      original = original,
      proposal = proposal,
      url = url,
      parent = site
    ).put()
    # increment index and put
    site.index +=1
    site.put()
  
  db.run_in_transaction(put_edit)
  
  # if not handler.is_dev():
  #   tweet("\"%s\" should be \"%s\" %s" % (original, proposal, url))
  handler.tweet("\"%s\" should be \"%s\" %s" % (original, proposal, url))
  handler.redirect("/sites/%s" % site.domain)
