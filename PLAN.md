# xmlguard — Secure XML Processing for Python

**Replaces:** [defusedxml](https://github.com/tiran/defusedxml) (150M downloads/month, last stable release March 2021)

**Package name:** xmlguard (verified available on PyPI)

**Language:** Python 3.10+

---

## Problem

defusedxml is the Python ecosystem's standard defense against XML attacks (entity expansion, external entity injection, DTD retrieval, decompression bombs). It is recommended in Python's official documentation, referenced by OWASP, and enforced by security linters (Bandit, Ruff). Despite 150M monthly downloads:

- Last stable release (0.7.1) was March 2021 — over 5 years ago
- Release candidate 0.8.0rc2 has been sitting unreleased since September 2023
- Official classifiers only declare Python 2.7–3.9 support
- Single maintainer (Christian Heimes) with minimal activity since 2023
- No active forks with traction (top fork: 1 star)
- Open compatibility questions for Python 3.12/3.13 with no response

## Scope

Drop-in replacement for defusedxml with:

1. **Safe XML parsers** — Wrap all stdlib XML modules with secure defaults
2. **Attack prevention** — Block entity expansion, external entities, DTD processing, decompression bombs
3. **Modern Python** — Target Python 3.10–3.13+, typed, zero dependencies
4. **API compatibility** — Match defusedxml's public API surface for easy migration
5. **Additional protections** — XInclude blocking, configurable limits, better error messages

## Architecture

### Module Structure

```
xmlguard/
├── __init__.py          # Version, convenience imports
├── _common.py           # Shared constants, limit config, exception base
├── ElementTree.py       # Safe ElementTree (parse, iterparse, fromstring, XMLParser)
├── minidom.py           # Safe minidom (parse, parseString)
├── sax.py               # Safe SAX (parse, parseString, make_parser)
├── pulldom.py           # Safe pulldom (parse, parseString)
├── expatreader.py       # Safe expat reader
├── expatbuilder.py      # Safe expatbuilder
├── xmlrpc.py            # Safe XML-RPC (monkey_patch, unmonkey_patch)
├── lxml.py              # Optional lxml integration (safe parse, fromstring, etc.)
└── py.typed             # PEP 561 marker
```

### Key Design Decisions

- **Namespace mirroring:** Each module mirrors its stdlib counterpart's public API, overriding only the unsafe entry points. `from xmlguard.ElementTree import parse` is a drop-in for `from defusedxml.ElementTree import parse`.
- **Configurable limits:** Global defaults with per-call overrides for max entity expansions, max DTD depth, max element depth, max XML size.
- **Exception hierarchy:** `XMLGuardError` base with specific subclasses: `EntitiesForbidden`, `ExternalEntitiesForbidden`, `DTDForbidden`, `NotSupportedError`.
- **Type annotations:** Full typing throughout, PEP 561 compliant.
- **defusedxml compat layer:** `xmlguard.compat` module that aliases defusedxml import paths for zero-change migration.

### Attack Vectors Mitigated

| Attack | Method |
|--------|--------|
| Billion Laughs (entity expansion bomb) | Disable entity expansion, enforce limits |
| External Entity Injection (XXE) | Disable external entity resolution |
| DTD Retrieval | Disable DTD processing |
| Decompression Bomb | Configurable max XML size limits |
| XInclude Injection | Disable XInclude processing by default |

## Deliverables

1. Core library with all safe parser wrappers
2. Full test suite covering all attack vectors with known payloads
3. defusedxml compatibility layer for zero-friction migration
4. Type stubs and PEP 561 compliance
5. PyPI package: `xmlguard`
6. Documentation with migration guide from defusedxml

## Non-Goals

- Custom XML parser implementation (we wrap stdlib)
- HTML parsing (out of scope)
- Schema validation (out of scope)
