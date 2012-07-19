# -*- coding: utf-8 -*-
"""
Global configuration file for TG2-specific settings in busmon.

This file complements development/deployment.ini.

Please note that **all the argument values are strings**. If you want to
convert them into boolean, for example, you should use the
:func:`paste.deploy.converters.asbool` function, as in::

    from paste.deploy.converters import asbool
    setting = asbool(global_conf.get('the_setting'))

"""

from tg.configuration import AppConfig

import busmon
from busmon.lib import app_globals, helpers

base_config = AppConfig()
base_config.renderers = []

base_config.package = busmon

#Enable json in expose
base_config.renderers.append('json')
#Set the default renderer
base_config.default_renderer = 'mako'
base_config.renderers.append('mako')
#Configure the base SQLALchemy Setup
base_config.use_sqlalchemy = False


base_config.use_toscawidgets=False
base_config.use_toscawidgets2=True
