Jellyfish(function () {
  this.bloom('*', function () {
    this.sting('.change-nickname/click', function ()
    {
      var current = $('#current-user');
      var permalink = $('#current-user-permalink').val();
      var nickname = prompt("What nickname would you like?", current.text());
      if (nickname == current.text())
      {
        alert("Okay, your nickname hasn't changed.");
      } else if (nickname)
      {
        var request = {
          nickname: nickname,
          json: 1
        };
        $.post(permalink+"/nickname", request, function (response)
        {
          alert("Great! Your new nickname is \""+response.user.nickname+"\".");
          current.text(response.user.nickname);
        }, 'json');
      }
    });
  });
});
