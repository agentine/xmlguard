"""Tests for xmlguard.xmlrpc monkey-patching."""

import xmlrpc.client

import pytest

from xmlguard._common import EntitiesForbidden
from xmlguard.xmlrpc import monkey_patch, unmonkey_patch


class TestMonkeyPatch:
    def setup_method(self) -> None:
        unmonkey_patch()

    def teardown_method(self) -> None:
        unmonkey_patch()

    def test_monkey_patch_replaces_parser(self) -> None:
        original = xmlrpc.client.ExpatParser
        monkey_patch()
        assert xmlrpc.client.ExpatParser is not original

    def test_unmonkey_patch_restores(self) -> None:
        original = xmlrpc.client.ExpatParser
        monkey_patch()
        unmonkey_patch()
        assert xmlrpc.client.ExpatParser is original

    def test_double_monkey_patch_safe(self) -> None:
        original = xmlrpc.client.ExpatParser
        monkey_patch()
        monkey_patch()  # Should not break
        unmonkey_patch()
        assert xmlrpc.client.ExpatParser is original

    def test_unmonkey_patch_without_patch(self) -> None:
        # Should be a no-op
        unmonkey_patch()

    def test_safe_parser_blocks_entities(self) -> None:
        monkey_patch()
        # The safe parser should block entity declarations
        target = xmlrpc.client.Unmarshaller()
        parser = xmlrpc.client.ExpatParser(target)  # type: ignore[arg-type]
        xml_data = b"""\
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe "test">
]>
<methodResponse><params><param><value><string>ok</string></value></param></params></methodResponse>
"""
        with pytest.raises(EntitiesForbidden):
            parser.feed(xml_data)
