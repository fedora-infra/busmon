from fedmsg.consumers import FedmsgConsumer
import time
import memcache


class MemcachedStuffer(FedmsgConsumer):
    topic = "*"
    config_key = 'busmon.consumers.memcached.enabled'
    jsonify = False

    def __init__(self, *args, **kwargs):
        super(MemcachedStuffer, self).__init__(*args, **kwargs)

        if not getattr(self, '_initialized', False):
            return

        servers = self.hub.config['busmon.memcached.servers'].split(',')
        self.mc = memcache.Client(servers)

    def consume(self, message):
        c = self.hub.config
        duration = c['busmon.memcached.duration']
        n = c['busmon.memcached.n']

        head = int(time.time() * 1000 / duration) % n
        key = "busmon_count_%i" % head

        # This try-except block is here to support both old and new versions of
        # python-memcached.
        try:
            if not self.mc.incr(key):
                raise ValueError("Not Found")
        except ValueError:
            self.mc.set(key, 1, time=duration / 1000.0 * n)
