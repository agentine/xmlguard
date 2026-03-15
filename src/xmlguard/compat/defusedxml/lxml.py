"""defusedxml.lxml compatibility — aliases to xmlguard.lxml."""

from xmlguard.lxml import (
    GlobalParserTLS,
    check_docinfo,
    fromstring,
    getDefaultParser,
    iterparse,
    parse,
    tostring,
)

__all__ = [
    "GlobalParserTLS",
    "check_docinfo",
    "fromstring",
    "getDefaultParser",
    "iterparse",
    "parse",
    "tostring",
]
