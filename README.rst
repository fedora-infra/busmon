busmon - Fedora Bus Monitor
===========================

busmon is a TurboGears2 app that watches the Fedora Message Bus with `fedmsg
<http://github.com/ralphbean/fedmsg>`_ and displays realtime graphs about the
activity on the bus.

Hacking on busmon
=================

Get the source for busmon::

    $ git clone git://github.com/ralphbean/busmon.git
    $ cd busmon

Install `virtualenvwrapper <http://pypi.python.org/pypi/virtualenvwrapper>`_ and
use it to create a virtualenv.  In that virtualenv, install all of busmon's
dependencies::

    $ sudo yum -y install python-virtualenvwrapper
    $ mkvirtualenv busmon
    (busmon)$ python setup.py develop

Now busmon is composed of two parts, a message processor run as a Consumer in
the fedmsg-hub, and a webapp.  The hub takes messages from the fedmsg bus and
forwards them via it's websocket server to the client's browser.  Since you're
developing, you'll also need some fake message for the fedmsg bus.  You'll need
**three** terminals to run these commands and watch the log messages.

In the first::

    $ workon busmon
    (busmon)$ python tools/fake-bus.py

In the second::

    $ workon busmon
    (busmon)$ fedmsg-hub --websocket-server-port 9919

In the third::

    $ workon busmon
    (busmon)$ paster serve --reload development.ini

Point your browser at http://localhost:8080/ for awesome.
