var url = 'http://www.emendapp.com?url='+location.href;
var link = document.getElementById("emend-edit-widget");
link.setAttribute('href', url);

function click(event)
{
  if (event && event.preventDefault) event.preventDefault()
  var selection = window.getSelection ? window.getSelection() :
    document.getSelection ? document.getSelection() :
    document.selection ? document.selection.createRange().text : false;
  if (selection && selection.toString()) {
    window.open(url+'&v=3&original='+encodeURIComponent(selection), '_blank');
  } else {
    alert("Select some text with a grammatical or spelling mistake and click this link again.");
  }
  return false;
};

if (link.attachEvent) link.attachEvent('onclick', click);
else link.addEventListener('click', click, false);
