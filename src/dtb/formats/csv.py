#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2016 Paulo Freitas
# MIT License (see LICENSE file)
'''
CSV file format module
'''
from __future__ import absolute_import

# Imports

# Package dependencies

from dtb.formats import Format

# Classes


class CsvFormat(Format):
    '''The file format class for CSV file format.'''

    @property
    def name(self):
        '''The file format name.'''
        return 'csv'

    @property
    def friendlyName(self):
        '''The file format friendly name.'''
        return 'CSV'

    @property
    def extension(self):
        '''The file format extension.'''
        return '.csv'

    @property
    def type(self):
        '''The file format type.'''
        return 'Data Interchange'

    @property
    def mimeType(self):
        '''The file format media type.'''
        return 'text/csv'

    @property
    def info(self):
        '''The file format reference info.'''
        return 'https://en.wikipedia.org/wiki/Comma-separated_values'

    def isExportable(self):
        '''Tells whether the file format is exportable or not.'''
        return True

    def isMinifiable(self):
        '''Tells whether the file format is minifiable or not.'''
        return True
