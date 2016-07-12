#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Brazilian territorial distribution data exporter

The MIT License (MIT)

Copyright (c) 2013-2016 Paulo Freitas

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''
# -- Metadata -----------------------------------------------------------------

__author__ = 'Paulo Freitas <me@paulofreitas.me>'
__copyright__ = 'Copyright (c) 2013-2016 Paulo Freitas'
__license__ = 'MIT'
__version__ = '1.0-dev'
__usage__ = '%(prog)s -b BASE -f FORMAT [-m] [-o FILENAME]'
__epilog__ =\
    'Report bugs and feature requests to https://github.com/paulofreitas/dtb-ibge/issues.'

# -- Imports ------------------------------------------------------------------

# Built-in modules

import argparse
import sys

# Package modules

import exporters
import parsers

from core.entities import Database, DTB

if __name__ == '__main__':
    # -- Logging initialization -----------------------------------------------

    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] %(message)s', '%H:%M:%S'
    )
    log_handler = logging.StreamHandler(sys.stdout)
    log_handler.setFormatter(formatter)
    logger = logging.getLogger('dtb')
    logger.addHandler(log_handler)

    # CLI parser
    parser = argparse.ArgumentParser(
        description=__doc__,
        usage=__usage__,
        epilog=__epilog__,
        conflict_handler='resolve',
        formatter_class=argparse.RawTextHelpFormatter
    )
    g_global = parser.add_argument_group('Global options')
    g_global.add_argument(
        '-h', '--help',
        action='help',
        help='Display this information'
    )
    g_global.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s ' + __version__,
        help='Show version information and exit'
    )
    g_global.add_argument(
        '-V', '--verbose',
        action='store_true',
        help='Display informational messages and warnings'
    )

    g_export = parser.add_argument_group('Export options')
    g_export.add_argument(
        '-b', '--base',
        type=int,
        help='Database year to export to.'
    )
    g_export.add_argument(
        '-f', '--format',
        metavar='FORMAT',
        choices=exporters.FORMATS.keys(),
        help='Format to export the database.\nOptions: %(choices)s'
    )
    g_export.add_argument(
        '-m', '--minify',
        dest='minified',
        action='store_true',
        help='Minifies output file whenever possible.'
    )
    g_export.add_argument(
        '-o', '--out',
        dest='filename',
        nargs='?',
        const='auto',
        help='Specify a file to write the export to.\n'
        + 'If none are specified, %(prog)s writes data to standard output.'
    )
    args = parser.parse_args()

    if not args.base:
        parser.error(
            'You need to specify the database year you want to export.'
        )

    if not args.format:
        parser.error(
            'You need to specify the database format you want to export.'
        )

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    try:
        dtb = DTB(args.base, logger)
        dtb.get_db().export_db(args.format, args.minified, args.filename)
    except Exception as e:
        sys.stdout.write(
            'EXCEPTION CAUGHT: {}: {}\n'.format(type(e).__name__, e.message)
        )
        sys.exit(1)
