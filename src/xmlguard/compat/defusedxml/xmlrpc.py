"""defusedxml.xmlrpc compatibility — aliases to xmlguard.xmlrpc."""

from xmlguard.xmlrpc import monkey_patch, unmonkey_patch

__all__ = [
    "monkey_patch",
    "unmonkey_patch",
]
