var MY_CLICKED_EVENT = 0;
var MY_EXACT_EXECUTED_BLOOM = 0;
var MY_GLOBAL_BLOOM_1 = 0;
var MY_GLOBAL_BLOOM_2 = 0;
var MY_OTHER_EXECUTED_BLOOM = 0;
var MY_REGEX_BLOOM = 0;
var MY_REGEX_PARAM_0;
var MY_REGEX_PARAM_1;
var MY_STRING_FORMAT_BLOOM = 0;
var MY_STRING_FORMAT_PARAM_0;
var MY_STRING_FORMAT_PARAM_1;
var MY_WRONG_STRING_FORMAT_BLOOM = 0;

// stub out the getPathName method so we can test a particular URL
Jellyfish.getPathName = function () {
  return "/foo/bar/13";
}

var jellyfishApp = Jellyfish(function () {
  this.bloom(/^\/foo/, function (params) {
    MY_REGEX_BLOOM = 1;
    this.sting("#test_button/click", function (evt) {
      MY_CLICKED_EVENT = 1;
    });
  });

  this.bloom('/other_page', function (params) {
    MY_OTHER_EXECUTED_BLOOM = 1;
  });

  this.bloom(/\/foo\/([^\/]+)\/([^\/]+)/, function (params) {
    MY_REGEX_PARAM_0 = params[0];
    MY_REGEX_PARAM_1 = params[1];
  });

  this.bloom('/foo/bar/13', function (params) {
    MY_EXACT_EXECUTED_BLOOM = 1;
  });

  this.bloom('/:base/bar/:id', function (params) {
    MY_STRING_FORMAT_BLOOM = 1;
    MY_STRING_FORMAT_PARAM_0 = params['base'];
    MY_STRING_FORMAT_PARAM_1 = params['id'];
  });

  this.bloom('/foo/bar/13/:id', function (params) {
    MY_WRONG_STRING_FORMAT_BLOOM = 1;
  });

  this.bloom('*', function (params) {
    MY_GLOBAL_BLOOM_1 = 1;
  });

  Jellyfish.getPathName = function () {
    return '/example';
  }

  this.bloom('*', function (params) {
    MY_GLOBAL_BLOOM_2 = 1;
  });
});

var context = jqUnit.context;
var equals = jqUnit.equals;
context('Jellyfish', 'bare initializer', {
  before: function () {}
}).
should('execute a bloom with an exact matching string', function () {
  equals(MY_EXACT_EXECUTED_BLOOM, 1);
}).
should('not execute a bloom with a non-matching string', function () {
  equals(MY_OTHER_EXECUTED_BLOOM, 0);
}).
should('execute the correct bloom for a regex matcher', function () {
  equals(MY_REGEX_BLOOM, 1);
}).
should('give correct params for regex group matches', function () {
  equals(MY_REGEX_PARAM_0, 'bar');
  equals(MY_REGEX_PARAM_1, '13');
}).
should('execute the correct bloom for a matching string format', function () {
  equals(MY_STRING_FORMAT_BLOOM, 1);
}).
should('give correct params for a matching string format', function () {
  equals(MY_STRING_FORMAT_PARAM_0, 'foo');
  equals(MY_STRING_FORMAT_PARAM_1, '13');
}).
should('not execute a bloom with a non-matching string format', function () {
  equals(MY_WRONG_STRING_FORMAT_BLOOM, 0);
}).
should('add a sting for an element, by id', function () {
  equals(jellyfishApp.blooms[0].stings[0].selector, "#test_button");
}).
should('match all URLs with a global bloom', function () {
  equals(MY_GLOBAL_BLOOM_1, 1);
  equals(MY_GLOBAL_BLOOM_2, 1);
});
