#!/usr/bin/env python3
"""Generate Phase 1C spec fixtures: inputs/<source>/... with representative noise.
Deterministic (no RNG). Run: python3 mk_inputs.py  (writes fixtures/inputs/)
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
IN = os.path.join(HERE, "inputs")


def w(source, name, data: bytes):
    d = os.path.join(IN, source)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, name), "wb") as f:
        f.write(data)


# ---------- gutenberg/1342.txt ----------
# BOM, PG header, START/END markers, \r\n, windows-1252 0xE9, dash spam,
# page number, duplicated paragraph, repeated dialogue lines, footer.
gb = (
    b"\xef\xbb\xbf"
    b"The Project Gutenberg eBook of Foo, by A. Uthor\n"
    b"\n"
    b"This eBook is for the use of anyone anywhere at no cost.\n"
    b"\n"
    b"*** START OF THE PROJECT GUTENBERG EBOOK FOO ***\n"
    b"\n"
    b"\n"
    b"Chapter 1. Beginnings.\r\n"
    b"\r\n"
    b"It was the best of times,\r\n"
    b"it was the worst of times. Caf\xe9 society met.\n"
    b"\n"
    b"----------------------------------------\n"
    b"\n"
    b"* * *\n"
    b"\n"
    b"42\n"
    b"\n"
    b"Advertisement\n"
    b"\n"
    b"Table of Contents\n"
    b"\n"
    b"The well----------known fact__remains unchallenged.   \n"
    b"\n"
    b"Yes.\n"
    b"\n"
    b"No.\n"
    b"\n"
    b"Yes.\n"
    b"\n"
    b"It was the best of times,\n"
    b"it was the worst of times. Caf\xe9 society met.\n"
    b"\n"
    b"*** END OF THE PROJECT GUTENBERG EBOOK FOO ***\n"
    b"\n"
    b"End of the Project Gutenberg EBook footer license text.\n"
)
w("gutenberg", "1342.txt", gb)

# ---------- openstax/biology2e_ch3.xhtml ----------
ox = """<html><head><title>Biology 2e Ch 3</title><style>p{x}</style></head>
<body>
<p>Access for free at openstax.org</p>
<p>This content is available for free at https://cnx.org/contents/abc-123</p>
<h1>Chapter 3. Cell Structure</h1>
<p>The cell &amp; its organelles.</p>
<p>================================</p>
<p>   Spaced    out     text.   </p>
<p>Page 3 of 412</p>
<p>[Page 12]</p>
<!-- footer -->
</body></html>
"""
w("openstax", "biology2e_ch3.xhtml", ox.encode("utf-8"))

# ---------- stackexchange/cooking.xml ----------
se = """<posts>
<row Id="101" PostTypeId="1" Title="How to boil an egg?" Body="&lt;p&gt;Use &lt;b&gt;salt&lt;/b&gt; &amp;amp; heat.&lt;/p&gt;&#10;&#10;&lt;blockquote&gt;&#10;&lt;p&gt;&lt;strong&gt;Possible Duplicate:&lt;/strong&gt; &lt;a href=&quot;http://x&quot;&gt;How long to boil?&lt;/a&gt;&lt;/p&gt;&#10;&lt;/blockquote&gt;&#10;&#10;&lt;p&gt;The well------known method uses &amp;lt;egg&amp;gt; timers.&lt;/p&gt;&#10;&#10;&lt;p&gt;----------&lt;/p&gt;" />
<row Id="202" PostTypeId="2" Body="&lt;p&gt;11 minutes. In code: &lt;code&gt;if (a == b) { boil(); }&lt;/code&gt;.&lt;/p&gt;" />
</posts>
"""
w("stackexchange", "cooking.xml", se.encode("utf-8"))

# ---------- wikibooks/physics.xml ----------
wb = """<mediawiki>
<page>
<title>Physics/Mechanics</title>
<revision><text>From Wikibooks, open books for an open world

== [[Motion|Movement]] ==
The '''quick''' brown fox jumps. See [[inertia]] and {{formula|F=ma}}.&lt;ref&gt;A citation&lt;/ref&gt;

{| class="wikitable"
|-
| cell || cell2
|}

&#8592; Previous chapter

Index

Retrieved from "https://en.wikibooks.org/w/index.php?title=Physics/Mechanics"
</text></revision>
</page>
</mediawiki>
"""
w("wikibooks", "physics.xml", wb.encode("utf-8"))

print("fixtures written to", IN)
