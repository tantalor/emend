# Megaera

**Megaera** is a python module for [Google App Engine](http://code.google.com/appengine/) applications. It offers a subclass of _[webapp.RequestHandler](http://code.google.com/appengine/docs/python/tools/webapp/requesthandlerclass.html)_ called _MegaeraRequestHandler_ with additional functionality.

![Megaera, Tisipone, and Alecto](/dodgeballcannon/megaera/raw/master/megaera.jpg)

## Motivation

The _webapp.RequestHandler_ class lacks several features common to web application frameworks such as automatic rendering of templates and support for alternate output formats (e.g., YAML, JSON).

To solve this, _MegaeraRequestHandler_ (which bases _webapp.RequestHandler_) associates a "handler" with one or more django templates (e.g., html, atom). Each handler is stored in a distinct file and can respond to a GET or POST request (or both). If the request specifies YAML or JSON output, the handler's response is automatically rendered in the specified type.

The basic Google App Engine SDK also omits common tasks such as distinguishing development and production environments and accessing application-specific local configuration.

Megaera solves these problems together by relying on a single `local.yaml` file in the application's root which can store configuration data for the development and production environments. Megaera's `local.config()` function then will automatically load the correct configuration data depending on the application's current environment.

## Handling Requests

Suppose you have the following files in your application.

    templates/
      default.html
    handlers/
      __init__.py
      default.py
    main.py
    app.yaml

To get your Megaera app up and running, first add a route in `app.yaml` from all paths to your `main.py`. Put this at the end if your handlers so any static files or other handlers won't be caught by the url regex. This is the default setting for App Engine.

    - url: .*
      script: main.py

In your `main.py`, build your _WSGIApplication_ by routing "/" to a _MegaeraRequestHandler_  with `MegaeraRequestHandler.with_page()`. In this case, we are routing "/" to the `handlers.default` module.

    from google.appengine.ext.webapp import WSGIApplication
    from google.appengine.ext.webapp.util import run_wsgi_app
    
    from megaera import MegaeraRequestHandler
    
    def application():
      return WSGIApplication([
        ('/', MegaeraRequestHandler.with_page('handlers.default'))
      ], debug=True)
    
    def main():
      run_wsgi_app(application())
    
    if __name__ == "__main__":
      main()

The `handlers.default` module can respond to GET requests very simply by defining a `handlers.default.get()` function which accepts `handler` and `response` arguments. The `handler` argument is a _MegaeraRequestHandler_ (a _webapp.RequestHandler_). The `response` argument is a special data structure called a _recursivedefaultdict_.

    def get(handler, response):
      name = handler.request.get('name')
      response.messages.hello = "hello %s" % name

A _recursivedefaultdict_ is a _[defaultdict](http://docs.python.org/library/collections.html#collections.defaultdict)_ whose keys can be read/written by the dot operator (i.e., _[getattr](http://docs.python.org/reference/datamodel.html#object.__getattr__)_, _[setattr](http://docs.python.org/reference/datamodel.html#object.__setattr__)_) and whose "default" is another _recursivedefaultdict_. The end result is a very simple-to-use datastructure. Megaera's _recursivedefaultdict_ is based on code samples by [Kent S Johnson](http://personalpages.tds.net/~kent37/kk/00013.html).

Finally, `templates/default.html` is a standard django template.

    {% if messages %}
      <p>{{messages.hello}}</p>
    {% endif %}
    <p>Your host is {{handler.host}}.</p>
    {% if is_dev %}
      <p>This is development.</p>
    {% endif %}

Megaera also automatically exposes `handler` (the request handler) and `is_dev` (a boolean) parameters to the templates.

## Caching

Megaera knows how to cache your handler's output. `MegaeraRequestHandler.cache()` accepts arbitrary keyword parameters to cache indefinitely, keyed by the current handler and with optional `time` time-to-live and `vary` parameters. `MegaeraRequestHandler.cached()` will return `True` if there exists a cached value for the current handler and optional `vary` parameter.

    def get(handler, response):
      if not handler.cached():
        # cache the following
        foo_data = fetch_foo_from_datastore()
        bar_data = fetch_bar_from_datastore
        # sets response.foo and response.bar
        handler.cache(foo=foo_data, bar=bar_data, time=60)

The `vary` parameter can be used to key the cache by a variable local to the handler such as an object.

## Megeara Configuration

By default, Megaera will guess where your templates are located and what they are named based on the filename of your handler modules. For instance, the `handlers.default` module's template should be `templates/default.html`. If you want to change the handlers or templates directories, just set the `MegaeraRequestHandler.HANDLERS_BASE` and `MegaeraRequestHandler.TEMPLATES_BASE` to your desired values in your `main.py`.

## Local Configuration

Megaera will look for an optional local configuration in `local.yaml`.

The structure of the local configuration is a dictionary. Every value of the dictionary may optionally be a dictionary with _prod_ and _dev_ keys. In this case, the _prod_ value will be used in production and the _dev_ value will be used in development.

The local configuration will automatically be cached in memcached under they key _local_config_.

To load the entire configuration for a given environment, call `local.config()`.

To load a value for a particular key, call `local.config_get(key)`. This will throw a _KeyError_ if the key doesn't exist.

### Example

In this example, the _yahoo_ key has distinct _appId_ values for production and development.

    yahoo:
      prod:
        appId: 7d3a4304887748f01a492daa0a70e770
      dev:
        appid: 89823f9248a5e9408e63d47179f8a8b3

## JSON, YAML, Atom

If a request's query parameters contain a `json`, `yaml`, or `atom` key, then the handler's default template will be ignored and the handler's response will be rendered in the desired format.

For example, the `/?yaml` request will render your default handler in YAML.

In the case of Atom, instead of rendering the "html" template, Megaera will loook for a template ending with "atom", e.g., "templates/default.atom".

Megaera will recursively sanitize the response in JSON or YAML mode. You can (and should) define `sanitize()` methods on your models to return sanitized data for the client.

## Tests

Megaera is packaged with [unit tests](http://docs.python.org/library/unittest.html) in the `test/` directory. 
### Example

    $ python test/megaera_test.py
    ........
    ----------------------------------------------------------------------
    Ran 8 tests in 0.002s

    OK