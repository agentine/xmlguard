# xmlguard

Secure XML processing for Python. Drop-in replacement for [defusedxml](https://github.com/tiran/defusedxml).

## Features

- Safe wrappers for all stdlib XML parsers (ElementTree, minidom, SAX, pulldom, expat)
- Blocks entity expansion bombs (Billion Laughs), XXE injection, DTD retrieval
- Configurable limits for entity expansions, DTD depth, element depth, XML size
- Zero runtime dependencies, Python 3.10+
- Full type annotations (PEP 561)
- defusedxml compatibility layer for zero-change migration

## Installation

```
pip install xmlguard
```

## Usage

```python
from xmlguard.ElementTree import parse

# Safe by default — entities, external entities, and DTDs are blocked
tree = parse("data.xml")
```

## License

MIT
