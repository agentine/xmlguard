"""xmlguard — Secure XML processing for Python."""

__version__ = "0.1.0"

from xmlguard._common import (
    DTDForbidden,
    EntitiesForbidden,
    ExternalEntitiesForbidden,
    NotSupportedError,
    XMLGuardError,
)

__all__ = [
    "__version__",
    "DTDForbidden",
    "EntitiesForbidden",
    "ExternalEntitiesForbidden",
    "NotSupportedError",
    "XMLGuardError",
]
