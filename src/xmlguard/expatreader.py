"""Safe expat-based SAX reader wrapper.

Wraps xml.sax.expatreader with safe defaults — disables external entity
resolution and entity expansion.
"""

from __future__ import annotations

from xml.sax.expatreader import ExpatParser
from xml.sax.handler import feature_external_ges, feature_external_pes
from xml.sax.xmlreader import XMLReader

from xmlguard._common import (
    DTDForbidden,
    EntitiesForbidden,
    ExternalEntitiesForbidden,
    get_default_config,
)

__all__ = [
    "ExpatReader",
    "create_parser",
]


class ExpatReader(ExpatParser):
    """Safe expat-based SAX reader.

    Subclasses the stdlib ExpatParser to intercept and block entity
    declarations, external entity references, and DTD declarations.
    """

    def __init__(
        self,
        *,
        forbid_dtd: bool | None = None,
        forbid_entities: bool | None = None,
        forbid_external: bool | None = None,
    ) -> None:
        super().__init__()
        cfg = get_default_config()
        self._forbid_dtd = forbid_dtd if forbid_dtd is not None else cfg.forbid_dtd
        self._forbid_entities = (
            forbid_entities if forbid_entities is not None else cfg.forbid_entities
        )
        self._forbid_external = (
            forbid_external if forbid_external is not None else cfg.forbid_external
        )

    def reset(self) -> None:
        """Reset the parser and install safety handlers."""
        super().reset()
        parser = getattr(self, "_parser", None)
        if parser is not None:
            parser.EntityDeclHandler = self._entity_decl_handler
            parser.ExternalEntityRefHandler = self._external_entity_ref_handler
            parser.StartDoctypeDeclHandler = self._start_doctype_decl_handler

            if self._forbid_external:
                try:
                    self.setFeature(feature_external_ges, False)
                except Exception:
                    pass
                try:
                    self.setFeature(feature_external_pes, False)
                except Exception:
                    pass

    def _entity_decl_handler(
        self,
        entity_name: str,
        is_parameter_entity: bool,
        value: str | None,
        base: str | None,
        system_id: str | None,
        public_id: str | None,
        notation_name: str | None,
    ) -> None:
        if self._forbid_entities:
            raise EntitiesForbidden(entity_name, system_id, public_id)

    def _external_entity_ref_handler(
        self,
        context: str,
        base: str | None,
        system_id: str | None,
        public_id: str | None,
    ) -> bool:
        if self._forbid_external:
            raise ExternalEntitiesForbidden(context, system_id, public_id)
        return False

    def _start_doctype_decl_handler(
        self,
        name: str,
        system_id: str | None,
        public_id: str | None,
        has_internal_subset: bool,
    ) -> None:
        if self._forbid_dtd:
            raise DTDForbidden(name, system_id, public_id)


def create_parser(
    *,
    forbid_dtd: bool | None = None,
    forbid_entities: bool | None = None,
    forbid_external: bool | None = None,
) -> XMLReader:
    """Create a safe expat-based SAX parser.

    Args:
        forbid_dtd: Raise DTDForbidden on DTD declarations.
        forbid_entities: Raise EntitiesForbidden on entity declarations.
        forbid_external: Raise ExternalEntitiesForbidden on external entities.

    Returns:
        A safe ExpatReader instance.
    """
    return ExpatReader(
        forbid_dtd=forbid_dtd,
        forbid_entities=forbid_entities,
        forbid_external=forbid_external,
    )
