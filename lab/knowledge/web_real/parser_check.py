#!/usr/bin/env python3
"""parser_check.py — run Sol's edge-case checklist against html_parse (test-only)."""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BIN = os.path.join(HERE, "src", "html_parse")
WORK = os.path.join(HERE, "evidence", "_pcheck")
os.makedirs(WORK, exist_ok=True)

CASES = [
    ("<p>Hello</p>", "B|p|Hello\n"),
    ("<p>  Hello   world  </p>", "B|p|Hello world\n"),
    ("<p>Hello\n\tworld</p>", "B|p|Hello world\n"),
    ("<p>  </p>", ""),
    ("<p>Hello &amp; goodbye</p>", "B|p|Hello & goodbye\n"),
    ("<p>&lt;x&gt; &quot;q&quot; &#39;</p>", "B|p|<x> \"q\" '\n"),
    ("<p>&#65; &#8364;</p>", "B|p|A \u20ac\n"),
    ("<p>A &unknown; B</p>", "B|p|A &unknown; B\n"),
    ("<p>A <b>B</b> C</p>", "B|p|A B C\n"),
    ("<p>A <!-- hidden --> B</p>", "B|p|A B\n"),
    ("<script><p>hidden</p></script><p>shown</p>", "B|p|shown\n"),
    ("<style>.x{display:none}</style><h1>Title</h1>", "B|h1|Title\n"),
    ("<h1>One</h1><h2>Two</h2>", "B|h1|One\nB|h2|Two\n"),
    ("<p>Before <a href=/x>Link</a> after</p>",
     "L|/x|Link\nB|p|Before Link after\n"),
    ("<p><a href='/x'> A   B </a></p>", "L|/x|A B\nB|p|A B\n"),
    ("<p><a href='/x?a=1&amp;b=2'>Link</a></p>", "L|/x?a=1&b=2|Link\nB|p|Link\n"),
    ("<p><a href=/x>One</a> <a href='/y'>Two</a></p>",
     "L|/x|One\nL|/y|Two\nB|p|One Two\n"),
    ("<p>2 < 3</p>", "B|p|2 < 3\n"),
    ("<p>Text", "B|p|Text\n"),
    ("<!-- no terminator", ""),
    ("<script>unclosed", ""),
    ("<title>T</title>", "B|title|T\n"),
    ("<p><a>NoHref</a></p>", "B|p|NoHref\n"),
    ("<a href=/x>outside</a><p>in</p>", "B|p|in\n"),
]

fails = 0
for idx, (inp, want) in enumerate(CASES):
    ip = os.path.join(WORK, "c%02d.html" % idx)
    op = os.path.join(WORK, "c%02d.parse" % idx)
    with open(ip, "w", encoding="utf-8", newline="") as f:
        f.write(inp)
    if os.path.exists(op):
        os.remove(op)
    r = subprocess.run([BIN, ip, op], capture_output=True, timeout=30)
    got = ""
    if os.path.exists(op):
        with open(op, encoding="utf-8") as f:
            got = f.read()
    if r.returncode != 0 or got != want:
        fails += 1
        print("FAIL case %d rc=%d" % (idx, r.returncode))
        print("  in:   %r" % inp)
        print("  want: %r" % want)
        print("  got:  %r" % got)
print("%d/%d pass" % (len(CASES) - fails, len(CASES)))
sys.exit(1 if fails else 0)
