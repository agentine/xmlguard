"""defusedxml.minidom compatibility — aliases to xmlguard.minidom."""

from xmlguard.minidom import parse, parseString

__all__ = [
    "parse",
    "parseString",
]
