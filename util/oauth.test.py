from oauth import signed_url
import unittest

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
