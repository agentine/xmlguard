"""Shared constants, exception hierarchy, and configurable limits."""

from __future__ import annotations

from dataclasses import dataclass


class XMLGuardError(Exception):
    """Base exception for all xmlguard errors."""


class EntitiesForbidden(XMLGuardError):
    """Raised when entity expansion is detected and forbidden.

    Attributes:
        name: The entity name that triggered the error.
        system_id: The system identifier, if available.
        public_id: The public identifier, if available.
    """

    def __init__(
        self,
        name: str = "",
        system_id: str | None = None,
        public_id: str | None = None,
    ) -> None:
        self.name = name
        self.system_id = system_id
        self.public_id = public_id
        msg = f"EntitiesForbidden(name='{name}'"
        if system_id is not None:
            msg += f", system_id='{system_id}'"
        if public_id is not None:
            msg += f", public_id='{public_id}'"
        msg += ")"
        super().__init__(msg)


class ExternalEntitiesForbidden(XMLGuardError):
    """Raised when external entity resolution is attempted.

    Attributes:
        name: The entity name that triggered the error.
        system_id: The system identifier, if available.
        public_id: The public identifier, if available.
    """

    def __init__(
        self,
        name: str = "",
        system_id: str | None = None,
        public_id: str | None = None,
    ) -> None:
        self.name = name
        self.system_id = system_id
        self.public_id = public_id
        msg = f"ExternalEntitiesForbidden(name='{name}'"
        if system_id is not None:
            msg += f", system_id='{system_id}'"
        if public_id is not None:
            msg += f", public_id='{public_id}'"
        msg += ")"
        super().__init__(msg)


class DTDForbidden(XMLGuardError):
    """Raised when DTD processing is attempted.

    Attributes:
        name: The DTD name, if available.
        system_id: The system identifier, if available.
        public_id: The public identifier, if available.
    """

    def __init__(
        self,
        name: str = "",
        system_id: str | None = None,
        public_id: str | None = None,
    ) -> None:
        self.name = name
        self.system_id = system_id
        self.public_id = public_id
        msg = f"DTDForbidden(name='{name}'"
        if system_id is not None:
            msg += f", system_id='{system_id}'"
        if public_id is not None:
            msg += f", public_id='{public_id}'"
        msg += ")"
        super().__init__(msg)


class NotSupportedError(XMLGuardError):
    """Raised when a feature is not supported by xmlguard."""


@dataclass
class XMLGuardConfig:
    """Configuration for xmlguard safety limits.

    Attributes:
        forbid_dtd: If True, raise DTDForbidden when a DTD is encountered.
        forbid_entities: If True, raise EntitiesForbidden on entity declarations.
        forbid_external: If True, raise ExternalEntitiesForbidden on external entities.
        max_entity_expansions: Maximum number of entity expansions allowed (0 = unlimited).
        max_xml_size: Maximum XML document size in bytes (0 = unlimited).
    """

    forbid_dtd: bool = False
    forbid_entities: bool = True
    forbid_external: bool = True
    max_entity_expansions: int = 0
    max_xml_size: int = 0


_DEFAULT_CONFIG: XMLGuardConfig = XMLGuardConfig()


def get_default_config() -> XMLGuardConfig:
    """Return the current global default configuration."""
    return _DEFAULT_CONFIG


def set_default_config(config: XMLGuardConfig) -> None:
    """Set the global default configuration."""
    global _DEFAULT_CONFIG
    _DEFAULT_CONFIG = config


def reset_default_config() -> None:
    """Reset the global default configuration to factory defaults."""
    global _DEFAULT_CONFIG
    _DEFAULT_CONFIG = XMLGuardConfig()
