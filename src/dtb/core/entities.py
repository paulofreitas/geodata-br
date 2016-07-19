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
from __future__ import unicode_literals

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

import ftplib
import io
import sys
import urlparse
import zipfile

from io import open
from os import makedirs
from os.path import dirname, exists, join as path

# Dependency modules

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql.schema import Column, ForeignKey, Index, MetaData
from sqlalchemy.types import BigInteger, Integer, SmallInteger, String
import yaml

# Package modules

from .. import exporters, parsers
from ..core.helpers import PKG_DIR, SRC_DIR
from .value_objects import Struct

# -- Constants ---------------------------------------------------------------

BASE_LIST = path(PKG_DIR, 'data/bases.yaml')

# -- Classes ------------------------------------------------------------------


Base = declarative_base()


class AbstractBase(Base):
    __abstract__ = True

    convention = {
      'pk': 'pk_%(table_name)s',
      'fk': 'fk_%(table_name)s_%(column_0_name)s',
      'ix': 'ix_%(column_0_label)s',
      'uq': 'uq_%(table_name)s_%(column_0_name)s',
    }

    metadata = MetaData(naming_convention=convention)

    @hybrid_property
    def table(self):
        return str(self.__table__.name)

    @hybrid_property
    def columns(self):
        return (str(column.name) for column in self.__table__.columns)

class Uf(AbstractBase):
    __tablename__ = 'uf'

    id = Column(SmallInteger, nullable=False, primary_key=True)
    nome = Column(String(32), nullable=False, index=True)


class Mesorregiao(AbstractBase):
    __tablename__ = 'mesorregiao'

    id = Column(SmallInteger, nullable=False, primary_key=True)
    id_uf = Column(SmallInteger,
                   ForeignKey('uf.id', use_alter=True),
                   nullable=False,
                   index=True)
    nome = Column(String(64), nullable=False, index=True)


class Microrregiao(AbstractBase):
    __tablename__ = 'microrregiao'

    id = Column(Integer, nullable=False, primary_key=True)
    id_mesorregiao = Column(SmallInteger,
                            ForeignKey('mesorregiao.id', use_alter=True),
                            nullable=False,
                            index=True)
    id_uf = Column(SmallInteger,
                   ForeignKey('uf.id', use_alter=True),
                   nullable=False,
                   index=True)
    nome = Column(String(64), nullable=False, index=True)


class Municipio(AbstractBase):
    __tablename__ = 'municipio'

    id = Column(Integer, nullable=False, primary_key=True)
    id_microrregiao = Column(Integer,
                             ForeignKey('microrregiao.id', use_alter=True),
                             nullable=False,
                             index=True)
    id_mesorregiao = Column(SmallInteger,
                            ForeignKey('mesorregiao.id', use_alter=True),
                            nullable=False,
                            index=True)
    id_uf = Column(SmallInteger,
                   ForeignKey('uf.id', use_alter=True),
                   nullable=False,
                   index=True)
    nome = Column(String(64), nullable=False, index=True)


class Distrito(AbstractBase):
    __tablename__ = 'distrito'

    id = Column(Integer, nullable=False, primary_key=True)
    id_municipio = Column(Integer,
                          ForeignKey('municipio.id', use_alter=True),
                          nullable=False,
                          index=True)
    id_microrregiao = Column(Integer,
                             ForeignKey('microrregiao.id', use_alter=True),
                             nullable=False,
                             index=True)
    id_mesorregiao = Column(SmallInteger,
                            ForeignKey('mesorregiao.id', use_alter=True),
                            nullable=False,
                            index=True)
    id_uf = Column(SmallInteger,
                   ForeignKey('uf.id', use_alter=True),
                   nullable=False,
                   index=True)
    nome = Column(String(64), nullable=False, index=True)


