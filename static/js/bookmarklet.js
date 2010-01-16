function()
{
  window.open(
    'http://www.emendapp.com?url='+location.href+'&v=3&original='+
      encodeURIComponent(
        window.getSelection ? window.getSelection() :
        document.getSelection ? document.getSelection() :
        document.selection ? document.selection.createRange().text :
        ''
      ),
    '_blank');
}
