#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""
Datasets schema module.

This module provides the entities used to describe the datasets.
"""
# Imports

# External dependencies

from sqlalchemy import orm, types
from sqlalchemy.sql import schema

# Package dependencies

from geodatabr.core import datasets

# Classes


class State(datasets.Entity):
    """Entity class for states."""

    _name = 'state'

    __table__ = schema.Table(
        'states',
        datasets.Entity.metadata,
        schema.Column('id',
                      types.SmallInteger,
                      nullable=False,
                      primary_key=True),
        schema.Column('name',
                      types.String(32),
                      nullable=False,
                      index=True))

    # Relationships
    mesoregions = orm.relationship('Mesoregion', back_populates='state')
    microregions = orm.relationship('Microregion', back_populates='state')
    municipalities = orm.relationship('Municipality', back_populates='state')
    districts = orm.relationship('District', back_populates='state')
    subdistricts = orm.relationship('Subdistrict', back_populates='state')


class Mesoregion(datasets.Entity):
    """Entity class for mesoregions."""

    _name = 'mesoregion'

    __table__ = schema.Table(
        'mesoregions',
        datasets.Entity.metadata,
        schema.Column('id',
                      types.SmallInteger,
                      nullable=False,
                      primary_key=True),
        schema.Column('state_id',
                      types.SmallInteger,
                      schema.ForeignKey('states.id', use_alter=True),
                      nullable=False,
                      index=True),
        schema.Column('name',
                      types.String(64),
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


class Microregion(datasets.Entity):
    """Entity class for microregions."""

    _name = 'microregion'

    __table__ = schema.Table(
        'microregions',
        datasets.Entity.metadata,
        schema.Column('id',
                      types.Integer,
                      nullable=False,
                      primary_key=True),
        schema.Column('mesoregion_id',
                      types.SmallInteger,
                      schema.ForeignKey('mesoregions.id', use_alter=True),
                      nullable=False,
                      index=True),
        schema.Column('state_id',
                      types.SmallInteger,
                      schema.ForeignKey('states.id', use_alter=True),
                      nullable=False,
                      index=True),
        schema.Column('name',
                      types.String(64),
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


class Municipality(datasets.Entity):
    """Entity class for municipalities."""

    _name = 'municipality'

    __table__ = schema.Table(
        'municipalities',
        datasets.Entity.metadata,
        schema.Column('id',
                      types.Integer,
                      nullable=False,
                      primary_key=True),
        schema.Column('microregion_id',
                      types.Integer,
                      schema.ForeignKey('microregions.id', use_alter=True),
                      nullable=False,
                      index=True),
        schema.Column('mesoregion_id',
                      types.SmallInteger,
                      schema.ForeignKey('mesoregions.id', use_alter=True),
                      nullable=False,
                      index=True),
        schema.Column('state_id',
                      types.SmallInteger,
                      schema.ForeignKey('states.id', use_alter=True),
                      nullable=False,
                      index=True),
        schema.Column('name',
                      types.String(64),
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


class District(datasets.Entity):
    """Entity class for districts."""

    _name = 'district'

    __table__ = schema.Table(
        'districts',
        datasets.Entity.metadata,
        schema.Column('id',
                      types.Integer,
                      nullable=False,
                      primary_key=True),
        schema.Column('municipality_id',
                      types.Integer,
                      schema.ForeignKey('municipalities.id', use_alter=True),
                      nullable=False,
                      index=True),
        schema.Column('microregion_id',
                      types.Integer,
                      schema.ForeignKey('microregions.id', use_alter=True),
                      nullable=False,
                      index=True),
        schema.Column('mesoregion_id',
                      types.SmallInteger,
                      schema.ForeignKey('mesoregions.id', use_alter=True),
                      nullable=False,
                      index=True),
        schema.Column('state_id',
                      types.SmallInteger,
                      schema.ForeignKey('states.id', use_alter=True),
                      nullable=False,
                      index=True),
        schema.Column('name',
                      types.String(64),
                      nullable=False,
                      index=True))

    # Relationships
    state = orm.relationship('State', back_populates='districts')
    mesoregion = orm.relationship('Mesoregion', back_populates='districts')
    microregion = orm.relationship('Microregion', back_populates='districts')
    municipality =\
        orm.relationship('Municipality', back_populates='districts')
    subdistricts = orm.relationship('Subdistrict', back_populates='district')


class Subdistrict(datasets.Entity):
    """Entity class for subdistricts."""

    _name = 'subdistrict'

    __table__ = schema.Table(
        'subdistricts',
        datasets.Entity.metadata,
        schema.Column('id',
                      types.BigInteger,
                      nullable=False,
                      primary_key=True),
        schema.Column('district_id',
                      types.Integer,
                      schema.ForeignKey('districts.id', use_alter=True),
                      nullable=False,
                      index=True),
        schema.Column('municipality_id',
                      types.Integer,
                      schema.ForeignKey('municipalities.id', use_alter=True),
                      nullable=False,
                      index=True),
        schema.Column('microregion_id',
                      types.Integer,
                      schema.ForeignKey('microregions.id', use_alter=True),
                      nullable=False,
                      index=True),
        schema.Column('mesoregion_id',
                      types.SmallInteger,
                      schema.ForeignKey('mesoregions.id', use_alter=True),
                      nullable=False,
                      index=True),
        schema.Column('state_id',
                      types.SmallInteger,
                      schema.ForeignKey('states.id', use_alter=True),
                      nullable=False,
                      index=True),
        schema.Column('name',
                      types.String(64),
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
