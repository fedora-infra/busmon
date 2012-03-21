#!/usr/bin/env python
import random
import time
import zmq
import simplejson

# TODO -- have this use fedmsg.

def main():
    """ main method """

    # Prepare our context and publisher
    context = zmq.Context(1)
    publisher = context.socket(zmq.PUB)
    publisher.bind("tcp://*:6543")
    time.sleep(1)

    # Probabilities of us emitting an event on each topic.
    probs = {
        'koji': 0.35,
        'bodhi': 0.2,
        'pkgdb': 0.1,
        'fas': 0.2,
        'autoqa': 0.3,
        'tagger': 0.6,
    }

    i = 0
    while True:
        for topic, thresh in probs.iteritems():
            if random.random() < thresh:
                publisher.send_multipart(
                    [topic, simplejson.dumps({
                        'topic': topic, 'msg': "We" + str(i)
                    })]
                )
        time.sleep(random.random())
        i = i + 1

    # We never get here but clean up anyhow
    publisher.close()
    context.term()

if __name__ == "__main__":
    main()
