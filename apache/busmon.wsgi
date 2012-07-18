import os
os.environ['PYTHON_EGG_CACHE'] = '/var/cache/busmon/.egg_cache'
import __main__
__main__.__requires__ = 'busmon'
import pkg_resources

from paste.deploy import loadapp
application = loadapp('config:/etc/busmon/production.ini')
