"""Tests for xmlguard.minidom safe wrappers."""

import io
import os
import tempfile

import pytest

from xmlguard._common import DTDForbidden, EntitiesForbidden
from xmlguard.minidom import parse, parseString
from tests.test_attack_payloads import (
    BILLION_LAUGHS,
    ENTITY_DECL,
    SAFE_XML,
    SAFE_XML_BYTES,
    SIMPLE_DTD,
    XXE_FILE,
)


class TestParseString:
    def test_safe_xml(self) -> None:
        doc = parseString(SAFE_XML)
        root = doc.documentElement
        assert root.tagName == "root"

    def test_safe_xml_bytes(self) -> None:
        doc = parseString(SAFE_XML_BYTES)
        assert doc.documentElement.tagName == "root"

    def test_blocks_entity_declaration(self) -> None:
        with pytest.raises(EntitiesForbidden):
            parseString(ENTITY_DECL)

    def test_blocks_billion_laughs(self) -> None:
        with pytest.raises(EntitiesForbidden):
            parseString(BILLION_LAUGHS)

    def test_blocks_xxe(self) -> None:
        with pytest.raises(EntitiesForbidden):
            parseString(XXE_FILE)

    def test_allows_entities_when_disabled(self) -> None:
        doc = parseString(ENTITY_DECL, forbid_entities=False)
        assert doc.documentElement.tagName == "foo"

    def test_blocks_dtd_when_enabled(self) -> None:
        with pytest.raises(DTDForbidden):
            parseString(SIMPLE_DTD, forbid_dtd=True)


class TestParse:
    def test_parse_file(self) -> None:
        with tempfile.NamedTemporaryFile(suffix=".xml", delete=False) as f:
            f.write(SAFE_XML_BYTES)
            f.flush()
            try:
                doc = parse(f.name)
                assert doc.documentElement.tagName == "root"
            finally:
                os.unlink(f.name)

    def test_parse_file_object(self) -> None:
        doc = parse(io.BytesIO(SAFE_XML_BYTES))
        assert doc.documentElement.tagName == "root"

    def test_parse_blocks_entities(self) -> None:
        with pytest.raises(EntitiesForbidden):
            parse(io.BytesIO(ENTITY_DECL.encode()))
