"""Tests for xmlguard.compat.defusedxml compatibility layer."""

import pytest

from xmlguard._common import EntitiesForbidden, XMLGuardError
from tests.test_attack_payloads import ENTITY_DECL, SAFE_XML


class TestCompatImports:
    def test_import_base_exception(self) -> None:
        from xmlguard.compat.defusedxml import DefusedXmlException
        assert issubclass(DefusedXmlException, XMLGuardError)

    def test_import_elementtree(self) -> None:
        from xmlguard.compat.defusedxml.ElementTree import parse, fromstring, XMLParser
        assert callable(parse)
        assert callable(fromstring)

    def test_import_minidom(self) -> None:
        from xmlguard.compat.defusedxml.minidom import parse, parseString
        assert callable(parse)
        assert callable(parseString)

    def test_import_sax(self) -> None:
        from xmlguard.compat.defusedxml.sax import make_parser, parse, parseString
        assert callable(make_parser)

    def test_import_pulldom(self) -> None:
        from xmlguard.compat.defusedxml.pulldom import parse, parseString
        assert callable(parse)

    def test_import_expatreader(self) -> None:
        from xmlguard.compat.defusedxml.expatreader import ExpatReader, create_parser
        assert callable(create_parser)

    def test_import_expatbuilder(self) -> None:
        from xmlguard.compat.defusedxml.expatbuilder import parse, parseString
        assert callable(parse)

    def test_import_xmlrpc(self) -> None:
        from xmlguard.compat.defusedxml.xmlrpc import monkey_patch, unmonkey_patch
        assert callable(monkey_patch)

    def test_import_lxml(self) -> None:
        from xmlguard.compat.defusedxml.lxml import parse, fromstring
        assert callable(parse)


class TestCompatFunctionality:
    def test_elementtree_blocks_entities(self) -> None:
        from xmlguard.compat.defusedxml.ElementTree import fromstring
        with pytest.raises(EntitiesForbidden):
            fromstring(ENTITY_DECL)

    def test_elementtree_parses_safe_xml(self) -> None:
        from xmlguard.compat.defusedxml.ElementTree import fromstring
        root = fromstring(SAFE_XML)
        assert root.tag == "root"

    def test_minidom_blocks_entities(self) -> None:
        from xmlguard.compat.defusedxml.minidom import parseString
        with pytest.raises(EntitiesForbidden):
            parseString(ENTITY_DECL)

    def test_expatbuilder_blocks_entities(self) -> None:
        from xmlguard.compat.defusedxml.expatbuilder import parseString
        with pytest.raises(EntitiesForbidden):
            parseString(ENTITY_DECL)
