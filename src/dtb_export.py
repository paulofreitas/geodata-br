#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Brazilian territorial distribution data exporter

The MIT License (MIT)

Copyright (c) 2013 Paulo Freitas

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
# -- Imports ------------------------------------------------------------------

import exporters
import parsers

# Built-in modules

import argparse
import fnmatch
import ftplib
import io
import logging
import os
import sys
import zipfile

# -- Module docstrings --------------------------------------------------------

__author__ = 'Paulo Freitas <me@paulofreitas.me>'
__copyright__ = 'Copyright (c) 2013-2015 Paulo Freitas'
__license__ = 'MIT'
__version__ = '1.0-dev'
__usage__ = '%(prog)s -b BASE -f FORMAT [-m] [-o FILENAME]'
__epilog__ =\
    'Report bugs and feature requests to https://github.com/paulofreitas/dtb-ibge/issues.'

# -- Module initialization ----------------------------------------------------

formatter = logging.Formatter(
    '[%(asctime)s] [%(levelname)s] %(message)s', '%H:%M:%S'
)
log_handler = logging.StreamHandler(sys.stdout)
log_handler.setFormatter(formatter)
logger = logging.getLogger('dtb')
logger.addHandler(log_handler)

# -- Classes ------------------------------------------------------------------


class Database(object):
    _tables = (
        'uf',
        'mesorregiao',
        'microrregiao',
        'municipio',
        'distrito',
        'subdistrito'
    )
    _fields = {
        'uf': (
            'id',
            'nome'
        ),
        'mesorregiao': (
            'id',
            'id_uf',
            'nome'
        ),
        'microrregiao': (
            'id',
            'id_mesorregiao',
            'id_uf',
            'nome'
        ),
        'municipio': (
            'id',
            'id_microrregiao',
            'id_mesorregiao',
            'id_uf',
            'nome'
        ),
        'distrito': (
            'id',
            'id_municipio',
            'id_microrregiao',
            'id_mesorregiao',
            'id_uf',
            'nome'
        ),
        'subdistrito': (
            'id',
            'id_distrito',
            'id_municipio',
            'id_microrregiao',
            'id_mesorregiao',
            'id_uf',
            'nome'
        )
    }
    _cols = []
    _rows = []
    _data = {}
    _rawdata = None

    def __init__(self, base):
        self._base = str(base)
        self._name = 'dtb_{}'.format(self._base)

        for table_name in self._tables:
            self._cols.append('id_' + table_name)
            self._cols.append('nome_' + table_name)
            self._data[table_name] = []


class DTB(object):
    def __init__(self, base):
        self._db = Database(base)

    def _download_db(self):
        ftp = ftplib.FTP('geoftp.ibge.gov.br')
        logger.debug('Connecting to FTP server...')
        ftp.connect()
        logger.debug('Logging into the FTP server...')
        ftp.login()
        ftp.cwd('organizacao_territorial/divisao_territorial')

        bases_available = [item for item in ftp.nlst() if item.isdigit()]

        if self._db._base not in bases_available:
            raise Exception('This base is not available to download.')

        ftp.cwd(self._db._base)
        zip_filename = fnmatch.filter(
            ftp.nlst(),
            'dtb_*{}.zip'.format(self._db._base)
        )[0]
        zip_data = io.BytesIO()
        logger.info('Retrieving database...')
        ftp.retrbinary('RETR {}'.format(zip_filename), zip_data.write)
        xls_file = io.BytesIO()

        with zipfile.ZipFile(zip_data, 'r') as zip_file:
            logger.info('Reading database...')
            xls_file.write(zip_file.open(zip_file.namelist()[0]).read())

        return xls_file

    def get_db(self, cacheFiles=True):
        xls_file = io.BytesIO()

        if cacheFiles:
            temp_dir = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                '.cache'
            )
            temp_file = os.path.join(temp_dir, self._db._base)

            if not os.path.exists(temp_file):
                xls_file = self._download_db()

                try:
                    os.makedirs(temp_dir)
                except OSError:
                    pass

                open(temp_file, 'wb').write(xls_file.getvalue())
            else:
                xls_file.write(open(temp_file, 'rb').read())
        else:
            xls_file = self._download_db()

        self._db._rawdata = xls_file.getvalue()

        return self

    def export_db(self, format, minified=False, filename=None):
        self._db = parsers.XLS(self._db).parse()

        if format not in FORMATS:
            raise Exception('Unsupported output format.')

        exporter = dict(
            (exporter._format, exporter) for exporter in EXPORTERS
        )[format]
        logger.info(
            'Exporting database to {} format...'.format(exporter.__name__)
        )
        data = str(exporter(self._db, minified))
        logger.info('Done.')

        if filename:
            if filename == 'auto':
                filename = 'dtb' + exporter._extension

            open(filename, 'w').write(data)
        else:
            sys.stdout.write(data)


class Struct(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value

    def copy(self):
        return Struct(dict.copy(self))

# -- Module constants ---------------------------------------------------------

EXPORTERS = (
    exporters.CSV,
    exporters.JSON,
    exporters.PHP,
    exporters.plist,
    exporters.SQL,
    exporters.SQLite3,
    exporters.XML,
    exporters.YAML
)
FORMATS = tuple(exporter._format for exporter in EXPORTERS)

if __name__ == '__main__':
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
        choices=FORMATS,
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
        dtb = DTB(args.base)
        dtb.get_db() \
            .export_db(args.format, args.minified, args.filename)
    except Exception as e:
        sys.stdout.write(
            'EXCEPTION CAUGHT: {}: {}\n'.format(type(e).__name__, e.message)
        )
        sys.exit(1)
