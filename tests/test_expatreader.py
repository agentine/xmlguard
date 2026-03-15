"""Tests for xmlguard.expatreader safe wrappers."""

import io

import pytest
from xml.sax import ContentHandler
from xml.sax.xmlreader import XMLReader

from xmlguard._common import EntitiesForbidden, DTDForbidden
from xmlguard.expatreader import ExpatReader, create_parser
from tests.test_attack_payloads import (
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


class TestCreateParser:
    def test_returns_xmlreader(self) -> None:
        parser = create_parser()
        assert isinstance(parser, XMLReader)

    def test_returns_expat_reader(self) -> None:
        parser = create_parser()
        assert isinstance(parser, ExpatReader)


class TestExpatReader:
    def test_safe_xml(self) -> None:
        handler = _TestHandler()
        reader = ExpatReader()
        reader.setContentHandler(handler)
        reader.parse(io.BytesIO(SAFE_XML_BYTES))
        assert "root" in handler.elements

    def test_blocks_entities(self) -> None:
        handler = _TestHandler()
        reader = ExpatReader()
        reader.setContentHandler(handler)
        with pytest.raises(EntitiesForbidden):
            reader.parse(io.BytesIO(ENTITY_DECL.encode()))

    def test_blocks_dtd_when_enabled(self) -> None:
        handler = _TestHandler()
        reader = ExpatReader(forbid_dtd=True)
        reader.setContentHandler(handler)
        with pytest.raises(DTDForbidden):
            reader.parse(io.BytesIO(SIMPLE_DTD.encode()))

    def test_allows_entities_when_disabled(self) -> None:
        handler = _TestHandler()
        reader = ExpatReader(forbid_entities=False)
        reader.setContentHandler(handler)
        reader.parse(io.BytesIO(ENTITY_DECL.encode()))
        assert "foo" in handler.elements
