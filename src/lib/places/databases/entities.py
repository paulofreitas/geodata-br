#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
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

from places.core.i18n import _, Translator
from places.core.types import Entity, LegacyEntity

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


class DatabaseColumn(object):
    '''
    Entity class for database columns.
    '''

    def __init__(self, name, **rules):
        '''
        Constructor.

        Arguments:
            name (str): The column name
            rules (dict): The column rules
        '''
        self.name = name
        self.localized_name = _(name)
        self.rules = rules


class DatabaseRow(object):
    '''
    Entity class for database rows.
    '''

    __columns__ = [
        DatabaseColumn('state_id',
                       requires='state_name',
                       cast_type=int),
        DatabaseColumn('state_name'),
        DatabaseColumn('mesoregion_id',
                       requires='mesoregion_name',
                       min_length=2,
                       suffix='state_id',
                       cast_type=int),
        DatabaseColumn('mesoregion_name'),
        DatabaseColumn('microregion_id',
                       requires='microregion_name',
                       min_length=3,
                       suffix='state_id',
                       cast_type=int),
        DatabaseColumn('microregion_name'),
        DatabaseColumn('municipality_id',
                       requires='municipality_name',
                       min_length=5,
                       suffix='state_id',
                       cast_type=int),
        DatabaseColumn('municipality_name'),
        DatabaseColumn('district_id',
                       requires='district_name',
                       min_length=2,
                       suffix='municipality_id',
                       cast_type=int),
        DatabaseColumn('district_name'),
        DatabaseColumn('subdistrict_id',
                       requires='subdistrict_name',
                       min_length=2,
                       suffix='district_id',
                       cast_type=int),
        DatabaseColumn('subdistrict_name'),
    ]

    def __init__(self):
        '''
        Constructor.
        '''
        # Initialize attributes
        for column in self.__columns__:
            self.__dict__[column.name] = None

        self._name = None

    def columns(self, localized=True):
        '''
        Returns the row column names.

        Arguments:
            localized (bool): Whether or not it should localize column names

        Returns:
            list: The row column names
        '''
        return [column.localized_name if localized else column.name
                for column in self.__columns__]

    def values(self):
        '''
        Returns the row column values.

        Returns:
            list: The row column values
        '''
        return [self.__dict__[column.name] for column in self.__columns__]

    def normalize(self, force_str=False):
        '''
        Normalizes the row data as needed.

        Arguments:
            force_str (bool): Whether or not it should convert columns to string

        Returns:
            DatabaseRow: The self DatabaseRow instance
        '''
        # pylint: disable=unidiomatic-typecheck
        for column in self.__columns__:
            value = self.__dict__[column.name]

            # Skip unset values
            if not value:
                continue

            # Convert non-string columns
            if force_str:
                if type(value) == float:
                    value = '{:.0f}'.format(value)

            # Unset/skip unused columns
            if (('requires' in column.rules
                    and not self.__dict__[column.rules['requires']])
                    or ('cast_type' in column.rules
                        and not column.rules['cast_type'](value))):
                self.__dict__[column.name] = None
                continue

            # Reformat columns as needed
            if 'min_length' in column.rules:
                if len(value) < column.rules['min_length']:
                    value = '{:0>{}}'.format(value, column.rules['min_length'])

                if ('suffix' in column.rules
                        and len(value) == column.rules['min_length']):
                    value = str(self.__dict__[column.rules['suffix']]) + value

            # Cast columns
            if 'cast_type' in column.rules:
                value = column.rules['cast_type'](value)

            # Save normalized value
            self.__dict__[column.name] = value

        return self

    def serialize(self, localized=True):
        '''
        Returns the serialized row data dictionary.

        Arguments:
            localized (bool): Whether or not it should localize column names

        Returns:
            dict: The serialized row data dictionary
        '''
        if localized:
            return {column.localized_name: self.__dict__[column.name]
                    for column in self.__columns__}

        return {column.name: self.__dict__[column.name]
                for column in self.__columns__}

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
            base (places.databases.Database): The database where data belongs
            columns (list): The parsed columns
            rows (list): The parsed rows
            records (places.core.types.Map): The parsed records
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
            places.core.type.Map: The database records
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
