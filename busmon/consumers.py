import pygments.lexers
import pygments.formatters
from moksha.api.hub import Consumer

import fedmsg
import fedmsg.json


class MessageColorizer(Consumer):
    app = "busmon"
    topic = "*"
    destination_topic = "colorized-messages"
    jsonify = False

    def consume(self, message):
        if self.destination_topic in message.topic:
            return

        html_args = {'full': False}
        code = pygments.highlight(
            fedmsg.json.pretty_dumps(fedmsg.json.loads(message.body)),
            pygments.lexers.JavascriptLexer(),
            pygments.formatters.HtmlFormatter(**html_args)
        )

        code = code.strip()

        fedmsg.send_message(
            topic=self.destination_topic,
            msg=code,
        )
