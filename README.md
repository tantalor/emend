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

Setup the environment in the project root,

    virtualenv -p /usr/bin/python2.7 --no-site-packages .

Activate the environment,

    source bin/activate

Install Emend's requirements,

    pip install -r pip-requirements.txt

Emend's application root is "app".
