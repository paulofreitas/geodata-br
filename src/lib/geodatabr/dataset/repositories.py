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

from geodatabr.core.types import AbstractClass, List
from geodatabr.dataset import Database
from geodatabr.dataset.schema import Entity, \
    State, Mesoregion, Microregion, Municipality, District, Subdistrict

# Classes


class Repository(AbstractClass):
    """
    Abstract implementation of repository pattern.

    Attributes:
        db (sqlalchemy.orm.session.Session): The database session instance
        entity (geodatabr.dataset.schema.Entity): The repository entity class
    """

    db = Database.session()
    entity = None

    @classmethod
    def add(cls, instance: Entity):
        """
        Saves an entity instance.

        Args:
            instance: The entity instance to save
        """
        cls.db.add(instance)

    @classmethod
    def count(cls) -> int:
        """
        Returns the total entity items count.

        Returns:
            The total entity items count
        """
        return cls.db.query(cls.entity).count()

    @classmethod
    def findAll(cls) -> List:
        """
        Retrieves all entity items.

        Returns:
            A list with all entity items
        """
        return List(cls.db.query(cls.entity).all())

    @classmethod
    def findById(cls, _id: int) -> Entity:
        """
        Retrieves a single entity item by ID.

        Args:
            _id: The entity item ID

        Returns:
            An entity item
        """
        return cls.db.query(cls.entity) \
            .filter(cls.entity.id == _id) \
            .first()

    @classmethod
    def findByName(cls, name: str) -> Entity:
        """
        Retrieves a single entity item by name.

        Args:
            name: The entity item name

        Returns:
            An entity item
        """
        return cls.db.query(cls.entity) \
            .filter(cls.entity.name == name) \
            .first()

    @classmethod
    def delete(cls):
        """Removes all entity items."""
        cls.db.query(cls.entity).delete()


class StateRepository(Repository):
    """
    Implementation of states repository.

    Attributes:
        entity (geodatabr.dataset.schema.State): The repository entity class
    """

    entity = State

    @classmethod
    def add(cls, instance: State):
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
    def findAll(cls) -> List:
        """
        Retrieves all states.

        Returns:
            A list with all states
        """
        return super().findAll()

    @classmethod
    def loadAll(cls) -> List:
        """
        Retrieves all states with relationships loaded.

        Returns:
            A list with all states with relationships loaded
        """
        return List(cls.db.query(State)
                    .options(subqueryload(State.mesoregions),
                             subqueryload(State.microregions),
                             subqueryload(State.municipalities),
                             subqueryload(State.districts),
                             subqueryload(State.subdistricts))
                    .all())

    @classmethod
    def findById(cls, _id: int) -> State:
        """
        Retrieves a single state by ID.

        Args:
            _id: The state ID

        Returns:
            The state record
        """
        return super().findById(_id)

    @classmethod
    def findByName(cls, name: str) -> State:
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


class MesoregionRepository(Repository):
    """
    Implementation of mesoregions repository.

    Attributes:
        entity (geodatabr.dataset.schema.Mesoregion):
            The repository entity class
    """

    entity = Mesoregion

    @classmethod
    def add(cls, instance: Mesoregion):
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
    def findAll(cls) -> List:
        """
        Retrieves all mesoregions.

        Returns:
            A list with all mesoregions
        """
        return super().findAll()

    @classmethod
    def loadAll(cls) -> List:
        """
        Retrieves all mesoregions with relationships loaded.

        Returns:
            A list with all mesoregions with relationships loaded
        """
        return List(cls.db.query(Mesoregion)
                    .options(subqueryload(Mesoregion.microregions),
                             subqueryload(Mesoregion.municipalities),
                             subqueryload(Mesoregion.districts),
                             subqueryload(Mesoregion.subdistricts))
                    .all())

    @classmethod
    def findById(cls, _id: int) -> Mesoregion:
        """
        Retrieves a single mesoregion by ID.

        Args:
            _id: The mesoregion ID

        Returns:
            The mesoregion record
        """
        return super().findById(_id)

    @classmethod
    def findByName(cls, name: str) -> Mesoregion:
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


