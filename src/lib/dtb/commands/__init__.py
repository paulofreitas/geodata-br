#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2016 Paulo Freitas
# MIT License (see LICENSE file)
'''
Commands package

This package provides an application class, an abstract command class and
concrete command modules.
'''
# Imports

# Built-in dependencies

import argparse
import sys

# Package dependencies

from dtb.core.logging import Logger
from dtb.core.types import AbstractClass

# Package metadata

__version__ = '1.0-dev'
__author__ = 'Paulo Freitas <me@paulofreitas.me>'
__copyright__ = 'Copyright (c) 2013-2016 Paulo Freitas'
__license__ = 'MIT License'

# Module logging

logger = Logger.instance(__name__)

# Classes

class Application(object):
    '''Main application class.'''

    def __init__(self):
        '''Constructor.'''
        self._parser = argparse.ArgumentParser(
            description=self.description,
            epilog=self.epilog,
            add_help=False,
            conflict_handler='resolve',
            formatter_class=HelpFormatter)
        self._subparsers = self._parser.add_subparsers(
            title='Commands',
            dest='command',
            metavar='')
        self._commands = {}

        self.setDefaults()

    def setDefaults(self):
        '''Sets the application default arguments.'''
        default_args = self.addArgumentGroup('Arguments')

        self.addArgument(default_args,
                         '-h', '--help',
                         action='help',
                         help='Display this information')
        self.addArgument(default_args,
                         '-v', '--version',
                         action='version',
                         version='%(prog)s ' + self.version,
                         help='Show version information and exit')
        self.addArgument(default_args,
                         '-V', '--verbose',
                         action='store_true',
                         help='Display informational messages and warnings')

    def addParser(self, *args, **kwargs):
        '''Adds a new command parser to the application.

        Returns:
            argparse.ArgumentParser: The command argument parser
        '''
        return self._subparsers.add_parser(*args, **kwargs)

    def addCommand(self, command_class):
        '''Adds a new command to the application.

        Arguments:
            command_class (Command): The command class
        '''
        command = command_class(self)
        command.configure()

        self._commands[command.name] = command

    def addArgumentGroup(self, title):
        '''Adds a new argument group.

        Arguments:
            title (str): The argument group title

        Returns:
            argparse._ArgumentGroup: The argument group instance
        '''
        return self._parser.add_argument_group(title)

    def addArgument(self, group, *args, **kwargs):
        '''Adds a new argument to the given argument group.

        Arguments:
            group (argparse._ArgumentGroup): The argument group
        '''
        group.add_argument(*args, **kwargs)

    def registerCommands(self):
        '''Registers the available command modules into the application.'''
        for command in Command.childs():
            self.addCommand(command)

    def parse(self):
        '''Parses the given application arguments.'''
        args = self._parser.parse_args()

        Logger.setup(args.verbose)

        return args

    def run(self):
        '''Runs the application.'''
        self.registerCommands()

        args = self.parse()
        command = self._commands.get(args.command)

        if command:
            command.handle(args)

    @property
    def version(self):
        '''Defines the application version.'''
        return __version__

    @property
    def description(self):
        '''Defines the application description.'''
        return 'Brazilian territorial data exporter'''

    @property
    def epilog(self):
        '''Defines the application epilog message.'''
        return 'Report bugs and feature requests to {}.' \
            .format('https://github.com/paulofreitas/dtb-ibge/issues')


class Command(AbstractClass):
    '''Abstract command class.'''

    def __init__(self, application):
        '''Constructor.

        Arguments:
            application (Application): The application class instance
        '''
        self._parser = application.addParser(
            self.name,
            help=self.description,
            usage=self.usage,
            description=self.description,
            epilog=self.epilog,
            conflict_handler='resolve',
            formatter_class=HelpFormatter)

        self.setDefaults()

    def setDefaults(self):
        '''Sets the command default arguments.'''
        self.addArgument('-h', '--help',
                         action='help',
                         help='Display this information')

    def addArgument(self, *args, **kwargs):
        '''Adds a new argument to the command.'''
        self._parser.add_argument(*args, **kwargs)

    @property
    def name(self):
        '''Defines the command name.'''
        raise NotImplementedError

    @property
    def description(self):
        '''Defines the command description.'''
        return None

    @property
    def usage(self):
        '''Defines the command usage syntax.'''
        return None

    @property
    def epilog(self):
        '''Defines the command epilog message.'''
        return None

    def configure(self):
        '''Defines the command arguments.'''
        pass

    def handle(self, args):
        '''Handles the command.

        Arguments:
            args (argparser.Namespace): The command arguments
        '''
        raise NotImplementedError


class HelpFormatter(argparse.HelpFormatter):
    '''Custom help formatter class to use when parsing arguments.'''

    def start_section(self, heading):
        heading = heading.replace('optional arguments', 'Arguments')

        return super(self.__class__, self).start_section(heading)
