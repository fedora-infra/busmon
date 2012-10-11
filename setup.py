# -*- coding: utf-8 -*-
#quckstarted Options:
#
# sqlalchemy: True
# auth:       None
# mako:       True
#
#

import sys

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

testpkgs=['WebTest >= 1.2.3',
               'nose',
               'coverage',
               'wsgiref',
               'repoze.who-testutil >= 1.0.1',
               ]
install_requires=[
    "Pylons<=1.0",
    "WebOb<=1.1.1",
    "TurboGears2",
    "PasteDeploy",
    "Mako",
    "repoze.tm2 == 1.0a4",
    "tw2.d3>=0.0.5",
    "moksha.wsgi",
    "tg.devtools",
    "tw2.core",
    "tw2.forms",
    "python-memcached",
    ]

if sys.version_info[:2] == (2,4):
    testpkgs.extend(['hashlib'])
    install_requires.extend(['hashlib'])

if sys.version_info[0] == 2 and sys.version_info[1] <= 6:
    install_requires.extend([
        'ordereddict',
    ])

setup(
    name='busmon',
    version='0.4.6',
    description='A webapp for visualizing activity on the Fedora Message Bus.',
    author='Ralph Bean',
    author_email='rbean@redhat.com',
    url='http://github.com/ralphbean/busmon',
    license='GPLv2+',
    setup_requires=["PasteScript >= 1.7"],
    paster_plugins=['PasteScript', 'Pylons', 'TurboGears2', 'tg.devtools'],
    packages=find_packages(exclude=['ez_setup']),
    install_requires=install_requires,
    include_package_data=True,
    test_suite='nose.collector',
    tests_require=testpkgs,
    package_data={'busmon': ['i18n/*/LC_MESSAGES/*.mo',
                                 'templates/*/*',
                                 #'public/*/*',
                            ]},
    message_extractors={'busmon': [
            ('**.py', 'python', None),
            ('templates/**.mako', 'mako', None),
            ('public/**', 'ignore', None)]},

    entry_points={
        'paste.app_factory': (
            'main = busmon.config.middleware:make_app',
        ),
        'paste.app_install': (
            'main = pylons.util:PylonsInstaller',
        ),
        'moksha.widget': (
            'topics_bar = busmon.widgets:TopicsBarChart',
            'messages_series = busmon.widgets:MessagesTimeSeries',
            'colorized_msgs = busmon.widgets:ColorizedMessagesWidget',
        ),
        'tw2.widgets': (
            # FIXME -- this is a hack until the following is resolved
            # https://fedorahosted.org/moksha/ticket/247
            "moksha_js = moksha.widgets.moksha_js",
            # FIXME -- I dunno whats up with this one
            "gritter_js = tw2.jqplugins.gritter.base",
        ),
    },
    dependency_links=[
        "http://www.turbogears.org/2.1/downloads/current/"
        ],
    zip_safe=False
)
