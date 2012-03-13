
import collections

import moksha.api.widgets.live

import tw2.core as twc
import tw2.d3

class TopicsBarChart(tw2.d3.BarChart, moksha.api.widgets.live.LiveWidget):
    id = 'topics-bar-chart'
    topic = "*"  # zmq_strict = False :D
    onmessage = """
    tw2.d3.util.bump_value('${id}', json['topic'], 1);
    """

    data = collections.OrderedDict()  # empty

    padding = [30, 10, 10, 120]
    width = 400
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
