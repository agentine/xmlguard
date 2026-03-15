"""xmlguard — Secure XML processing for Python."""

__version__ = "0.1.0"

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

__all__ = [
    "__version__",
    "DTDForbidden",
    "EntitiesForbidden",
    "ExternalEntitiesForbidden",
    "NotSupportedError",
    "XMLGuardConfig",
    "XMLGuardError",
    "get_default_config",
    "reset_default_config",
    "set_default_config",
]
