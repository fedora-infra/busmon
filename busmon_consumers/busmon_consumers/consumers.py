import pygments.lexers
import pygments.formatters
from fedmsg.consumers import FedmsgConsumer
import time
import math
import memcache

import fedmsg
import fedmsg.encoding


class MessageColorizer(FedmsgConsumer):
    topic = "*"
    config_key = 'busmon.consumers.colorizer.enabled'
    jsonify = False
    destination_topic = "colorized-messages"

    def consume(self, message):

        if self.destination_topic in message.topic:
            return

        html_args = {'full': False}
        code = pygments.highlight(
            fedmsg.encoding.pretty_dumps(fedmsg.encoding.loads(message.body)),
            pygments.lexers.JavascriptLexer(),
            pygments.formatters.HtmlFormatter(**html_args)
        )

        code = code.strip()

        fedmsg.publish(
            topic=self.destination_topic,
            msg=code,
            modname="busmon",
        )


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
        if MessageColorizer.destination_topic in message.topic:
            return

        c = self.hub.config
        duration = c['busmon.memcached.duration']
        n = c['busmon.memcached.n']

        head = int(time.time() * 1000 / duration) % n
        key = "busmon_count_%i" % head

        if not self.mc.incr(key):
            self.mc.set(key, 1, time=duration / 1000.0 * n)
