from random import getrandbits
from time import time
from urllib import quote, urlencode
import hmac
from hashlib import sha1


def escape(s):
  return quote(str(s), safe='~')

def hmac_sha1_base64(key, value):
  """Base-64 encoded HMAC SHA1 hash."""
  return hmac.new(key, value, sha1).digest().encode('base64')[:-1]

def signed_url(url, oauth_consumer_secret, oauth_token_secret,
               method="GET", **kwargs):
  """The signed URL with the given arguments and method."""
  return '%s?%s' % (url, signed_args(url, oauth_consumer_secret,
                                     oauth_token_secret, method, **kwargs))

def sig_key(oauth_consumer_secret, oauth_token_secret):
  """The signature key."""
  return '&'.join([escape(oauth_consumer_secret), escape(oauth_token_secret)])

def sig_base(url, method="GET", **kwargs):
  """The signature base."""
  params = ['%s=%s' % (escape(k), escape(kwargs[k])) for k in sorted(kwargs)]
  return '&'.join(map(escape, (method.upper(), url, '&'.join(params))))

def signed_args(url, oauth_consumer_secret, oauth_token_secret,
                method="GET", **kwargs):
  """The signed arguments for the given URL and method."""
  # start with defaults
  args = dict(
    oauth_version='1.0',
    oauth_signature_method='HMAC-SHA1',
    oauth_timestamp=int(time()),
    oauth_nonce=getrandbits(64),
  )
  # add overrides
  args.update(kwargs)
  # build key from secrets
  key = sig_key(oauth_consumer_secret, oauth_token_secret)
  # build base from arguments
  base = sig_base(url, method, **args)
  # compute signature digest from key and signature base
  args['oauth_signature'] = hmac_sha1_base64(key, base)
  # sort and encode args
  return urlencode([(k, args[k]) for k in sorted(args)])
