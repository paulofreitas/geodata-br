#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""Brazilian geographic data exporter package."""
# Package imports

from pkg_resources import resource_string

# Constants

VERSION = (18, 6, 'dev0')  # CalVer YY.MM[.ID] (see https://calver.org/)

# Package metadata

__package_name__ = 'geodatabr'
__description__ = 'Brazilian geographic data exporter'
__version__ = '.'.join(map(str, VERSION))
__copyright__ = 'Copyright (c) 2013-2018 Paulo Freitas'
__license__ = 'MIT'
__url__ = 'https://github.com/paulofreitas/geodata-br'
__author_name__ = 'Paulo Freitas'
__author_email__ = 'me@paulofreitas.me'
__author__ = '{0} <{1}>'.format(__author_name__, __author_email__)
__prolog__ = '{0}, version {1}\n{2}' \
             .format(__package_name__, __version__, __copyright__)
__epilog__ = 'Report bugs and feature requests to <{0}>.' \
             .format(__url__ + '/issues')

try:
    __license_text__ = resource_string(__name__, 'LICENSE').decode()
except RuntimeError:
    __license_text__ = ''
