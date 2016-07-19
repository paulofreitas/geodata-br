#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Brazilian territorial distribution data exporter

The MIT License (MIT)

Copyright (c) 2013-2016 Paulo Freitas

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''
from __future__ import absolute_import

# -- Imports ------------------------------------------------------------------

# Built-in modules

import collections

# -- Implementation -----------------------------------------------------------


class BaseExporter(object):
    binary_format = False

    '''Base exporter class.'''
    def __init__(self, data, minified=False):
        if type(self) == BaseExporter:
            raise Exception('<BaseExporter> must be subclassed.')

        self._data = data
        self._minified = minified

    def __str__(self):
        raise NotImplementedError

    def __toDict__(self, strKeys=False, unicode=False):
        _dict = collections.OrderedDict()

        for entity in self._data.entities:
            if not self._data._dict[entity.table]:
                continue

            _dict[entity.table] = collections.OrderedDict()

            for row in self._data._dict[entity.table]:
                row_data = collections.OrderedDict()

                for column in entity.columns:
                    row_data[column] = unicode(row[column]) \
                        if unicode and type(row[column]) == str else row[column]

                row_id = str(row_data['id']) if strKeys else row_data['id']
                del row_data['id']
                _dict[entity.table][row_id] = row_data

        return _dict

    @property
    def data(self):
        return self.__str__()
