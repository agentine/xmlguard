"""defusedxml compatibility — maps defusedxml imports to xmlguard equivalents.

Usage:
    from xmlguard.compat.defusedxml.ElementTree import parse
    from xmlguard.compat.defusedxml import DefusedXmlException
"""

from xmlguard._common import (
    DTDForbidden,
    EntitiesForbidden,
    ExternalEntitiesForbidden,
    NotSupportedError,
    XMLGuardError,
)

# defusedxml exception aliases
DefusedXmlException = XMLGuardError

__all__ = [
    "DefusedXmlException",
    "DTDForbidden",
    "EntitiesForbidden",
    "ExternalEntitiesForbidden",
    "NotSupportedError",
]
