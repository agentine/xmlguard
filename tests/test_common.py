"""Tests for xmlguard._common: exceptions and configuration."""

import pytest

from xmlguard._common import (
    DTDForbidden,
    EntitiesForbidden,
    ExternalEntitiesForbidden,
    NotSupportedError,
    XMLGuardConfig,
    XMLGuardError,
    get_default_config,
    reset_default_config,
    set_default_config,
)


class TestExceptionHierarchy:
    def test_base_exception(self) -> None:
        assert issubclass(XMLGuardError, Exception)

    def test_entities_forbidden_is_xmlguard_error(self) -> None:
        assert issubclass(EntitiesForbidden, XMLGuardError)

    def test_external_entities_forbidden_is_xmlguard_error(self) -> None:
        assert issubclass(ExternalEntitiesForbidden, XMLGuardError)

    def test_dtd_forbidden_is_xmlguard_error(self) -> None:
        assert issubclass(DTDForbidden, XMLGuardError)

    def test_not_supported_error_is_xmlguard_error(self) -> None:
        assert issubclass(NotSupportedError, XMLGuardError)


class TestEntitiesForbidden:
    def test_default(self) -> None:
        exc = EntitiesForbidden()
        assert exc.name == ""
        assert exc.system_id is None
        assert exc.public_id is None
        assert "EntitiesForbidden" in str(exc)

    def test_with_name(self) -> None:
        exc = EntitiesForbidden("xxe")
        assert exc.name == "xxe"
        assert "xxe" in str(exc)

    def test_with_all_fields(self) -> None:
        exc = EntitiesForbidden("ent", "sys.dtd", "pub")
        assert exc.name == "ent"
        assert exc.system_id == "sys.dtd"
        assert exc.public_id == "pub"
        assert "sys.dtd" in str(exc)
        assert "pub" in str(exc)


class TestExternalEntitiesForbidden:
    def test_default(self) -> None:
        exc = ExternalEntitiesForbidden()
        assert exc.name == ""

    def test_with_details(self) -> None:
        exc = ExternalEntitiesForbidden("xxe", "http://evil.com/x.dtd", None)
        assert exc.name == "xxe"
        assert exc.system_id == "http://evil.com/x.dtd"
        assert "http://evil.com/x.dtd" in str(exc)


class TestDTDForbidden:
    def test_default(self) -> None:
        exc = DTDForbidden()
        assert exc.name == ""

    def test_with_details(self) -> None:
        exc = DTDForbidden("root", "sys.dtd", "pub")
        assert exc.name == "root"
        assert exc.system_id == "sys.dtd"


class TestXMLGuardConfig:
    def test_defaults(self) -> None:
        cfg = XMLGuardConfig()
        assert cfg.forbid_dtd is False
        assert cfg.forbid_entities is True
        assert cfg.forbid_external is True
        assert cfg.max_entity_expansions == 0
        assert cfg.max_xml_size == 0

    def test_custom_values(self) -> None:
        cfg = XMLGuardConfig(
            forbid_dtd=True,
            forbid_entities=False,
            max_entity_expansions=100,
        )
        assert cfg.forbid_dtd is True
        assert cfg.forbid_entities is False
        assert cfg.max_entity_expansions == 100


class TestGlobalConfig:
    def setup_method(self) -> None:
        reset_default_config()

    def teardown_method(self) -> None:
        reset_default_config()

    def test_get_default_config(self) -> None:
        cfg = get_default_config()
        assert isinstance(cfg, XMLGuardConfig)
        assert cfg.forbid_entities is True

    def test_set_default_config(self) -> None:
        new_cfg = XMLGuardConfig(forbid_dtd=True)
        set_default_config(new_cfg)
        assert get_default_config().forbid_dtd is True

    def test_reset_default_config(self) -> None:
        set_default_config(XMLGuardConfig(forbid_dtd=True))
        reset_default_config()
        assert get_default_config().forbid_dtd is False
