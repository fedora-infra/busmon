import pygments.lexers
import pygments.formatters
from fedmsg.consumers import FedmsgConsumer

import fedmsg
import fedmsg.encoding


class MessageColorizer(FedmsgConsumer):
    topic = "*"
    config_key = 'busmon.consumers.enabled'
    jsonify = False

    def consume(self, message):
        destination_topic = "colorized-messages"

        if destination_topic in message.topic:
            return

        html_args = {'full': False}
        code = pygments.highlight(
            fedmsg.encoding.pretty_dumps(fedmsg.encoding.loads(message.body)),
            pygments.lexers.JavascriptLexer(),
            pygments.formatters.HtmlFormatter(**html_args)
        )

        code = code.strip()

        fedmsg.publish(
            topic=destination_topic,
            msg=code,
            modname="busmon",
        )
