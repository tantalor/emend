jetpack.tabs.onReady(function (doc) {
  if (!doc.defaultView.frameElement) {
    jQuery.get('http://emend.appspot.com/search/edits?json', {
      q: doc.location.href
    }, function (response)
    {
      response.edits = $.grep(response.edits, function (edit) {
        return edit.status == 'open';
      });
      if (response.edits.length) {
        // "(n) open edit(s) on (url)" notification
        jetpack.notifications.show(response.edits.length+" open edit"+(response.edits.length>1?'s':'')+" on "+doc.location.href);
        // insert our CSS
        $('head', doc).append('<style type="text/css" media="screen">.emend {color: red}</style>');
        // mark edits
        var body = $('body', doc);
        $.each(response.edits, function (_, edit) {
          var proposal = '<b class="emend" title="'+edit.original+'">'+edit.proposal+'</b>';
          var el = $(":contains('"+edit.original+"')", body).eq(0);
          el.html(el.html().replace(edit.original, proposal));
        });
      }
    }, 'json');
  }
});
