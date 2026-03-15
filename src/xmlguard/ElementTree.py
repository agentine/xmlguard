"""Safe ElementTree wrapper — drop-in replacement for xml.etree.ElementTree.

Disables entity expansion and external entity resolution by default.
"""

from __future__ import annotations

import io
from typing import IO, Any, Iterator, Union
from xml.etree.ElementTree import (
    Element,
    ElementTree,
    TreeBuilder,
    iterparse as _stdlib_iterparse,
)
from xml.parsers import expat

from xmlguard._common import (
    DTDForbidden,
    EntitiesForbidden,
    ExternalEntitiesForbidden,
    get_default_config,
)

__all__ = [
    "parse",
    "iterparse",
    "fromstring",
    "XMLParser",
]


_Source = Union[str, bytes, IO[bytes], IO[str]]


class XMLParser:
    """Safe XMLParser that forbids entities and external references.

    Drop-in replacement for xml.etree.ElementTree.XMLParser.
    """

    def __init__(
        self,
        *,
        target: Any | None = None,
        encoding: str | None = None,
        forbid_dtd: bool | None = None,
        forbid_entities: bool | None = None,
        forbid_external: bool | None = None,
    ) -> None:
        cfg = get_default_config()
        self._forbid_dtd = forbid_dtd if forbid_dtd is not None else cfg.forbid_dtd
        self._forbid_entities = (
            forbid_entities if forbid_entities is not None else cfg.forbid_entities
        )
        self._forbid_external = (
            forbid_external if forbid_external is not None else cfg.forbid_external
        )

        if target is None:
            target = TreeBuilder()

        self._target = target

        parser_kwargs: dict[str, Any] = {}
        if encoding is not None:
            parser_kwargs["encoding"] = encoding

        self._parser = expat.ParserCreate(**parser_kwargs)
        self._parser.DefaultHandlerExpand = self._default_handler
        self._parser.StartElementHandler = getattr(target, "start", None)
        self._parser.EndElementHandler = getattr(target, "end", None)
        self._parser.CharacterDataHandler = getattr(target, "data", None)

        # Disable external entity resolution
        self._parser.ExternalEntityRefHandler = self._external_entity_ref_handler
        self._parser.EntityDeclHandler = self._entity_decl_handler
        self._parser.StartDoctypeDeclHandler = self._start_doctype_decl_handler

    def _default_handler(self, data: str) -> None:
        pass

    def _entity_decl_handler(
        self,
        entity_name: str,
        is_parameter_entity: bool,
        value: str | None,
        base: str | None,
        system_id: str | None,
        public_id: str | None,
        notation_name: str | None,
    ) -> None:
        if self._forbid_entities:
            raise EntitiesForbidden(entity_name, system_id, public_id)

    def _external_entity_ref_handler(
        self,
        context: str,
        base: str | None,
        system_id: str | None,
        public_id: str | None,
    ) -> bool:
        if self._forbid_external:
            raise ExternalEntitiesForbidden(context, system_id, public_id)
        return False

    def _start_doctype_decl_handler(
        self,
        name: str,
        system_id: str | None,
        public_id: str | None,
        has_internal_subset: bool,
    ) -> None:
        if self._forbid_dtd:
            raise DTDForbidden(name, system_id, public_id)

    def feed(self, data: str | bytes) -> None:
        """Feed XML data to the parser."""
        self._parser.Parse(data, False)

    def close(self) -> Element:
        """Finish parsing and return the root element."""
        self._parser.Parse(b"", True)
        result: Element = self._target.close()
        return result


def parse(
    source: _Source,
    *,
    forbid_dtd: bool | None = None,
    forbid_entities: bool | None = None,
    forbid_external: bool | None = None,
) -> ElementTree:
    """Safely parse an XML file, returning an ElementTree.

    Args:
        source: Filename, file object, or URL.
        forbid_dtd: Raise DTDForbidden on DTD declarations.
        forbid_entities: Raise EntitiesForbidden on entity declarations.
        forbid_external: Raise ExternalEntitiesForbidden on external entities.

    Returns:
        An ElementTree instance.
    """
    parser = XMLParser(
        forbid_dtd=forbid_dtd,
        forbid_entities=forbid_entities,
        forbid_external=forbid_external,
    )
    if isinstance(source, (str, bytes)):
        if isinstance(source, str):
            with open(source, "rb") as f:
                data = f.read()
        else:
            data = source
        parser.feed(data)
        root = parser.close()
    else:
        raw = source.read()
        if isinstance(raw, str):
            data = raw.encode("utf-8")
        else:
            data = raw
        parser.feed(data)
        root = parser.close()
    tree = ElementTree(root)
    return tree


def fromstring(
    text: str | bytes,
    *,
    forbid_dtd: bool | None = None,
    forbid_entities: bool | None = None,
    forbid_external: bool | None = None,
) -> Element:
    """Safely parse an XML string, returning the root Element.

    Args:
        text: XML string or bytes.
        forbid_dtd: Raise DTDForbidden on DTD declarations.
        forbid_entities: Raise EntitiesForbidden on entity declarations.
        forbid_external: Raise ExternalEntitiesForbidden on external entities.

    Returns:
        The root Element.
    """
    parser = XMLParser(
        forbid_dtd=forbid_dtd,
        forbid_entities=forbid_entities,
        forbid_external=forbid_external,
    )
    parser.feed(text)
    return parser.close()


def iterparse(
    source: _Source,
    events: tuple[str, ...] | None = None,
    *,
    forbid_dtd: bool | None = None,
    forbid_entities: bool | None = None,
    forbid_external: bool | None = None,
) -> Iterator[tuple[str, Element]]:
    """Safely incrementally parse an XML file.

    Args:
        source: Filename or file object.
        events: Tuple of event names to report.
        forbid_dtd: Raise DTDForbidden on DTD declarations.
        forbid_entities: Raise EntitiesForbidden on entity declarations.
        forbid_external: Raise ExternalEntitiesForbidden on external entities.

    Yields:
        (event, element) tuples.
    """
    # Read all data first for safety checking, then use stdlib iterparse
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

    # Pre-validate with our safe parser (will raise on forbidden content)
    validator = XMLParser(
        forbid_dtd=forbid_dtd,
        forbid_entities=forbid_entities,
        forbid_external=forbid_external,
    )
    validator.feed(data)
    validator.close()

    # Now safe to use stdlib iterparse
    if events is None:
        events = ("end",)
    yield from _stdlib_iterparse(io.BytesIO(data), events=events)
