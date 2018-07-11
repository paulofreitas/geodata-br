#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""
Core datasets module.

This module provides the core classes to query and manage the database.
"""
# Imports

# Built-in dependencies

import contextlib
from typing import Iterator

# External dependencies

import sqlalchemy as db
from sqlalchemy import orm as db_orm
from sqlalchemy.engine import base as db_engine
from sqlalchemy.ext import declarative as db_declarative_api
from sqlalchemy.orm import session as db_session
from sqlalchemy.sql import schema as db_schema

# Package dependencies

from geodatabr.core import decorators, i18n, types
from geodatabr.core.utils import io

# Classes


class Database(object):
    """Database service class."""

    @classmethod
    def engine(cls, **options) -> db_engine.Engine:
        """
        Factories a new database engine.

        Args:
            **options: The engine options

        Returns:
            The database engine instance
        """
        return db.create_engine(
            'sqlite:///' + str(io.CacheFile('geodatabr.db')),
            **options)

    @classmethod
    def session(cls) -> db_session.Session:
        """
        Factories a new database session.

        Returns:
            The database session instance
        """
        session = db_orm.sessionmaker(bind=cls.engine())()
        session.execute('PRAGMA foreign_keys = OFF')

        return session

    @classmethod
    @contextlib.contextmanager
    def transaction(cls,
                    session: db_session.Session) -> Iterator[db_session.Session]:
        """
        Provides a transactional context-based database session.

        Args:
            session: The database session instance to wrap

        Yields:
            The wrapped database session instance
        """
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    @classmethod
    def create(cls):
        """Creates the database."""
        io.Directory(io.Path.CACHE_DIR).create(parents=True)
        Entity.metadata.create_all(cls.engine())

    @classmethod
    def clear(cls):
        """Clears the database."""
        Entity.metadata.drop_all(cls.engine())

    @classmethod
    def delete(cls):
        """Removes the database."""
        io.CacheFile('geodatabr.db').unlink()

    @classmethod
    def optimize(cls):
        """Optimizes the database."""
        cls.engine().execute('VACUUM')


class Entity(db_declarative_api.declarative_base()):
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

    metadata = db_schema.MetaData(naming_convention=naming_convention)

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


class Repository(types.AbstractClass):
    """
    Base repository class.

    Attributes:
        db (sqlalchemy.orm.session.Session): The database session instance
        entity (geodatabr.core.datasets.Entity): The entity class
    """

    db = Database.session()
    entity = Entity

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
    def findAll(cls) -> types.List:
        """
        Retrieves all entity items.

        Returns:
            A list with all entity items
        """
        return types.List(cls.db.query(cls.entity).all())

    @classmethod
    def findByCriteria(cls, *criterias) -> types.List:
        """
        Retrieves all entity items that matches the given criterias.

        Args:
            criterias: A list of Criteria objects

        Returns:
            A list with all matching entity items
        """
        query = cls.db.query(cls.entity)

        for criteria in criterias:
            query = criteria.apply(query)

        return types.List(query.all())

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


class Criteria(types.AbstractClass):
    """Base criteria class."""

    @decorators.abstractmethod
    def apply(self, query: db_orm.query.Query):
        """
        Applies a criteria to the given query object.

        Args:
            query: The query object to apply the criteria

        Returns:
            An adjusted query object
        """
        raise NotImplementedError


class Seeder(types.AbstractClass):
    """
    Base database seeder class.

    Attributes:
        db (geodatabr.core.datasets.Database): The database instance
        entity (geodatabr.core.datasets.Entity): The entity class
        repository (geodatabr.core.datasets.Repository): The repository class
    """

    db = Database
    entity = Entity
    repository = Repository

    @classmethod
    @decorators.abstractmethod
    def run(cls):
        """Runs the database seeder."""
        raise NotImplementedError


class Serializer(object):
    """Dataset serializer class."""

    def __init__(self, **options):
        """
        Setup the serializer.

        Args:
            **options: The serialization options
        """
        self._options = types.OrderedMap(
            # Whether or not it should localize mapping keys
            localize=bool(options.get('localize', True)),
            # Whether or not it should coerce mapping values to string
            forceStr=bool(options.get('forceStr', False)),
        )

    @decorators.cachedmethod()
    def serialize(self, entities: Iterator[Entity]) -> types.OrderedMap:
        """
        Serializes the dataset rows.

        Args:
            entities: The list of entities to serialize

        Returns:
            The serialized dataset rows mapping
        """
        rows = types.OrderedMap()

        for entity in entities:
            table_name = str(entity.__table__.name)
            repository = RepositoryFactory.fromEntity(entity)
            _rows = repository.findAll()

            if not _rows:
                continue

            if self._options.localize:
                table_name = i18n._(table_name)

            rows[table_name] = types.List()

            for _row in _rows:
                row = types.OrderedMap()

                for column, value in _row.serialize().items():
                    if self._options.localize:
                        column = i18n._(column)

                    if self._options.forceStr or column == 'name':
                        value = str(value)

                    row[column] = value

                rows[table_name].append(row)

        return rows


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
            geodatabr.core.datasets.UnknownEntityError:
                If a given entity is not supported
        """
        for repository in Repository.childs():
            if repository.entity is entity:
                return repository()

        raise UnknownEntityError(
            'No repository for entity "{}"'.format(entity.__name__))


class SeederFactory(object):
    """Factory class for instantiation of concrete seeder classes."""

    @staticmethod
    def fromEntity(entity: Entity) -> Seeder:
        """
        Factories a seeder class for a given entity class.

        Args:
            entity: The entity class to retrieve a seeder

        Returns:
            The seeder class instance

        Raises:
            geodatabr.core.datasets.UnknownEntityError:
                If a given entity is not supported
        """
        for seeder in Seeder.childs():
            if seeder.entity is entity:
                return seeder()

        raise UnknownEntityError(
            'No seeder for entity "{}"'.format(entity.__name__))


class UnknownEntityError(Exception):
    """
    Exception class raised when a given entity class can not be used to factory
    the subject class.
    """
