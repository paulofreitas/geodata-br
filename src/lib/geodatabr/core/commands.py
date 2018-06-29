#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""
Core commands module.

This module provides the command-line parsing functionality.
"""
# Imports

# Built-in dependencies

import argparse
import sys
import textwrap
from typing import Any

# Package dependencies

from geodatabr import __meta__
from geodatabr.core import logging, types

# Classes


class ArgumentParser(argparse.ArgumentParser):
    """Custom argument parser class."""

    class _LicenseAction(argparse.Action):
        """Custom action class to output the license information and exit."""

        def __init__(self,
                     option_strings: list,
                     dest: str = None,
                     license: str = None,
                     help: str = 'Output license information and exit'):
            """Creates a new license action instance."""
            super().__init__(option_strings=option_strings,
                             dest=dest,
                             nargs=0,
                             help=help)

            self.license = license

        def __call__(self,
                     parser: 'ArgumentParser',
                     namespace: argparse.Namespace,
                     values: list,
                     option_string: str = None):
            """Invokes the license action class."""
            # pylint: disable=W0212
            formatter = parser._get_formatter()
            formatter.add_text(self.license)
            parser._print_message(formatter.format_help(), sys.stdout)
            parser.exit()


    def __init__(self, *args, **kwargs):
        """
        Creates a new argument parser instance.

        Args:
            *args: The argument parser position arguments
            **kwargs: The argument parser keyword arguments
        """
        prolog = kwargs.pop('prolog', None)

        super().__init__(*args, **kwargs)

        # Support for prolog
        self.prolog = prolog

        # Support for license action
        self.register('action', 'license', ArgumentParser._LicenseAction)

        # Default title for positional arguments
        self._optionals.title = 'Arguments'

    def format_usage(self) -> str:
        """Formats usage information."""
        formatter = self._get_formatter()

        # Prolog
        formatter.add_text(self.prolog)

        # Usage
        formatter.add_usage(self.usage,
                            self._actions,
                            self._mutually_exclusive_groups,
                            prefix='Usage: ')

        return formatter.format_help()

    def format_help(self) -> str:
        """Formats help information."""
        # pylint: disable=W0212
        formatter = self._get_formatter()

        # Prolog
        formatter.add_text(self.prolog)

        # Description
        formatter.add_text(self.description)

        # Usage
        formatter.add_usage(self.usage,
                            self._actions,
                            self._mutually_exclusive_groups,
                            prefix='Usage: ')

        # Arguments
        for action_group in self._action_groups:
            formatter.start_section(action_group.title)
            formatter.add_text(action_group.description)
            formatter.add_arguments(action_group._group_actions)
            formatter.end_section()

        # Epilog
        formatter.add_text(self.epilog)

        return formatter.format_help()

    def error(self, message: str):
        """
        Prints an error message to strerr and exits.

        Args:
            message: The error message
        """
        self.print_usage(sys.stderr)
        self.exit(1, '\nERROR: {}\n'.format(message))

    def terminate(self, message: str = None):
        """
        Prints an interruption message to stderr and exits.

        Args:
            message: The interruption message
        """
        self.exit(130, '\r{}\n'.format(message or ''))


class Application(object):
    """
    Main application class.

    Attributes:
        _parser (geodatabr.commands.ArgumentParser): The command-line parser
        _subparsers (argparse._SubParsersAction): The command-line subparsers
        _commands (dict): The application commands mapping
    """

    def __init__(self):
        """Creates a new application instance."""
        self._parser = ArgumentParser(
            description=self.description,
            prolog=self.prolog,
            epilog=self.epilog,
            add_help=False,
            conflict_handler='resolve',
            formatter_class=argparse.RawTextHelpFormatter)
        self._subparsers = self._parser.add_subparsers(
            title='Commands',
            dest='command',
            metavar='')
        self._commands = {}

        self.setDefaults()

    def addCommand(self, command_class: 'Command'):
        """
        Adds a new command to the application.

        Args:
            command_class: The command class
        """
        command = command_class(self)
        command.configure()

        self._commands[command.name] = command

    def addSubparser(self, *args, **kwargs) -> ArgumentParser:
        """
        Adds a new command parser to the application.

        Args:
            *args: The command parser positional arguments
            **kwargs: The command parser keyword arguments

        Returns:
            The command argument parser
        """
        return self._subparsers.add_parser(*args, **kwargs)

    def addArgumentGroup(self, *args, **kwargs) -> argparse._ArgumentGroup:
        """
        Adds a new argument group into the application parser.

        Args:
            *args: The argument group positional arguments
            **kwargs: The argument group keyword arguments

        Returns:
            The argument group instance
        """
        return self._parser.add_argument_group(*args, **kwargs)

    def addArgument(self, *args, **kwargs):
        """
        Adds a new argument into the application parser.

        Args:
            *args: The argument positional arguments
            **kwargs: The argument keyword arguments
        """
        # Allows adding arguments to argument groups
        if isinstance(args[0], argparse._ArgumentGroup):
            args[0].add_argument(*args[1:], **kwargs)

            return

        self._parser.add_argument(*args, **kwargs)

    def setDefaults(self):
        """Sets the application default arguments."""
        default_args = self.addArgumentGroup(title='Troubleshooting',
                                             description='')

        self.addArgument(default_args,
                         '-h', '--help',
                         action='help',
                         help='Display this usage information')
        self.addArgument(default_args,
                         '-V', '--version',
                         action='version',
                         help='Output version information and exit')
        self.addArgument(default_args,
                         '-L', '--license',
                         action='license',
                         license=self.prolog + '\n\n' + self.license,
                         help='Output license information and exit')
        self.addArgument(default_args,
                         '-v', '--verbose',
                         action='store_true',
                         help='Display informational messages and warnings')

    def registerCommands(self):
        """Registers the available command modules into the application."""
        for command in Command.childs():
            self.addCommand(command)

    def parse(self) -> argparse.Namespace:
        """
        Parses the given application arguments.

        Returns:
            The application arguments
        """
        args = self._parser.parse_args()

        logging.Logger.setup(args.verbose)

        return args

    def run(self):
        """Runs the application."""
        self.registerCommands()

        args = self.parse()
        command = self._commands.get(args.command)

        if not command:
            self._parser.print_help()
            self._parser.exit()

        command.handle(args)

    @property
    def name(self) -> str:
        """Gets the application name."""
        return __meta__.__package_name__

    @property
    def version(self) -> str:
        """Gets the application version."""
        return __meta__.__version__

    @property
    def description(self) -> str:
        """Gets the application description."""
        return __meta__.__description__

    @property
    def license(self) -> str:
        """Gets the application license."""
        return textwrap.indent(__meta__.__license_text__, 4 * ' ')

    @property
    def prolog(self) -> str:
        """Gets the application prologue message."""
        return __meta__.__prolog__

    @property
    def epilog(self) -> str:
        """Gets the application epilogue message."""
        return __meta__.__epilog__


class Command(types.AbstractClass):
    """
    Abstract command class.

    Attributes:
        _application (Application): The command application instance
        _parser (ArgumentParser): The command-line parser instance
    """

    def __init__(self, application: Application):
        """
        Creates a new command instance.

        Args:
            application: The application class instance
        """
        self._application = application
        self._parser = application.addSubparser(
            self.name,
            help=self.description,
            usage=self.usage,
            description=self.description,
            prolog=application.prolog,
            epilog=self.epilog,
            conflict_handler='resolve',
            formatter_class=argparse.RawTextHelpFormatter)

        self.setDefaults()

    def setDefaults(self):
        """Sets the command default arguments."""
        default_args = self.addArgumentGroup(title='Troubleshooting',
                                             description='')

        self.addArgument(default_args,
                         '-h', '--help',
                         action='help',
                         help='Display this usage information')

    def addArgumentGroup(self, *args, **kwargs) -> argparse._ArgumentGroup:
        """
        Adds a new argument group into the command parser.

        Args:
            *args: The argument group positional arguments
            **kwargs: The argument group keyword arguments

        Returns:
            The argument group instance
        """
        return self._parser.add_argument_group(*args, **kwargs)

    def addArgument(self, *args, **kwargs):
        """
        Adds a new argument into the command parser.

        Args:
            *args: The argument positional arguments
            **kwargs: The argument keyword arguments
        """
        # Allows adding arguments to argument groups
        if isinstance(args[0], argparse._ArgumentGroup):
            args[0].add_argument(*args[1:], **kwargs)

            return

        self._parser.add_argument(*args, **kwargs)

    @property
    def name(self) -> str:
        """Gets the command name."""
        raise NotImplementedError

    @property
    def description(self) -> str:
        """Gets the command description."""
        raise NotImplementedError

    @property
    def usage(self) -> Any:
        """Gets the command usage syntax."""
        return None

    @property
    def epilog(self) -> Any:
        """Gets the command epilog message."""
        return None

    @property
    def application(self) -> Application:
        """Gets the command application."""
        return self._application

    def configure(self):
        """Registers the command arguments."""
        pass

    def handle(self, args: argparse.Namespace):
        """
        Handles the command.

        Args:
            args: The command arguments
        """
        raise NotImplementedError
