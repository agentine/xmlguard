"""Tests for xmlguard.sax safe wrappers."""

import io

import pytest
from xml.sax import ContentHandler
from xml.sax.xmlreader import XMLReader

from xmlguard._common import EntitiesForbidden, DTDForbidden
from xmlguard.sax import make_parser, parse, parseString
from tests.test_attack_payloads import (
    BILLION_LAUGHS,
    ENTITY_DECL,
    SAFE_XML,
    SAFE_XML_BYTES,
    SIMPLE_DTD,
)


class _TestHandler(ContentHandler):
    """Simple handler that collects element names."""

    def __init__(self) -> None:
        super().__init__()
        self.elements: list[str] = []

    def startElement(self, name: str, attrs: object) -> None:
        self.elements.append(name)


class TestMakeParser:
    def test_returns_xmlreader(self) -> None:
        parser = make_parser()
        assert isinstance(parser, XMLReader)


class TestParse:
    def test_safe_xml(self) -> None:
        handler = _TestHandler()
        parse(io.BytesIO(SAFE_XML_BYTES), handler)
        assert "root" in handler.elements
        assert "child" in handler.elements

    def test_safe_xml_string_input(self) -> None:
        handler = _TestHandler()
        parse(SAFE_XML_BYTES, handler)
        assert "root" in handler.elements

    def test_blocks_entities(self) -> None:
        handler = _TestHandler()
        with pytest.raises(EntitiesForbidden):
            parse(ENTITY_DECL.encode(), handler)

    def test_blocks_billion_laughs(self) -> None:
        handler = _TestHandler()
        with pytest.raises(EntitiesForbidden):
            parse(BILLION_LAUGHS.encode(), handler)

    def test_blocks_dtd_when_enabled(self) -> None:
        handler = _TestHandler()
        with pytest.raises(DTDForbidden):
            parse(SIMPLE_DTD.encode(), handler, forbid_dtd=True)


class TestParseString:
    def test_safe_xml(self) -> None:
        handler = _TestHandler()
        parseString(SAFE_XML, handler)
        assert "root" in handler.elements

    def test_safe_xml_bytes(self) -> None:
        handler = _TestHandler()
        parseString(SAFE_XML_BYTES, handler)
        assert "root" in handler.elements

    def test_blocks_entities(self) -> None:
        handler = _TestHandler()
        with pytest.raises(EntitiesForbidden):
            parseString(ENTITY_DECL, handler)
