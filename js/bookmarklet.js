function()
{
  window.open(
    'http://emend.appspot.com?url='+location.href+'&original='+
      (
        window.getSelection ? window.getSelection() :
        document.getSelection ? document.getSelection() :
        document.selection ? document.selection.createRange().text :
        ''
      ),
    '_blank');      
}
