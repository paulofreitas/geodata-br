#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
CSV file format package
'''
# Imports

# Package dependencies

from places.core.helpers.decorators import classproperty
from places.formats import Format

# Classes


class CsvFormat(Format):
    '''
    The file format class for CSV file format.
    '''

    @classproperty
    def name(self):
        '''
        The file format name.
        '''
        return 'csv'

    @classproperty
    def friendlyName(self):
        '''
        The file format friendly name.
        '''
        return 'CSV'

    @classproperty
    def extension(self):
        '''
        The file format extension.
        '''
        return '.csv'

    @classproperty
    def type(self):
        '''
        The file format type.
        '''
        return 'Tabular Text'

    @classproperty
    def mimeType(self):
        '''
        The file format media type.
        '''
        return 'text/csv'

    @classproperty
    def info(self):
        '''
        The file format reference info.
        '''
        return 'https://en.wikipedia.org/wiki/Comma-separated_values'

    @classproperty
    def isExportable(self):
        '''
        Tells whether the file format is exportable or not.
        '''
        return True
