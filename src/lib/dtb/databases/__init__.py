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
import zipfile

# Package dependencies

from dtb.core.constants import SRC_DIR
from dtb.core.helpers.decorators import classproperty
from dtb.core.helpers.filesystem import Directory, File, Path
from dtb.core.logging import Logger
from dtb.core.types import Bytes, Map
from dtb.databases.entities import Entities, LegacyEntities, DatabaseData
from dtb.exporters import ExporterFactory
from dtb.parsers import ParserFactory

# Package metadata

__version__ = '1.0-dev'
__author__ = 'Paulo Freitas <me@paulofreitas.me>'
__copyright__ = 'Copyright (c) 2013-2016 Paulo Freitas'
__license__ = 'MIT License'

# Module logging

logger = Logger.instance(__name__)

# Classes


class Database(object):
    '''
    Database class.
    '''

    def __init__(self, **info):
        '''
        Constructor.

        Arguments:
            info (dict): The database info
        '''
        self._info = Map(info)
        self._data = None

    @property
    def year(self):
        '''
        The database year.
        '''
        return str(self._info.year)

    @property
    def archive(self):
        '''
        The database archive, if any.
        '''
        return self._info.get('archive')

    @property
    def file(self):
        '''
        The database file.
        '''
        return self._info.file

    @property
    def format(self):
        '''
        The database format.
        '''
        return self._info.format

    @property
    def sheet(self):
        '''
        The database sheet, if any.
        '''
        return self._info.get('sheet')

    @property
    def entities(self):
        '''
        The database entities.
        '''
        return self._info.get('entities', Entities)

    @property
    def cacheFile(self):
        '''
        The cached database file.
        '''
        return Path(SRC_DIR, '.cache', '{}.{}'.format(self.year, self.format))

    def download(self):
        '''
        Downloads the given database.
        '''
        ftp = ftplib.FTP('geoftp.ibge.gov.br')
        archive_data = io.BytesIO()
        base_data = io.BytesIO()

        logger.debug('Connecting to FTP server...')
        ftp.connect()

        logger.debug('Logging into the FTP server...')
        ftp.login()
        ftp.cwd(str(Path('organizacao_do_territorio',
                         'estrutura_territorial',
                         'divisao_territorial',
                         self.year)))

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
            Directory(self.cacheFile.parent).create()
        except OSError:
            pass

        with self.cacheFile.open('wb') as cache_file:
            cache_file.write(base_data.getvalue())

        return self

    def read(self):
        '''
        Reads the given database.

        Returns:
            dtb.core.types.Bytes: The database raw binary data
        '''
        if not self.cacheFile.exists():
            self.download()

        base_data = File(self.cacheFile).readBytes()

        return Bytes(base_data)

    def parse(self, **options):
        '''
        Parses the given database.

        Arguments:
            options (dict): The parsing options

        Raises:
            ParseError: When database fails to parse
        '''
        parser = ParserFactory.fromFormat(self.format)

        self._data = parser(self).parse(**options)

        return self

    def export(self, _format, filename, **options):
        '''
        Exports the given database.

        Arguments:
            _format: The file format to export the database
            filename (str): The filename to write
            options (dict): The exporting options

        Raises:
            ExportError: When database fails to export
        '''
        exporter = ExporterFactory.fromFormat(_format, self._data)

        return exporter.exportToFile(filename, **options)


class DatabaseFactory(object):
    '''
    Database factory class.
    '''

    @classmethod
    def fromYear(cls, year):
        '''
        Factories a database class for a given database year.

        Arguments:
            year (int): The database year to retrieve a database object

        Raises:
            UnknownDatabaseError: If no database is found with the given year
        '''
        return DatabaseRepository.findByYear(year)


class DatabaseRepository(object):
    '''
    Database repository class.
    '''

    @staticmethod
    def findAll():
        '''
        Returns a list with all available databases.

        Returns:
            list: A list with all available atabases
        '''
        return [
            Database(year=2014,
                     archive='dtb_2014_v2.zip',
                     file='DTB_2014_v2/DTB_2014_subdistrito.xls',
                     format='xls',
                     sheet='Plan1'),
            Database(year=2013,
                     archive='dtb_2013.zip',
                     file='dtb_2013.xls',
                     format='xls',
                     sheet='dtb_2013'),
            Database(year=2012,
                     archive='dtb_2012.zip',
                     file='dtb_2012.xls',
                     format='xls',
                     sheet='Estrutura_2012___Município'),
            Database(year=2011,
                     archive='dtb_2011.zip',
                     file='dtb_2011.xls',
                     format='xls',
                     sheet='DTB_2011'),
            Database(year=2010,
                     archive='dtb_2010.zip',
                     file='dtb_2010.xls',
                     format='xls',
                     sheet='Município'),
            Database(year=2009,
                     archive='dtb_05_05_2009.zip',
                     file='DTB_05_05_2009.xls',
                     format='xls',
                     sheet='DTB_05_05_2009n'),
            Database(year=2008,
                     archive='dtb_2008.zip',
                     file='DTB_2008.xls',
                     format='xls',
                     sheet='DTB_Nome_Comum'),
            Database(year=2007,
                     archive='dtb_2007.zip',
                     file='DTB_2007.xls',
                     format='xls',
                     sheet='DTB_Nome_Comum'),
            Database(year=2006,
                     archive='dtb_2006.zip',
                     file='DTB_2006.xls',
                     format='xls',
                     sheet='Completo'),
            Database(year=2005,
                     archive='dtb_2005.zip',
                     file='DTB_2005.xls',
                     format='xls',
                     sheet='NomeNormal'),
            Database(year=2003,
                     archive='dtb17112003nome.zip',
                     file='DTB17112003nome.xls',
                     format='xls',
                     sheet='DTBnome'),
            Database(year=1980,
                     file='h_dtb_1980.xls',
                     format='xls',
                     sheet='H__DTB___1980',
                     entities=LegacyEntities),
            Database(year=1970,
                     file='g_dtb_1970.xls',
                     format='xls',
                     sheet='G__DTB___1970',
                     entities=LegacyEntities),
            Database(year=1960,
                     file='f_dtb_1960.xls',
                     format='xls',
                     sheet='F__DTB___1960',
                     entities=LegacyEntities),
            Database(year=1950,
                     file='e_dtb_1950.xls',
                     format='xls',
                     sheet='E__DTB___1950',
                     entities=LegacyEntities),
            Database(year=1940,
                     file='d_dtb_1940.xls',
                     format='xls',
                     sheet='D__DTB___1940',
                     entities=LegacyEntities),
        ]

    @classmethod
    def findByYear(cls, year):
        '''
        Returns the database for the given year.

        Arguments:
            year (int): The database year

        Returns:
            Database: The database instance for the given year

        Raises:
            UnknownDatabaseError: If no database is found with the given year
        '''
        for database in cls.findAll():
            if database.year == year:
                return database

        raise UnknownDatabaseError('This database is not available: {}' \
                                       .format(year))

    @classmethod
    def listYears(cls):
        '''
        Returns a list with all database years.

        Returns:
            list: List with all database years
        '''
        return [str(database.year) for database in cls.findAll()]


class DatabaseError(Exception):
    '''
    Generic exception class for database errors.
    '''
    pass


class UnknownDatabaseError(DatabaseError):
    '''
    Exception class raised when a given database is not found.
    '''
    pass
