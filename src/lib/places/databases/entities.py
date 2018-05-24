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

Translator.load('databases')

# Classes


class State(Entity):
    '''
    Entity for states.
    '''
    __table__ = Table(
        'states',
        Entity.metadata,
        Column('id',
               SmallInteger,
               nullable=False,
               primary_key=True),
        Column('name',
               String(32),
               nullable=False,
               index=True)
    )

    # Columns mapping
    __columns__ = {
        'id': 'state_id',
        'name': 'state_name',
    }


class Mesoregion(Entity):
    '''
    Entity for mesoregions.
    '''
    __table__ = Table(
        'mesoregions',
        Entity.metadata,
        Column('id',
               SmallInteger,
               nullable=False,
               primary_key=True),
        Column('state_id',
               SmallInteger,
               ForeignKey('states.id', use_alter=True),
               nullable=False,
               index=True),
        Column('name',
               String(64),
               nullable=False,
               index=True)
    )

    # Columns mapping
    __columns__ = {
        'id': 'mesoregion_id',
        'state_id': 'state_id',
        'name': 'mesoregion_name',
    }


class Microregion(Entity):
    '''
    Entity for microregions.
    '''
    __table__ = Table(
        'microregions',
        Entity.metadata,
        Column('id',
               Integer,
               nullable=False,
               primary_key=True),
        Column('mesoregion_id',
               SmallInteger,
               ForeignKey('mesoregions.id', use_alter=True),
               nullable=False,
               index=True),
        Column('state_id',
               SmallInteger,
               ForeignKey('states.id', use_alter=True),
               nullable=False,
               index=True),
        Column('name',
               String(64),
               nullable=False,
               index=True)
    )

    # Columns mapping
    __columns__ = {
        'id': 'microregion_id',
        'mesoregion_id': 'mesoregion_id',
        'state_id': 'state_id',
        'name': 'microregion_name',
    }


class Municipality(Entity):
    '''
    Entity for municipalities.
    '''
    __table__ = Table(
        'municipalities',
        Entity.metadata,
        Column('id',
               Integer,
               nullable=False,
               primary_key=True),
        Column('microregion_id',
               Integer,
               ForeignKey('microregions.id', use_alter=True),
               nullable=False,
               index=True),
        Column('mesoregion_id',
               SmallInteger,
               ForeignKey('mesoregions.id', use_alter=True),
               nullable=False,
               index=True),
        Column('state_id',
               SmallInteger,
               ForeignKey('states.id', use_alter=True),
               nullable=False,
               index=True),
        Column('name',
               String(64),
               nullable=False,
               index=True)
    )

    # Columns mapping
    __columns__ = {
        'id': 'municipality_id',
        'microregion_id': 'microregion_id',
        'mesoregion_id': 'mesoregion_id',
        'state_id': 'state_id',
        'name': 'municipality_name',
    }


class District(Entity):
    '''
    Entity for districts.
    '''
    __table__ = Table(
        'districts',
        Entity.metadata,
        Column('id',
               Integer,
               nullable=False,
               primary_key=True),
        Column('municipality_id',
               Integer,
               ForeignKey('municipalities.id', use_alter=True),
               nullable=False,
               index=True),
        Column('microregion_id',
               Integer,
               ForeignKey('microregions.id', use_alter=True),
               nullable=False,
               index=True),
        Column('mesoregion_id',
               SmallInteger,
               ForeignKey('mesoregions.id', use_alter=True),
               nullable=False,
               index=True),
        Column('state_id',
               SmallInteger,
               ForeignKey('states.id', use_alter=True),
               nullable=False,
               index=True),
        Column('name',
               String(64),
               nullable=False,
               index=True)
    )

    # Columns mapping
    __columns__ = {
        'id': 'district_id',
        'municipality_id': 'municipality_id',
        'microregion_id': 'microregion_id',
        'mesoregion_id': 'mesoregion_id',
        'state_id': 'state_id',
        'name': 'district_name',
    }


