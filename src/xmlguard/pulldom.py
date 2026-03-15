"""Safe pulldom wrapper — drop-in replacement for xml.dom.pulldom.

Disables entity expansion and external entity resolution by default.
"""

from __future__ import annotations

import io
from typing import IO, Union
from xml.dom.pulldom import DOMEventStream

from xmlguard.ElementTree import XMLParser as _SafeXMLParser

__all__ = [
    "parse",
    "parseString",
]

_Source = Union[str, IO[bytes]]


def parseString(
    string: str | bytes,
    parser: object | None = None,  # noqa: ARG001
    *,
    forbid_dtd: bool | None = None,
    forbid_entities: bool | None = None,
    forbid_external: bool | None = None,
) -> DOMEventStream:
    """Safely parse an XML string using pulldom, returning a DOMEventStream.

    Args:
        string: XML string or bytes.
        parser: Ignored (kept for API compatibility).
        forbid_dtd: Raise DTDForbidden on DTD declarations.
        forbid_entities: Raise EntitiesForbidden on entity declarations.
        forbid_external: Raise ExternalEntitiesForbidden on external entities.

    Returns:
        A DOMEventStream.
    """
    # Pre-validate with safe parser
    if isinstance(string, str):
        data = string.encode("utf-8")
    else:
        data = string

    validator = _SafeXMLParser(
        forbid_dtd=forbid_dtd,
        forbid_entities=forbid_entities,
        forbid_external=forbid_external,
    )
    validator.feed(data)
    validator.close()

    # Safe to parse with stdlib pulldom
    import xml.dom.pulldom

    return xml.dom.pulldom.parse(io.BytesIO(data))


def parse(
    stream_or_string: _Source,
    parser: object | None = None,  # noqa: ARG001
    bufsize: int | None = None,  # noqa: ARG001
    *,
    forbid_dtd: bool | None = None,
    forbid_entities: bool | None = None,
    forbid_external: bool | None = None,
) -> DOMEventStream:
    """Safely parse an XML file using pulldom, returning a DOMEventStream.

    Args:
        stream_or_string: Filename or file object.
        parser: Ignored (kept for API compatibility).
        bufsize: Ignored (kept for API compatibility).
        forbid_dtd: Raise DTDForbidden on DTD declarations.
        forbid_entities: Raise EntitiesForbidden on entity declarations.
        forbid_external: Raise ExternalEntitiesForbidden on external entities.

    Returns:
        A DOMEventStream.
    """
    if isinstance(stream_or_string, str):
        with open(stream_or_string, "rb") as f:
            data: bytes = f.read()
    else:
        raw = stream_or_string.read()
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
