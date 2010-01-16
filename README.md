# Emend

**Emend** is a service built on [Google App Engine][] for alerting website owners and authors of grammatical and spelling mistakes found on their site.

[Google App Engine]: http://code.google.com/appengine/

## Local configuration

Emend will look for a local configuration in "local.yaml". This file is
optional. It will automatically be cached in memcached.

### Twitter configuration

Twitter credentials are read from the _twitter_ key in the local
configuration. The value should contain two keys, _prod_ and _dev_, which
should each contain _oauth_consumer_key_, _oauth_consumer_secret_,
_oauth_token_, _oauth_token_secret_, _user_id_ and _screen_name_ keys.

### Bitly credentials

Bitly credentials are read from the _bitly_ key in the local configuration.
The value should contain two keys, _prod_ and _dev_, which should each contain
a _login_ and _apiKey_ key.

### Admin configuration

The _admin_ key in the local configuration should map to a flat {key: value,
...} dictionary. Each item corresponds to a link in the admin section of the
footer. The key is the inner HTML of each link and the value is the href.
