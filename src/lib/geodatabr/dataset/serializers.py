#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
Dataset serialization module

This module provides the serializers classes used to export the dataset.
'''
# Imports

# Package dependencies

from geodatabr.core.helpers.decorators import cachedmethod
from geodatabr.core.types import OrderedMap
from geodatabr.core.i18n import _, Translator
from geodatabr.dataset.schema import Entities
from geodatabr.dataset.repositories import StateRepository

# Translator setup

Translator.load('dataset')

# Classes


class BaseSerializer(object):
    '''
    Abstract serializer class.
    '''

    @property
    @cachedmethod()
    def __records__(self):
        '''
        Retrieves the dataset records.

        Returns:
            geodatabr.core.types.OrderedMap: The dataset records
        '''
        records = OrderedMap(states=StateRepository().loadAll())

        for _entity in Entities:
            entity = _entity.__table__.name

            if entity not in records:
                records[entity] = [item
                                   for state in records.states
                                   for item in getattr(state, entity)]

        return records

    def __init__(self, **options):
        '''
        Setup the serializer.

        Args:
            options (dict): The serialization options
        '''
        self._options = OrderedMap(options)

    def serialize(self):
        '''
        Abstract serialization method.
        '''
        raise NotImplementedError


class Serializer(BaseSerializer):
    '''
    Default serialization implementation.
    '''

    def __init__(self,
                 localize=True,
                 forceStr=False,
                 forceStrKeys=False,
                 includeKey=False):
        '''
        Setup the serializer.

        Args:
            localize (bool): Whether or not it should localize dictionary keys
            forceStr (bool):
                Whether or not it should coerce mapping values to string
            forceStrKeys (bool):
                Whether or not it should coerce mapping keys to string
            includeKey (bool): Whether or not it should include the primary key
        '''
        super().__init__(localize=localize,
                         forceStr=forceStr,
                         forceStrKeys=forceStrKeys,
                         includeKey=includeKey)

    @cachedmethod()
    def serialize(self):
        '''
        Serializes the dataset records.

        Returns:
            geodatabr.core.types.OrderedMap:
                The serialized dataset records mapping
        '''
        records = OrderedMap()

        for entity in Entities:
            table = str(entity.__table__.name)
            _records = self.__records__[table]

            if not _records:
                continue

            if self._options.localize:
                table = _(table)

            records[table] = OrderedMap()

            for _record in _records:
                _record = _record.serialize()
                record = OrderedMap()

                for column in entity.__table__.columns:
                    column = str(column.name)
                    value = _record[column]

                    if self._options.localize:
                        column = _(column)

                    record[column] = str(value) if self._options.forceStr else value

                row_id = str(record.id) if self._options.forceStrKeys else record.id

                if not self._options.includeKey:
                    del record.id

                records[table][row_id] = record

        return records


class FlattenedSerializer(BaseSerializer):
    '''
    Flattened serialization implementation.
    '''

    @cachedmethod()
    def serialize(self):
        '''
        Serializes the dataset records.

        Returns:
            list: The serialized dataset records list
        '''
        records = []

        for entity in Entities:
            for record in self.__records__[entity.__table__.name]:
                records.append(OrderedMap(
                    [(_(key), value)
                     for key, value in record.serialize(flatten=True).items()]))

        return sorted(records,
                      key=lambda record: (record.get('state_id') or 0,
                                          record.get('mesoregion_id') or 0,
                                          record.get('microregion_id') or 0,
                                          record.get('municipality_id') or 0,
                                          record.get('district_id') or 0,
                                          record.get('subdistrict_id') or 0))