class Subdistrito(AbstractBase):
    __tablename__ = 'subdistrito'

    id = Column(BigInteger, nullable=False, primary_key=True)
    id_distrito = Column(Integer,
                         ForeignKey('distrito.id', use_alter=True),
                         nullable=False,
                         index=True)
    id_municipio = Column(Integer,
                          ForeignKey('municipio.id', use_alter=True),
                          nullable=False,
                          index=True)
    id_microrregiao = Column(Integer,
                             ForeignKey('microrregiao.id', use_alter=True),
                             nullable=False,
                             index=True)
    id_mesorregiao = Column(SmallInteger,
                            ForeignKey('mesorregiao.id', use_alter=True),
                            nullable=False,
                            index=True)
    id_uf = Column(SmallInteger,
                   ForeignKey('uf.id', use_alter=True),
                   nullable=False,
                   index=True)
    nome = Column(String(64), nullable=False, index=True)


class TerritorialData(object):
    entities = (Uf, Mesorregiao, Microrregiao, Municipio, Distrito, Subdistrito)

    def __init__(self, base):
        self._base = Struct(base)
        self._name = 'dtb_{}'.format(self._base.year)
        self._cols = []
        self._rows = []
        self._dict = {}
        self._rawdata = None

        for entity in self.entities:
            self._cols.append('id_' + entity.table)
            self._cols.append('nome_' + entity.table)
            self._dict[entity.table] = []

    def load(self, rawdata):
        self._rawdata = rawdata


class TerritorialBase(object):
    base_list = dict((str(database['year']), database)
                     for database in yaml.load(open(BASE_LIST)))
    bases = tuple(reversed(sorted(base_list.keys())))

    def __init__(self, year, logger):
        if year not in self.bases:
            raise Exception('This base is not available to download.')

        self._data = TerritorialData(self.base_list.get(year))
        self._logger = logger

    @property
    def year(self):
        return str(self._data._base.year)

    @property
    def archive(self):
        return self._data._base.archive

    @property
    def file(self):
        return self._data._base.file

    @property
    def format(self):
        return self._data._base.format

    @property
    def sheet(self):
        return self._data._base.sheet

    @property
    def sheet_file(self):
        return path(SRC_DIR, '.cache', self.year)

    def download(self):
        url_info = urlparse.urlparse(self.archive)
        ftp = ftplib.FTP(url_info.netloc)
        zip_data = io.BytesIO()
        sheet_data = io.BytesIO()

        self._logger.debug('Connecting to FTP server...')
        ftp.connect()

        self._logger.debug('Logging into the FTP server...')
        ftp.login()
        ftp.cwd(dirname(url_info.path))

        self._logger.info('Retrieving database...')
        ftp.retrbinary(
            'RETR {}'.format(os.path.basename(url_info.path)),
            zip_data.write
        )

        with zipfile.ZipFile(zip_data, 'r') as zip_file:
            self._logger.info('Reading database...')
            with zipfile.open(self.file, 'r') as sheet_file:
                sheet_data.write(sheet_file.read())

        try:
            makedirs(dirname(self.sheet_file))
        except OSError:
            pass

        with open(self.sheet_file, 'wb') as sheet_file:
            sheet_file.write(sheet_data.getvalue())

        return self

    def retrieve(self):
        if not exists(self.sheet_file):
            self.download()

        sheet_data = io.BytesIO()

        with open(self.sheet_file, 'rb') as sheet_file:
            sheet_data.write(sheet_file.read())

        self._data.load(sheet_data.getvalue())

        return self

    def parse(self):
        parser = parsers.FORMATS.get(self.format)

        try:
            self._data = parser(self._data, self._logger).parse()
        except:
            raise Exception('Failed to parse data using the given parser')

        return self

    def export(self, format, minified=False, filename=None):
        if format not in exporters.FORMATS:
            raise Exception('Unsupported output format.')
        exporter = exporters.FORMATS.get(format)

        if minified:
            self._logger.info('Exporting database to minified {} format...' \
                .format(exporter.format))
        else:
            self._logger.info('Exporting database to {} format...' \
                .format(exporter.format))

        data = exporter(self._data, minified).data
        binary_data = exporter.binary_format

        if not binary_data and not type(data) == unicode:
            data = unicode(data.decode('utf-8'))

        self._logger.debug('Done.')

        if filename:
            if filename == 'auto':
                filename = 'dtb' + exporter.extension

            with open(filename, 'wb' if binary_data else 'w') as export_file:
                export_file.write(data)
        else:
            sys.stdout.write(data)
