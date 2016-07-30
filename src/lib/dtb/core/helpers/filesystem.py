#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2016 Paulo Freitas
# MIT License (see LICENSE file)
'''
Filesystem helper module

This module provides classes to work with filesystem files and directories.
'''
# Imports

# Built-in dependencies

from pathlib import Path

# Package dependencies

from dtb.formats import FormatRepository, FormatError

# Classes


class Directory(object):
    def __init__(self, dirname):
        '''Constructor.

        :param dirname: the directory path to give a new Directory object
        '''
        self._path = Path(dirname)

    @property
    def name(self):
        '''Returns the directory name.'''
        return self._path.name

    def files(self, pattern='*'):
        '''Returns a list with all directory files matching the given pattern.'''
        return [File(_file) for _file in self._path.iterdir()
                if _file.match(pattern)]

    def __str__(self):
        '''String representation of this directory object.'''
        return str(self._path)


class File(object):
    def __init__(self, filename):
        '''Constructor.

        :param filename: the file path to give a new File object
        '''
        self._path = Path(filename)

    @property
    def name(self):
        '''Returns the file name.'''
        return self._path.name

    @property
    def path(self):
        '''Returns the file path.'''
        return self._path.parent

    @property
    def extension(self):
        '''Returns the file extension.'''
        return ''.join(self._path.suffixes)

    @property
    def format(self):
        '''Returns the file format.'''
        try:
            return FormatRepository.findFormatByExtension(self.extension)
        except FormatError:
            return None

    @property
    def size(self):
        '''Returns the file size.'''
        return self._path.stat().st_size

    def __str__(self):
        '''String representation of this file object.'''
        return str(self._path)
