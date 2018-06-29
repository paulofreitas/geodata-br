#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""
Dataset schema module.

This module provides the entities used to describe the database.
"""
# Imports

# External dependencies

from sqlalchemy import orm, types as sql_types
from sqlalchemy.ext import declarative
from sqlalchemy.sql import schema

# Package dependencies

from geodatabr.core import types

# Classes


class Entity(declarative.declarative_base()):
    """
    Abstract entity class.

    Attributes:
        naming_convention (dict): The constraint naming conventions
        metadata (sqlalchemy.sql.schema.MetaData): The entity metadata
    """

    __abstract__ = True

    naming_convention = {
        'pk': 'pk_%(table_name)s',
        'fk': 'fk_%(table_name)s_%(column_0_name)s',
        'uq': 'uq_%(table_name)s_%(column_0_name)s',
        'ix': 'ix_%(column_0_label)s',
    }

    metadata = schema.MetaData(naming_convention=naming_convention)

    def serialize(self, columns: list = None) -> types.OrderedMap:
        """
        Serializes the entity to an ordered mapping.

        Args:
            columns: An optional list of column names to serialize

        Returns:
            The entity columns/values pairs
        """
        columns = columns or [column.name for column in self.__table__.columns]

        return types.OrderedMap((str(column), getattr(self, column))
                                for column in columns)


class State(Entity):
    """Entity class for states."""

    _name = 'state'

    __table__ = schema.Table(
        'states',
        Entity.metadata,
        schema.Column('id',
                      sql_types.SmallInteger,
                      nullable=False,
                      primary_key=True),
        schema.Column('name',
                      sql_types.String(32),
                      nullable=False,
                      index=True))

    # Relationships
    mesoregions = orm.relationship('Mesoregion', back_populates='state')
    microregions = orm.relationship('Microregion', back_populates='state')
    municipalities = orm.relationship('Municipality', back_populates='state')
    districts = orm.relationship('District', back_populates='state')
    subdistricts = orm.relationship('Subdistrict', back_populates='state')


class Mesoregion(Entity):
    """Entity class for mesoregions."""

    _name = 'mesoregion'

    __table__ = schema.Table(
        'mesoregions',
        Entity.metadata,
        schema.Column('id',
                      sql_types.SmallInteger,
                      nullable=False,
                      primary_key=True),
        schema.Column('state_id',
                      sql_types.SmallInteger,
                      schema.ForeignKey('states.id', use_alter=True),
                      nullable=False,
                      index=True),
        schema.Column('name',
                      sql_types.String(64),
                      nullable=False,
                      index=True))

    # Relationships
    state = orm.relationship('State', back_populates='mesoregions')
    microregions =\
        orm.relationship('Microregion', back_populates='mesoregion')
    municipalities =\
        orm.relationship('Municipality', back_populates='mesoregion')
    districts = orm.relationship('District', back_populates='mesoregion')
    subdistricts =\
        orm.relationship('Subdistrict', back_populates='mesoregion')


class Microregion(Entity):
    """Entity class for microregions."""

    _name = 'microregion'

    __table__ = schema.Table(
        'microregions',
        Entity.metadata,
        schema.Column('id',
                      sql_types.Integer,
                      nullable=False,
                      primary_key=True),
        schema.Column('mesoregion_id',
                      sql_types.SmallInteger,
                      schema.ForeignKey('mesoregions.id', use_alter=True),
                      nullable=False,
                      index=True),
        schema.Column('state_id',
                      sql_types.SmallInteger,
                      schema.ForeignKey('states.id', use_alter=True),
                      nullable=False,
                      index=True),
        schema.Column('name',
                      sql_types.String(64),
                      nullable=False,
                      index=True))

    # Relationships
    state = orm.relationship('State', back_populates='microregions')
    mesoregion = orm.relationship('Mesoregion', back_populates='microregions')
    municipalities =\
        orm.relationship('Municipality', back_populates='microregion')
    districts = orm.relationship('District', back_populates='microregion')
    subdistricts =\
        orm.relationship('Subdistrict', back_populates='microregion')


class Municipality(Entity):
    """Entity class for municipalities."""

    _name = 'municipality'

    __table__ = schema.Table(
        'municipalities',
        Entity.metadata,
        schema.Column('id',
                      sql_types.Integer,
                      nullable=False,
                      primary_key=True),
        schema.Column('microregion_id',
                      sql_types.Integer,
                      schema.ForeignKey('microregions.id', use_alter=True),
                      nullable=False,
                      index=True),
        schema.Column('mesoregion_id',
                      sql_types.SmallInteger,
                      schema.ForeignKey('mesoregions.id', use_alter=True),
                      nullable=False,
                      index=True),
        schema.Column('state_id',
                      sql_types.SmallInteger,
                      schema.ForeignKey('states.id', use_alter=True),
                      nullable=False,
                      index=True),
        schema.Column('name',
                      sql_types.String(64),
                      nullable=False,
                      index=True))

    # Relationships
    state = orm.relationship('State', back_populates='municipalities')
    mesoregion =\
        orm.relationship('Mesoregion', back_populates='municipalities')
    microregion =\
        orm.relationship('Microregion', back_populates='municipalities')
    districts = orm.relationship('District', back_populates='municipality')
    subdistricts =\
        orm.relationship('Subdistrict', back_populates='municipality')


class District(Entity):
    """Entity class for districts."""

    _name = 'district'

    __table__ = schema.Table(
        'districts',
        Entity.metadata,
        schema.Column('id',
                      sql_types.Integer,
                      nullable=False,
                      primary_key=True),
        schema.Column('municipality_id',
                      sql_types.Integer,
                      schema.ForeignKey('municipalities.id', use_alter=True),
                      nullable=False,
                      index=True),
        schema.Column('microregion_id',
                      sql_types.Integer,
                      schema.ForeignKey('microregions.id', use_alter=True),
                      nullable=False,
                      index=True),
        schema.Column('mesoregion_id',
                      sql_types.SmallInteger,
                      schema.ForeignKey('mesoregions.id', use_alter=True),
                      nullable=False,
                      index=True),
        schema.Column('state_id',
                      sql_types.SmallInteger,
                      schema.ForeignKey('states.id', use_alter=True),
                      nullable=False,
                      index=True),
        schema.Column('name',
                      sql_types.String(64),
                      nullable=False,
                      index=True))

    # Relationships
    state = orm.relationship('State', back_populates='districts')
    mesoregion = orm.relationship('Mesoregion', back_populates='districts')
    microregion = orm.relationship('Microregion', back_populates='districts')
    municipality =\
        orm.relationship('Municipality', back_populates='districts')
    subdistricts = orm.relationship('Subdistrict', back_populates='district')


class Subdistrict(Entity):
    """Entity class for subdistricts."""

    _name = 'subdistrict'

    __table__ = schema.Table(
        'subdistricts',
        Entity.metadata,
        schema.Column('id',
                      sql_types.BigInteger,
                      nullable=False,
                      primary_key=True),
        schema.Column('district_id',
                      sql_types.Integer,
                      schema.ForeignKey('districts.id', use_alter=True),
                      nullable=False,
                      index=True),
        schema.Column('municipality_id',
                      sql_types.Integer,
                      schema.ForeignKey('municipalities.id', use_alter=True),
                      nullable=False,
                      index=True),
        schema.Column('microregion_id',
                      sql_types.Integer,
                      schema.ForeignKey('microregions.id', use_alter=True),
                      nullable=False,
                      index=True),
        schema.Column('mesoregion_id',
                      sql_types.SmallInteger,
                      schema.ForeignKey('mesoregions.id', use_alter=True),
                      nullable=False,
                      index=True),
        schema.Column('state_id',
                      sql_types.SmallInteger,
                      schema.ForeignKey('states.id', use_alter=True),
                      nullable=False,
                      index=True),
        schema.Column('name',
                      sql_types.String(64),
                      nullable=False,
                      index=True))

    # Relationships
    state = orm.relationship('State', back_populates='subdistricts')
    mesoregion = orm.relationship('Mesoregion', back_populates='subdistricts')
    microregion =\
        orm.relationship('Microregion', back_populates='subdistricts')
    municipality =\
        orm.relationship('Municipality', back_populates='subdistricts')
    district = orm.relationship('District', back_populates='subdistricts')


# Constants

ENTITIES = (State, Mesoregion, Microregion, Municipality, District, Subdistrict)
TABLES = tuple(entity.__table__.name for entity in ENTITIES)
