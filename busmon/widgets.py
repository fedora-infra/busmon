
import collections
import moksha.api.widgets.live
import tw2.d3

class TopicsBarChart(tw2.d3.BarChart, moksha.api.widgets.live.LiveWidget):
    id = 'topics-bar-chart'
    topic = "*"  # zmq_strict = False :D
    onmessage = "console.log(json);"  # TODO -- make barchart flip out.

    data = collections.OrderedDict()  # empty

    width = 400
    height = 200

