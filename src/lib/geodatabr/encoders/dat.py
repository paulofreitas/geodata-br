#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""Generic Data File encoder module."""
# Imports

# Package dependencies

from geodatabr.encoders import EncoderFormat

# Classes


class DatFormat(EncoderFormat):
    """Encoder format class for Generic Data File file format."""

    @property
    def name(self) -> str:
        """Gets the encoder format name."""
        return 'dat'

    @property
    def friendlyName(self) -> str:
        """Gets the encoder format friendly name."""
        return 'Generic Data File'

    @property
    def extension(self) -> str:
        """Gets the encoder format extension."""
        return '.dat'

    @property
    def type(self) -> str:
        """Gets the encoder format type."""
        return 'Data'

    @property
    def mimeType(self) -> None:
        """Gets the encoder format media type."""
        return None
