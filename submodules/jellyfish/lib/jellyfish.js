/**
  Jellyfish
  2009-05-19 / Brad Fults <bfults@gmail.com>
**/

Jellyfish = function(blkApp) {

  var app = this;
  this.blooms = [];
  this.usejQuery = false;

  var RX_URL_STRING_FORMAT = /\/:(\w+)/;
  var RX_URL_STRING_FORMAT_TOKEN = /\\:(\w+)/g;

  // *-* public API *-*

  function bloom(matcher, blkBloom) {
    var b = new Bloom(matcher);
    if (b.matchesLocation()) {
      function sting(spec, fn) {
        b.stings.push(new Sting(spec, fn));
        return contextBloom;
      };

      var contextBloom = {sting: sting};
      blkBloom.call(contextBloom, b.params);
      app.blooms.push(b);
    }
    return contextApp;
  };

  // *-* object defintions *-*
  /*
   class Bloom
     RegExp matcher
     Hash params
     Array[Sting] stings

   class Sting
     String selector
     String event
     Function callback
  */
  function Bloom(matcher) {
    this.matcher = matcher;
    this.params = {};
    this.stings = [];

    this.matchesLocation = function() {
      var locMatch = this.matcher;
      var locActual = Jellyfish.getPathName();
      if (locMatch.constructor == String) {
        return this.matchesLocationString(locActual);
      }
      else if (locMatch.constructor == RegExp) {
        var m = locMatch.exec(locActual);
        if (m) {
          if (m.length > 1) {
            this.params = m.slice(1);
          }
          return true;
        }
      }
      return false;
    };

    this.matchesLocationString = function (locActual) {
      var locMatch = this.matcher;
      if (locMatch == '*') {
        return true;
      }
      var m;
      if (m = RX_URL_STRING_FORMAT.test(locMatch)) {
        var keys = [];
        var segments = locMatch.split('/');
        for (var i=0; i < segments.length; i++) {
          if (segments[i].charAt(0) == ':') {
            keys.push(segments[i].slice(1));
          }
        }
        var values = [];
        var rx = new RegExp(
          '^' + replaceTokensWithRegexen(escapeForRegex(locMatch)) + '$'
        );
        if (m = rx.exec(locActual)) {
          values = m.slice(1);
          for (var i=0; i < values.length; i++) {
            this.params[keys[i]] = values[i];
          }
          return true;
        }
      }
      else {
        return (locMatch == locActual);
      }
      return false;
    };
  }

  function Sting(spec, fn) {
    var sel_evt = spec.split('/');
    this.selector = sel_evt.shift();
    this.event = sel_evt.shift();
    this.callback = fn;
    addEventForSelector(this.selector, this.event, this.callback);
  }

  // *-* utility methods *-*

  var addEvent = window.attachEvent ? function (el, sEvent, fnCallback) {
    el.attachEvent('on' + sEvent, function (e) {fnCallback.call(el, e);});
  } :
  function (el, sEvent, fnCallback) {
    el.addEventListener(sEvent, function (e) {fnCallback.call(el, e);}, false);
  };

  function addEventForSelector(sSelector, sEvent, fnCallback) {
    if (app.usejQuery) {
      jQuery(document).ready(function (jQuery) {
        jQuery(sSelector).bind(sEvent, fnCallback);
      });
    }
    else {
      Jellyfish.ready(function () {
        var el = getElementFromSelector(sSelector);
        el && addEvent(el, sEvent, fnCallback);
      });
    }
  }

  function getElementFromSelector(sel) {
    if (sel == 'window') {
      return window;
    }
    else if (/#\w+/.test(sel)) {
      return document.getElementById(sel.slice(1));
    }
    return null;
  }

  function escapeForRegex(str) {
    return str.replace(/([\\\^\$*+[\]?{}.=!:(|)])/g, "\\$1");
  }

  function replaceTokensWithRegexen(str) {
    return str.replace(RX_URL_STRING_FORMAT_TOKEN, "([^/]+)");
  }

  if (typeof(jQuery) != 'undefined' && jQuery.fn.bind) {
    this.usejQuery = true;
  }

  var contextApp = {bloom: bloom};
  blkApp.call(contextApp);
  return this;
};

// *-* meta utilities *-*

Jellyfish.loadStack = [];
Jellyfish.isLoaded = false;

Jellyfish.ready = function (fn) {
  (Jellyfish.isLoaded) ? fn() : Jellyfish.loadStack.push(fn);
};

Jellyfish.eventPageLoaded = function () {
  Jellyfish.isLoaded = true;
  if (Jellyfish.loadStack.length > 0) {
    var fn;
    while (fn = Jellyfish.loadStack.shift()) {
      fn();
    }
  }
};

Jellyfish.getPathName = function () {
  return window.location.pathname;
}

// DOM Ready script from Dean Edwards -- http://dean.edwards.name/
Jellyfish.uniqueLoadEvent=function(){if(arguments.callee.done)return;
arguments.callee.done=true;Jellyfish.eventPageLoaded();}
if(document.addEventListener){document.addEventListener('DOMContentLoaded',
Jellyfish.uniqueLoadEvent,false);}(function(){if(/loaded|complete/.test(
document.readyState)){return Jellyfish.uniqueLoadEvent();}
if(!Jellyfish.uniqueLoadEvent.done)setTimeout(arguments.callee,30);})();
if(window.addEventListener){window.addEventListener('load',
Jellyfish.uniqueLoadEvent,false);}else if(window.attachEvent)
{window.attachEvent('onload',Jellyfish.uniqueLoadEvent);}
