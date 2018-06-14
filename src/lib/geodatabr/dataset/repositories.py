#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""
Dataset repositories module.

This module provides the repositories classes used to query the dataset.
"""
# Imports

# External dependencies

from sqlalchemy.orm import subqueryload

# Package dependencies

from geodatabr.core.types import AbstractClass
from geodatabr.dataset import Database
from geodatabr.dataset.schema import \
    State, Mesoregion, Microregion, Municipality, District, Subdistrict

# Classes


class Repository(AbstractClass):
    """Abstract implementation of repository pattern."""

    entity = None

    @classmethod
    def add(cls, instance):
        """
        Saves an entity instance.

        Args:
            instance (geodatabr.dataset.schema.Entity):
                The entity instance to save
        """
        Database.add(instance)

    @classmethod
    def count(cls):
        """
        Returns the total entity items count.

        Returns:
            int: The total entity items count
        """
        return Database.query(cls.entity).count()

    @classmethod
    def findAll(cls):
        """
        Retrieves all entity items.

        Returns:
            list: A list with all entity items
        """
        return Database.query(cls.entity).all()

    @classmethod
    def findById(cls, _id):
        """
        Retrieves a single entity item by ID.

        Args:
            _id (int): The entity item ID

        Returns:
            geodatabr.dataset.schema.Entity: An entity item
        """
        return Database.query(cls.entity) \
            .filter(cls.entity.id == _id) \
            .first()

    @classmethod
    def findByName(cls, name):
        """
        Retrieves a single entity item by name.

        Args:
            name (str): The entity item name

        Returns:
            geodatabr.dataset.schema.Entity: An entity item
        """
        return Database.query(cls.entity) \
            .filter(cls.entity.name == name) \
            .first()

    @classmethod
    def delete(cls):
        """Removes all entity items."""
        Database.query(cls.entity).delete()


class StateRepository(Repository):
    """Implementation of states repository."""

    entity = State

    @classmethod
    def add(cls, instance):
        """
        Saves a State instance.

        Args:
            instance (geodatabr.dataset.schema.State):
                The State instance to save
        """
        super().add(instance)

    @classmethod
    def count(cls):
        """
        Returns the total states count.

        Returns:
            int: The total states count
        """
        return super().count()

    @classmethod
    def findAll(cls):
        """
        Retrieves all states.

        Returns:
            list: A list with all states
        """
        return super().findAll()

    @classmethod
    def loadAll(cls):
        """
        Retrieves all states with relationships loaded.

        Returns:
            list: A list with all states with relationships loaded
        """
        return Database.query(State) \
            .options(subqueryload(State.mesoregions),
                     subqueryload(State.microregions),
                     subqueryload(State.municipalities),
                     subqueryload(State.districts),
                     subqueryload(State.subdistricts)) \
            .all()

    @classmethod
    def findById(cls, _id):
        """
        Retrieves a single state by ID.

        Args:
            _id (int): The state ID

        Returns:
            geodatabr.dataset.schema.State: The state record
        """
        return super().findById(_id)

    @classmethod
    def findByName(cls, name):
        """
        Retrieves a single state by name.

        Args:
            name (str): The state name

        Returns:
            geodatabr.dataset.schema.State: The state record
        """
        return super().findByName(name)

    @classmethod
    def delete(cls):
        """Removes all states."""
        super().delete()


class MesoregionRepository(Repository):
    """Implementation of mesoregions repository."""

    entity = Mesoregion

    @classmethod
    def add(cls, instance):
        """
        Saves a Mesoregion instance.

        Args:
            instance (geodatabr.dataset.schema.Mesoregion):
                The Mesoregion instance to save
        """
        super().add(instance)

    @classmethod
    def count(cls):
        """
        Returns the total mesoregions count.

        Returns:
            int: The total mesoregions count
        """
        return super().count()

    @classmethod
    def findAll(cls):
        """
        Retrieves all mesoregions.

        Returns:
            list: A list with all mesoregions
        """
        return super().findAll()

    @classmethod
    def loadAll(cls):
        """
        Retrieves all mesoregions with relationships loaded.

        Returns:
            list: A list with all mesoregions with relationships loaded
        """
        return Database.query(Mesoregion) \
            .options(subqueryload(Mesoregion.microregions),
                     subqueryload(Mesoregion.municipalities),
                     subqueryload(Mesoregion.districts),
                     subqueryload(Mesoregion.subdistricts)) \
            .all()

    @classmethod
    def findById(cls, _id):
        """
        Retrieves a single mesoregion by ID.

        Args:
            _id (int): The mesoregion ID

        Returns:
            geodatabr.dataset.schema.Mesoregion: The mesoregion record
        """
        return super().findById(_id)

    @classmethod
    def findByName(cls, name):
        """
        Retrieves a single mesoregion by name.

        Args:
            name (str): The mesoregion name

        Returns:
            geodatabr.dataset.schema.Mesoregion: The mesoregion record
        """
        return super().findByName(name)

    @classmethod
    def delete(cls):
        """Removes all mesoregions."""
        super().delete()


class MicroregionRepository(Repository):
    """Implementation of microregions repository."""

    entity = Microregion

    @classmethod
    def add(cls, instance):
        """
        Saves a Microregion instance.

        Args:
            instance (geodatabr.dataset.schema.Microregion):
                The Microregion instance to save
        """
        super().add(instance)

    @classmethod
    def count(cls):
        """
        Returns the total microregions count.

        Returns:
            int: The total microregions count
        """
        return super().count()

    @classmethod
    def findAll(cls):
        """
        Retrieves all microregions.

        Returns:
            list: A list with all microregions
        """
        return super().findAll()

    @classmethod
    def loadAll(cls):
        """
        Retrieves all microregions with relationships loaded.

        Returns:
            list: A list with all microregions with relationships loaded
        """
        return Database.query(Microregion) \
            .options(subqueryload(Microregion.municipalities),
                     subqueryload(Microregion.districts),
                     subqueryload(Microregion.subdistricts)) \
            .all()

    @classmethod
    def findById(cls, _id):
        """
        Retrieves a single microregion by ID.

        Args:
            _id (int): The microregion ID

        Returns:
            geodatabr.dataset.schema.Microregion: The microregion record
        """
        return super().findById(_id)

    @classmethod
    def findByName(cls, name):
        """
        Retrieves a single microregion by name.

        Args:
            name (str): The microregion name

        Returns:
            geodatabr.dataset.schema.Microregion: The microregion record
        """
        return super().findByName(name)

    @classmethod
    def delete(cls):
        """Removes all microregions."""
        super().delete()


class MunicipalityRepository(Repository):
    """Implementation of municipalities repository."""

    entity = Municipality

    @classmethod
    def add(cls, instance):
        """
        Saves a Municipality instance.

        Args:
            instance (geodatabr.dataset.schema.Municipality):
                The Municipality instance to save
        """
        super().add(instance)

    @classmethod
    def count(cls):
        """
        Returns the total municipalities count.

        Returns:
            int: The total municipalities count
        """
        return super().count()

    @classmethod
    def findAll(cls):
        """
        Retrieves all municipalities.

        Returns:
            list: A list with all municipalities
        """
        return super().findAll()

    @classmethod
    def loadAll(cls):
        """
        Retrieves all municipalities with relationships loaded.

        Returns:
            list: A list with all municipalities with relationships loaded
        """
        return Database.query(Municipality) \
            .options(subqueryload(Municipality.districts),
                     subqueryload(Municipality.subdistricts)) \
            .all()

    @classmethod
    def findById(cls, _id):
        """
        Retrieves a single municipality by ID.

        Args:
            _id (int): The municipality ID

        Returns:
            geodatabr.dataset.schema.Municipality: The municipality record
        """
        return super().findById(_id)

    @classmethod
    def findByName(cls, name):
        """
        Retrieves a single municipality by name.

        Args:
            name (str): The municipality name

        Returns:
            geodatabr.dataset.schema.Municipality: The municipality record
        """
        return super().findByName(name)

    @classmethod
    def delete(cls):
        """Removes all municipalities."""
        super().delete()


class DistrictRepository(Repository):
    """Implementation of districts repository."""

    entity = District

    @classmethod
    def add(cls, instance):
        """
        Saves a District instance.

        Args:
            instance (geodatabr.dataset.schema.District):
                The District instance to save
        """
        super().add(instance)

    @classmethod
    def count(cls):
        """
        Returns the total districts count.

        Returns:
            int: The total districts count
        """
        return super().count()

    @classmethod
    def findAll(cls):
        """
        Retrieves all districts.

        Returns:
            list: A list with all districts
        """
        return super().findAll()

    @classmethod
    def loadAll(cls):
        """
        Retrieves all districts with relationships loaded.

        Returns:
            list: A list with all districts with relationships loaded
        """
        return Database.query(District) \
            .options(subqueryload(District.subdistricts)) \
            .all()

    @classmethod
    def findById(cls, _id):
        """
        Retrieves a single district by ID.

        Args:
            _id (int): The district ID

        Returns:
            geodatabr.dataset.schema.District: The district record
        """
        return super().findById(_id)

    @classmethod
    def findByName(cls, name):
        """
        Retrieves a single district by name.

        Args:
            name (str): The district name

        Returns:
            geodatabr.dataset.schema.District: The district record
        """
        return super().findByName(name)

    @classmethod
    def delete(cls):
        """Removes all districts."""
        super().delete()


class SubdistrictRepository(Repository):
    """Implementation of subdistricts repository."""

    entity = Subdistrict

    @classmethod
    def add(cls, instance):
        """
        Saves a Subdistrict instance.

        Args:
            instance (geodatabr.dataset.schema.Subdistrict):
                The Subdistrict instance to save
        """
        super().add(instance)

    @classmethod
    def count(cls):
        """
        Returns the total subdistricts count.

        Returns:
            int: The total subdistricts count
        """
        return super().count()

    @classmethod
    def findAll(cls):
        """
        Retrieves all subdistricts.

        Returns:
            list: A list with all subdistricts
        """
        return super().findAll()

    @classmethod
    def findById(cls, _id):
        """
        Retrieves a single subdistrict by ID.

        Args:
            _id (int): The subdistrict ID

        Returns:
            geodatabr.dataset.schema.Subdistrict: The subdistrict record
        """
        return super().findById(_id)

    @classmethod
    def findByName(cls, name):
        """
        Retrieves a single subdistrict by name.

        Args:
            name (str): The subdistrict name

        Returns:
            geodatabr.dataset.schema.Subdistrict: The subdistrict record
        """
        return super().findByName(name)

    @classmethod
    def delete(cls):
        """Removes all subdistricts."""
        super().delete()


class RepositoryFactory(object):
    """Factory class for instantiation of concrete repositories."""

    @staticmethod
    def fromEntity(entity):
        """
        Factories a repository class for a given entity class.

        Args:
            entity (geodatabr.dataset.schema.Entity):
                The entity class to retrieve a repository

        Returns:
            geodatabr.dataset.repositories.Repository:
                The repository class instance

        Raises:
            geodatabr.dataset.repositories.UnknownEntityError:
                If a given entity is not supported
        """
        for repository in Repository.childs():
            if repository.entity is entity:
                return repository()

        raise UnknownEntityError(
            'No repository for entity "{}"'.format(entity.__name__))


class UnknownEntityError(Exception):
    """
    Exception class raised when a given entity does not belong to any
    repository.
    """
    pass
