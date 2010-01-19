Jellyfish(function () {
  /* all pages */
  this.bloom('*', function () {
    /* change nickname */
    this.sting('.change-nickname/click', function () {
      var current = $('#current-user');
      var permalink = $('#current-user-permalink').val();
      var nickname = prompt("What nickname would you like?", current.text());
      if (nickname == current.text()) {
        alert("Okay, your nickname hasn't changed.");
      } else if (nickname) {
        var request = {
          nickname: nickname,
          json: 1
        };
        $.post(permalink+"/nickname", request, function (response) {
          alert("Great! Your new nickname is \""+response.user.nickname+"\".");
          current.text(response.user.nickname);
        }, 'json');
      }
    });
  });
  /* home page */
  this.bloom('/', function () {
    /* suggestion */
    this.sting('.click-suggestion/click', function () {
      $('[name=proposal]').val($(this).text());
    });
  });
  /* edit detail */
  this.bloom('/sites/:site/edits/:index', function () {
    /* edit permalink */
    function permalink () {
      return $('link[rel=canonical]').attr('href');
    }
    /* close edit */
    this.sting('.click-close/click', function () {
      $.post(permalink()+"/test", {json: 1}, function (response) {
        if (response.status == 'fixed') {
          alert("Thanks!");
          window.location.reload();
        } else {
          var again;
          if (response.status == 'unfixed') {
            again = confirm("Looks like it hasn't been fixed yet, change it anyway?");
          } else if (response.status == 'uncertain') {
            again = confirm("I couldn't tell if it was fixed, change it anyway?");
          } else if (response.error) {
            alert("An error occured: "+response.error);
          }
          if (again) {
            $.post(permalink()+"/close", {json: 1}, function () {
              alert("Thanks!");
              window.location.reload();
            });
          }
        }
      }, 'json');
    });
    /* open edit */
    this.sting('.click-open/click', function () {
      $.post(permalink()+"/open", {json: 1}, function () {
        alert("Thanks!");
        window.location.reload();
      });
    });
    /* delete edit */
    this.sting('.click-delete/click', function () {
      if (confirm("Are you sure?")) {
        $.postTo(permalink()+"/delete");
      }
    });
    /* pingback */
    this.sting('.click-pingback/click', function () {
      var el = $(this);
      el.text('Sending pingback...');
      $.post(permalink()+"/pingback", {json: 1}, function (response) {
        if (response.success) {
          alert('Success!');
        } else if (response.error) {
          alert("Sorry, something went wrong.\n\n"+response.error);
        }
        el.text('Pingback');
      }, 'json');
    });
  });
});
