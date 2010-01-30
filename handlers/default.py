from urlparse import urlparse
import logging

from model.site import Site
from model.edit import Edit
from model.user import User

from util.suggest import suggest
from util.bookmarklet import bookmarklet
from util.megaera.local import MissingCredentials
from util.megaera.env import is_dev

from google.appengine.ext import db
from google.appengine.api import memcache

from os import environ

def get(handler, response):
  # redirect to emendapp.com
  if not is_dev() and environ['HTTP_HOST'] == 'emend.appspot.com':
    return handler.redirect('http://www.emendapp.com?'+environ['QUERY_STRING'])
  # get params
  response.url = handler.request.get('url')
  response.original = handler.request.get('original')
  response.proposal = handler.request.get('proposal') or response.original
  # get a suggestion
  if response.original:
    query = response.original.encode('utf8')
    try:
      response.suggestion = suggest(query)
    except MissingCredentials, e:
      logging.warn('Missing credentials: %s', e)
  # check cache
  if not handler.cached():
    # get latest edits
    edits = Edit.all()\
      .filter('status =', 'open')\
      .order('-created')\
      .fetch(3)
    # cache these and update the response
    handler.cache(bookmarklet=bookmarklet(), edits=edits)

def post(handler, response):
  if not handler.current_user():
    return handler.redirect('/')
  # post params
  url = handler.request.get('url').strip()
  original = handler.request.get('original').strip()
  proposal = handler.request.get('proposal').strip()
  # copy params for error case
  response.url = url
  response.original = original
  response.proposal = proposal
  # parse url
  domain = urlparse(url).netloc
  if not domain:
    # fix URL by prefixing with default scheme
    url = "http://%s" % url
    domain = urlparse(url).netloc
  # error cases
  if not domain:
    handler.form_error(url="Invalid URL")
  if not original:
    handler.form_error(original="Original required")
  if not proposal:
    handler.form_error(proposal="Proposal required")
  # exit if errors occured
  if handler.has_errors():
    return
  
  # get site
  key_name = Site.key_name_from_domain(domain)
  site = Site.get_or_insert(key_name, domain=domain)
  
  # check for an existing instance of this edit
  existing = Edit.all()\
    .ancestor(site)\
    .filter('original =', original)\
    .filter('proposal =', proposal)\
    .filter('url =', url)\
    .get()
  
  if existing:
    handler.redirect(existing.permalink())
    return
  
  def put_edit():
    edit = Edit(
      index = site.index,
      author = handler.current_user(),
      original = original,
      proposal = proposal,
      url = url,
      parent = site
    )
    edit.put()
    # increment index and count, put
    site.index += 1
    site.open += 1
    site.put()
    return edit
  
  edit = db.run_in_transaction(put_edit)
  
  # clear cache
  handler.invalidate()
  
  # fiddle user's count
  edit.author.open += 1
  edit.author.put()
  
  # notifications
  edit.tweet()
  handler.ping_blogsearch()
  
  handler.redirect(edit.permalink())
