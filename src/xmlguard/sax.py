"""Safe SAX wrapper — drop-in replacement for xml.sax.

Disables external entity resolution and DTD processing by default.
"""

from __future__ import annotations

import io
from typing import IO, Union
from xml.sax import ContentHandler, ErrorHandler, make_parser as _stdlib_make_parser
from xml.sax.handler import (
    feature_external_ges,
    feature_external_pes,
)
from xml.sax.xmlreader import XMLReader

from xmlguard._common import get_default_config

__all__ = [
    "make_parser",
    "parse",
    "parseString",
]

_Source = Union[str, bytes, IO[bytes]]


def make_parser(
    parser_list: list[str] | None = None,
    *,
    forbid_external: bool | None = None,
) -> XMLReader:
    """Create a safe SAX parser with external entities disabled.

    Args:
        parser_list: Optional list of parser module names.
        forbid_external: Raise ExternalEntitiesForbidden on external entities.

    Returns:
        A configured SAX XMLReader.
    """
    cfg = get_default_config()
    _forbid_external = (
        forbid_external if forbid_external is not None else cfg.forbid_external
    )

    if parser_list is not None:
        parser = _stdlib_make_parser(parser_list)
    else:
        parser = _stdlib_make_parser()

    if _forbid_external:
        try:
            parser.setFeature(feature_external_ges, False)
        except Exception:
            pass
        try:
            parser.setFeature(feature_external_pes, False)
        except Exception:
            pass

    return parser


def parse(
    source: _Source,
    handler: ContentHandler,
    error_handler: ErrorHandler | None = None,
    *,
    forbid_dtd: bool | None = None,
    forbid_entities: bool | None = None,
    forbid_external: bool | None = None,
) -> None:
    """Safely parse an XML source using SAX.

    Args:
        source: Filename, URL, or file object.
        handler: SAX ContentHandler.
        error_handler: Optional SAX ErrorHandler.
        forbid_dtd: Raise DTDForbidden on DTD declarations.
        forbid_entities: Raise EntitiesForbidden on entity declarations.
        forbid_external: Raise ExternalEntitiesForbidden on external entities.
    """
    from xmlguard.ElementTree import XMLParser as _SafeXMLParser

    # Pre-validate with safe parser
    if isinstance(source, str):
        with open(source, "rb") as f:
            data = f.read()
    elif isinstance(source, bytes):
        data = source
    else:
        raw = source.read()
        if isinstance(raw, str):
            data = raw.encode("utf-8")
        else:
            data = raw

    validator = _SafeXMLParser(
        forbid_dtd=forbid_dtd,
        forbid_entities=forbid_entities,
        forbid_external=forbid_external,
    )
    validator.feed(data)
    validator.close()

    # Now safe to use stdlib SAX parser
    import xml.sax

    if error_handler is not None:
        xml.sax.parse(io.BytesIO(data), handler, error_handler)
    else:
        xml.sax.parse(io.BytesIO(data), handler)


def parseString(
    string: str | bytes,
    handler: ContentHandler,
    error_handler: ErrorHandler | None = None,
    *,
    forbid_dtd: bool | None = None,
    forbid_entities: bool | None = None,
    forbid_external: bool | None = None,
) -> None:
    """Safely parse an XML string using SAX.

    Args:
        string: XML string or bytes.
        handler: SAX ContentHandler.
        error_handler: Optional SAX ErrorHandler.
        forbid_dtd: Raise DTDForbidden on DTD declarations.
        forbid_entities: Raise EntitiesForbidden on entity declarations.
        forbid_external: Raise ExternalEntitiesForbidden on external entities.
    """
    if isinstance(string, str):
        data = string.encode("utf-8")
    else:
        data = string

    parse(
        data,
        handler,
        error_handler,
        forbid_dtd=forbid_dtd,
        forbid_entities=forbid_entities,
        forbid_external=forbid_external,
    )
