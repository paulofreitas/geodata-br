#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
TSV file format package
'''
from __future__ import absolute_import

# Imports

# Package dependencies

from places.core.helpers.decorators import classproperty
from places.formats import Format

# Classes


class TsvFormat(Format):
    '''
    The file format class for TSV file format.
    '''

    @classproperty
    def name(self):
        '''
        The file format name.
        '''
        return 'tsv'

    @classproperty
    def friendlyName(self):
        '''
        The file format friendly name.
        '''
        return 'TSV'

    @classproperty
    def extension(self):
        '''
        The file format extension.
        '''
        return '.tsv'

    @classproperty
    def type(self):
        '''
        The file format type.
        '''
        return 'Data Interchange'

    @classproperty
    def mimeType(self):
        '''
        The file format media type.
        '''
        return 'text/tab-separated-values'

    @classproperty
    def info(self):
        '''
        The file format reference info.
        '''
        return 'https://en.wikipedia.org/wiki/Tab-separated_values'

    @classproperty
    def isExportable(self):
        '''
        Tells whether the file format is exportable or not.
        '''
        return True

    @classproperty
    def isMinifiable(self):
        '''
        Tells whether the file format is minifiable or not.
        '''
        return True
