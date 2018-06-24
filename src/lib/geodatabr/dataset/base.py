#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""
Dataset base module.

This module provides the core classes to access and manage the database.
"""
# Imports

# Built-in dependencies

import contextlib
from typing import Iterator

# External dependencies

import sqlalchemy as sql
from sqlalchemy import orm as sql_orm
from sqlalchemy.engine import base as sql_engine
from sqlalchemy.orm import session as sql_session

# Package dependencies

from geodatabr.core.utils import filesystem as io
from geodatabr.dataset import schema

# Classes


class Database(object):
    """Database service class."""

    @classmethod
    def engine(cls, **options) -> sql_engine.Engine:
        """
        Factories a new database engine.

        Args:
            **options: The engine options

        Returns:
            The database engine instance
        """
        return sql.create_engine(
            'sqlite:///' + str(io.CacheFile('geodatabr.db')),
            **options)

    @classmethod
    def session(cls) -> sql_session.Session:
        """
        Factories a new database session.

        Returns:
            The database session instance
        """
        session = sql_orm.sessionmaker(bind=cls.engine())()
        session.execute('PRAGMA foreign_keys = OFF')

        return session

    @classmethod
    @contextlib.contextmanager
    def transaction(cls,
                    session: sql_session.Session) -> Iterator[sql_session.Session]:
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
        schema.Entity.metadata.create_all(cls.engine())

    @classmethod
    def clear(cls):
        """Clears the database."""
        schema.Entity.metadata.drop_all(cls.engine())

    @classmethod
    def delete(cls):
        """Removes the database."""
        io.CacheFile('geodatabr.db').unlink()
