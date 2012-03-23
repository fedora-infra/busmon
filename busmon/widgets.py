
import collections

import moksha.api.widgets.live

import tw2.core as twc
import tw2.d3

global_width = 940


class TopicsBarChart(tw2.d3.BarChart, moksha.api.widgets.live.LiveWidget):
    id = 'topics-bar-chart'
    topic = "*"  # zmq_strict = False :D
    onmessage = "tw2.d3.util.bump_value('${id}', json['topic'], 1);"

    data = collections.OrderedDict()  # empty

    padding = [30, 10, 10, 120]
    width = global_width
    height = 200
    interval = 2000

    def prepare(self):
        super(TopicsBarChart, self).prepare()
        self.add_call(twc.js_function('tw2.d3.bar.schedule_halflife')(
            self.attrs['id'],
            2000,
            1000,
            0.001,
        ))


class MessagesTimeSeries(tw2.d3.TimeSeriesChart,
                        moksha.api.widgets.live.LiveWidget):
    id = 'messages-time-series'
    topic = "*"
    onmessage = "tw2.store['${id}'].value++"

    width = global_width
    height = 200

    # Keep this many data points
    n = 400
    # Initialize to n zeros
    data = [0] * n


class ColorizedMessagesWidget(moksha.api.widgets.live.LiveWidget):
    id = 'colorized-messages'
    template = "mako:busmon.templates.colorized_messages"
    resources = [twc.CSSLink(link="css/monokai.css")]
    css_class = "hll"

    topic = 'org.fedoraproject.busmon.colorized-messages'
    onmessage = """
    var container = $('#${id}');
    if ( container.children().size() > 15 ) {
        container.children().first().remove();
    }
    container.append(json.msg);
    """
