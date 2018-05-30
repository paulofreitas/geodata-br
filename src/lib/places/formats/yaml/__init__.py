#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
YAML file format package
'''
# Imports

# Package dependencies

from places.core.helpers.decorators import classproperty
from places.formats import Format

# Classes


class YamlFormat(Format):
    '''
    The file format class for YAML file format.
    '''

    @classproperty
    def name(self):
        '''
        The file format name.
        '''
        return 'yaml'

    @classproperty
    def friendlyName(self):
        '''
        The file format friendly name.
        '''
        return 'YAML'

    @classproperty
    def extension(self):
        '''
        The file format extension.
        '''
        return '.yaml'

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
        return None

    @classproperty
    def info(self):
        '''
        The file format reference info.
        '''
        return 'https://en.wikipedia.org/wiki/YAML'

    @classproperty
    def isExportable(self):
        '''
        Tells whether the file format is exportable or not.
        '''
        return True
