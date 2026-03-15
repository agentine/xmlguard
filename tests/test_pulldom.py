"""Tests for xmlguard.pulldom safe wrappers."""

import io
import os
import tempfile

import pytest

from xmlguard._common import EntitiesForbidden, DTDForbidden
from xmlguard.pulldom import parse, parseString
from tests.test_attack_payloads import (
    BILLION_LAUGHS,
    ENTITY_DECL,
    SAFE_XML,
    SAFE_XML_BYTES,
    SIMPLE_DTD,
)


class TestParseString:
    def test_safe_xml(self) -> None:
        stream = parseString(SAFE_XML)
        events = [(event, node) for event, node in stream]
        assert len(events) > 0

    def test_safe_xml_bytes(self) -> None:
        stream = parseString(SAFE_XML_BYTES)
        events = list(stream)
        assert len(events) > 0

    def test_blocks_entities(self) -> None:
        with pytest.raises(EntitiesForbidden):
            parseString(ENTITY_DECL)

    def test_blocks_billion_laughs(self) -> None:
        with pytest.raises(EntitiesForbidden):
            parseString(BILLION_LAUGHS)

    def test_blocks_dtd_when_enabled(self) -> None:
        with pytest.raises(DTDForbidden):
            parseString(SIMPLE_DTD, forbid_dtd=True)


class TestParse:
    def test_parse_file(self) -> None:
        with tempfile.NamedTemporaryFile(suffix=".xml", delete=False) as f:
            f.write(SAFE_XML_BYTES)
            f.flush()
            try:
                stream = parse(f.name)
                events = list(stream)
                assert len(events) > 0
            finally:
                os.unlink(f.name)

    def test_parse_file_object(self) -> None:
        stream = parse(io.BytesIO(SAFE_XML_BYTES))
        events = list(stream)
        assert len(events) > 0

    def test_parse_blocks_entities(self) -> None:
        with pytest.raises(EntitiesForbidden):
            parse(io.BytesIO(ENTITY_DECL.encode()))
