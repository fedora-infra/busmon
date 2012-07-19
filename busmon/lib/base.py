# -*- coding: utf-8 -*-
"""The base Controller API."""

from tg import TGController, tmpl_context
from tg import config

import moksha.api.widgets

__all__ = ['BaseController']

class BaseController(TGController):
    def __call__(self, environ, start_response):
        tmpl_context.moksha_socket = \
            moksha.api.widgets.get_moksha_socket(config)
        return TGController.__call__(self, environ, start_response)
