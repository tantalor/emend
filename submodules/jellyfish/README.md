# Jellyfish

Jellyfish is a framework for writing JavaScript for an entire web site or grouping of pages. Instead of focusing on each page and component individually as is traditional, Jellyfish lets you step back and specify the high-level structure and interaction of your JS across multiple pages from a single JS source file.

## Why create Jellyfish?

I kept running into situations where I wanted to create a relatively simple web site that had many static pages and a small amount of scripting on each. Previously, I would have to create a separate .js file for each static page, then loading each different .js file from each .html file.

Instead of worrying about all of these different .js files for a small amount of scripting, I created Jellyfish. This way, I can write a single .js file that controls all of the scripting across the site, partitioned by page (or sets of pages). I can include the single .js file in my layout file and avoid the headache of managing myriad .js files. Isn't that nice?

## A Complementary Framework

Jellyfish doesn't replace other JS frameworks like jQuery or YUI&mdash;it runs right alongside them and complements their functionality with page-level abilities. Jellyfish is most at home with jQuery, but can perform simple duties without any library present.

## Dive In with an Example

    Jellyfish(function () {

      this.bloom('/about', function () {
        this.sting('#header/click', function (evt) {
          alert("Hi there.");
        });
      });

    });

Hopefully you can see how this could be useful when spread out across many URLs and with many events, all without using separate .js files.

## Concepts

Jellyfish defines a couple of its own concepts to separate page-level interaction from event-level interaction within a page.

### Blooms

Blooms can be thought of as sections of code that are only run if their given URL matches the current URL loaded in the browser. Blooms also provide convenient access to page-level attributes like the query parameters and, optionally, can treat other pieces of the URL as parameters (akin to Rails' routes).

Accordingly, the URL matcher for a bloom can be a simple string, a route-like string with embedded parameters, or a `RegExp` object. Matches from a route string or a `RegExp` will be passed in to the bloom's executable method for later use.

#### Bloom Examples

    bloom('/about', function (params) { /* ... */ });

This bloom will only match the URL `/about` at the root of the URL's path. So it will match `http://example.com/about` but not `http://example.com/about.html` or `http://example.com/learn/about`.

    bloom('/things/:id', function (params) { /* ... */ });

As with [Rails' routes][routes], you can specify named parameters to be looked for and extracted from the URL. In this case, only URLs like `/things/10` or `/things/foo` will be matched and `params['id']` will contain "10" or "foo", respectively.

 [routes]: http://guides.rubyonrails.org/routing.html

    bloom(/number_(\d+)/, function (params) { /* ... */ });

In this case the `RegExp` will match `/number_10` as well as `/foo/barnumber_10/banana`, setting `params[0]` to be "10" in both cases.

### Stings

Stings are event-level specifications within a bloom that indicate which event listeners should be added on which elements within a page. Each string has a specification string in the format `"{selector}/{event}"` and a corresponding function to execute when the given event is fired.

#### Sting Example

    sting('#header/click', function(evt) { console.log(evt.target.id); });

This sting will attach a `click` event listener to the element with `id` "header" (if it exists). In this case, when that element is clicked, the console should see a long entry of "header".

## Advanced Usage

### Global Bloom

You can create a bloom that applies on all pages by specifying the string `'*'`.

### Loading Other JavaScript Files

TODO: Implement

### Custom Events

TODO: Implement

## Testing

Run the bundled tests by opening `test/jellyfish.html` in your web browser.

## Author

Jellyfish was written by Brad Fults ([h3h.net][site], [bfults@gmail.com][email]).

  [site]: http://h3h.net/
  [email]: mailto:bfults@gmail.com

## Inspiration

Inspiration for this project came from [quirkey's sammy][sammy] and [Sinatra][sinatra], a Ruby microframework.

 [sammy]:   http://github.com/quirkey/sammy
 [sinatra]: http://github.com/sinatra/sinatra

## License

Jellyfish is released under the MIT License. See LICENSE for more information.
