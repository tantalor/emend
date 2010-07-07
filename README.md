# Emend

**Emend** is a service built on [Google App
Engine](http://code.google.com/appengine/) for alerting website owners and
authors of grammatical and spelling mistakes found on their site.

Emend uses [Megaera](http://github.com/tantalor/megaera/) to handle the
dirty work.

## Local configuration

Emend will look for an optional local configuration in "local.yaml".

The structure of the local configuration is a dictionary. Every value of the
dictionary may optionally be a dictionary with _prod_ and _dev_ keys. In this
case, the _prod_ value will be used in production and the _dev_ value will be
used in development.

The local configuration will automatically be cached in memcached under they key
_local_config_. To reload it, GET /admin/memclear?key=local_config&yaml.

### Twitter credentials

[Twitter](http://twitter.com) credentials are stored under the _twitter_ key as
a dictionary wth _oauth_consumer_key_, _oauth_consumer_secret_, _oauth_token_,
_oauth_token_secret_, _user_id_ and _screen_name_ keys.

### Bitly credentials

[bit.ly](http://bit.ly) credentials are stored under the _bitly_ key as a
dictionary with _login_ and _apiKey_ keys.

### Admin links

The site footer's admin links are stored under the _admin_ key as a flat
dictionary. The key of each item is the text of a link and the value is
the link's href.
