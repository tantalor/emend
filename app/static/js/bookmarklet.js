function()
{
  window.open(
    'http://www.emendapp.com?url='+encodeURIComponent(location.href.replace(/#.*/, ''))+
      '&v=5&original='+
      encodeURIComponent(
        window.getSelection ? window.getSelection() :
        document.getSelection ? document.getSelection() :
        document.selection ? document.selection.createRange().text :
        ''
      ),
    '_blank');
}
