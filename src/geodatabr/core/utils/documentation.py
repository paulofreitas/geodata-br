#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""
Documentation helper module.

This module provides helper classes to write documentation files.
"""
# Imports

# Built-in dependencies

import itertools

# Package dependencies

from geodatabr.core import encoders, i18n, types
from geodatabr.core.utils import io, markup
from geodatabr.dataset import serializers

# Classes


class Readme(types.AbstractClass):
    """
    An abstract README documentation file.

    Attributes:
        _readme_file (geodatabr.core.utils.io.File): The README file
        _stub_file (geodatabr.core.utils.io.File): The template README file
        _stub (str): template README contents
        _markdown (geodatabr.core.utils.markup.GithubMarkdown):
            The Github Markdown helper
    """

    def __init__(self, readme_file: io.File, stub_file: io.File = None):
        """
        Creates a new README file.

        Args:
            readme_file: The README file
            stub_file: The template README file
        """
        self._readme_file = readme_file
        self._stub_file = stub_file
        self._stub = self._stub_file.read() if stub_file else ''
        self._markdown = markup.GithubMarkdown

    def render(self) -> str:
        """Renders the file."""
        raise NotImplementedError

    def write(self):
        """Writes the file to disk."""
        self._readme_file.write(self.render())


class ProjectReadme(Readme):
    """The project README documentation file."""

    def __init__(self):
        """Creates a new project README documentation file instance."""
        readme_file = io.File(io.Path.CURRENT_DIR / 'README.md')
        stub_file = io.File(io.Path.PKG_STUB_DIR / 'README.stub.md')

        super().__init__(readme_file, stub_file)

    def render(self) -> str:
        """
        Renders the file.

        Returns:
            The rendered project README contents
        """
        i18n.Translator.locale = 'en'

        return self._stub.format(
            badges=self.renderBadges().strip(),
            data_formats=self.renderDataFormats().strip()
        )

    def renderBadges(self) -> str:
        """
        Renders the document badges.

        Returns:
            The document badges
        """
        dataset = serializers.Serializer().serialize()

        return '\n'.join(str(CustomBadge(entity,
                                         '{:,d}'.format(len(dataset[entity])),
                                         '97c554'))
                         for entity in dataset)

    def renderDataFormats(self) -> str:
        """
        Renders the available data formats.

        Returns:
            The available data formats
        """
        grouped_formats = encoders.EncoderFormatRepository.groupByType()

        return self._markdown.unorderedList([
            '{format_type}: {formats}\n'.format(
                format_type=self._markdown.bold(format_type),
                formats=types.String.sentence(
                    [self._markdown.link(_format.info,
                                         _format.friendlyName,
                                         'File extension: {}' \
                                             .format(_format.extension))
                     for _format in formats],
                    last_delimiter=' and '))
            for format_type, formats in grouped_formats])


class DatasetReadme(Readme):
    """A dataset README documentation file."""

    def __init__(self, dataset_dir: io.Directory):
        """
        Creates a new dataset README documentation file instance.

        Args:
            dataset_dir: The dataset directory
        """
        readme_file = io.File(dataset_dir / 'README.md')
        stub_file = io.File(io.Path.PKG_STUB_DIR / 'BASE_README.stub.md')

        super().__init__(readme_file, stub_file)

        self._dataset_dir = dataset_dir

    def render(self) -> str:
        """
        Renders the file.

        Returns:
            The rendered dataset README contents
        """
        return self._stub.format(
            dataset_records=self.renderDatasetRecords().strip(),
            dataset_files=self.renderDatasetFiles().strip())

    def renderDatasetRecords(self) -> str:
        """
        Renders the dataset records counts.

        Returns:
            The dataset records counts
        """
        headers = ['Table/Collection', 'Records']
        alignment = ['>', '>']
        dataset = serializers.Serializer().serialize()
        data = [
            [self._markdown.code(entity),
             '{:,d}'.format(len(dataset[entity]))]
            for entity in dataset
        ]

        return self._markdown.table([headers] + data, alignment)

    def renderDatasetFiles(self) -> str:
        """
        Renders the dataset files info.

        Returns:
            The dataset files info
        """
        files = list(self._dataset_dir.files(
            pattern=i18n._('dataset_name') + '*'))
        grouped_files = itertools.groupby(
            sorted(files, key=lambda file: file.format.type),
            key=lambda file: file.format.type)
        listing = []

        for dataset_type, dataset_files in grouped_files:
            listing.append(self._markdown.header(dataset_type, depth=4))
            headers = ['File', 'Format', 'Size']
            alignment = ['<', '^', '>']
            rows = []

            for dataset_file in dataset_files:
                dataset_format = '-'

                if dataset_file.format:
                    dataset_format = self._markdown.link(
                        dataset_file.format.info,
                        dataset_file.format.friendlyName)

                rows.append([self._markdown.code(dataset_file.name),
                             dataset_format,
                             '{:9,d}'.format(dataset_file.size)])

            listing.append(self._markdown.table([headers] + rows, alignment))

        return '\n'.join(listing)


class Badge(types.AbstractClass, types.Map):
    """An abstract badge image."""

    def __str__(self) -> str:
        """Renders the badge image."""
        raise NotImplementedError


class CustomBadge(Badge):
    """A custom badge image."""

    def __init__(self,
                 label: str,
                 value: str,
                 color: str = None,
                 style: str = None):
        """
        Creates a new custom badge image.

        Args:
            label: The badge label text
            value: The badge value text
            color: The badge color (defaults to "brightgreen")
            style: The badge style (defaults to "flat")
        """
        self.label = label
        self.value = value
        self.color = color or 'brightgreen'
        self.style = style or 'flat'

    def __str__(self) -> str:
        """Renders the badge image."""
        return markup.GithubMarkdown.image(
            'https://img.shields.io/badge/{label}-{value}-{color}.svg' \
            '?style={style}'
            .format(label=self.label,
                    value=self.value,
                    color=self.color,
                    style=self.style),
            self.label + ': ' + self.value,
            self.label + ': ' + self.value)
