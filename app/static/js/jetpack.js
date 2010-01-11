// returns true if the given element is a child of the matched elements 
jQuery.fn.hasChild = function (el) { return jQuery(this).children().index(el) >= 0;};

// replaces <from> string with <to> string in the matched elements,
// returns the deepest elements that were affected
jQuery.fn.replace = function (from, to) {
  // find elements that contain the desired text
  // var els = jQuery(this).contains(from);
  var els = jQuery(":contains('"+from.replace("'", "\\'")+"')", this);
  return els.filter(function (i) {
      // last element or the next element isn't a child of this one
      return i == els.size()-1 || !jQuery(this).hasChild(els.get(i+1));
    }).
    each(function () {
      // replace <from> text with <to> text
      var el = jQuery(this); el.html(el.html().replace(from, to))
    });
}

jetpack.tabs.onReady(function (doc) {
  if (!doc.defaultView.frameElement) {
    // search for edits to this page
    jQuery.get('http://www.emendapp.com/search/edits?json', {
      q: doc.location.href
    }, function (response) {
      response.edits = jQuery.grep(response.edits, function (edit) {
        return edit.status == 'open';
      });
      if (response.edits.length) {
        // "(n) open edit(s) on (url)" notification
        jetpack.notifications.show(response.edits.length+" open edit"+(response.edits.length>1?'s':'')+" on "+doc.location.href);
        // insert our CSS
        jQuery('head', doc).append('<style type="text/css" media="screen">.emend {color: red}</style>');
        // mark edits
        var body = jQuery('body', doc);
        jQuery.each(response.edits, function (_, edit) {
          body.replace(edit.original, '<b class="emend" title="'+edit.original+'">'+edit.proposal+'</b>');
        });
      }
    }, 'json');
  }
});
