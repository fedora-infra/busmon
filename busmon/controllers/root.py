# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import expose

from busmon.lib.base import BaseController
from busmon.controllers.error import ErrorController

from busmon.widgets import (
    TopicsBarChart,
    MessagesTimeSeries,
    ColorizedMessagesWidget,
)

__all__ = ['RootController']


class RootController(BaseController):
    error = ErrorController()

    @expose('busmon.templates.index')
    def index(self):
        """Handle the front-page."""
        return dict(
            barchart=TopicsBarChart,
            timeseries=MessagesTimeSeries,
            colorized_messages=ColorizedMessagesWidget,
        )
