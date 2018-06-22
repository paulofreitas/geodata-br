#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""
Filesystem helper module.

This module provides classes to work with filesystem files and directories.
"""
# Imports

# Built-in dependencies

import os
import pathlib
import uuid
from typing import Iterator
import pkg_resources

# Classes


class _Path(type(pathlib.Path())):
    """A filesystem path type."""


class Path(_Path):
    """
    A filesystem path object.

    Attributes:
        HOME_DIR (geodatabr.core.helpers.filesystem._Path):
            The path for home directory
        CACHE_DIR (geodatabr.core.helpers.filesystem._Path):
            The path for cache directory
        CURRENT_DIR (geodatabr.core.helpers.filesystem._Path):
            The path for current working directory
        DATA_DIR (geodatabr.core.helpers.filesystem._Path):
            The path for data directory
        PKG_DIR (geodatabr.core.helpers.filesystem._Path):
            The path for package directory
        PKG_DATA_DIR (geodatabr.core.helpers.filesystem._Path):
            The path for package data directory
        PKG_STUB_DIR (geodatabr.core.helpers.filesystem._Path):
            The path for package stubs directory
        PKG_TRANSLATION_DIR (geodatabr.core.helpers.filesystem._Path):
            The path for package translations directory
    """

    HOME_DIR = _Path.home()
    CACHE_DIR = HOME_DIR / '.geodatabr'
    CURRENT_DIR = _Path.cwd()
    DATA_DIR = CURRENT_DIR / 'data'
    PKG_DIR = _Path(pkg_resources.resource_filename('geodatabr', ''))
    PKG_DATA_DIR = PKG_DIR / 'data'
    PKG_STUB_DIR = PKG_DATA_DIR / 'stubs'
    PKG_TRANSLATION_DIR = PKG_DATA_DIR / 'translations'

    def _init(self):
        """Private constructor."""
        super()._init()

        #: geodatabr.core.helpers.filesystem._Path: The previous working directory
        self._old_dir = None

    def __enter__(self) -> 'Path':
        """
        Magic method to allow changing the working directory to this path.

        Returns:
            This path instance
        """
        self._old_dir = self.cwd()
        os.chdir(str(self))

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Magic method to allow changing the working directory to the previous
        path.
        """
        os.chdir(str(self._old_dir))

    def __contains__(self, segment: str) -> bool:
        """
        Magic method to test if a path segment is in this path.

        Args:
            segment: A path segment

        Returns:
            Whether or not the given path segment is in this path
        """
        return segment in str(self)

    def __iter__(self) -> Iterator['Path']:
        """
        Magic method to allow iterating this path components.

        Returns:
            An iterator with this path components
        """
        return iter(Path(part) for part in self.parts)

    # Properties

    @property
    def atime(self) -> float:
        """Gets the path's last access time."""
        return self.stat().st_atime

    @property
    def ctime(self) -> float:
        """Gets the path's last change time."""
        return self.stat().st_ctime

    @property
    def gid(self) -> int:
        """Gets the path's owner group ID."""
        return self.stat().st_gid

    @property
    def mode(self) -> int:
        """Gets the path's mode."""
        return self.stat().st_mode

    @property
    def mtime(self) -> float:
        """Gets the path's last modification time."""
        return self.stat().st_mtime

    @property
    def size(self) -> int:
        """Gets the path's size in bytes."""
        return self.stat().st_size

    @property
    def uid(self) -> int:
        """Gets the path's owner user ID."""
        return self.stat().st_uid

    # Method aliases

    def join(self, *args) -> 'Path':
        """Alias for .joinpath() method."""
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
    def basename(self) -> str:
        """Alias for .stem property."""
        return self.stem


class Directory(Path):
    """A filesystem directory object."""

    def create(self, mode: int = 0o755, parents: bool = False) -> bool:
        """
        Creates a new directory at this given path.

        Args:
            mode: The file mode
            parents: Whether the missing parents of this path should be
                created as needed or not

        Returns:
            Whether the directory has been created or not
        """
        try:
            self.mkdir(mode, parents)

            return True
        except OSError:
            return False

    def directories(self,
                    pattern: str = '*',
                    recursive: bool = False) -> Iterator['Directory']:
        """
        Yields a generator with all directories matching the given pattern.

        Args:
            pattern: The search pattern
            recursive: Whether or not it should return directories recursively

        Yields:
            A generator with all directories matching the given pattern
        """
        search_method = self.rglob if recursive else self.glob

        for path in search_method(pattern):
            if path.is_dir():
                yield Directory(path)

    def files(self,
              pattern: str = '*',
              recursive: bool = False) -> Iterator['File']:
        """
        Yields a generator with all files matching the given pattern.

        Args:
            pattern: The search pattern
            recursive: Whether or not it should return files recursively

        Yields:
            A generator with all files matching the given pattern
        """
        search_method = self.rglob if recursive else self.glob

        for path in search_method(pattern):
            if path.is_file():
                yield File(path)


class File(Path):
    """A filesystem file object."""

    def read(self, **options) -> str:
        """
        Returns the decoded file contents as string.

        Args:
            **options: The file reading options

        Returns:
            The file contents
        """
        with self.open(mode='r', **options) as file_:
            return file_.read()

    def readBytes(self, **options) -> bytes:
        """
        Returns the decoded file contents as bytes.

        Args:
            **options: The file reading options

        Returns:
            The file contents
        """
        with self.open(mode='rb', **options) as file_:
            return file_.read()

    def write(self, data: str, **options):
        """
        Opens the file in text mode, write data to it, and closes the file.

        Args:
            data: The content to be written
            **options: The file writing options
        """
        with self.open(mode='w', **options) as file_:
            file_.write(data)

    def writeBytes(self, data: bytes, **options):
        """
        Opens the file in binary mode, write data to it, and closes the file.

        Args:
            data: The content to be written
            **options: The file writing options
        """
        with self.open(mode='wb', **options) as file_:
            file_.write(data)

    # Properties

    @property
    def format(self):
        """Gets the file format."""
        from geodatabr.core.encoders import \
            EncoderFormatRepository, UnknownEncoderFormatError

        try:
            return EncoderFormatRepository.findByExtension(self.extension)
        except UnknownEncoderFormatError:
            return None

    # Property aliases

    extension = Path.suffix


class CacheFile(File):
    """A filesystem cache file object."""

    def __new__(cls, *args, **kwargs) -> File:
        """
        Creates a new cache file instance.

        Args:
            *args: The optional path segments
            **kwargs: The file options
        """
        if not args:
            args += (str(uuid.uuid4()),)

        return File(Path.CACHE_DIR, *args, **kwargs)
