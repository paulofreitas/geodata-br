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
    '''
    Markdown markup generator.
    '''
    # Headers

    @staticmethod
    def header(heading_text, depth=1, alternative=False):
        '''
        Creates a header.

        Arguments:
            heading_text (str): The header text
            depth (int): The header depth level
            alternative (bool): Whether it should use the alternative syntax

        Returns:
            str: A header
        '''
        assert depth >= 1 and depth <= 6, 'Invalid depth level'

        if alternative and depth in (1, 2):
            return '\n'.join([
                heading_text,
                ['=', '-'][depth -1] * len(heading_text)
            ]) + '\n'

        return '#' * depth + ' ' + heading_text + '\n'

    # Emphasis

    @staticmethod
    def bold(text, alternative=False):
        '''
        Creates a bold text.

        Arguments:
            text (str): The text to be bolded
            alternative (bool): Whether it should use the alternative syntax

        Returns:
            str: A bolded text
        '''
        if alternative:
            return '__{}__'.format(text)

        return '**{}**'.format(text)

    @staticmethod
    def italic(text, alternative=True):
        '''
        Creates an italic text.

        Arguments:
            text (str): The text to be italicized
            alternative (bool): Whether it should use the alternative syntax

        Returns:
            str: An italicized text
        '''
        if alternative:
            return '_{}_'.format(text)

        return '*{}*'.format(text)

    # Lists

    @staticmethod
    def unorderedList(items, bullet_char='*'):
        '''
        Creates a bullet list.

        Arguments:
            items (list): The list items
            bullet_char (str): The bullet character to use

        Returns:
            str: A bullet list
        '''
        assert bullet_char in ['*', '-', '+'], 'Invalid bullet char'

        return '\n'.join('{} {}'.format(bullet_char, item)
                         for item in items) + '\n'

    @staticmethod
    def orderedList(items):
        '''
        Creates a numbered list.

        Arguments:
            items (list): The list items

        Returns:
            str: A numbered list
        '''
        return '\n'.join('{}. {}'.format(index + 1, item)
                         for index, item in enumerate(items)) + '\n'

    # Code

    @staticmethod
    def code(content, inline=True):
        '''
        Creates an inline or block code.

        Arguments:
            content (str): The code content
            inline (bool): Whether it should be rendered inline or not

        Returns:
            str: An inline or block code
        '''
        if inline:
            return '`{}`'.format(content)

        return '    {}\n'.format(content)

    # Images

    @staticmethod
    def image(url, text='', title=''):
        '''
        Creates an image.

        Arguments:
            url (str): The image URL
            text (str): The optional image alternate text
            title (str): The optional image title

        Returns:
            str: An image
        '''
        if not title:
            return '![{}]({})'.format(text, url)

        return '![{}]({} "{}")'.format(text, url, title)

    # Links

    @staticmethod
    def link(url, text='', title=''):
        '''
        Creates a link to an URL.

        Arguments:
            url (str): The link URL
            text (str): The optional link text
            title (str): The optional link title

        Returns:
            str: A link
        '''
        if not text and not title:
            return url

        if not title:
            return '[{}]({})'.format(text, url)

        return '[{}]({} "{}")'.format(text, url, title)

    # Quoting

    @staticmethod
    def blockquote(text, simple=False):
        '''
        Creates a block quoted text.

        Arguments:
            text (str): The text to be quoted
            simple (bool):

        Returns:
            str: A quoted text
        '''
        if simple:
            return '> {}\n'.format(text)

        return '\n'.join(['> {}'.format(line) for line in text.splitlines()])

    # Misc

    @staticmethod
    def rule(rule_char='-'):
        '''
        Creates an horizontal rule.

        Arguments:
            rule_char (str): The rule character to use

        Returns:
            str: An horizontal rule
        '''
        assert rule_char in ['-', '*', '_']

        return rule_char * 3 + '\n'

    @staticmethod
    def literal(text):
        '''
        Generates an escaped text.

        Arguments:
            text (str): The text to be escaped

        Returns:
            str: The escaped text
        '''
        chars = '\\`*_{}[]()#+-.!<>'

        return ''.join('\\' + char if char in chars else char for char in text)


class GithubMarkdown(Markdown):
    '''
    GitHub Flavored Markdown
    '''
    # Emphasis

    @staticmethod
    def strikethrough(text):
        '''
        Strikes out the provided text.

        Arguments:
            text (str): The text to be striked out

        Returns:
            str: A striked text
        '''
        return '~~{}~~'.format(text)

    # Lists

    @staticmethod
    def taskList(tasks):
        '''
        Creates a task list.

        Arguments:
            tasks (dict): A dictionary of task items

        Returns:
            str: A task list
        '''
        assert isinstance(tasks, dict)

        return '\n'.join(
            '- [{}] {}'.format('x' if task_completed else ' ', task_item)
            for task_item, task_completed in tasks.items()
        ) + '\n'

    # Code

    @staticmethod
    def code(content, inline=True, syntax=None):
        '''
        Creates an inline or block code.

        Arguments:
            content (str): The code content
            inline (bool): Whether it should be rendered inline or not
            syntax (str): The code language it should highlight the syntax

        Returns:
            str: An inline or block code
        '''
        # pylint: disable=arguments-differ
        if not syntax:
            return Markdown.code(content, inline)

        return '```{}\n{}\n```'.format(syntax, content)

    # Misc

    @staticmethod
    def table(data, aligning=None):
        '''
        Creates a table from a 2 dimensional list.

        Arguments:
            table (list): A two-dimensional list
            aligning (str): The table alignment

        Returns:
            str: A table
        '''
        assert isinstance(data, list)
        assert aligning in ['<', '^', '>']

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
            (' {{:' + aligning[col] + '{}}} ').format(column_sizes[col]) \
                                              .replace('^', '<') \
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
                (' {{:' + aligning[col] + '{}}} ').format(column_sizes[col]) \
                                                  .replace('^', '<') \
                                                  .format(cell)
                for col, cell in enumerate(row)
            ]))
            for row in data[1:]
        ])

        return md
