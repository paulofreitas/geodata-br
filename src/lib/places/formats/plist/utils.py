#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2016 Paulo Freitas
# MIT License (see LICENSE file)
'''
Property List file format utils module
'''
from __future__ import absolute_import

# Imports

# Built-in dependencies

from sys import version_info

if version_info >= (3, 0):
    from plistlib import _PlistWriter as PlistWriter, dumps as PlistDumper
else:
    from plistlib import PlistWriter, writePlistToString as PlistDumper

# External compatibility dependencies

from future.utils import iteritems

# Functions


def writeOrderedDict(self, d):
    self.beginElement('dict')

    for key, value in iteritems(d):
        if not isinstance(key, (str, unicode)):
            raise TypeError('keys must be strings')

        self.simpleElement('key', key)
        self.writeValue(value)

    self.endElement('dict')


# Enhancements

PlistWriter.writeDict = writeOrderedDict
