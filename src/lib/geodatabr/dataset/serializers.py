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

from typing import Iterable

# Package dependencies

from geodatabr.core import decorators, i18n, types
from geodatabr.dataset import repositories, schema

# Classes


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
    def serialize(self, entities: Iterable[schema.Entity]) -> types.OrderedMap:
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
            repository = repositories.RepositoryFactory.fromEntity(entity)
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
