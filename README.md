# Emend

**Emend** is a service built on [Google App Engine][] for alerting website owners and authors of grammatical and spelling mistakes found on their site.

[Google App Engine]: http://code.google.com/appengine/

## Local configuration

Emend will look for a local configuration in "local.yaml". This file is
optional. It will automatically be cached in memcached.

### Twitter configuration

Twitter credentials are read from the "twitter" key in the local
configuration. The value should contain two keys, "prod" and "dev", which
should each contain a "username" and "password" key.

### Bitly credentials

Bitly credentials are read from the "bitly" key in the local configuration.
The value should contain two keys, "prod" and "dev", which should each contain
a "login" and "apiKey" key.

### Admin configuration

The "admin" key in the local configuration should map to a flat {key: value,
...} dictionary. Each item corresponds to a link in the admin section of the
footer. The key is the inner HTML of each link and the value is the href.
