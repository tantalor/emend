from random import getrandbits
from time import time
from urllib import quote, urlencode
import hmac
from hashlib import sha1
import unittest


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


class TestOAuth(unittest.TestCase):
  def test_oauth(self):
    """The canonical test from http://oauth.net/core/1.0"""
    url = signed_url(
      url="http://photos.example.net/photos",
      method="GET",
      oauth_consumer_key="dpf43f3p2l4k3l03",
      oauth_consumer_secret="kd94hf93k423kf44",
      oauth_token="nnch734d00sl2jdk",
      oauth_token_secret="pfkkdhi9sl3r4s00",
      oauth_signature_method="HMAC-SHA1",
      oauth_timestamp="1191242096",
      oauth_nonce="kllo9940pd9333jh",
      oauth_version="1.0",
      file="vacation.jpg",
      size="original")
    expected_url =\
      "http://photos.example.net/photos?file=vacation.jpg&"\
      "oauth_consumer_key=dpf43f3p2l4k3l03&oauth_nonce=kllo9940pd9333jh&"\
      "oauth_signature=tR3%2BTy81lMeYAr%2FFid0kMTYa%2FWM%3D&"\
      "oauth_signature_method=HMAC-SHA1&oauth_timestamp=1191242096&"\
      "oauth_token=nnch734d00sl2jdk&oauth_version=1.0&size=original"
    self.assertEqual(url, expected_url)


if __name__ == "__main__":
  unittest.main()
