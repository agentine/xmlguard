"""Tests for xmlguard.lxml optional integration."""

import pytest

from xmlguard._common import NotSupportedError


class TestLxmlMissing:
    """Tests that run regardless of lxml installation."""

    def test_import_works(self) -> None:
        import xmlguard.lxml  # Should not raise

    def test_check_lxml_raises_when_missing(self) -> None:
        try:
            from lxml import etree  # type: ignore[import-untyped]
            pytest.skip("lxml is installed")
        except ImportError:
            pass

        with pytest.raises(NotSupportedError, match="lxml is not installed"):
            from xmlguard.lxml import parse
            parse("<root/>")

    def test_fromstring_raises_when_missing(self) -> None:
        try:
            from lxml import etree  # type: ignore[import-untyped]
            pytest.skip("lxml is installed")
        except ImportError:
            pass

        with pytest.raises(NotSupportedError):
            from xmlguard.lxml import fromstring
            fromstring("<root/>")
