#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
Dataset base module

This module provides the core classes to access and manage the database.
'''
# Imports

# External dependencies

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Package dependencies

from geodatabr.core.helpers.filesystem import CacheDirectory, CacheFile
from geodatabr.dataset.schema import Entity

# Classes


class DatabaseEngine(object):
    '''
    Database engine factory class.
    '''

    def __new__(cls, **options):
        '''
        Factories a new database engine.

        Args:
            options (dict): The engine options

        Returns:
            sqlalchemy.engine.base.Engine: The database engine
        '''
        return create_engine('sqlite:///' + str(CacheFile('geodatabr.db')),
                             **options)


class DatabaseSession(object):
    '''
    Database session factory class.
    '''

    def __new__(cls):
        '''
        Factories a new database session.

        Returns:
            sqlalchemy.orm.session.Session: The database session
        '''
        return sessionmaker(bind=DatabaseEngine())()


class DatabaseHelper(object):
    '''
    Database helper methods.
    '''

    @staticmethod
    def create():
        '''
        Creates the database.
        '''
        CacheDirectory().create(parents=True)
        Entity.metadata.create_all(Database.bind)

    @staticmethod
    def clear():
        '''
        Clears the database.
        '''
        Entity.metadata.drop_all(Database.bind)

    @staticmethod
    def delete():
        '''
        Removes the database.
        '''
        CacheFile('geodatabr.db').unlink()

# Instances

Database = DatabaseSession()
