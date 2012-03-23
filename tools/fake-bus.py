#!/usr/bin/env python
""" This script just emits a bunch of random messages on an endpoint to which
busmon is listening.  Run it while busmon is running to provide it with fake
test data.

    :author: Ralph Bean <rbean@redhat.com>

"""

import random
import time
import simplejson

import fedmsg
import fedmsg.schema


def main():
    # Prepare our context and publisher
    fedmsg.init(publish_endpoint="tcp://*:5432")

    # Probabilities of us emitting an event on each topic.
    probs = {
        'koji': 0.35,
        'bodhi': 0.2,
        'pkgdb': 0.1,
        'fas': 0.2,
        'autoqa': 0.3,
        'tagger': 0.6,
    }

    # Main loop
    i = 0
    while True:
        for service, thresh in probs.iteritems():
            if random.random() < thresh:
                print service, thresh
                fedmsg.send_message(
                    topic='fake_data',
                    msg={fedmsg.schema.TEST: "Test data."},
                    modname=service,
                )
        time.sleep(random.random())
        i = i + 1

if __name__ == "__main__":
    main()
