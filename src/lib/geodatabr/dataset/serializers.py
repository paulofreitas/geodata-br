#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""
Dataset serialization module.

This module provides the serializers classes used to export the dataset.
"""
# Imports

# Built-in dependencies

from typing import Any

# Package dependencies

from geodatabr.core import decorators, i18n, types
from geodatabr.dataset import repositories, schema

# Classes


class BaseSerializer(object):
    """Abstract serializer class."""

    @property
    @decorators.cachedmethod()
    def __records__(self) -> types.OrderedMap:
        """
        Retrieves the dataset records.

        Returns:
            The dataset records
        """
        records = types.OrderedMap(
            states=repositories.StateRepository.loadAll())

        for entity in schema.ENTITIES:
            table = entity.__table__.name

            if table not in records:
                records[table] = types.List([item
                                             for state in records.states
                                             for item in getattr(state,
                                                                 table)])

        return records

    def __init__(self, **options):
        """
        Setup the serializer.

        Args:
            **options: The serialization options
        """
        self._options = types.OrderedMap(options)

    def serialize(self) -> Any:
        """
        Abstract serialization method.
        """
        raise NotImplementedError


class Serializer(BaseSerializer):
    """Default serialization implementation."""

    def __init__(self,
                 localize: bool = True,
                 forceStr: bool = False):
        """
        Setup the serializer.

        Args:
            localize: Whether or not it should localize mapping keys
            forceStr: Whether or not it should coerce mapping values to string
        """
        super().__init__(localize=localize,
                         forceStr=forceStr)

    @decorators.cachedmethod()
    def serialize(self) -> types.OrderedMap:
        """
        Serializes the dataset records.

        Returns:
            The serialized dataset records mapping
        """
        records = types.OrderedMap()

        for entity in schema.ENTITIES:
            table = str(entity.__table__.name)
            _records = self.__records__[table]

            if not _records:
                continue

            if self._options.localize:
                table = i18n._(table)

            records[table] = types.List()

            for _record in _records:
                _record = _record.serialize()
                record = types.OrderedMap()

                for column in entity.__table__.columns:
                    column = str(column.name)
                    value = _record[column]

                    if self._options.localize:
                        column = i18n._(column)

                    record[column] = str(value) if self._options.forceStr else value

                records[table].append(record)

        return records


class FlattenedSerializer(BaseSerializer):
    """Flattened serialization implementation."""

    @decorators.cachedmethod()
    def serialize(self) -> types.List:
        """
        Serializes the dataset records.

        Returns:
            The serialized dataset records list
        """
        records = types.List()

        for entity in schema.ENTITIES:
            for record in self.__records__[entity.__table__.name]:
                records.append(types.OrderedMap(
                    [(i18n._(key), value)
                     for key, value in record.serialize(flatten=True).items()]))

        records.sort(key=lambda record: (record.get('state_id') or 0,
                                         record.get('mesoregion_id') or 0,
                                         record.get('microregion_id') or 0,
                                         record.get('municipality_id') or 0,
                                         record.get('district_id') or 0,
                                         record.get('subdistrict_id') or 0))

        return records
