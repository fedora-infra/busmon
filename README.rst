busmon - Fedora Bus Monitor
===========================

busmon is a TurboGears2 app that watches the Fedora Message Bus with `fedmsg
<http://github.com/ralphbean/fedmsg>`_ and displays realtime graphs about the
activity on the bus.

Hacking on busmon
=================

busmon requires `Moksha <http://moksha.fedorahosted.org>`_ to do it's
work.  First you'll need to get moksha's source::

    $ git clone git://git.fedorahosted.org/git/moksha.git

Moksha provides some development tools to setup your development
environment, and busmon wraps these.  You'll need to create a
configuration file for yourself in ``~/.moksha/ctl.conf``.  In it,
put the following::

    [busmon]
    venv = busmon
    busmon-src-dir = /home/threebean/devel/busmon
    moksha-src-dir = /home/threebean/devel/moksha
    verbose = True

Get the source for busmon::

    $ git clone git://github.com/ralphbean/busmon.git
    $ cd busmon

The ``busmon-ctl.py`` script references ``~/.moksha/ctl.conf`` so you'll
need that in place first.  If that's all good, use ``busmon-ctl.py`` to
bootstrap your environment, build the virtualenv, install all dependencies,
and start busmon::

    $ ./busmon-ctl.py bootstrap
    $ ./busmon-ctl.py rebuild
    $ ./busmon-ctl.py restart
    $ ./busmon-ctl.py logs

After you have run ``./busmon-ctl.py bootstrap`` for the first time, you can
chain subsequent commands, like::

    $ ./busmon-ctl.py restart logs

If you point your browser at http://localhost:8080/, you should see busmon
running but with no activity on the charts.  You'll need to run
``tools/fake-bus.py`` to get some toy development data::

    $ workon busmon
    (busmon)$ ./tools/fake-bus.py
