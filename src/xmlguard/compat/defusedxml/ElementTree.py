"""defusedxml.ElementTree compatibility — aliases to xmlguard.ElementTree."""

from xmlguard.ElementTree import (
    XMLParser,
    fromstring,
    iterparse,
    parse,
)

__all__ = [
    "XMLParser",
    "fromstring",
    "iterparse",
    "parse",
]
