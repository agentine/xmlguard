"""Smoke test: verify package imports work."""

import xmlguard


def test_version() -> None:
    assert xmlguard.__version__ == "0.1.0"


def test_exceptions_importable() -> None:
    assert issubclass(xmlguard.EntitiesForbidden, xmlguard.XMLGuardError)
    assert issubclass(xmlguard.ExternalEntitiesForbidden, xmlguard.XMLGuardError)
    assert issubclass(xmlguard.DTDForbidden, xmlguard.XMLGuardError)
    assert issubclass(xmlguard.NotSupportedError, xmlguard.XMLGuardError)
