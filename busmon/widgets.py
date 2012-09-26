
import tg
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

import moksha.wsgi.widgets.api.live

import tw2.core as twc
import tw2.d3
from tw2.jquery import jquery_js

global_width = 485


class BusmonWidget(moksha.wsgi.widgets.api.live.LiveWidget):
    resources = [
        twc.JSLink(link="javascript/busmon.js", resources=[jquery_js]),
    ]
    backend = tg.config.get('moksha.livesocket.backend', 'websocket')


class TopicsBarChart(tw2.d3.BarChart, BusmonWidget):
    id = 'topics-bar-chart'
    topic = "*"  # zmq_strict = False :D
    onmessage = """busmon.filter(function() {
        if (! json['topic']) { return; }
        topic = json['topic'].split('.').slice(3).join('.')
        tw2.d3.util.bump_value('${id}', topic, 1);
    }, json)"""

    data = OrderedDict()  # empty

    padding = [30, 10, 10, global_width / 2]
    width = global_width
    height = 225
    interval = 2000

    def prepare(self):
        super(TopicsBarChart, self).prepare()
        self.add_call(twc.js_function('tw2.d3.bar.schedule_halflife')(
            self.attrs['id'],
            60000,  # Halflife of one minute.
            1000,
            0.001,
        ))


class MessagesTimeSeries(tw2.d3.TimeSeriesChart, BusmonWidget):
    id = 'messages-time-series'
    topic = "*"
    onmessage = """busmon.filter(function() {
        tw2.store['${id}'].value++;
    }, json)"""

    width = global_width
    height = 150

    # Keep this many data points
    n = 200
    # Initialize to n zeros
    data = [0] * n


class ColorizedMessagesWidget(BusmonWidget):
    id = 'colorized-messages'
    template = "mako:busmon.templates.colorized_messages"
    resources = BusmonWidget.resources + [twc.CSSLink(link="css/monokai.css")]
    css_class = "hll"

    topic = 'org.fedoraproject.{env}.busmon.colorized-messages'.format(
        env=tg.config.get("fedmsg.environment")
    )

    onmessage = """busmon.filter_content(function() {
        var container = $('#${id}');
        if ( container.children().size() > 4 ) {
            container.children().first().slideUp(100, function () {
                $(this).remove();
                container.append(json.msg);
            });
        } else {
            container.append(json.msg);
        }
    }, json)"""