class MicroregionRepository(Repository):
    """
    Implementation of microregions repository.

    Attributes:
        entity (geodatabr.dataset.schema.Microregion):
            The repository entity class
    """

    entity = Microregion

    @classmethod
    def add(cls, instance: Microregion):
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
    def findAll(cls) -> List:
        """
        Retrieves all microregions.

        Returns:
            A list with all microregions
        """
        return super().findAll()

    @classmethod
    def loadAll(cls) -> List:
        """
        Retrieves all microregions with relationships loaded.

        Returns:
            A list with all microregions with relationships loaded
        """
        return List(cls.db.query(Microregion)
                    .options(subqueryload(Microregion.municipalities),
                             subqueryload(Microregion.districts),
                             subqueryload(Microregion.subdistricts))
                    .all())

    @classmethod
    def findById(cls, _id: int) -> Microregion:
        """
        Retrieves a single microregion by ID.

        Args:
            _id: The microregion ID

        Returns:
            The microregion record
        """
        return super().findById(_id)

    @classmethod
    def findByName(cls, name: str) -> Microregion:
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


class MunicipalityRepository(Repository):
    """
    Implementation of municipalities repository.

    Attributes:
        entity (geodatabr.dataset.schema.Municipality):
            The repository entity class
    """

    entity = Municipality

    @classmethod
    def add(cls, instance: Municipality):
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
    def findAll(cls) -> List:
        """
        Retrieves all municipalities.

        Returns:
            A list with all municipalities
        """
        return super().findAll()

    @classmethod
    def loadAll(cls) -> List:
        """
        Retrieves all municipalities with relationships loaded.

        Returns:
            A list with all municipalities with relationships loaded
        """
        return List(cls.db.query(Municipality)
                    .options(subqueryload(Municipality.districts),
                             subqueryload(Municipality.subdistricts))
                    .all())

    @classmethod
    def findById(cls, _id: int) -> Municipality:
        """
        Retrieves a single municipality by ID.

        Args:
            _id: The municipality ID

        Returns:
            The municipality record
        """
        return super().findById(_id)

    @classmethod
    def findByName(cls, name: str) -> Municipality:
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


class DistrictRepository(Repository):
    """
    Implementation of districts repository.

    Attributes:
        entity (geodatabr.dataset.schema.District):
            The repository entity class
    """

    entity = District

    @classmethod
    def add(cls, instance: District):
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
    def findAll(cls) -> List:
        """
        Retrieves all districts.

        Returns:
            A list with all districts
        """
        return super().findAll()

    @classmethod
    def loadAll(cls) -> List:
        """
        Retrieves all districts with relationships loaded.

        Returns:
            A list with all districts with relationships loaded
        """
        return List(cls.db.query(District)
                    .options(subqueryload(District.subdistricts))
                    .all())

    @classmethod
    def findById(cls, _id: int) -> District:
        """
        Retrieves a single district by ID.

        Args:
            _id: The district ID

        Returns:
            The district record
        """
        return super().findById(_id)

    @classmethod
    def findByName(cls, name: str) -> District:
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


class SubdistrictRepository(Repository):
    """
    Implementation of subdistricts repository.

    Attributes:
        entity (geodatabr.dataset.schema.Subdistrict):
            The repository entity class
    """

    entity = Subdistrict

    @classmethod
    def add(cls, instance: Subdistrict):
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
    def findAll(cls) -> List:
        """
        Retrieves all subdistricts.

        Returns:
            A list with all subdistricts
        """
        return super().findAll()

    @classmethod
    def findById(cls, _id: int) -> Subdistrict:
        """
        Retrieves a single subdistrict by ID.

        Args:
            _id: The subdistrict ID

        Returns:
            The subdistrict record
        """
        return super().findById(_id)

    @classmethod
    def findByName(cls, name: str) -> Subdistrict:
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


class RepositoryFactory(object):
    """Factory class for instantiation of concrete repositories."""

    @staticmethod
    def fromEntity(entity: Entity) -> Repository:
        """
        Factories a repository class for a given entity class.

        Args:
            entity: The entity class to retrieve a repository

        Returns:
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
