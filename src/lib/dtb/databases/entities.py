#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2016 Paulo Freitas
# MIT License (see LICENSE file)
'''
Database entities module

This module provides the database entities used across the package.
'''
from __future__ import unicode_literals

# Imports

# Built-in dependencies

from collections import OrderedDict
from operator import add

# External dependencies

from sqlalchemy.sql.schema import Column, ForeignKey, Table
from sqlalchemy.types import BigInteger, Integer, SmallInteger, String

# Package dependencies

from dtb.core.i18n import _, Translator
from dtb.core.types import Entity

# Translator setup

Translator.load(__package__)

# Classes


class State(Entity):
    '''
    Entity for states.
    '''
    __table__ = Table(
        _('states'),
        Entity.metadata,
        Column(_('id'),
               SmallInteger,
               nullable=False,
               primary_key=True),
        Column(_('name'),
               String(32),
               nullable=False,
               index=True)
    )

    # Columns mapping
    __columns__ = {
        _('id'): 'state_id',
        _('name'): 'state_name',
    }


class Mesoregion(Entity):
    '''
    Entity for mesoregions.
    '''
    __table__ = Table(
        _('mesoregions'),
        Entity.metadata,
        Column(_('id'),
               SmallInteger,
               nullable=False,
               primary_key=True),
        Column(_('state_id'),
               SmallInteger,
               ForeignKey(_('states.id'), use_alter=True),
               nullable=False,
               index=True),
        Column(_('name'),
               String(64),
               nullable=False,
               index=True)
    )

    # Columns mapping
    __columns__ = {
        _('id'): 'mesoregion_id',
        _('state_id'): 'state_id',
        _('name'): 'mesoregion_name',
    }


class Microregion(Entity):
    '''
    Entity for microregions.
    '''
    __table__ = Table(
        _('microregions'),
        Entity.metadata,
        Column(_('id'),
               Integer,
               nullable=False,
               primary_key=True),
        Column(_('mesoregion_id'),
               SmallInteger,
               ForeignKey(_('mesoregions.id'), use_alter=True),
               nullable=False,
               index=True),
        Column(_('state_id'),
               SmallInteger,
               ForeignKey(_('states.id'), use_alter=True),
               nullable=False,
               index=True),
        Column(_('name'),
               String(64),
               nullable=False,
               index=True)
    )

    # Columns mapping
    __columns__ = {
        _('id'): 'microregion_id',
        _('mesoregion_id'): 'mesoregion_id',
        _('state_id'): 'state_id',
        _('name'): 'microregion_name',
    }


class Municipality(Entity):
    '''
    Entity for municipalities.
    '''
    __table__ = Table(
        _('municipalities'),
        Entity.metadata,
        Column(_('id'),
               Integer,
               nullable=False,
               primary_key=True),
        Column(_('microregion_id'),
               Integer,
               ForeignKey(_('microregions.id'), use_alter=True),
               nullable=False,
               index=True),
        Column(_('mesoregion_id'),
               SmallInteger,
               ForeignKey(_('mesoregions.id'), use_alter=True),
               nullable=False,
               index=True),
        Column(_('state_id'),
               SmallInteger,
               ForeignKey(_('states.id'), use_alter=True),
               nullable=False,
               index=True),
        Column(_('name'),
               String(64),
               nullable=False,
               index=True)
    )

    # Columns mapping
    __columns__ = {
        _('id'): 'municipality_id',
        _('microregion_id'): 'microregion_id',
        _('mesoregion_id'): 'mesoregion_id',
        _('state_id'): 'state_id',
        _('name'): 'municipality_name',
    }


class District(Entity):
    '''
    Entity for districts.
    '''
    __table__ = Table(
        _('districts'),
        Entity.metadata,
        Column(_('id'),
               Integer,
               nullable=False,
               primary_key=True),
        Column(_('municipality_id'),
               Integer,
               ForeignKey(_('municipalities.id'), use_alter=True),
               nullable=False,
               index=True),
        Column(_('microregion_id'),
               Integer,
               ForeignKey(_('microregions.id'), use_alter=True),
               nullable=False,
               index=True),
        Column(_('mesoregion_id'),
               SmallInteger,
               ForeignKey(_('mesoregions.id'), use_alter=True),
               nullable=False,
               index=True),
        Column(_('state_id'),
               SmallInteger,
               ForeignKey(_('states.id'), use_alter=True),
               nullable=False,
               index=True),
        Column(_('name'),
               String(64),
               nullable=False,
               index=True)
    )

    # Columns mapping
    __columns__ = {
        _('id'): 'district_id',
        _('municipality_id'): 'municipality_id',
        _('microregion_id'): 'microregion_id',
        _('mesoregion_id'): 'mesoregion_id',
        _('state_id'): 'state_id',
        _('name'): 'district_name',
    }


