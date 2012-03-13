
from moksha.api.hub import Consumer

class BusmonConsumer(Consumer):

    app = "busmon"  # hopefully this won't be necessary anymore
    topic = "*"
    jsonify = False

    def consumer(self, message):
        # We may not actually need this.
        pass
