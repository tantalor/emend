# Emend

**Emend** is a service built on [Google App Engine][] for alerting website
owners and authors of grammatical and spelling mistakes found on their site.

[Google App Engine]: http://code.google.com/appengine/

## Local configuration

Emend will look for an optional local configuration in "local.yaml".

The structure of the local configuration is a dictionary. Every value of
the dictionary may optionally be a dictionary with two keys, _prod_ and _dev_.
In this case, the _prod_ value will be used in production and the _dev_ value
will be used in development.

The local configuration will automatically be cached in memcached under they key
_local_config_. To reload it, GET /admin/memclear?key=local_config&yaml.

### Twitter credentials

Twitter credentials are read from the _twitter_ key in the local
configuration. The value should contain contain _oauth_consumer_key_,
_oauth_consumer_secret_, _oauth_token_, _oauth_token_secret_, _user_id_
and _screen_name_ keys.

### Bitly credentials

Bitly credentials are read from the _bitly_ key in the local configuration.
The value should contain _login_ and _apiKey_ keys.

### Admin configuration

The _admin_ key in the local configuration should map to a flat {key: value,
...} dictionary. Each item corresponds to a link in the admin section of the
site's footer. The key is the inner HTML of each link and the value is the href.
