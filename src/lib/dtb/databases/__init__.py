#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2016 Paulo Freitas
# MIT License (see LICENSE file)
'''
Databases package

This package provides a database class, a database factory class and a database
repository class.
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
from os.path import dirname, exists, join as path

# Package dependencies

from dtb.core.constants import SRC_DIR
from dtb.core.entities import TerritorialData
from dtb.core.logging import Logger
from dtb.core.types import Bytes, Struct
from dtb.exporters import ExporterFactory
from dtb.parsers import ParserFactory

# Package metadata

__version__ = '1.0-dev'
__author__ = 'Paulo Freitas <me@paulofreitas.me>'
__copyright__ = 'Copyright (c) 2013-2016 Paulo Freitas'
__license__ = 'MIT License'

# Module logging

logger = Logger.instance(__name__)

# Constants

BASE_LIST = [
    Struct(year=2014,
           archive='dtb_2014_v2.zip',
           file='DTB_2014_v2/DTB_2014_subdistrito.xls',
           format='xls',
           sheet='Plan1'),
    Struct(year=2013,
           archive='dtb_2013.zip',
           file='dtb_2013.xls',
           format='xls',
           sheet='dtb_2013'),
    Struct(year=2012,
           archive='dtb_2012.zip',
           file='dtb_2012.xls',
           format='xls',
           sheet='Estrutura_2012___Município'),
    Struct(year=2011,
           archive='dtb_2011.zip',
           file='dtb_2011.xls',
           format='xls',
           sheet='DTB_2011'),
    Struct(year=2010,
           archive='dtb_2010.zip',
           file='dtb_2010.xls',
           format='xls',
           sheet='Município'),
    Struct(year=2009,
           archive='dtb_05_05_2009.zip',
           file='DTB_05_05_2009.xls',
           format='xls',
           sheet='DTB_05_05_2009n'),
    Struct(year=2008,
           archive='dtb_2008.zip',
           file='DTB_2008.xls',
           format='xls',
           sheet='DTB_Nome_Comum'),
    Struct(year=2007,
           archive='dtb_2007.zip',
           file='DTB_2007.xls',
           format='xls',
           sheet='DTB_Nome_Comum'),
    Struct(year=2006,
           archive='dtb_2006.zip',
           file='DTB_2006.xls',
           format='xls',
           sheet='Completo'),
    Struct(year=2005,
           archive='dtb_2005.zip',
           file='DTB_2005.xls',
           format='xls',
           sheet='NomeNormal'),
    Struct(year=2003,
           archive='dtb17112003nome.zip',
           file='DTB17112003nome.xls',
           format='xls',
           sheet='DTBnome'),
]

# Classes


class Database(object):
    '''Database class.'''

    def __init__(self, info):
        '''Constructor.

        Arguments:
            info (Struct): The database info
        '''
        self._info = info
        self._data = TerritorialData(self._info)

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

        logger.debug('Connecting to FTP server...')
        ftp.connect()

        logger.debug('Logging into the FTP server...')
        ftp.login()
        ftp.cwd(path('organizacao_do_territorio',
                     'estrutura_territorial',
                     'divisao_territorial',
                     self.year))

        logger.info('Retrieving database...')

        if self.archive:
            ftp.retrbinary('RETR {}'.format(self.archive), archive_data.write)

            with zipfile.ZipFile(archive_data, 'r') as archive_file:
                logger.info('Reading database...')

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

        #try:
        self._data = parser(self).parse()
        #except:
        #    raise Exception('Failed to parse data using the given parser')

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
            logger.info('Exporting database to minified {} format...' \
                .format(export_format.friendlyName))
        else:
            logger.info('Exporting database to {} format...' \
                .format(export_format.friendlyName))

        data = exporter(self._data, minified).data

        if not export_format.isBinary() and not isinstance(data, unicode):
            data = unicode(data.decode('utf-8'))

        logger.debug('Done.')

        if filename:
            if filename == 'auto':
                filename = 'dtb' + export_format.extension

            writeMode = 'wb' if export_format.isBinary() else 'w'

            with open(filename, writeMode) as export_file:
                export_file.write(data)
        else:
            sys.stdout.write(data)


class DatabaseFactory(object):
    '''Database factory class.'''

    @classmethod
    def fromYear(cls, year):
        '''Factories a database class for a given database year.

        Arguments:
            year (int): The database year to retrieve a database object

        Raises:
            UnknownDatabaseError: If no database is found with the given year
        '''
        return DatabaseRepository.findByYear(year)


class DatabaseRepository(object):
    '''Database repository class.'''

    @staticmethod
    def findByYear(year):
        '''Returns the database for the given year.

        Arguments:
            year (int): The database year

        Raises:
            UnknownDatabaseError: If no database is found with the given year
        '''
        for database_info in BASE_LIST:
            if database_info.year == int(year):
                return Database(database_info)

        raise UnknownDatabaseError('This base is not available: {}' \
                                       .format(year))

    @staticmethod
    def listYears():
        '''Returns a list with all database years.'''
        return [str(database.year) for database in BASE_LIST]


class DatabaseError(Exception):
    '''Generic exception class for database errors.'''
    pass


class UnknownDatabaseError(DatabaseError):
    '''Exception class raised when a given database is not found.'''
    pass
