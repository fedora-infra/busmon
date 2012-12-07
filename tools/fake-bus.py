#!/usr/bin/env python
""" This script just emits a bunch of random messages on an endpoint to which
busmon is listening.  Run it while busmon is running to provide it with fake
test data.

    :author: Ralph Bean <rbean@redhat.com>

"""

import random
import time
import socket

import fedmsg

# Clearly,
FACTOR = 100

hostname = socket.gethostname()


def main():
    # Prepare our context and publisher
    fedmsg.init(name="bodhi.%s" % hostname)

    # Probabilities of us emitting an event on each topic.
    probs = {
        'bodhi': 0.015 * FACTOR,
        'fedoratagger': 0.001 * FACTOR,
        'pkgdb': 0.001 * FACTOR,
        'fas': 0.005 * FACTOR,
        'mediawiki': 0.01 * FACTOR,
        'git': 0.01 * FACTOR,
    }

    # Main loop
    i = 0
    while True:
        for service, thresh in probs.iteritems():
            if random.random() < thresh:
                print service, thresh
                fedmsg.send_message(
                    topic='fake_data',
                    msg={'test': "Test data." + str(i)},
                    modname=service,
                )
                i = i + 1
        time.sleep(random.random())

if __name__ == "__main__":
    main()
