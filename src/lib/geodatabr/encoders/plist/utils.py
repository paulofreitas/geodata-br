#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
Property List file format utils module
'''
# Imports

# Built-in dependencies

from plistlib import _PlistWriter as PlistWriter

# Functions


def writeOrderedDict(self, _dict):
    self.beginElement('dict')

    for key, value in iter(_dict.items()):
        if not isinstance(key, str):
            raise TypeError('keys must be strings')

        self.simpleElement('key', key)
        self.writeValue(value)

    self.endElement('dict')


# Enhancements

PlistWriter.writeDict = writeOrderedDict
