#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
SQLite 3 file format module
'''
# Imports

# Package dependencies

from places.core.helpers.decorators import classproperty
from places.formats import Format

# Classes


class Sqlite3Format(Format):
    '''
    The file format class for SQLite 3 file format.
    '''

    @classproperty
    def name(self):
        '''
        The file format name.
        '''
        return 'sqlite3'

    @classproperty
    def friendlyName(self):
        '''
        The file format friendly name.
        '''
        return 'SQLite 3'

    @classproperty
    def extension(self):
        '''
        The file format extension.
        '''
        return '.sqlite3'

    @classproperty
    def type(self):
        '''
        The file format type.
        '''
        return 'Database'

    @classproperty
    def mimeType(self):
        '''
        The file format media type.
        '''
        return 'application/x-sqlite3'

    @classproperty
    def info(self):
        '''
        The file format reference info.
        '''
        return 'https://en.wikipedia.org/wiki/SQLite'

    @classproperty
    def isBinary(self):
        '''
        Tells whether the file format is binary or not.
        '''
        return True

    @classproperty
    def isExportable(self):
        '''
        Tells whether the file format is exportable or not.
        '''
        return True
