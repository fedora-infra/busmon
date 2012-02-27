# -*- coding: utf-8 -*-
"""Setup the busmon application"""

import logging
from tg import config
from busmon import model
import transaction

def bootstrap(command, conf, vars):
    """Place any commands to setup busmon here"""

    # <websetup.bootstrap.before.auth

    # <websetup.bootstrap.after.auth>
