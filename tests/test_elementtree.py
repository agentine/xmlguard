"""Tests for xmlguard.ElementTree safe wrappers."""

import io
import os
import tempfile

import pytest

from xmlguard._common import DTDForbidden, EntitiesForbidden, ExternalEntitiesForbidden
from xmlguard.ElementTree import XMLParser, fromstring, iterparse, parse
from tests.test_attack_payloads import (
    BILLION_LAUGHS,
    DTD_EXTERNAL,
    ENTITY_DECL,
    SAFE_XML,
    SAFE_XML_BYTES,
    SIMPLE_DTD,
    XXE_FILE,
    XXE_URL,
)


class TestFromstring:
    def test_safe_xml(self) -> None:
        root = fromstring(SAFE_XML)
        assert root.tag == "root"
        children = list(root)
        assert len(children) == 2
        assert children[0].get("attr") == "value"

    def test_safe_xml_bytes(self) -> None:
        root = fromstring(SAFE_XML_BYTES)
        assert root.tag == "root"

    def test_blocks_entity_declaration(self) -> None:
        with pytest.raises(EntitiesForbidden):
            fromstring(ENTITY_DECL)

    def test_blocks_billion_laughs(self) -> None:
        with pytest.raises(EntitiesForbidden):
            fromstring(BILLION_LAUGHS)

    def test_blocks_xxe_file(self) -> None:
        with pytest.raises(EntitiesForbidden):
            fromstring(XXE_FILE)

    def test_blocks_xxe_url(self) -> None:
        with pytest.raises(EntitiesForbidden):
            fromstring(XXE_URL)

    def test_allows_entities_when_disabled(self) -> None:
        # With forbid_entities=False, simple entity declarations should parse
        root = fromstring(ENTITY_DECL, forbid_entities=False)
        assert root.tag == "foo"

    def test_blocks_dtd_when_enabled(self) -> None:
        with pytest.raises(DTDForbidden):
            fromstring(SIMPLE_DTD, forbid_dtd=True)

    def test_allows_dtd_by_default(self) -> None:
        # By default, DTD without entities is allowed
        root = fromstring(SIMPLE_DTD)
        assert root.tag == "root"


class TestParse:
    def test_parse_file(self) -> None:
        with tempfile.NamedTemporaryFile(suffix=".xml", delete=False) as f:
            f.write(SAFE_XML_BYTES)
            f.flush()
            try:
                tree = parse(f.name)
                root = tree.getroot()
                assert root.tag == "root"
            finally:
                os.unlink(f.name)

    def test_parse_file_object(self) -> None:
        tree = parse(io.BytesIO(SAFE_XML_BYTES))
        root = tree.getroot()
        assert root.tag == "root"

    def test_parse_blocks_entities(self) -> None:
        with pytest.raises(EntitiesForbidden):
            parse(io.BytesIO(ENTITY_DECL.encode()))

    def test_parse_blocks_billion_laughs(self) -> None:
        with pytest.raises(EntitiesForbidden):
            parse(io.BytesIO(BILLION_LAUGHS.encode()))


class TestIterparse:
    def test_safe_xml(self) -> None:
        events = list(iterparse(io.BytesIO(SAFE_XML_BYTES)))
        tags = [tag for _, elem in events for tag in [elem.tag]]
        assert "root" in tags
        assert "child" in tags

    def test_custom_events(self) -> None:
        events = list(
            iterparse(io.BytesIO(SAFE_XML_BYTES), events=("start", "end"))
        )
        event_types = {e for e, _ in events}
        assert "start" in event_types
        assert "end" in event_types

    def test_blocks_entities(self) -> None:
        with pytest.raises(EntitiesForbidden):
            list(iterparse(io.BytesIO(ENTITY_DECL.encode())))


class TestXMLParser:
    def test_safe_feed(self) -> None:
        parser = XMLParser()
        parser.feed(SAFE_XML)
        root = parser.close()
        assert root.tag == "root"

    def test_blocks_entities(self) -> None:
        parser = XMLParser()
        with pytest.raises(EntitiesForbidden):
            parser.feed(ENTITY_DECL)

    def test_per_call_override(self) -> None:
        parser = XMLParser(forbid_entities=False)
        parser.feed(ENTITY_DECL)
        root = parser.close()
        assert root.tag == "foo"

    def test_forbid_dtd(self) -> None:
        parser = XMLParser(forbid_dtd=True)
        with pytest.raises(DTDForbidden):
            parser.feed(SIMPLE_DTD)