class Subdistrict(Entity):
    '''
    Entity for subdistricts.
    '''
    __table__ = Table(
        'subdistricts',
        Entity.metadata,
        Column('id',
               BigInteger,
               nullable=False,
               primary_key=True),
        Column('district_id',
               Integer,
               ForeignKey('districts.id', use_alter=True),
               nullable=False,
               index=True),
        Column('municipality_id',
               Integer,
               ForeignKey('municipalities.id', use_alter=True),
               nullable=False,
               index=True),
        Column('microregion_id',
               Integer,
               ForeignKey('microregions.id', use_alter=True),
               nullable=False,
               index=True),
        Column('mesoregion_id',
               SmallInteger,
               ForeignKey('mesoregions.id', use_alter=True),
               nullable=False,
               index=True),
        Column('state_id',
               SmallInteger,
               ForeignKey('states.id', use_alter=True),
               nullable=False,
               index=True),
        Column('name',
               String(64),
               nullable=False,
               index=True)
    )

    # Columns mapping
    __columns__ = {
        'id': 'subdistrict_id',
        'district_id': 'district_id',
        'municipality_id': 'municipality_id',
        'microregion_id': 'microregion_id',
        'mesoregion_id': 'mesoregion_id',
        'state_id': 'state_id',
        'name': 'subdistrict_name',
    }


class LegacyState(LegacyEntity):
    '''
    Legacy entity for states.
    '''
    __table__ = Table(
        'states',
        LegacyEntity.metadata,
        Column('id',
               SmallInteger,
               nullable=False,
               primary_key=True),
        Column('name',
               String(64),
               nullable=False,
               index=True)
    )

    # Columns mapping
    __columns__ = {
        'id': 'state_id',
        'name': 'state_name',
    }


class LegacyMunicipality(LegacyEntity):
    '''
    Legacy entity for municipalities.
    '''
    __table__ = Table(
        'municipalities',
        LegacyEntity.metadata,
        Column('id',
               Integer,
               nullable=False,
               primary_key=True),
        Column('state_id',
               SmallInteger,
               ForeignKey('states.id', use_alter=True),
               nullable=False,
               index=True),
        Column('name',
               String(64),
               nullable=False,
               index=True)
    )

    # Columns mapping
    __columns__ = {
        'id': 'municipality_id',
        'state_id': 'state_id',
        'name': 'municipality_name',
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

    def columns(self, localized=False):
        '''
        Returns the row column names.

        Arguments:
            localized (bool): Whether or not it should localize column names

        Returns:
            list: The row column names
        '''
        return [_(column.name) if localized else column.name
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

    def serialize(self):
        '''
        Returns the serialized row data dictionary.

        Returns:
            dict: The serialized row data dictionary
        '''
        return {_(column.name): self.__dict__[column.name]
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

        Arguments:
            strKeys (bool): Whether or not it should coerce dictionary keys to string
            forceUnicode (bool): Whether or not it should force coercing data to Unicode
            includeKey (bool): Whether or not it should include the primary key

        Returns:
            collections.OrderedDict: The ordered dictionary
        '''
        records = OrderedDict()

        for entity in self._base.entities:
            if not len(self._records[entity.__table__.name]):
                continue

            table = _(entity.__table__.name)
            records[table] = OrderedDict()

            for row in self._records[entity.__table__.name]:
                record = OrderedDict()

                for column in entity.columns:
                    value = row[column]
                    column = _(column)

                    if forceUnicode:
                        column = unicode(column)

                        if isinstance(value, str):
                            value = unicode(value)

                    record[column] = value

                row_id = str(record['id']) if strKeys else record['id']

                if not includeKey:
                    del record['id']

                records[table][row_id] = record

        return records


# Collections

Entities = (State, Mesoregion, Microregion, Municipality, District, Subdistrict)
LegacyEntities = (LegacyState, LegacyMunicipality)
