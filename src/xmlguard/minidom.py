"""Safe minidom wrapper — drop-in replacement for xml.dom.minidom.

Disables entity expansion and external entity resolution by default.
"""

from __future__ import annotations

from typing import IO, Union
from xml.dom.minidom import Document
from xml.dom.minidom import parseString as _stdlib_parseString

from xmlguard.ElementTree import XMLParser as _SafeXMLParser

__all__ = [
    "parse",
    "parseString",
]

_Source = Union[str, IO[bytes]]


def parseString(
    string: str | bytes,
    *,
    forbid_dtd: bool | None = None,
    forbid_entities: bool | None = None,
    forbid_external: bool | None = None,
) -> Document:
    """Safely parse an XML string using minidom, returning a Document.

    Args:
        string: XML string or bytes.
        forbid_dtd: Raise DTDForbidden on DTD declarations.
        forbid_entities: Raise EntitiesForbidden on entity declarations.
        forbid_external: Raise ExternalEntitiesForbidden on external entities.

    Returns:
        A minidom Document.
    """
    # Validate with safe parser first
    validator = _SafeXMLParser(
        forbid_dtd=forbid_dtd,
        forbid_entities=forbid_entities,
        forbid_external=forbid_external,
    )
    if isinstance(string, str):
        data = string.encode("utf-8")
    else:
        data = string
    validator.feed(data)
    validator.close()

    # Safe to parse with stdlib
    return _stdlib_parseString(data)


def parse(
    file: _Source,
    *,
    forbid_dtd: bool | None = None,
    forbid_entities: bool | None = None,
    forbid_external: bool | None = None,
) -> Document:
    """Safely parse an XML file using minidom, returning a Document.

    Args:
        file: Filename or file object.
        forbid_dtd: Raise DTDForbidden on DTD declarations.
        forbid_entities: Raise EntitiesForbidden on entity declarations.
        forbid_external: Raise ExternalEntitiesForbidden on external entities.

    Returns:
        A minidom Document.
    """
    if isinstance(file, str):
        with open(file, "rb") as f:
            data: bytes = f.read()
    else:
        raw = file.read()
        if isinstance(raw, str):
            data = raw.encode("utf-8")
        else:
            data = raw

    return parseString(
        data,
        forbid_dtd=forbid_dtd,
        forbid_entities=forbid_entities,
        forbid_external=forbid_external,
    )
