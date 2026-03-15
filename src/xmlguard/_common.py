"""Shared constants, exception hierarchy, and configurable limits."""


class XMLGuardError(Exception):
    """Base exception for all xmlguard errors."""


class EntitiesForbidden(XMLGuardError):
    """Raised when entity expansion is detected and forbidden."""


class ExternalEntitiesForbidden(XMLGuardError):
    """Raised when external entity resolution is attempted."""


class DTDForbidden(XMLGuardError):
    """Raised when DTD processing is attempted."""


class NotSupportedError(XMLGuardError):
    """Raised when a feature is not supported by xmlguard."""
