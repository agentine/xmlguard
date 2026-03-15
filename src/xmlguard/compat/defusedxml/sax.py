"""defusedxml.sax compatibility — aliases to xmlguard.sax."""

from xmlguard.sax import make_parser, parse, parseString

__all__ = [
    "make_parser",
    "parse",
    "parseString",
]
