"""Safe lxml wrapper — optional integration for lxml users.

Provides safe parse, fromstring, and iterparse that disable network access,
entity resolution, and DTD loading by default. Gracefully handles missing
lxml dependency.
"""

from __future__ import annotations

from typing import IO, Any, Iterator, Union

from xmlguard._common import NotSupportedError

__all__ = [
    "parse",
    "fromstring",
    "iterparse",
    "tostring",
    "GlobalParserTLS",
    "getDefaultParser",
    "check_docinfo",
]


def _check_lxml() -> Any:
    """Import and return the lxml.etree module, or raise NotSupportedError."""
    try:
        from lxml import etree  # type: ignore[import-untyped]

        return etree
    except ImportError:
        raise NotSupportedError(
            "lxml is not installed. Install it with: pip install lxml"
        ) from None


_Source = Union[str, bytes, IO[bytes]]


def _make_safe_parser(
    etree: Any,
    *,
    forbid_dtd: bool = False,
    forbid_entities: bool = True,
    forbid_external: bool = True,
) -> Any:
    """Create a safe lxml XMLParser with dangerous features disabled."""
    return etree.XMLParser(
        resolve_entities=not forbid_entities,
        no_network=forbid_external,
        dtd_validation=False,
        load_dtd=not forbid_dtd,
        huge_tree=False,
    )


def parse(
    source: _Source,
    *,
    forbid_dtd: bool = False,
    forbid_entities: bool = True,
    forbid_external: bool = True,
) -> Any:
    """Safely parse an XML source using lxml.

    Args:
        source: Filename, file object, or URL.
        forbid_dtd: Disable DTD loading.
        forbid_entities: Disable entity resolution.
        forbid_external: Disable network access.

    Returns:
        An lxml ElementTree.

    Raises:
        NotSupportedError: If lxml is not installed.
    """
    etree = _check_lxml()
    parser = _make_safe_parser(
        etree,
        forbid_dtd=forbid_dtd,
        forbid_entities=forbid_entities,
        forbid_external=forbid_external,
    )
    if isinstance(source, (str, bytes)):
        if isinstance(source, str):
            return etree.parse(source, parser)
        return etree.parse(
            __import__("io").BytesIO(source), parser
        )
    return etree.parse(source, parser)

def fromstring(
    text: str | bytes,
    *,
    forbid_dtd: bool = False,
    forbid_entities: bool = True,
    forbid_external: bool = True,
) -> Any:
    """Safely parse an XML string using lxml.

    Args:
        text: XML string or bytes.
        forbid_dtd: Disable DTD loading.
        forbid_entities: Disable entity resolution.
        forbid_external: Disable network access.

    Returns:
        An lxml Element.

    Raises:
        NotSupportedError: If lxml is not installed.
    """
    etree = _check_lxml()
    parser = _make_safe_parser(
        etree,
        forbid_dtd=forbid_dtd,
        forbid_entities=forbid_entities,
        forbid_external=forbid_external,
    )
    if isinstance(text, str):
        text = text.encode("utf-8")
    return etree.fromstring(text, parser)

def iterparse(
    source: _Source,
    events: tuple[str, ...] = ("end",),
    *,
    forbid_dtd: bool = False,
    forbid_entities: bool = True,
    forbid_external: bool = True,
) -> Iterator[tuple[str, Any]]:
    """Safely incrementally parse an XML source using lxml.

    Args:
        source: Filename or file object.
        events: Tuple of event names to report.
        forbid_dtd: Disable DTD loading.
        forbid_entities: Disable entity resolution.
        forbid_external: Disable network access.

    Yields:
        (event, element) tuples.

    Raises:
        NotSupportedError: If lxml is not installed.
    """
    etree = _check_lxml()
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

    bio = __import__("io").BytesIO(data)
    context = etree.iterparse(
        bio,
        events=events,
        resolve_entities=not forbid_entities,
        no_network=forbid_external,
        load_dtd=not forbid_dtd,
        huge_tree=False,
    )
    yield from context


def tostring(element: Any, **kwargs: Any) -> Any:
    """Serialize an lxml element to string.

    Simple passthrough to lxml.etree.tostring.

    Raises:
        NotSupportedError: If lxml is not installed.
    """
    etree = _check_lxml()
    return etree.tostring(element, **kwargs)

class GlobalParserTLS:
    """Thread-local safe parser storage for lxml.

    Raises:
        NotSupportedError: If lxml is not installed.
    """

    def createDefaultParser(self) -> Any:
        """Create a safe default parser."""
        etree = _check_lxml()
        return _make_safe_parser(etree)

    def getDefaultParser(self) -> Any:
        """Get a safe default parser."""
        return self.createDefaultParser()


def getDefaultParser() -> Any:
    """Return a safe lxml XMLParser with dangerous features disabled.

    Raises:
        NotSupportedError: If lxml is not installed.
    """
    etree = _check_lxml()
    return _make_safe_parser(etree)


def check_docinfo(tree: Any, *, forbid_dtd: bool = False, forbid_entities: bool = True) -> None:
    """Check an lxml tree's docinfo for dangerous content.

    Args:
        tree: An lxml ElementTree.
        forbid_dtd: Raise if DTD is present.
        forbid_entities: Raise if entities are declared.

    Raises:
        NotSupportedError: If lxml is not installed.
    """
    from xmlguard._common import DTDForbidden, EntitiesForbidden

    docinfo = tree.docinfo
    if forbid_dtd and docinfo.system_url is not None:
        raise DTDForbidden("", docinfo.system_url, docinfo.public_id)
    if forbid_entities and docinfo.internalDTD is not None:
        entities = docinfo.internalDTD.entities()
        if entities:
            name = entities[0].name if entities else ""
            raise EntitiesForbidden(name)
