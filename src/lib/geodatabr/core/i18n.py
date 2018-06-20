#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""
Core internationalization module.

This module provides the localization facilities.
"""
# External dependencies

from typing import Any

import yaml

# Package dependencies

from geodatabr.core.decorators import cachedmethod
from geodatabr.core.helpers.filesystem import Directory, File, Path
from geodatabr.core.types import Map

# Classes


class Localization(object):
    """Localization class."""

    def __init__(self, locale: str, locale_file: File):
        """
        Creates a new localization instance.

        Args:
            locale: The localization name
            locale_file: The localization file

        Raises:
            geodatabr.core.i18n.UnsupportedLocaleFileError:
                Raised when a localization file is invalid
        """
        self._locale = locale

        try:
            self._translations = Map(yaml.load(locale_file.read()))
        except Exception:
            raise UnsupportedLocaleFileError('Unsupported localization file')

    @property
    def locale(self) -> str:
        """Gets the localization name."""
        return self._locale

    @property
    def translations(self) -> Map:
        """Gets the localization translations."""
        return self._translations

    @cachedmethod()
    def translate(self, message: str, **placeholders) -> Any:
        """
        Translates the given message with their placeholders.

        Args:
            message: The message to be translated
            **placeholders: Any translation placeholder

        Returns:
            The translated message
        """
        if message in self.translations:
            translation = self.translations.get(message)

            if placeholders:
                return translation.format(placeholders)

            return translation

        return message

    def __repr__(self) -> str:
        """
        Returns the canonical string representation of the object.

        Returns:
            The canonical string representation of the object
        """
        return '{:s}(locale={!r})'.format(self.__class__.__name__,
                                          self.locale)


class Translator(object):
    """
    Translator service.

    Attributes:
        locale (str): The default locale name
        fallbackLocale (str): The default fallback locale name
    """

    # Default locale
    locale = 'en'

    # Default fallback locale
    fallbackLocale = 'en'

    @classmethod
    @cachedmethod()
    def locales(cls) -> Map:
        """
        Returns the available localizations.

        Returns:
            The available localizations mapping
        """
        return Map({locale: Localization(locale, locale_file)
                    for locale, locale_file in map(
                        lambda locale_file: (locale_file.basename,
                                             locale_file),
                        Directory(Path.PKG_TRANSLATION_DIR)
                        .files(pattern='*.yaml'))})

    @classmethod
    def translate(cls, message: str, **placeholders) -> str:
        """
        Translates the given message with their placeholders.

        Args:
            message: The message to be translated
            **placeholders: Any translation placeholder

        Returns:
            The translated message
        """
        locales = cls.locales()

        if cls.locale in locales:
            return locales[cls.locale].translate(message, **placeholders)

        # Try using the fallback locale
        if cls.fallbackLocale in locales:
            return locales[cls.fallbackLocale].translate(message,
                                                         **placeholders)

        # Fallback to the original message
        return message.format(**placeholders)


class UnsupportedLocaleFileError(Exception):
    """Exception class raised when an unsupported localization file is used."""

# Alias functions


_ = Translator.translate
