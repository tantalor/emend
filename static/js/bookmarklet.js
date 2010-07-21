function()
{
  window.open(
    'http://www.emendapp.com?url='+encodeURIComponent(location.protocol+"//"+location.host+location.pathname)+
      '&v=4&original='+
      encodeURIComponent(
        window.getSelection ? window.getSelection() :
        document.getSelection ? document.getSelection() :
        document.selection ? document.selection.createRange().text :
        ''
      ),
    '_blank');
}
