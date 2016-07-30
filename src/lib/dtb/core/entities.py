#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2016 Paulo Freitas
# MIT License (see LICENSE file)
'''
Core entities module

This module provides the common entities used across the packages.
'''
from __future__ import unicode_literals

# Imports

# Built-in dependencies

from collections import OrderedDict
from operator import add

# External dependencies

from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.types import BigInteger, Integer, SmallInteger, String

# Package dependencies

from dtb.core.types import Entity, Struct

# Classes


class Uf(Entity):
    '''Entity for states.'''
    __tablename__ = 'uf'

    id = Column(SmallInteger, nullable=False, primary_key=True)
    nome = Column(String(32), nullable=False, index=True)


class Mesorregiao(Entity):
    '''Entity for mesoregions.'''
    __tablename__ = 'mesorregiao'

    id = Column(SmallInteger, nullable=False, primary_key=True)
    id_uf = Column(SmallInteger,
                   ForeignKey('uf.id', use_alter=True),
                   nullable=False,
                   index=True)
    nome = Column(String(64), nullable=False, index=True)


class Microrregiao(Entity):
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


class Municipio(Entity):
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


class Distrito(Entity):
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


class Subdistrito(Entity):
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


class DatabaseRow(Struct):
    '''Entity class for database rows.'''

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
        # Initial fixes

        for key in self:
            # Convert empty and zero values to None
            if not self[key] or (key.startswith('id') and not int(self[key])):
                self[key] = None

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

        # Post-processing fixes

        for key in self:
            # Cast numeric values to integer
            if self[key] and key.startswith('id'):
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
