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

from itertools import groupby

# Package dependencies

from geodatabr.core import BASE_DIR, SRC_DIR
from geodatabr.core.helpers.filesystem import Directory, File
from geodatabr.core.helpers.markup import GithubMarkdown as Markdown, Html, \
    HtmlElement
from geodatabr.core.i18n import _, Translator
from geodatabr.core.types import AbstractClass, Map
from geodatabr.dataset.serializers import Serializer
from geodatabr.encoders import EncoderFormatRepository

# Setup translator

Translator.load('dataset')

# Classes


class Readme(AbstractClass):
    """An abstract README documentation file."""

    def __init__(self, readme_file: File, stub_file: File = None):
        """
        Creates a new README file.

        Args:
            readme_file: The README file
            stub_file: The README stub file
        """
        self._readme_file = readme_file
        self._stub_file = stub_file
        self._stub = self._stub_file.read() if stub_file else ''

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
        readme_file = File(BASE_DIR / 'README.md')
        stub_file = File(SRC_DIR / 'data/stubs/README.stub.md')

        super().__init__(readme_file, stub_file)

    def render(self) -> str:
        """
        Renders the file.

        Returns:
            The rendered project README contents
        """
        Translator.locale = 'en'

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
        dataset = Serializer().serialize()
        html = ['\n']

        for entity in dataset:
            html.append(CustomBadge(entity,
                                    len(dataset[entity]),
                                    'red').render())
            html.append('\n')

        return Html(Html.p(*html, align='center'))

    def renderDataFormats(self) -> str:
        """
        Renders the available data formats.

        Returns:
            The available data formats
        """
        grouped_formats = EncoderFormatRepository.groupByType()
        markdown = ''

        for format_type, formats in grouped_formats:
            markdown += '\n'.join([
                Markdown.header(format_type, depth=4),
                Markdown.unorderedList([
                    Markdown.link(_format.info, _format.friendlyName)
                    for _format in formats
                ]) + '\n'
            ])

        return markdown


class DatasetReadme(Readme):
    """A dataset README documentation file."""

    def __init__(self, dataset_dir: Directory):
        """
        Creates a new dataset README documentation file instance.

        Args:
            dataset_dir: The dataset directory
        """
        readme_file = File(dataset_dir / 'README.md')
        stub_file = File(SRC_DIR / 'data/stubs/BASE_README.stub.md')

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
        dataset = Serializer().serialize()
        data = [
            [Markdown.code(entity),
             '{:,d}'.format(len(dataset[entity]))]
            for entity in dataset
        ]

        return Markdown.table([headers] + data, alignment)

    def renderDatasetFiles(self) -> str:
        """
        Renders the dataset files info.

        Returns:
            The dataset files info
        """
        files = list(self._dataset_dir.files(pattern=_('dataset_name') + '*'))
        grouped_files = groupby(sorted(files, key=lambda file: file.format.type),
                                key=lambda file: file.format.type)
        listing = []

        for dataset_type, dataset_files in grouped_files:
            listing.append(Markdown.header(dataset_type, depth=4))
            headers = ['File', 'Format', 'Size']
            alignment = ['<', '^', '>']
            rows = []

            for dataset_file in dataset_files:
                dataset_format = '-'

                if dataset_file.format:
                    dataset_format = Markdown.link(dataset_file.format.info,
                                                   dataset_file.format.friendlyName)

                rows.append([
                    Markdown.code(dataset_file.name),
                    dataset_format,
                    '{:9,d}'.format(dataset_file.size),
                ])

            listing.append(Markdown.table([headers] + rows, alignment))

        return '\n'.join(listing)


class Badge(AbstractClass, Map):
    """An abstract badge image."""

    def render(self) -> HtmlElement:
        """Renders the badge image."""
        raise NotImplementedError

    def __str__(self) -> str:
        """Renders the badge image string."""
        return Html(self.render())


class CustomBadge(Badge):
    """A custom badge image."""

    def __init__(self, label: str, value: str, color: str):
        """
        Creates a new custom badge image.
        """
        self.label = label
        self.value = value
        self.color = color

    def render(self) -> HtmlElement:
        """Renders the badge image element."""
        return Html.img(
            src='https://img.shields.io/badge/{label}-{value}-{color}.svg'
            .format(label=self.label,
                    value=self.value,
                    color=self.color))
