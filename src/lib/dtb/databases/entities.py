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

# External dependencies

from sqlalchemy.sql.schema import Column, ForeignKey, Table
from sqlalchemy.types import BigInteger, Integer, SmallInteger, String

# Package dependencies

from dtb.core.i18n import _, Translator
from dtb.core.types import Entity, LegacyEntity

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


class LegacyState(LegacyEntity):
    '''
    Legacy entity for states.
    '''
    __table__ = Table(
        _('states'),
        LegacyEntity.metadata,
        Column(_('id'),
               SmallInteger,
               nullable=False,
               primary_key=True),
        Column(_('name'),
               String(64),
               nullable=False,
               index=True)
    )

    # Columns mapping
    __columns__ = {
        _('id'): 'state_id',
        _('name'): 'state_name',
    }


class LegacyMunicipality(LegacyEntity):
    '''
    Legacy entity for municipalities.
    '''
    __table__ = Table(
        _('municipalities'),
        LegacyEntity.metadata,
        Column(_('id'),
               Integer,
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
        _('id'): 'municipality_id',
        _('state_id'): 'state_id',
        _('name'): 'municipality_name',
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

    @property
    def columns(self):
        '''
        Returns the row column names.

        Returns:
            list: The row column names
        '''
        return self.__slots__

    @property
    def _columns(self):
        '''
        Returns the translated row column names.

        Returns:
            list: The translated row column names
        '''
        return [_(column) for column in self.columns]

    @property
    def values(self):
        '''
        Returns the row column values.

        Returns:
            list: The row column values
        '''
        return [getattr(self, column) for column in self.columns]

    def _fixValues(self):
        '''
        Fixes the row values.
        '''
        # Unset empty and zero values
        for column in self.columns:
            value = getattr(self, column)

            if not value or (column.endswith('_id') and not int(value)):
                setattr(self, column, None)

        # Unset needless values
        if self.mesoregion_id and not self.mesoregion_name:
            self.mesoregion_id = None

        if self.microregion_id and not self.microregion_name:
            self.microregion_id = None

        if self.municipality_id and not self.municipality_name:
            self.municipality_id = None

        if self.district_id and not self.district_name:
            self.district_id = None

        if self.subdistrict_id and not self.subdistrict_name:
            self.subdistrict_id = None

    def _formatValues(self):
        '''
        Formats the row values.
        '''
        # Reformat numeric values
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

        # Cast numeric values to integer
        for column in self.columns:
            if column.endswith('_id'):
                value = getattr(self, column)

                if value:
                    setattr(self, column, int(value))

    def normalize(self):
        '''
        Normalizes the row data as needed.

        Returns:
            DatabaseRow: The self DatabaseRow instance
        '''
        self._fixValues()
        self._formatValues()

        return self

    def serialize(self):
        '''
        Returns the serialized row data dictionary.

        Returns:
            dict: The serialized row data dictionary
        '''
        return {_(column): getattr(self, column) for column in self.columns}

    def __repr__(self):
        '''
        Returns the string representation of this object.

        Returns:
            str: The string representation of this object
        '''
        return repr(self.serialize())


class DatabaseData(object):
    '''
    Entity for database data.
    '''

    def __init__(self, base, columns, rows, records):
        '''
        Constructor.

        Arguments:
            base (dtb.databases.Database): The database where data belongs
            columns (list): The parsed columns
            rows (list): The parsed rows
            records (dtb.core.types.Map): The parsed records
        '''
        self._base = base
        self._columns = columns
        self._rows = rows
        self._records = records

    @property
    def columns(self):
        '''
        Returns the database columns.

        Returns:
            list: The database columns
        '''
        return self._columns

    @property
    def rows(self):
        '''
        Returns the database rows.

        Returns:
            list: The database rows
        '''
        return self._rows

    @property
    def records(self):
        '''
        Returns the database records.

        Returns:
            dtb.core.type.Map: The database records
        '''
        return self._records

    def normalize(self, strKeys=False, forceUnicode=False, includeKey=False):
        '''
        Converts this database data into an ordered dictionary.

        Returns:
            collections.OrderedDict: The ordered dictionary
        '''
        records = OrderedDict()

        for entity in self._base.entities:
            if not len(self._records[entity.table]):
                continue

            records[entity.table] = OrderedDict()

            for row in self._records[entity.table]:
                record = OrderedDict()

                for column in entity.columns:
                    value = row[column]

                    if forceUnicode:
                        column = unicode(column)

                        if isinstance(value, str):
                            value = unicode(value)

                    record[column] = value

                row_id = str(record['id']) if strKeys else record['id']

                if not includeKey:
                    del record['id']

                records[entity.table][row_id] = record

        return records


# Collections

Entities = (State, Mesoregion, Microregion, Municipality, District, Subdistrict)
LegacyEntities = (LegacyState, LegacyMunicipality)
