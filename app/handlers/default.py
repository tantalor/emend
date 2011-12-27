from urlparse import urlparse
import logging

from emend import Site, Edit, User

from emend import suggest, bookmarklet, site_name, blogsearch, canonical_url
from emend.model.edit import get_url_sha1_bloom
from megaera.env import is_dev

from google.appengine.ext import db
from google.appengine.api.urlfetch import DownloadError

from os import environ


PAGE_SIZE = 3


def get(handler, response):
  # redirect to emendapp.com
  if not is_dev() and environ.get('HTTP_HOST') == 'emend.appspot.com':
    return handler.redirect('http://www.emendapp.com?'+environ['QUERY_STRING'])
  # get params
  response.url = handler.request.get('url')
  response.original = handler.request.get('original')
  response.proposal = handler.request.get('proposal') or response.original
  response.original_eq_proposal = response.proposal == response.original
  # get a suggestion
  if response.original:
    try:
      response.suggestion = suggest(response.original)
    except KeyError, e:
      logging.warn('Missing credentials: %s', e)
  if response.url:
    # get canonical URL
    try:
      my_canonical_url = canonical_url(response.url)
      if my_canonical_url:
        response.url = my_canonical_url
    except DownloadError:
      handler.form_error(url="Connection refused")
    except Exception, e:
      handler.form_error(url="Error, %s" % e);
    # lookup latest edit for the URL
    local_edits = Edit.all().\
      filter('url =', response.url).\
      order('-created').\
      fetch(1)
    if local_edits:
      response.local_edit = local_edits[0]
  # get latest edits and bookmarklet (cached)
  if not handler.cached():
    edits = Edit.all()\
      .filter('status =', 'open')\
      .order('-created')\
      .fetch(PAGE_SIZE+1)
    has_next, next_from = None, None
    if len(edits) > PAGE_SIZE:
      has_next = 1
      next_from = edits[PAGE_SIZE].key()
    # cache these and update the response
    handler.cache(
      bookmarklet=bookmarklet(),
      edits=edits[:PAGE_SIZE],
      has_next=has_next,
      next_from=next_from,
    )

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
  
  # add to bloom
  bloom = get_url_sha1_bloom()
  if bloom:
    bloom.add(edit.url_sha1)
    bloom.put()
  
  # clear cache
  handler.invalidate()
  
  # fiddle user's count
  edit.author.open += 1
  edit.author.put()
    
  # tweet
  edit.tweet()
  
  # ping blogsearch
  host_url = 'http://%s' % handler.host()
  changes_url = '%s?atom' % host_url
  blogsearch.ping(name=site_name(), url=host_url, changesURL=changes_url)
  
  handler.redirect(edit.permalink())
