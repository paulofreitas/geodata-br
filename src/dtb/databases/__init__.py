#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2016 Paulo Freitas
# MIT License (see LICENSE file)
'''
Databases package

This package provides a database class.
'''
from __future__ import absolute_import, unicode_literals

# Imports

# Built-in dependencies

import ftplib
import io
import sys
import zipfile

from io import open
from os import makedirs
from os.path import basename, dirname, exists, join as path

# External dependencies

import yaml

# Package dependencies

from dtb.core.constants import PKG_DIR, SRC_DIR
from dtb.core.entities import TerritorialData
from dtb.core.types import Bytes, Struct
from dtb.exporters import ExporterFactory
from dtb.parsers import ParserFactory

# Package metadata

__version__ = '1.0-dev'
__author__ = 'Paulo Freitas <me@paulofreitas.me>'
__copyright__ = 'Copyright (c) 2013-2016 Paulo Freitas'
__license__ = 'MIT License'

# Constants

BASE_LIST = path(PKG_DIR, 'data/bases.yaml')

# Classes


class Database(object):
    '''Database class.'''
    base_list = dict((str(database['year']), database)
                     for database in yaml.load(open(BASE_LIST)))
    bases = tuple(reversed(sorted(base_list.keys())))

    def __init__(self, year, logger):
        if year not in self.bases:
            raise Exception('This base is not available to download.')

        self._info = Struct(self.base_list.get(year))
        self._data = TerritorialData(self._info)
        self._logger = logger

    @property
    def year(self):
        '''The database year.'''
        return str(self._info.year)

    @property
    def archive(self):
        '''The database archive, if any.'''
        return self._info.get('archive')

    @property
    def file(self):
        '''The database file.'''
        return self._info.file

    @property
    def format(self):
        '''The database format.'''
        return self._info.format

    @property
    def sheet(self):
        '''The database sheet, if any.'''
        return self._info.get('sheet')

    @property
    def cacheFile(self):
        '''The cached database file.'''
        return path(SRC_DIR, '.cache', '{}.{}'.format(self.year, self.format))

    def download(self):
        '''Downloads the given database.'''
        ftp = ftplib.FTP('geoftp.ibge.gov.br')
        archive_data = io.BytesIO()
        base_data = io.BytesIO()

        self._logger.debug('Connecting to FTP server...')
        ftp.connect()

        self._logger.debug('Logging into the FTP server...')
        ftp.login()
        ftp.cwd(path('organizacao_do_territorio',
                     'estrutura_territorial',
                     'divisao_territorial',
                     self.year))

        self._logger.info('Retrieving database...')

        if self.archive:
            ftp.retrbinary('RETR {}'.format(basename(self.archive)),
                           archive_data.write)

            with zipfile.ZipFile(archive_data, 'r') as archive_file:
                self._logger.info('Reading database...')

                with archive_file.open(self.file, 'r') as base_file:
                    base_data.write(base_file.read())
        else:
            ftp.retrbinary('RETR {}'.format(self.file), base_data.write)

        try:
            makedirs(dirname(self.cacheFile))
        except OSError:
            pass

        with open(self.cacheFile, 'wb') as cache_file:
            cache_file.write(base_data.getvalue())

        return self

    def read(self):
        '''Reads the given database.

        Returns:
            dtb.core.types.Bytes: The database raw binary data
        '''
        if not exists(self.cacheFile):
            self.download()

        with open(self.cacheFile, 'rb') as cache_file:
            base_data = cache_file.read()

        return Bytes(base_data)

    def parse(self):
        '''Parses the given database.'''
        parser = ParserFactory.fromFormat(self.format)

        try:
            self._data = parser(self, self._logger).parse()
        except:
            raise Exception('Failed to parse data using the given parser')

        return self

    def export(self, _format, minified=False, filename=None):
        '''Exports the given database.

        Arguments:
            _format: The file format to export the database
            minified (bool): Whether or not the exported file should be minified
            filename (str): The exported filename
        '''
        exporter = ExporterFactory.fromFormat(_format)
        export_format = exporter._format()

        if minified:
            self._logger.info('Exporting database to minified {} format...' \
                .format(export_format.friendlyName))
        else:
            self._logger.info('Exporting database to {} format...' \
                .format(export_format.friendlyName))

        data = exporter(self._data, minified).data

        if not export_format.isBinary() and not isinstance(data, unicode):
            data = unicode(data.decode('utf-8'))

        self._logger.debug('Done.')

        if filename:
            if filename == 'auto':
                filename = 'dtb' + export_format.extension

            writeMode = 'wb' if export_format.isBinary() else 'w'

            with open(filename, writeMode) as export_file:
                export_file.write(data)
        else:
            sys.stdout.write(data)
