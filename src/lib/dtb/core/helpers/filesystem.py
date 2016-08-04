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

import os
import pathlib

# Package dependencies

from dtb.formats import FormatRepository, FormatError

# Classes


class Path(type(pathlib.Path())):
    '''
    A filesystem path object.
    '''

    def __enter__(self):
        '''
        Magic method to allow changing the working directory to this path.
        '''
        self._old_dir = self.cwd()
        os.chdir(str(self))

        return self

    def __exit__(self, *_):
        '''
        Magic method to allow changing the working directory to the previous
        path.
        '''
        os.chdir(str(self._old_dir))

    def __contains__(self, segment):
        '''
        Magic method to test if a path segment is in this path.

        Arguments:
            segment (str): A path segment

        Returns:
            bool: Whether or not the given path segment is in this path
        '''
        return segment in str(self)

    def __iter__(self):
        '''
        Magic method to allow iterating this path components.

        Returns:
            iterator: An iterator with this path components
        '''
        return iter(Path(part) for part in self.parts)

    # Properties

    @property
    def atime(self):
        '''
        Returns the path's last access time.
        '''
        return self.stat().st_atime

    @property
    def ctime(self):
        '''
        Returns the path's last change time.
        '''
        return self.stat().st_ctime

    @property
    def gid(self):
        '''
        Returns the path's owner group ID.
        '''
        return self._gid

    @property
    def mode(self):
        '''
        Returns the path's mode.
        '''
        return self.stat().st_mode

    @property
    def mtime(self):
        '''
        Returns the path's last modification time.
        '''
        return self.stat().st_mtime

    @property
    def size(self):
        '''
        Returns the path's size in bytes.
        '''
        return self.stat().st_size

    @property
    def uid(self):
        '''
        Returns the path's owner user ID.
        '''
        return self.stat().st_uid

    # Method aliases

    def join(self, *args):
        '''
        Alias for .joinpath() method.
        '''
        return self.joinpath(*args)

    # Property aliases

    accessed = atime
    accessTime = atime
    changed = ctime
    changeTime = ctime
    groupId = gid
    modificated = mtime
    modificationTime = mtime
    userId = uid

    @property
    def basename(self):
        '''
        Alias for .stem property.
        '''
        return self.stem


class Directory(Path):
    '''
    A filesystem directory object.
    '''

    def __init__(self, *args):
        '''
        Constructor.
        '''
        super(self.__class__, self).__init__(*args)

        if not self.exists():
            raise IOError(2, "No such directory: '{}'".format(self))

        if not self.is_dir():
            raise OSError(20, "Not a directory: '{}'".format(self))

    def directories(self, pattern='*', recursive=False):
        '''
        Yields a generator with all directories matching the given pattern.

        Arguments:
            pattern (str): The search pattern
            recursive (bool): Whether or not it should return directories
                recursively

        Yields:
            A generator with all directories matching the given pattern
        '''
        search_method = self.rglob if recursive else self.glob

        for path in search_method(pattern):
            if path.is_dir():
                yield Directory(path)

    def files(self, pattern='*', recursive=False):
        '''
        Yields a generator with all files matching the given pattern.

        Arguments:
            pattern (str): The search pattern
            recursive (bool): Whether or not it should return files recursively

        Yields:
            A generator with all files matching the given pattern
        '''
        search_method = self.rglob if recursive else self.glob

        for path in search_method(pattern):
            if path.is_file():
                yield File(path)

    # Method aliases

    def create(self, **kwargs):
        '''
        Alias for .mkdir() method.
        '''
        return self.mkdir(**kwargs)


class File(Path):
    '''
    A filesystem file object.
    '''

    def __init__(self, *args):
        '''
        Constructor.
        '''
        super(self.__class__, self).__init__(*args)

        if not self.exists():
            raise IOError(2, "No such file: '{}'".format(self))

        if self.is_dir():
            raise OSError(21, "Is a directory: '{}'".format(self))

    def read(self, **kwargs):
        '''
        Returns the decoded file contents as string.

        Returns:
            str: The file contents
        '''
        with self.open('r', **kwargs) as file_:
            return file_.read()

    def readBytes(self, **kwargs):
        '''
        Returns the decoded file contents as bytes.

        Returns:
            bytes: The file contents
        '''
        with self.open('rb', **kwargs) as file_:
            return file_.read()

    def write(self, data, **kwargs):
        '''
        Opens the file in text mode, write data to it, and closes the file.

        Arguments:
            data (str): The content to be written
        '''
        with self.open('w', **kwargs) as file_:
            file_.write(data)

    # Properties

    @property
    def extension(self):
        '''
        Returns the full file extension.

        Returns:
            str: The full file extension
        '''
        return ''.join(self.suffixes)

    @property
    def format(self):
        '''
        Returns the file format.

        Returns:
            The file format
        '''
        try:
            return FormatRepository.findByExtension(self.extension)
        except FormatError:
            return None
