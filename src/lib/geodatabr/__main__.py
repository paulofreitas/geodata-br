#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""Main console script."""
# Imports

# Package dependencies

from geodatabr.core import commands

# Functions


def main():
    """Main entry point."""
    app = commands.Application()
    app.run()


if __name__ == '__main__':
    main()
