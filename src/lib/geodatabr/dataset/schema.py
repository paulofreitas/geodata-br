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

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship as Relationship
from sqlalchemy.sql.schema import Column, ForeignKey, MetaData, Table
from sqlalchemy.types import BigInteger, Integer, SmallInteger, String

# Package dependencies

from geodatabr.core.types import OrderedMap

# Classes


class Entity(declarative_base()):
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

    metadata = MetaData(naming_convention=naming_convention)

    def serialize(self, flatten: bool = False) -> OrderedMap:
        """
        Serializes the entity to an ordered mapping.

        Args:
            flatten: Whether it should flatten column names or not

        Returns:
            The entity columns/values pairs
        """
        if not flatten:
            return OrderedMap({column.name: getattr(self, column.name)
                               for column in self.__table__.columns})

        def _flatten(entity):
            flattened = OrderedMap()

            for column in entity.__table__.columns:
                if not column.foreign_keys:
                    flattened[entity._name + '_' + column.name] =\
                        getattr(entity, column.name)

            return flattened

        flattened = OrderedMap()

        for column in reversed(list(self.__table__.columns)):
            for foreign_key in column.foreign_keys:
                for relationship in self.__mapper__.relationships:
                    if relationship.table == foreign_key.column.table:
                        flattened.update(
                            _flatten(getattr(self, relationship.key)))

        flattened.update(_flatten(self))

        return flattened


class State(Entity):
    """Entity class for states."""

    _name = 'state'

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
               index=True))

    # Relationships
    mesoregions = Relationship('Mesoregion', back_populates='state')
    microregions = Relationship('Microregion', back_populates='state')
    municipalities = Relationship('Municipality', back_populates='state')
    districts = Relationship('District', back_populates='state')
    subdistricts = Relationship('Subdistrict', back_populates='state')


class Mesoregion(Entity):
    """Entity class for mesoregions."""

    _name = 'mesoregion'

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
               index=True))

    # Relationships
    state = Relationship('State', back_populates='mesoregions')
    microregions = Relationship('Microregion', back_populates='mesoregion')
    municipalities = Relationship('Municipality', back_populates='mesoregion')
    districts = Relationship('District', back_populates='mesoregion')
    subdistricts = Relationship('Subdistrict', back_populates='mesoregion')


class Microregion(Entity):
    """Entity class for microregions."""

    _name = 'microregion'

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
               index=True))

    # Relationships
    state = Relationship('State', back_populates='microregions')
    mesoregion = Relationship('Mesoregion', back_populates='microregions')
    municipalities = Relationship('Municipality', back_populates='microregion')
    districts = Relationship('District', back_populates='microregion')
    subdistricts = Relationship('Subdistrict', back_populates='microregion')


class Municipality(Entity):
    """Entity class for municipalities."""

    _name = 'municipality'

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
               index=True))

    # Relationships
    state = Relationship('State', back_populates='municipalities')
    mesoregion = Relationship('Mesoregion', back_populates='municipalities')
    microregion = Relationship('Microregion', back_populates='municipalities')
    districts = Relationship('District', back_populates='municipality')
    subdistricts = Relationship('Subdistrict', back_populates='municipality')


class District(Entity):
    """Entity class for districts."""

    _name = 'district'

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
               index=True))

    # Relationships
    state = Relationship('State', back_populates='districts')
    mesoregion = Relationship('Mesoregion', back_populates='districts')
    microregion = Relationship('Microregion', back_populates='districts')
    municipality = Relationship('Municipality', back_populates='districts')
    subdistricts = Relationship('Subdistrict', back_populates='district')


class Subdistrict(Entity):
    """Entity class for subdistricts."""

    _name = 'subdistrict'

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
               index=True))

    # Relationships
    state = Relationship('State', back_populates='subdistricts')
    mesoregion = Relationship('Mesoregion', back_populates='subdistricts')
    microregion = Relationship('Microregion', back_populates='subdistricts')
    municipality = Relationship('Municipality', back_populates='subdistricts')
    district = Relationship('District', back_populates='subdistricts')


# Constants

ENTITIES = (State, Mesoregion, Microregion, Municipality, District, Subdistrict)
