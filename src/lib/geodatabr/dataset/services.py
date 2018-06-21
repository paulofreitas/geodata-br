#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""
Dataset services module.

This module provides the services that are used to create the dataset.
"""
# Imports

# Built-in dependencies

import logging
from urllib import parse

# External dependencies

import ratelimit
import requests
from requests import adapters, exceptions, models
from requests.packages.urllib3.util import retry

# Package dependencies

from geodatabr import __meta__
from geodatabr.core import types

# Logging setup

logging.getLogger('requests').setLevel(logging.ERROR)

# Settings

HTTP_MAX_RETRIES = 5
HTTP_BACKOFF_FACTOR = 0.5
HTTP_RETRY_STATUSES = (500, 502, 503, 504)
HTTP_THROTTLING_INTERVAL = 5
HTTP_CONNECT_TIMEOUT = 3
HTTP_READ_TIMEOUT = 5

# Constants

SIDRA_STATE = 3
SIDRA_MESOREGION = 8
SIDRA_MICROREGION = 9
SIDRA_MUNICIPALITY = 6
SIDRA_DISTRICT = 10
SIDRA_SUBDISTRICT = 11

# Classes


class HttpSession(requests.Session):
    """Custom HTTP session implementation."""

    def __init__(self, base_url: str, *args, **kwargs):
        """
        Creates a new HTTP session instance.

        Args:
            base_url: The base URL for this HTTP session
            *args: The optional positional arguments
            **kwargs: The optional keyword arguments
        """
        super().__init__(*args, **kwargs)
        self._base_url = base_url

        # Custom headers
        self.headers.update({
            'User-Agent': 'geodatabr/{version} ({url})'
                          .format(version=__meta__.__version__,
                                  url=__meta__.__url__),
        })

        # Automatic retries
        for protocol in ('http://', 'https://'):
            self.mount(protocol, adapters.HTTPAdapter(
                max_retries=retry.Retry(total=HTTP_MAX_RETRIES,
                                        backoff_factor=HTTP_BACKOFF_FACTOR,
                                        status_forcelist=HTTP_RETRY_STATUSES)))

    @ratelimit.sleep_and_retry
    @ratelimit.limits(calls=1, period=HTTP_THROTTLING_INTERVAL)
    def request(self, method: str, url: str, **kwargs) -> models.Response:
        """
        HTTP throttled requests with custom timeouts.

        Args:
            method: The HTTP method for this request
            url: The target URL of this request
            **kwargs: The optional request keyword arguments

        Returns:
            The HTTP response object
        """
        if kwargs.get('timeout') is None:
            kwargs.update(timeout=(HTTP_CONNECT_TIMEOUT, HTTP_READ_TIMEOUT))

        response = super().request(method,
                                   parse.urljoin(self._base_url, url),
                                   **kwargs)
        response.raise_for_status()

        return response


class SidraApi(object):
    """Main service to query the SIDRA API."""

    def __init__(self):
        """Creates a new SidraApi instance."""
        self._session = HttpSession('http://api.sidra.ibge.gov.br')

    def query(self, params: str) -> 'SidraApiResponse':
        """
        Runs a query over the API.

        Args:
            params: The query params

        Returns:
            The SidraApiResponse instance
        """
        return SidraApiResponse(self._session.get('/values' + params).json())


class SidraApiResponse(object):
    """Response object returned by SidraApi service."""

    def __init__(self, data: dict):
        """
        Creates a new instance.

        Args:
            data: The API JSON response
        """
        self._data = data

    def get(self, keys: list = None) -> list:
        """
        Retrieves the API response records.

        Args:
            keys: The response records keys to retrieve

        Returns:
            The API response records

        Raises:
            KeyError: When a given record key is not valid
        """
        records = []

        for _record in self._data:
            record = []

            if not keys:
                keys = _record.keys()

            for key in keys:
                if key not in _record:
                    raise KeyError('Invalid key')

                record.append(_record[key])

            records.append(record)

        return records


class SidraDataset(object):
    """Main service to query the SIDRA database of geographic territories."""

    def __init__(self):
        """Creates a new SidraDataset instance."""
        self._session = HttpSession('https://sidra.ibge.gov.br')

    def findAll(self, level: int) -> 'SidraDatasetResponse':
        """
        Finds all geographic territories for a given territorial level.

        Args:
            level: The territorial level constant

        Returns:
            The list of geographic territories
        """
        try:
            records = self._session \
                .get('/Territorio/Unidades', params={'nivel': level}) \
                .json()
        except exceptions.RequestException:
            records = {}

        return SidraDatasetResponse(records)

    def findChildren(self,
                     child_level: int,
                     parent_level: int,
                     parent_id: int):
        """
        Finds all geographic territories belonging to a parent territory.

        Args:
            child_level: The children territorial level
            parent_level: The parent territorial level
            parent_id: The parent territory ID

        Returns:
            The list of geographic territories
        """
        try:
            records = self._session \
                .get('/Territorio/UnidadesAbrangidas',
                     params={'abrangido': child_level,
                             'abrangente': parent_level,
                             'unidade': parent_id}) \
                .json()
        except exceptions.RequestException:
            records = {}

        return SidraDatasetResponse(records)


class SidraDatasetResponse(list):
    """Response object returned by SidraDataset service."""

    def __init__(self, data: dict):
        """
        Creates a new instance.

        Args:
            data: The API JSON response
        """
        super().__init__([
            types.Map(id=_id, name=name)
            for (_id, name) in zip(data['Codigos'], data['Nomes'])
        ])
