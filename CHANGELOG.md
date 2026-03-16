# Changelog

## 0.1.0 — 2026-03-15

Initial release. Drop-in replacement for defusedxml with secure defaults.

### Added

- Safe wrappers for all stdlib XML modules: ElementTree, minidom, sax, pulldom, expatreader, expatbuilder
- XML-RPC monkey-patching (`xmlguard.xmlrpc`)
- Optional lxml integration (`xmlguard.lxml`)
- defusedxml compatibility layer (`xmlguard.compat.defusedxml`) for zero-change migration
- Configurable security limits via `XMLGuardConfig`
- Exception hierarchy: `XMLGuardError`, `EntitiesForbidden`, `ExternalEntitiesForbidden`, `DTDForbidden`, `NotSupportedError`
- Protection against Billion Laughs, XXE, DTD retrieval, and decompression bombs
- Full type annotations (PEP 561 compliant)
- 102 tests covering all attack vectors and parser modules
