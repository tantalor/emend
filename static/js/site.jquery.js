(function ($)
{
  $.to = function (action, args, method)
  {
    var form = $('<form>').attr({method: method || 'get', action: action});
    for (var key in args)
    {
      $('<input type="hidden">')
        .attr({name: key})
        .val(args[key])
        .appendTo(form);
    }
    return form.appendTo('body').submit();
  };
  
  $.postTo = function (action, args)
  {
    return $.to(action, args, 'post');
  }
}
)(jQuery);
