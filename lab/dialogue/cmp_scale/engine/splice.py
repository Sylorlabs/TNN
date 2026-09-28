#!/usr/bin/env python3
"""Build the prototype fork: copy integrated dialogue.zag, replace the
old keyword-scan do_compare with the principled cmp_engine.zag.

Splice anchors (asserted):
  start: 'fn do_compare(ubuf:[]u8,uo:i32,ul:i32,sal:[]u8,pv:[]u8'
  end:   the closing '}' of that function = the line '}' immediately
         preceding the line '// --- F3-ARITHMETIC'
Everything else byte-identical to the integrated source.
"""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "..", "baseline", "dialogue.zag")
ENG = os.path.join(ROOT, "cmp_engine.zag")
DST = os.path.join(ROOT, "dialogue.zag")

with open(SRC) as f:
    src = f.read()
with open(ENG) as f:
    eng = f.read()

start = src.index("fn do_compare(ubuf:[]u8,uo:i32,ul:i32,sal:[]u8,pv:[]u8")
f3 = src.index("// --- F3-ARITHMETIC")
# end of do_compare: last '}\n' before the F3 comment block
end = src.rindex("}\n", 0, f3) + 2
old = src[start:end]
assert old.count("fn do_compare") == 1, "anchor not unique"
assert "time_marker_idx" in old, "unexpected span"

new = src[:start] + eng + src[end:]
with open(DST, "w") as f:
    f.write(new)

# sanity: only the do_compare span changed
assert new.replace(eng, old, 1) == src, "splice mismatch"
print(f"spliced {len(old)} -> {len(eng)} chars; dst={len(new)} chars")
print("old sha:", __import__("hashlib").sha256(old.encode()).hexdigest()[:16])
