#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
Dataset schema module

This module provides the entities used to describe the database.
'''
# Imports

# Package dependencies

from geodatabr.core.types import OrderedMap

# External dependencies

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey, MetaData, Table
from sqlalchemy.types import BigInteger, Integer, SmallInteger, String

# Aliases

Relationship = lambda entity, backref, **kwargs: \
    relationship(entity, back_populates=backref, **kwargs)

# Classes


class Entity(declarative_base()):
    '''
    Abstract entity class.
    '''
    __abstract__ = True

    naming_convention = {
        'pk': 'pk_%(table_name)s',
        'fk': 'fk_%(table_name)s_%(column_0_name)s',
        'ix': 'ix_%(column_0_label)s',
        'uq': 'uq_%(table_name)s_%(column_0_name)s',
    }

    metadata = MetaData(naming_convention=naming_convention)

    def serialize(self, flatten=False):
        '''
        Serializes the entity to an ordered mapping.

        Args:
            flatten (bool): Whether it should flatten column names or not

        Returns:
            geodatabr.core.types.OrderedMap: The entity columns/values pairs
        '''
        if not flatten:
            return Map({column.name: getattr(self, column.name)
                       for column in self.__table__.columns})

        def _flatten(entity):
            flattened = Map()

            for column in entity.__table__.columns:
                if not column.foreign_keys:
                    flattened[entity.__name__ + '_' + column.name] =\
                        getattr(entity, column.name)

            return flattened

        flattened = Map()

        for column in reversed(list(self.__table__.columns)):
            for foreign_key in column.foreign_keys:
                for relationship in self.__mapper__.relationships:
                    if relationship.table == foreign_key.column.table:
                        flattened.update(
                            _flatten(getattr(self, relationship.key)))

        flattened.update(_flatten(self))

        return flattened


class State(Entity):
    '''
    Entity for states.
    '''
    __name__ = 'state'

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
    mesoregions = Relationship('Mesoregion', 'state')
    microregions = Relationship('Microregion', 'state')
    municipalities = Relationship('Municipality', 'state')
    districts = Relationship('District', 'state')
    subdistricts = Relationship('Subdistrict', 'state')


class Mesoregion(Entity):
    '''
    Entity for mesoregions.
    '''
    __name__ = 'mesoregion'

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
    state = Relationship('State', 'mesoregions')
    microregions = Relationship('Microregion', 'mesoregion')
    municipalities = Relationship('Municipality', 'mesoregion')
    districts = Relationship('District', 'mesoregion')
    subdistricts = Relationship('Subdistrict', 'mesoregion')


class Microregion(Entity):
    '''
    Entity for microregions.
    '''
    __name__ = 'microregion'

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
    state = Relationship('State', 'microregions')
    mesoregion = Relationship('Mesoregion', 'microregions')
    municipalities = Relationship('Municipality', 'microregion')
    districts = Relationship('District', 'microregion')
    subdistricts = Relationship('Subdistrict', 'microregion')


class Municipality(Entity):
    '''
    Entity for municipalities.
    '''
    __name__ = 'municipality'

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
    state = Relationship('State', 'municipalities')
    mesoregion = Relationship('Mesoregion', 'municipalities')
    microregion = Relationship('Microregion', 'municipalities')
    districts = Relationship('District', 'municipality')
    subdistricts = Relationship('Subdistrict', 'municipality')


class District(Entity):
    '''
    Entity for districts.
    '''
    __name__ = 'district'

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
    state = Relationship('State', 'districts')
    mesoregion = Relationship('Mesoregion', 'districts')
    microregion = Relationship('Microregion', 'districts')
    municipality = Relationship('Municipality', 'districts')
    subdistricts = Relationship('Subdistrict', 'district')


class Subdistrict(Entity):
    '''
    Entity for subdistricts.
    '''
    __name__ = 'subdistrict'

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
    state = Relationship('State', 'subdistricts')
    mesoregion = Relationship('Mesoregion', 'subdistricts')
    microregion = Relationship('Microregion', 'subdistricts')
    municipality = Relationship('Municipality', 'subdistricts')
    district = Relationship('District', 'subdistricts')


# Collections

Entities = (State, Mesoregion, Microregion, Municipality, District, Subdistrict)
