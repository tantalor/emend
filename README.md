# Emend

**Emend** is a service built on [Google App
Engine](http://code.google.com/appengine/) for alerting website owners and
authors of grammatical and spelling mistakes found on their site.

Emend uses [Megaera](http://github.com/tantalor/megaera/) to handle the
dirty work.

Emend integrates with [Twitter](http://twitter.com) and [bit.ly](http://bit.ly)
to publish a live stream of edits. Spelling suggestions are provided by
[Yahoo! Search BOSS](http://developer.yahoo.com/search/boss/boss_guide/Spelling_Suggest.html)
via [YQL](http://developer.yahoo.com/yql/).

## Environment and Requirements

Emend expects its requirements to be installed by `pip` in a `virtualenv` environment.

From your project root, setup the environment,

    virtualenv -p /usr/bin/python2.5 --no-site-packages env

Then install Emend's requirements,

    env/bin/pip -E env install -r pip-requirements.txt

You can put your environment anywhere. In this example it is a directory called "env".

Lastly, add a symlink to your site-packages directory,

    ln -s env/lib/python2.5/site-packages
