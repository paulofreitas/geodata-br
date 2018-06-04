#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
Databases package

This package provides a database class, a database factory class and a database
repository class.
'''
# Imports

# Built-in dependencies

import ftplib
import io
import zipfile

# Package dependencies

from geodatabr.core.constants import DATA_DIR
from geodatabr.core.helpers.decorators import classproperty
from geodatabr.core.helpers.filesystem import Directory, File, Path
from geodatabr.core.logging import Logger
from geodatabr.core.types import Bytes, Map
from geodatabr.dataset.entities import Entities, DatabaseData
from geodatabr.exporters import ExporterFactory
from geodatabr.parsers import ParserFactory
from geodatabr.parsers.xls import XlsMerger

# Package metadata

__version__ = '1.0-dev'
__author__ = 'Paulo Freitas <me@paulofreitas.me>'
__copyright__ = 'Copyright (c) 2013-2018 Paulo Freitas'
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
        self._contents = io.BytesIO()
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
        return File(DATA_DIR / '.cache' / str(self.year + '.' + self.format))

    def download(self):
        '''
        Downloads the database archive/file.
        '''
        ftp = ftplib.FTP('geoftp.ibge.gov.br')

        logger.debug('Connecting to FTP server...')
        ftp.connect()

        logger.debug('Logging into the FTP server...')
        ftp.login()
        ftp.cwd(str(Path('organizacao_do_territorio',
                         'estrutura_territorial',
                         'divisao_territorial',
                         self.year)))

        logger.info('Retrieving database...')

        ftp.retrbinary('RETR {}'.format(self.archive or self.file),
                       self._contents.write)

    def process(self):
        '''
        Process the database archive.
        '''
        logger.info('Extracting database...')

        with zipfile.ZipFile(self._contents, 'r') as archive:
            if type(self.file) == list:
                logger.info('Merging database files...')

                merger = XlsMerger(self.sheet)

                for base_file in self.file:
                    with archive.open(base_file) as base:
                        merger.merge(base, 0)

                self._contents = merger.save()

                return

            with archive.open(self.file, 'r') as database:
                self._contents = io.BytesIO()
                self._contents.write(database.read())

    def cache(self):
        '''
        Caches the database file.
        '''
        try:
            Directory(self.cacheFile.parent).create()
        except OSError:
            pass

        with self.cacheFile.open('wb') as cache:
            cache.write(self._contents.getvalue())

    def read(self):
        '''
        Reads the given database.

        Returns:
            geodatabr.core.types.Bytes: The database raw binary data
        '''
        if not self.cacheFile.exists():
            self.download()

            if self.archive:
                self.process()

            self.cache()

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

    @staticmethod
    def create():
        '''
        Factories a database object for the latest dataset available.

        Returns:
            geodatabr.dataset.Database: A database object for the latest dataset
        '''
        return Database(year=2016,
                        archive='DTB_2016_v2.zip',
                        file=[
                            'DTB_2016_v2/DTB_2016/DTB_BRASIL_SUBDISTRITO.xls',
                            'DTB_2016_v2/DTB_2016/DTB_BRASIL_DISTRITO.xls',
                            'DTB_2016_v2/DTB_2016/DTB_BRASIL_MUNICIPIO.xls',
                        ],
                        format='xls',
                        sheet='DTB_2016_SubDistrito')


class DatabaseError(Exception):
    '''
    Generic exception class for database errors.
    '''
    pass
