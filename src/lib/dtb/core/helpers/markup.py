#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2016 Paulo Freitas
# MIT License (see LICENSE file)
'''
Markup helper module

This module provides a Markdown markup generator class.
'''
# Imports

# Built-in dependencies

from collections import defaultdict

# Classes

class Markdown(object):
    '''Markdown markup generator.'''
    # Emphasis

    @staticmethod
    def bold(text, alternative=False):
        '''Creates a bold text.'''
        if alternative:
            return '__{}__'.format(text)

        return '**{}**'.format(text)

    @staticmethod
    def italic(text, alternative=True):
        '''Creates text in italics.'''
        if alternative:
            return '_{}_'.format(text)

        return '*{}*'.format(text)

    @staticmethod
    def strikethrough(text):
        '''Strikes through the provided text.'''
        return '~~{}~~'.format(text)

    # Lists

    @staticmethod
    def orderedList(items):
        '''Generates a numbered list.'''
        return '\n'.join('{}. {}'.format(index + 1, item)
                         for index, item in enumerate(items)) + '\n'

    @staticmethod
    def unorderedList(items, bullet_char='*'):
        '''Generates a bullet list.'''
        assert bullet_char in ['*', '-', '+'], 'Invalid bullet char'

        return '\n'.join('{} {}'.format(bullet_char, item)
                         for item in items) + '\n'

    # Others

    @staticmethod
    def blockquote(text, simple=False):
        '''Creates a block quoted text.'''
        if simple:
            return '> {}\n'.format(text)

        return '\n'.join(['> {}'.format(line) for line in text.splitlines()])

    @staticmethod
    def code(content, inline=True, syntax=None):
        if inline and not syntax:
            return '`{}`'.format(content)

        return '```{}\n{}\n```'.format(syntax or '', content)

    @staticmethod
    def header(heading_text, depth=1, alternative=False):
        '''Creates a header.'''
        assert depth >= 1 and depth <= 6, 'Invalid depth'

        if alternative and depth in (1, 2):
            return '\n'.join([
                heading_text,
                ['=', '-'][depth -1] * len(heading_text)
            ]) + '\n'

        return '#' * depth + ' ' + heading_text + '\n'

    @staticmethod
    def horizontalRule(rule_char='-'):
        '''Creates an horizontal rule.'''
        assert rule_char in ['-', '*', '_']

        return rule_char * 3 + '\n'

    @staticmethod
    def link(url, text='', title=''):
        '''Generates a link to an URL.'''
        if not text and not title:
            return url

        if not title:
            return '[{}]({})'.format(text, url)

        return '[{}]({} "{}")'.format(text, url, title)

    @staticmethod
    def literal(text):
        chars = '\\`*_{}[]()#+-.!'

        return ''.join('\\' + char if char in chars else char for char in text)

    @staticmethod
    def table(data, aligning=None):
        '''Generates a table from a 2 dimentional list.'''
        md = ''

        # No aligning: default is left
        if not aligning:
            aligning = ['<'] * len(data[0])

        if len(data[0]) > len(aligning):
            difference = len(data[0]) - len(aligning)
            aligning.extend(['<'] * difference)

        assert len(aligning) >= len(data[0])

        # Calculate max size of each column
        column_sizes = defaultdict(int)

        for row in data:
            for column, cell in enumerate(map(str, row)):
                column_sizes[column] = max(column_sizes[column], len(cell))

        # Headers

        md = '|{}|\n'.format('|'.join([
            (' {{:' + aligning[col] + '{}}} ').format(column_sizes[col])
                                              .replace('^', '<')
                                              .format(cell)
            for col, cell in enumerate(data[0])
        ]))

        # Heading separator
        md += '|{}|\n'.format('|'.join([
            ''.join([
                ':' if aligning[col] == '^' else ' ', # left char
                '-' * column_sizes[col],
                ' ' if aligning[col] == '<' else ':', # right char
            ])
            for col in range(len(data[0]))
        ]))

        # Data
        md += ''.join([
            '|{}|\n'.format('|'.join([
                (' {{:' + aligning[col] + '{}}} ').format(column_sizes[col])
                                                  .replace('^', '<')
                                                  .format(cell)
                for col, cell in enumerate(row)
            ]))
            for row in data[1:]
        ])

        return md
