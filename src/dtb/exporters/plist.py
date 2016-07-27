#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2016 Paulo Freitas
# MIT License (see LICENSE file)
'''
Property List file exporter module
'''
from __future__ import absolute_import, unicode_literals

# Imports

# Built-in dependencies

import re

from sys import version_info

if version_info >= (3, 0):
    from plistlib import _PlistWriter as PlistWriter, dumps as PlistDumper
else:
    from plistlib import PlistWriter, writePlistToString as PlistDumper

# Package dependencies

from dtb.exporters import Exporter
from dtb.formats.plist import PlistFormat

# Enhancements


def __unsortable_write_dict(self, d):
    self.beginElement('dict')
    items = d.items()

    for key, value in items:
        if not isinstance(key, (str, unicode)):
            raise TypeError('keys must be strings')

        self.simpleElement('key', key)
        self.writeValue(value)

    self.endElement('dict')

PlistWriter.writeDict = __unsortable_write_dict


# Classes


class PlistExporter(Exporter):
    '''Property List exporter class.'''

    # Exporter format
    _format = PlistFormat

    @property
    def data(self):
        '''Formatted Property List representation of data.'''
        data = self._data.toDict(strKeys=True, forceUnicode=True)
        plist_str = unicode(PlistDumper(data).decode('utf-8'))

        if self._minified:
            plist_str = re.sub('[\n\t]+', '', plist_str)

        return plist_str
