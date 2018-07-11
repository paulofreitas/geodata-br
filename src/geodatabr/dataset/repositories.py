#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""
Datasets repositories module.

This module provides the repositories classes used to query the datasets.
"""
# Imports

# External dependencies

from sqlalchemy import orm

# Package dependencies

from geodatabr.core import datasets, types
from geodatabr.dataset import schema

# Classes


class StateRepository(datasets.Repository):
    """
    Implementation of states repository.

    Attributes:
        entity (geodatabr.dataset.schema.State): The repository entity class
    """

    entity = schema.State

    @classmethod
    def add(cls, instance: schema.State):
        """
        Saves a State instance.

        Args:
            instance: The State instance to save
        """
        super().add(instance)

    @classmethod
    def count(cls) -> int:
        """
        Returns the total states count.

        Returns:
            The total states count
        """
        return super().count()

    @classmethod
    def findAll(cls) -> types.List:
        """
        Retrieves all states.

        Returns:
            A list with all states
        """
        return super().findAll()

    @classmethod
    def loadAll(cls) -> types.List:
        """
        Retrieves all states with relationships loaded.

        Returns:
            A list with all states with relationships loaded
        """
        state = cls.entity

        return types.List(
            cls.db.query(state)
            .options(orm.subqueryload(state.mesoregions),
                     orm.subqueryload(state.microregions),
                     orm.subqueryload(state.municipalities),
                     orm.subqueryload(state.districts),
                     orm.subqueryload(state.subdistricts))
            .all())

    @classmethod
    def findById(cls, _id: int) -> schema.State:
        """
        Retrieves a single state by ID.

        Args:
            _id: The state ID

        Returns:
            The state record
        """
        return super().findById(_id)

    @classmethod
    def findByName(cls, name: str) -> schema.State:
        """
        Retrieves a single state by name.

        Args:
            name: The state name

        Returns:
            The state record
        """
        return super().findByName(name)

    @classmethod
    def delete(cls):
        """Removes all states."""
        super().delete()


class MesoregionRepository(datasets.Repository):
    """
    Implementation of mesoregions repository.

    Attributes:
        entity (geodatabr.dataset.schema.Mesoregion):
            The repository entity class
    """

    entity = schema.Mesoregion

    @classmethod
    def add(cls, instance: schema.Mesoregion):
        """
        Saves a Mesoregion instance.

        Args:
            instance: The Mesoregion instance to save
        """
        super().add(instance)

    @classmethod
    def count(cls) -> int:
        """
        Returns the total mesoregions count.

        Returns:
            The total mesoregions count
        """
        return super().count()

    @classmethod
    def findAll(cls) -> types.List:
        """
        Retrieves all mesoregions.

        Returns:
            A list with all mesoregions
        """
        return super().findAll()

    @classmethod
    def loadAll(cls) -> types.List:
        """
        Retrieves all mesoregions with relationships loaded.

        Returns:
            A list with all mesoregions with relationships loaded
        """
        mesoregion = cls.entity

        return types.List(
            cls.db.query(mesoregion)
            .options(orm.subqueryload(mesoregion.microregions),
                     orm.subqueryload(mesoregion.municipalities),
                     orm.subqueryload(mesoregion.districts),
                     orm.subqueryload(mesoregion.subdistricts))
            .all())

    @classmethod
    def findById(cls, _id: int) -> schema.Mesoregion:
        """
        Retrieves a single mesoregion by ID.

        Args:
            _id: The mesoregion ID

        Returns:
            The mesoregion record
        """
        return super().findById(_id)

    @classmethod
    def findByName(cls, name: str) -> schema.Mesoregion:
        """
        Retrieves a single mesoregion by name.

        Args:
            name: The mesoregion name

        Returns:
            The mesoregion record
        """
        return super().findByName(name)

    @classmethod
    def delete(cls):
        """Removes all mesoregions."""
        super().delete()


class MicroregionRepository(datasets.Repository):
    """
    Implementation of microregions repository.

    Attributes:
        entity (geodatabr.dataset.schema.Microregion):
            The repository entity class
    """

    entity = schema.Microregion

    @classmethod
    def add(cls, instance: schema.Microregion):
        """
        Saves a Microregion instance.

        Args:
            instance: The Microregion instance to save
        """
        super().add(instance)

    @classmethod
    def count(cls) -> int:
        """
        Returns the total microregions count.

        Returns:
            The total microregions count
        """
        return super().count()

    @classmethod
    def findAll(cls) -> types.List:
        """
        Retrieves all microregions.

        Returns:
            A list with all microregions
        """
        return super().findAll()

    @classmethod
    def loadAll(cls) -> types.List:
        """
        Retrieves all microregions with relationships loaded.

        Returns:
            A list with all microregions with relationships loaded
        """
        microregion = cls.entity

        return types.List(
            cls.db.query(microregion)
            .options(orm.subqueryload(microregion.municipalities),
                     orm.subqueryload(microregion.districts),
                     orm.subqueryload(microregion.subdistricts))
            .all())

    @classmethod
    def findById(cls, _id: int) -> schema.Microregion:
        """
        Retrieves a single microregion by ID.

        Args:
            _id: The microregion ID

        Returns:
            The microregion record
        """
        return super().findById(_id)

    @classmethod
    def findByName(cls, name: str) -> schema.Microregion:
        """
        Retrieves a single microregion by name.

        Args:
            name: The microregion name

        Returns:
            The microregion record
        """
        return super().findByName(name)

    @classmethod
    def delete(cls):
        """Removes all microregions."""
        super().delete()


class MunicipalityRepository(datasets.Repository):
    """
    Implementation of municipalities repository.

    Attributes:
        entity (geodatabr.dataset.schema.Municipality):
            The repository entity class
    """

    entity = schema.Municipality

    @classmethod
    def add(cls, instance: schema.Municipality):
        """
        Saves a Municipality instance.

        Args:
            instance: The Municipality instance to save
        """
        super().add(instance)

    @classmethod
    def count(cls) -> int:
        """
        Returns the total municipalities count.

        Returns:
            The total municipalities count
        """
        return super().count()

    @classmethod
    def findAll(cls) -> types.List:
        """
        Retrieves all municipalities.

        Returns:
            A list with all municipalities
        """
        return super().findAll()

    @classmethod
    def loadAll(cls) -> types.List:
        """
        Retrieves all municipalities with relationships loaded.

        Returns:
            A list with all municipalities with relationships loaded
        """
        municipality = cls.entity

        return types.List(
            cls.db.query(municipality)
            .options(orm.subqueryload(municipality.districts),
                     orm.subqueryload(municipality.subdistricts))
            .all())

    @classmethod
    def findById(cls, _id: int) -> schema.Municipality:
        """
        Retrieves a single municipality by ID.

        Args:
            _id: The municipality ID

        Returns:
            The municipality record
        """
        return super().findById(_id)

    @classmethod
    def findByName(cls, name: str) -> schema.Municipality:
        """
        Retrieves a single municipality by name.

        Args:
            name: The municipality name

        Returns:
            The municipality record
        """
        return super().findByName(name)

    @classmethod
    def delete(cls):
        """Removes all municipalities."""
        super().delete()


class DistrictRepository(datasets.Repository):
    """
    Implementation of districts repository.

    Attributes:
        entity (geodatabr.dataset.schema.District):
            The repository entity class
    """

    entity = schema.District

    @classmethod
    def add(cls, instance: schema.District):
        """
        Saves a District instance.

        Args:
            instance: The District instance to save
        """
        super().add(instance)

    @classmethod
    def count(cls) -> int:
        """
        Returns the total districts count.

        Returns:
            The total districts count
        """
        return super().count()

    @classmethod
    def findAll(cls) -> types.List:
        """
        Retrieves all districts.

        Returns:
            A list with all districts
        """
        return super().findAll()

    @classmethod
    def loadAll(cls) -> types.List:
        """
        Retrieves all districts with relationships loaded.

        Returns:
            A list with all districts with relationships loaded
        """
        district = cls.entity

        return types.List(cls.db.query(district)
                          .options(orm.subqueryload(district.subdistricts))
                          .all())

    @classmethod
    def findById(cls, _id: int) -> schema.District:
        """
        Retrieves a single district by ID.

        Args:
            _id: The district ID

        Returns:
            The district record
        """
        return super().findById(_id)

    @classmethod
    def findByName(cls, name: str) -> schema.District:
        """
        Retrieves a single district by name.

        Args:
            name: The district name

        Returns:
            The district record
        """
        return super().findByName(name)

    @classmethod
    def delete(cls):
        """Removes all districts."""
        super().delete()


class SubdistrictRepository(datasets.Repository):
    """
    Implementation of subdistricts repository.

    Attributes:
        entity (geodatabr.dataset.schema.Subdistrict):
            The repository entity class
    """

    entity = schema.Subdistrict

    @classmethod
    def add(cls, instance: schema.Subdistrict):
        """
        Saves a Subdistrict instance.

        Args:
            instance: The Subdistrict instance to save
        """
        super().add(instance)

    @classmethod
    def count(cls) -> int:
        """
        Returns the total subdistricts count.

        Returns:
            The total subdistricts count
        """
        return super().count()

    @classmethod
    def findAll(cls) -> types.List:
        """
        Retrieves all subdistricts.

        Returns:
            A list with all subdistricts
        """
        return super().findAll()

    @classmethod
    def findById(cls, _id: int) -> schema.Subdistrict:
        """
        Retrieves a single subdistrict by ID.

        Args:
            _id: The subdistrict ID

        Returns:
            The subdistrict record
        """
        return super().findById(_id)

    @classmethod
    def findByName(cls, name: str) -> schema.Subdistrict:
        """
        Retrieves a single subdistrict by name.

        Args:
            name: The subdistrict name

        Returns:
            The subdistrict record
        """
        return super().findByName(name)

    @classmethod
    def delete(cls):
        """Removes all subdistricts."""
        super().delete()
