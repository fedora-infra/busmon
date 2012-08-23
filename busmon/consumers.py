import pygments.lexers
import pygments.formatters
from fedmsg.consumers import FedmsgConsumer

import fedmsg
import fedmsg.encoding

# TODO - Is there an equivalent thing in kitchen?
from paste.deploy.converters import asbool

import logging
log = logging.getLogger("moksha.hub")


class MessageColorizer(FedmsgConsumer):
    topic = "*"
    destination_topic = "colorized-messages"
    config_key = 'busmon.consumers.enabled'
    jsonify = False

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

        fedmsg.send_message(
            topic=self.destination_topic,
            msg=code,
        )
