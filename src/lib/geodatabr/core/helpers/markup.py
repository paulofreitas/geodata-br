#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""
Markup helper module.

This module provides markup generators for HTML and Markdown.
"""
# Imports

# Built-in dependencies

import html
from lxml import builder, etree, html as _html

# Classes


class MarkupElement(object):
    """Abstract markup element class."""

    def __init__(self):
        """No-op constructor."""
        raise NotImplementedError

    def __repr__(self) -> str:
        """
        Returns the canonical string representation of the object.

        Returns:
            The canonical string representation of the object
        """
        return '{:s}({!s})' \
               .format(self.__class__.__name__,
                       ', '.join('{}={}'.format(key, repr(value))
                                 for key, value in self.__dict__.items()))


class MarkdownGenerator(type):
    """Metaclass for Markdown generators."""

    def __getattr__(cls, name: str) -> str:
        """
        Magic method to call a Markdown generator alias method.

        Args:
            name: The alias method name

        Returns:
            The alias method result

        Raises:
            AttributeError: If alias method name is invalid
        """
        aliases = cls.__aliases__
        aliases.update({alias: resolver
                        for parent in cls.__bases__
                        if hasattr(parent, '__aliases__')
                        for alias, resolver in parent.__aliases__.items()
                        if alias not in aliases})

        if name == '__aliases__' or name not in aliases:
            raise AttributeError('Invalid method')

        def _wrapper(*args, **kwargs):
            return str(aliases.get(name)(*args, **kwargs))

        return _wrapper


class MarkdownElement(MarkupElement):
    """Abstract Markdown element class."""


class Markdown(metaclass=MarkdownGenerator):
    """
    Markdown markup generator.

    Attributes:
        __aliases__ (dict): Method aliases
    """

    class Header(MarkdownElement):
        """Markdown header element."""

        STYLE_SETEXT = 'setext'
        STYLE_ATX = 'atx'

        def __init__(self, text: str, depth: int = 1, style: str = STYLE_ATX):
            """
            Creates a heading text.

            Args:
                text: The heading text
                depth: The header depth level
                style: The header style

            Raises:
                ValueError: If depth level is invalid
                ValueError: If header style is invalid
            """
            if style not in (self.STYLE_SETEXT, self.STYLE_ATX):
                raise ValueError('Invalid header style')

            if (style == self.STYLE_SETEXT and depth not in range(1, 3)) \
                    or (style == self.STYLE_ATX and depth not in range(1, 7)):
                raise ValueError('Invalid depth level')

            self.text = text
            self.depth = depth
            self.style = style

        def __str__(self) -> str:
            """Renders the element."""
            if self.style == self.STYLE_SETEXT:
                return '\n'.join([
                    self.text,
                    ['=', '-'][self.depth - 1] * len(self.text)
                ]) + '\n'

            return '#' * self.depth + ' ' + self.text + '\n'

    class Bold(MarkdownElement):
        """Markdown bold element."""

        def __init__(self, text: str, style: str = '*'):
            """
            Creates a bold emphasized text.

            Args:
                text: The text to be bolded
                style: The emphasis style to use

            Raises:
                ValueError: If emphasis style is invalid
            """
            if style not in ('_', '*'):
                raise ValueError('Invalid emphasis style')

            self.text = text
            self.style = style

        def __str__(self) -> str:
            """Renders the element."""
            return '{_}{}{_}'.format(self.text, _=self.style * 2)

    class Italic(MarkdownElement):
        """Markdown italic element."""

        def __init__(self, text: str, style: str = '*'):
            """
            Creates an italic emphasized text.

            Args:
                text: The text to be italicized
                style: The emphasis style to use

            Raises:
                ValueError: If emphasis style is invalid
            """
            if style not in ('_', '*'):
                raise ValueError('Invalid emphasis style')

            self.text = text
            self.style = style

        def __str__(self) -> str:
            """Renders the element."""
            return '{_}{}{_}'.format(self.text, _=self.style)

    class UnorderedList(MarkdownElement):
        """Markdown unordered list element."""

        def __init__(self, items: list, bullet_char: str = '*'):
            """
            Creates a bullet list.

            Args:
                items: The list items
                bullet_char: The bullet character to use

            Raises:
                ValueError: If bullet char is invalid
            """
            if bullet_char not in ['*', '-', '+']:
                raise ValueError('Invalid bullet char')

            self._items = items
            self.bullet_char = bullet_char

        def __str__(self) -> str:
            """Renders the element."""
            return '\n'.join('{} {}'.format(self.bullet_char, item)
                             for item in self._items) + '\n'

    class OrderedList(MarkdownElement):
        """Markdown ordered list element."""

        def __init__(self, items: list):
            """
            Creates a numbered list.

            Args:
                items: The list items
            """
            self.items = items

        def __str__(self) -> str:
            """Renders the element."""
            return '\n'.join('{}. {}'.format(index + 1, item)
                             for index, item in enumerate(self.items)) + '\n'

    class Code(MarkdownElement):
        """Markdown code element."""

        def __init__(self, source: str, inline: bool = True):
            """
            Creates an inline or block code.

            Args:
                source: The source code
                inline: Whether it should be rendered inline or not
            """
            self.source = source
            self.inline = inline

        def __str__(self) -> str:
            """Renders the element."""
            if self.inline:
                return '`{}`'.format(html.escape(self.source))

            return '    {}\n'.format(html.escape(self.source))

    class Image(MarkdownElement):
        """Markdown image element."""

        def __init__(self, url: str, text: str = '', title: str = ''):
            """
            Creates an image.

            Args:
                url: The image URL
                text: The optional image alternate text
                title: The optional image title
            """
            self.url = url
            self.text = text
            self.title = title

        def __str__(self) -> str:
            """Renders the element."""
            if not self.title:
                return '![{}]({})'.format(self.text, self.url)

            return '![{}]({} "{}")'.format(self.text, self.url, self.title)

    class Link(MarkdownElement):
        """Markdown link element."""

        def __init__(self, url: str, text: str = '', title: str = ''):
            """
            Creates a link to an URL.

            Args:
                url: The link URL
                text: The optional link text
                title: The optional link title
            """
            self.url = url
            self.text = text
            self.title = title

        def __str__(self) -> str:
            """Renders the element."""
            if not self.text and not self.title:
                return self.url

            if not self.title:
                return '[{}]({})'.format(self.text, self.url)

            return '[{}]({} "{}")'.format(self.text, self.url, self.title)

    class Blockquote(MarkdownElement):
        """Markdown blockquote element."""

        def __init__(self, text: str):
            """
            Creates a quoted text.

            Args:
                text: The text to be quoted
            """
            self.text = text

        def __str__(self) -> str:
            """Renders the element."""
            return '\n'.join(['> {}'.format(line)
                              for line in self.text.splitlines()]) + '\n'

    class HorizontalRule(MarkdownElement):
        """Markdown horizontal rule element."""

        def __init__(self, rule_char: str = '-'):
            """
            Creates an horizontal rule.

            Args:
                rule_char: The rule character to use

            Raises:
                ValueError: If rule character is invalid
            """
            if rule_char not in ['-', '*', '_']:
                raise ValueError('Invalid rule character')

            self.rule_char = rule_char

        def __str__(self) -> str:
            """Renders the element."""
            return self.rule_char * 3 + '\n'

    class Literal(MarkdownElement):
        """Markdown literal text element."""

        def __init__(self, text: str):
            """
            Generates an escaped text.

            Args:
                text: The text to be escaped
            """
            self.text = text

        def __str__(self) -> str:
            """Renders the element."""
            chars = '\\`*_{}[]()#+-.!<>'

            return ''.join('\\' + char if char in chars else char
                           for char in self.text)

    __aliases__ = dict(header=Header,
                       bold=Bold,
                       italic=Italic,
                       unorderedList=UnorderedList,
                       orderedList=OrderedList,
                       code=Code,
                       image=Image,
                       link=Link,
                       blockquote=Blockquote,
                       rule=HorizontalRule,
                       literal=Literal)


class GithubMarkdown(Markdown, metaclass=MarkdownGenerator):
    """
    GitHub Flavored Markdown extension.

    Attributes:
        __aliases__ (dict): Method aliases
    """

    class Strikethrough(MarkdownElement):
        """Markdown strikethrough element."""

        def __init__(self, text: str):
            """
            Creates a striked text.

            Args:
                text: The text to be striked out
            """
            self.text = text

        def __str__(self) -> str:
            """Renders the element."""
            return '~~{}~~'.format(self.text)

    class TaskList(MarkdownElement):
        """Markdown task list element."""

        def __init__(self, tasks: dict):
            """
            Creates a task list.

            Args:
                tasks: A dictionary of task items
            """
            self.tasks = tasks

        def __str__(self) -> str:
            """Renders the element."""
            return '\n'.join(
                '- [{}] {}'.format('x' if task_completed else ' ', task_item)
                for task_item, task_completed in self.tasks.items()
            ) + '\n'

    class Code(MarkdownElement):
        """Markdown code element."""

        def __init__(self,
                     source: str,
                     inline: bool = True,
                     lang: str = None):
            """
            Creates an inline or block code.

            Args:
                source: The source code
                inline: Whether it should be rendered inline or not
                lang: The code language it should highlight the syntax
            """
            self.source = source
            self.inline = inline
            self.lang = lang

        def __str__(self) -> str:
            """Renders the element."""
            if not self.lang:
                return Markdown.code(self.source, self.inline)

            return '```{}\n{}\n```'.format(self.lang, html.escape(self.source))

    class Table(MarkdownElement):
        """Markdown table element."""

        def __init__(self, data: list, aligning: list = None):
            """
            Creates a table from a 2 dimensional list.

            Args:
                table: A two-dimensional list
                aligning: The table alignments

            Raises:
                ValueError: If table alignments are invalid
            """
            # No aligning: default is left
            if not aligning:
                aligning = ['<'] * len(data[0])

            if not set(aligning).issubset(set(['<', '^', '>'])):
                raise ValueError('Invalid table alignments')

            # Partial aligning: fill missing
            if len(data[0]) > len(aligning):
                aligning.extend(['<'] * (len(data[0]) - len(aligning)))

            self.data = data
            self.aligning = aligning
            self.column_sizes = [max(len(str(item)) for item in row)
                                 for row in zip(*data)]

        def __str__(self) -> str:
            """Renders the element."""
            def _table_row(row, heading=False):
                return '|{}|\n'.format('|'.join([
                    ''.join([
                        ':' if self.aligning[col] == '^' else ' ',  # left char
                        '-' * self.column_sizes[col],
                        ' ' if self.aligning[col] == '<' else ':',  # right char
                    ])
                    if heading else
                    (' {{:' + self.aligning[col] + '{}}} ')
                    .format(self.column_sizes[col]) \
                    .replace('^', '<') \
                    .format(item)
                    for col, item in enumerate(row)
                ]))

            headers = _table_row(self.data[0])
            separators = _table_row(self.data[0], True)
            data = ''.join([_table_row(row) for row in self.data[1:]])

            return headers + separators + data

    __aliases__ = dict(strikethrough=Strikethrough,
                       taskList=TaskList,
                       code=Code,
                       table=Table)


class HtmlGenerator(type):
    """Metaclass for HTML generator."""

    def __getattr__(cls, name: str) -> str:
        """
        Magic method to call a HTML element.

        Args:
            name: The HTML element name

        Returns:
            HTML element

        Raises:
            AttributeError: If an HTML element name is invalid
        """
        if name == '__elements__' or name not in cls.__elements__:
            raise AttributeError('Invalid element')

        parser = etree.HTMLParser()
        parser.set_element_class_lookup(
            etree.ElementDefaultClassLookup(element=HtmlElement))

        def _wrapper(*args, **kwargs):
            return \
                getattr(builder.ElementMaker(makeelement=parser.makeelement),
                        name)(*args, **kwargs)

        return _wrapper


class HtmlElement(MarkupElement, etree.ElementBase):
    """Abstract HTML element class."""

    def __repr__(self) -> str:
        """
        Returns the canonical string representation of the object.

        Returns:
            The canonical string representation of the object
        """
        attr = ''

        if self.text:
            attr += repr(self.text)

        if self.attrib:
            if attr:
                attr += ', '

            attr += ', '.join('{}={}'.format(key, repr(value))
                              for key, value in self.attrib.items())

        return 'Html.{:s}({!s})'.format(self.tag, attr)


class Html(object, metaclass=HtmlGenerator):
    """
    HTML markup generator.

    Attributes:
        __elements__ (list): List of allowed elements
    """

    __elements__ = ['a', 'abbr', 'address', 'area', 'article', 'aside',
                    'audio', 'b', 'base', 'bdi', 'bdo', 'blockquote', 'body',
                    'br', 'button', 'canvas', 'caption', 'cite', 'code',
                    'col', 'colgroup', 'data', 'datalist', 'dd', 'del',
                    'details', 'dfn', 'dialog', 'div', 'dl', 'dt', 'em',
                    'embed', 'fieldset', 'figcaption', 'figure', 'footer',
                    'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'head',
                    'header', 'hr', 'html', 'i', 'iframe', 'img', 'input',
                    'ins', 'kbd', 'label', 'legend', 'li', 'link', 'main',
                    'map', 'mark', 'menu', 'menuitem', 'meta', 'meter', 'nav',
                    'noscript', 'object', 'ol', 'optgroup', 'option',
                    'output', 'p', 'param', 'picture', 'pre', 'progress', 'q',
                    's', 'samp', 'script', 'section', 'select', 'small',
                    'source', 'span', 'strong', 'style', 'sub', 'summary',
                    'sup', 'svg', 'table', 'tbody', 'td', 'template',
                    'textarea', 'tfoot', 'th', 'thead', 'time', 'title', 'tr',
                    'track', 'u', 'ul', 'var', 'video', 'wbr']

    def __new__(cls, element: HtmlElement) -> str:
        """
        Renders an HTML element.

        Attributes:
            element: The HTML element to render
        """
        return _html.tostring(element).decode()
