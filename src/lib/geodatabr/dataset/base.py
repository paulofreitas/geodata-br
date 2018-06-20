#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""
Dataset base module.

This module provides the core classes to access and manage the database.
"""
# Imports

# External dependencies

from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

# Package dependencies

from geodatabr.core.helpers.filesystem import CacheFile, Directory, Path
from geodatabr.dataset.schema import Entity

# Classes


class Database(object):
    """Database service class."""

    @classmethod
    def engine(cls, **options) -> Engine:
        """
        Factories a new database engine.

        Args:
            **options: The engine options

        Returns:
            The database engine instance
        """
        return create_engine('sqlite:///' + str(CacheFile('geodatabr.db')),
                             **options)

    @classmethod
    def session(cls) -> Session:
        """
        Factories a new database session.

        Returns:
            The database session instance
        """
        return sessionmaker(bind=cls.engine())()

    @classmethod
    def create(cls):
        """Creates the database."""
        Directory(Path.CACHE_DIR).create(parents=True)
        Entity.metadata.create_all(cls.engine())

    @classmethod
    def clear(cls):
        """Clears the database."""
        Entity.metadata.drop_all(cls.engine())

    @classmethod
    def delete(cls):
        """Removes the database."""
        CacheFile('geodatabr.db').unlink()
