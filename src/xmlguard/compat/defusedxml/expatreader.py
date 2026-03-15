"""defusedxml.expatreader compatibility — aliases to xmlguard.expatreader."""

from xmlguard.expatreader import ExpatReader, create_parser

__all__ = [
    "ExpatReader",
    "create_parser",
]
