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

# Imports

# Built-in dependencies

from collections import OrderedDict
from operator import add

# External dependencies

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql.schema import Column, ForeignKey, MetaData
from sqlalchemy.types import BigInteger, Integer, SmallInteger, String

# Package dependencies

from .value_objects import Struct

# Classes


Base = declarative_base()


class AbstractBase(Base):
    '''Abstract entity class.'''
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
        '''Shortcut property for table name.'''
        return str(self.__table__.name)

    @hybrid_property
    def columns(self):
        '''Shortcut property for table column names.'''
        return (str(column.name) for column in self.__table__.columns)

    @hybrid_property
    def data(self):
        '''Shortcut property for ordered table data.'''
        return OrderedDict((column, getattr(self, column))
                           for column in self.__table__.columns.keys())


class Uf(AbstractBase):
    '''Entity for states.'''
    __tablename__ = 'uf'

    id = Column(SmallInteger, nullable=False, primary_key=True)
    nome = Column(String(32), nullable=False, index=True)


class Mesorregiao(AbstractBase):
    '''Entity for mesoregions.'''
    __tablename__ = 'mesorregiao'

    id = Column(SmallInteger, nullable=False, primary_key=True)
    id_uf = Column(SmallInteger,
                   ForeignKey('uf.id', use_alter=True),
                   nullable=False,
                   index=True)
    nome = Column(String(64), nullable=False, index=True)


class Microrregiao(AbstractBase):
    '''Entity for microregions.'''
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
    '''Entity for municipalities.'''
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
    '''Entity for districts.'''
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
    '''Entity for subdistricts.'''
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


class TerritorialDatabaseRow(Struct):
    '''Entity for territorial database row'''

    def __init__(self):
        '''Constructor.'''
        super(self.__class__, self).__init__()

        self.id_uf = None
        self.id_mesorregiao = None
        self.id_microrregiao = None
        self.id_municipio = None
        self.id_distrito = None
        self.id_subdistrito = None
        self.nome_uf = None
        self.nome_mesorregiao = None
        self.nome_microrregiao = None
        self.nome_municipio = None
        self.nome_distrito = None
        self.nome_subdistrito = None

    def normalize(self):
        '''Normalize row data as needed.'''
        # Data length fixes

        if self.id_mesorregiao and len(self.id_mesorregiao) == 2:
            self.id_mesorregiao = self.id_uf + self.id_mesorregiao

        if self.id_microrregiao and len(self.id_microrregiao) == 3:
            self.id_microrregiao = self.id_uf + self.id_microrregiao

        if self.id_municipio and len(self.id_municipio) == 5:
            self.id_municipio = self.id_uf + self.id_municipio

        if self.id_distrito and len(self.id_distrito) == 2:
            self.id_distrito = self.id_municipio + self.id_distrito

        if self.id_subdistrito and len(self.id_subdistrito) == 2:
            self.id_subdistrito = self.id_distrito + self.id_subdistrito

        # Misc fixes

        for key in self:
            # Convert empty values to None
            if not self[key]:
                self[key] = None

            # Cast numeric values to integer
            elif key.startswith('id'):
                self[key] = int(self[key])

    @property
    def value(self):
        entities = ((self.id_uf, self.nome_uf),
                    (self.id_mesorregiao, self.nome_mesorregiao),
                    (self.id_microrregiao, self.nome_microrregiao),
                    (self.id_municipio, self.nome_municipio),
                    (self.id_distrito, self.nome_distrito),
                    (self.id_subdistrito, self.nome_subdistrito))
        cols = []
        cols.extend([entity_id, entity_name]
                    for entity_id, entity_name in entities
                    if entity_name)

        return reduce(add, cols) if cols else []

    @property
    def uf(self):
        '''Returns a new struct object with Uf properties.'''
        return Struct(id=self.id_uf,
                      nome=self.nome_uf)

    @property
    def mesorregiao(self):
        '''Returns a new struct object with Mesorregiao properties.'''
        return Struct(id=self.id_mesorregiao,
                      id_uf=self.id_uf,
                      nome=self.nome_mesorregiao)

    @property
    def microrregiao(self):
        '''Returns a new struct object with Microrregiao properties.'''
        return Struct(id=self.id_microrregiao,
                      id_mesorregiao=self.id_mesorregiao,
                      id_uf=self.id_uf,
                      nome=self.nome_microrregiao)

    @property
    def municipio(self):
        '''Returns a new struct object with Municipio properties.'''
        return Struct(id=self.id_municipio,
                      id_microrregiao=self.id_microrregiao,
                      id_mesorregiao=self.id_mesorregiao,
                      id_uf=self.id_uf,
                      nome=self.nome_municipio)

    @property
    def distrito(self):
        '''Returns a new struct object with Distrito properties.'''
        return Struct(id=self.id_distrito,
                      id_municipio=self.id_municipio,
                      id_microrregiao=self.id_microrregiao,
                      id_mesorregiao=self.id_mesorregiao,
                      id_uf=self.id_uf,
                      nome=self.nome_distrito)

    @property
    def subdistrito(self):
        '''Returns a new struct object with Subdistrito properties.'''
        return Struct(id=self.id_subdistrito,
                      id_distrito=self.id_distrito,
                      id_municipio=self.id_municipio,
                      id_microrregiao=self.id_microrregiao,
                      id_mesorregiao=self.id_mesorregiao,
                      id_uf=self.id_uf,
                      nome=self.nome_subdistrito)


class TerritorialData(object):
    '''Entity for territorial data.'''
    entities = (Uf, Mesorregiao, Microrregiao, Municipio, Distrito, Subdistrito)

    def __init__(self, base):
        '''Constructor.

        :param base: the territorial database where data will be retrieved
        '''
        self._base = base
        self._name = 'dtb_{}'.format(base.year)
        self._cols = []
        self._rows = []
        self._dict = {}

    def toDict(self, strKeys=False, forceUnicode=False, includeKey=False):
        '''Converts this territorial data into an ordered dictionary.'''
        _dict = OrderedDict()

        for entity in self.entities:
            if not self._dict[entity.table]:
                continue

            _dict[entity.table] = OrderedDict()

            for row in self._dict[entity.table]:
                row_data = OrderedDict()

                for column in entity.columns:
                    if forceUnicode and isinstance(row[column], str):
                        row_data[column] = unicode(row[column])
                    else:
                        row_data[column] = row[column]

                row_id = str(row_data['id']) if strKeys else row_data['id']

                if not includeKey:
                    del row_data['id']

                _dict[entity.table][row_id] = row_data

        return _dict
