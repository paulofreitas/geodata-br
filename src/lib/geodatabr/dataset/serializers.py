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
    def __rows__(self) -> types.OrderedMap:
        """
        Retrieves the dataset rows.

        Returns:
            The dataset rows
        """
        rows = types.OrderedMap(states=repositories.StateRepository.loadAll())

        for entity in schema.ENTITIES:
            table = entity.__table__.name

            if table not in rows:
                rows[table] = types.List([item
                                          for state in rows.states
                                          for item in getattr(state, table)])

        return rows

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
        Serializes the dataset rows.

        Returns:
            The serialized dataset rows mapping
        """
        rows = types.OrderedMap()

        for entity in schema.ENTITIES:
            table = str(entity.__table__.name)
            _rows = self.__rows__[table]

            if not _rows:
                continue

            if self._options.localize:
                table = i18n._(table)

            rows[table] = types.List()

            for _row in _rows:
                _row = _row.serialize()
                row = types.OrderedMap()

                for column in entity.__table__.columns:
                    column = str(column.name)
                    value = _row[column]

                    if self._options.localize:
                        column = i18n._(column)

                    if self._options.forceStr or column == 'name':
                        value = str(value)

                    row[column] = value

                rows[table].append(row)

        return rows


class FlattenedSerializer(BaseSerializer):
    """Flattened serialization implementation."""

    @decorators.cachedmethod()
    def serialize(self) -> types.List:
        """
        Serializes the dataset rows.

        Returns:
            The serialized dataset rows list
        """
        rows = types.List()

        for entity in schema.ENTITIES:
            for row in self.__rows__[entity.__table__.name]:
                rows.append(types.OrderedMap(
                    [(i18n._(key), value)
                     for key, value in row.serialize(flatten=True).items()]))

        rows.sort(key=lambda row: (row.get('state_id') or 0,
                                   row.get('mesoregion_id') or 0,
                                   row.get('microregion_id') or 0,
                                   row.get('municipality_id') or 0,
                                   row.get('district_id') or 0,
                                   row.get('subdistrict_id') or 0))

        return rows
