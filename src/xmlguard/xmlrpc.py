"""Safe XML-RPC wrapper with monkey-patching support.

Provides monkey_patch() and unmonkey_patch() to replace the XML parsers
used by xmlrpc.client and xmlrpc.server with safe alternatives.
"""

from __future__ import annotations

import xmlrpc.client
from typing import Any

from xmlguard._common import (
    EntitiesForbidden,
    ExternalEntitiesForbidden,
    get_default_config,
)

__all__ = [
    "monkey_patch",
    "unmonkey_patch",
]

_original_gp_class: type[xmlrpc.client.ExpatParser] | None = None


class _SafeExpatParser(xmlrpc.client.ExpatParser):
    """ExpatParser subclass that blocks entity expansion and external entities."""

    def __init__(self, target: Any) -> None:
        super().__init__(target)
        cfg = get_default_config()

        parser = getattr(self, "_parser")
        if cfg.forbid_entities:

            def entity_decl_handler(
                entity_name: str,
                is_parameter_entity: bool,
                value: str | None,
                base: str | None,
                system_id: str | None,
                public_id: str | None,
                notation_name: str | None,
            ) -> None:
                raise EntitiesForbidden(entity_name, system_id, public_id)

            parser.EntityDeclHandler = entity_decl_handler

        if cfg.forbid_external:

            def external_entity_ref_handler(
                context: str,
                base: str | None,
                system_id: str | None,
                public_id: str | None,
            ) -> bool:
                raise ExternalEntitiesForbidden(context, system_id, public_id)

            parser.ExternalEntityRefHandler = external_entity_ref_handler


def monkey_patch() -> None:
    """Replace xmlrpc.client's parser with a safe version.

    Call unmonkey_patch() to restore the original.
    """
    global _original_gp_class
    if _original_gp_class is None:
        _original_gp_class = xmlrpc.client.ExpatParser
    xmlrpc.client.ExpatParser = _SafeExpatParser  # type: ignore[misc]


def unmonkey_patch() -> None:
    """Restore the original xmlrpc.client parser."""
    global _original_gp_class
    if _original_gp_class is not None:
        xmlrpc.client.ExpatParser = _original_gp_class  # type: ignore[misc]
        _original_gp_class = None
