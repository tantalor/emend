from urlparse import urlparse

from model.site import Site
from model.edit import Edit
from model.user import User

from util.bookmarklet import bookmarklet

from google.appengine.ext import db
from google.appengine.api import memcache

__CACHE_KEY = 'app/default-edits'

def invalidate():
  memcache.delete(__CACHE_KEY)

def get(handler, response):
  # get params
  response.url = handler.request.get('url');
  response.original = handler.request.get('original')
  response.proposal = handler.request.get('proposal') or response.original
  # check cache
  cached = memcache.get(__CACHE_KEY)
  if cached:
    response.update(cached)
  else:
    # get latest edits
    edits = list(Edit.all().order('-created').fetch(3))
    # cache
    cached = dict(bookmarklet=bookmarklet(), edits=edits)
    response.update(cached)
    memcache.set(__CACHE_KEY, cached)

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
  invalidate()
  
  # fiddle user's count
  edit.author.open += 1
  edit.author.put()
  
  # notifications
  edit.tweet()
  handler.ping_blogsearch()
  
  handler.redirect(edit.permalink())