class Subdistrict(Entity):
    '''
    Entity for subdistricts.
    '''
    __table__ = Table(
        _('subdistricts'),
        Entity.metadata,
        Column(_('id'),
               BigInteger,
               nullable=False,
               primary_key=True),
        Column(_('district_id'),
               Integer,
               ForeignKey(_('districts.id'), use_alter=True),
               nullable=False,
               index=True),
        Column(_('municipality_id'),
               Integer,
               ForeignKey(_('municipalities.id'), use_alter=True),
               nullable=False,
               index=True),
        Column(_('microregion_id'),
               Integer,
               ForeignKey(_('microregions.id'), use_alter=True),
               nullable=False,
               index=True),
        Column(_('mesoregion_id'),
               SmallInteger,
               ForeignKey(_('mesoregions.id'), use_alter=True),
               nullable=False,
               index=True),
        Column(_('state_id'),
               SmallInteger,
               ForeignKey(_('states.id'), use_alter=True),
               nullable=False,
               index=True),
        Column(_('name'),
               String(64),
               nullable=False,
               index=True)
    )

    # Columns mapping
    __columns__ = {
        _('id'): 'subdistrict_id',
        _('district_id'): 'district_id',
        _('municipality_id'): 'municipality_id',
        _('microregion_id'): 'microregion_id',
        _('mesoregion_id'): 'mesoregion_id',
        _('state_id'): 'state_id',
        _('name'): 'subdistrict_name',
    }


class DatabaseRow(object):
    '''
    Entity class for database rows.
    '''

    __slots__ = ('state_id',
                 'state_name',
                 'mesoregion_id',
                 'mesoregion_name',
                 'microregion_id',
                 'microregion_name',
                 'municipality_id',
                 'municipality_name',
                 'district_id',
                 'district_name',
                 'subdistrict_id',
                 'subdistrict_name')

    def __init__(self):
        '''
        Constructor.
        '''
        # Initialize attributes
        self.state_id = None
        self.state_name = None
        self.mesoregion_id = None
        self.mesoregion_name = None
        self.microregion_id = None
        self.microregion_name = None
        self.municipality_id = None
        self.municipality_name = None
        self.district_id = None
        self.district_name = None
        self.subdistrict_id = None
        self.subdistrict_name = None

    def normalize(self):
        '''Normalize row data as needed.'''
        # Initial fixes

        for column in self.__slots__:
            # Convert empty and zero values to None
            value = getattr(self, column)

            if not value or (column.endswith('_id') and not int(value)):
                setattr(self, column, None)

        # Data length fixes

        if self.mesoregion_id and len(self.mesoregion_id) == 2:
            self.mesoregion_id = self.state_id + self.mesoregion_id

        if self.microregion_id and len(self.microregion_id) == 3:
            self.microregion_id = self.state_id + self.microregion_id

        if self.municipality_id and len(self.municipality_id) == 5:
            self.municipality_id = self.state_id + self.municipality_id

        if self.district_id and len(self.district_id) == 2:
            self.district_id = self.municipality_id + self.district_id

        if self.subdistrict_id and len(self.subdistrict_id) == 2:
            self.subdistrict_id = self.district_id + self.subdistrict_id

        # Post-processing fixes

        for column in self.__slots__:
            # Cast numeric values to integer
            value = getattr(self, column)

            if value and column.endswith('_id'):
                setattr(self, column, int(value))

    @property
    def value(self):
        entities = ((self.state_id, self.state_name),
                    (self.mesoregion_id, self.mesoregion_name),
                    (self.microregion_id, self.microregion_name),
                    (self.municipality_id, self.municipality_name),
                    (self.district_id, self.district_name),
                    (self.subdistrict_id, self.subdistrict_name))
        cols = []
        cols.extend([entity_id, entity_name]
                    for entity_id, entity_name in entities
                    if entity_name)

        return reduce(add, cols) if cols else []

    @property
    def columns(self):
        '''
        Returns the translated row column names.

        Returns:
            list: The translated row column names
        '''
        return [_(column) for column in self.__slots__]

    def __str__(self):
        '''
        Returns the string representation of this object.

        Returns:
            str: The string representation of this object
        '''
        return str(self.value)


class DatabaseData(object):
    '''
    Entity for database data.
    '''

    entities = (State,
                Mesoregion,
                Microregion,
                Municipality,
                District,
                Subdistrict)

    def __init__(self, base):
        '''
        Constructor.

        Arguments:
            base (dtb.databases.Database): The database where data will be
                retrieved
        '''
        self._base = base
        self._name = 'dtb_{}'.format(base.year)
        self._cols = []
        self._rows = []
        self._dict = {}

    def toDict(self, strKeys=False, forceUnicode=False, includeKey=False):
        '''
        Converts this database data into an ordered dictionary.
        '''
        _dict = OrderedDict()

        for entity in self.entities:
            if not self._dict[entity.table]:
                continue

            _dict[entity.table] = OrderedDict()

            for row in self._dict[entity.table]:
                row_data = OrderedDict()

                for column in entity.columns:
                    value = row[column]

                    if forceUnicode:
                        column = unicode(column)

                        if isinstance(value, str):
                            value = unicode(value)

                    row_data[column] = value

                row_id = str(row_data['id']) if strKeys else row_data['id']

                if not includeKey:
                    del row_data['id']

                _dict[entity.table][row_id] = row_data

        return _dict
