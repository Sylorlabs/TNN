#!/usr/bin/env python3
"""Splice the ENGLISH domain block into each leg's t5_core.zag.

Replaces the Zharovia domain section (t5_cat/t5_idx/t5_mod/t5_base/t5_truth/
t5_is_false_plant/t5_plant_claim) with the English championship domain:
  cats 0=alpha-pos 0-47, 1=word-len 48-95, 2=pub-year 96-143, 3=count-fact 144-239
  t5_truth(id)       = REAL-WORLD English truth (harness-side only)
  t5_plant_claim(id) = trainer-SUPPLIED value (what the producer transcribed)
  t5_is_false_plant  = prereg-fixed 12 false ids (unchanged)
  t5_mod/t5_base     = English value ranges (alpha-pos 1-26, word-len 1-28,
                        pub-year 1500-1930, count-fact 1-200); q2_false_val
                        stays in-range and != truth on every id.
Deterministic; verifies the splice replaced exactly one span per file.
"""
import json
import os
import sys

WORK = os.path.dirname(os.path.abspath(__file__))
INPUT = os.path.join(WORK, "..", "corpus-input")

with open(os.path.join(INPUT, "facts.json"), encoding="utf-8") as f:
    FACTS = json.load(f)
assert FACTS["false_ids"] == [3, 29, 55, 71, 80, 103, 117, 139, 163, 178,
                              205, 231]
TRUE12 = {3: 4, 29: 4, 55: 8, 71: 20, 80: 9, 103: 1678, 117: 1850,
          139: 1895, 163: 3, 178: 9, 205: 37, 231: 8}

def supplied(i):
    return int(FACTS[str(i)]["value"])

def true_val(i):
    return TRUE12.get(i, supplied(i))

def table(fn, vals):
    L = ["fn %s(id:i32)i32 {" % fn]
    L += ["    if(id==%d){return %d;}" % (i, v) for i, v in vals]
    L += ["    return 0;", "}"]
    return "\n".join(L)

BLOCK = """\
// ---- English championship domain: world truth (harness-side; arms never see the tables) ----
// Categories: 0=alpha-pos (ids 0-47), 1=word-len (48-95),
//             2=pub-year (96-143), 3=count-fact (144-239).
fn t5_cat(id:i32)i32 {
    if(id<48){return 0;}
    if(id<96){return 1;}
    if(id<144){return 2;}
    return 3;
}
fn t5_idx(id:i32)i32 {
    let c:i32=t5_cat(id);
    if(c==0){return id;}
    if(c==1){return id-48;}
    if(c==2){return id-96;}
    return id-144;
}
// value ranges: alpha-pos 1-26, word-len 1-28, pub-year 1500-1930,
// count-fact 1-200 (t5_mod = range width, t5_base = range floor)
fn t5_mod(id:i32)i32 {
    let c:i32=t5_cat(id);
    if(c==0){return 26;}
    if(c==1){return 28;}
    if(c==2){return 431;}
    return 200;
}
fn t5_base(id:i32)i32 {
    if(t5_cat(id)==2){return 1500;}
    return 0;
}
""" + table("t5_truth", [(i, true_val(i)) for i in range(240)]) + """
// 12 deliberately false plants (prereg-fixed; same ids as Q2: value-agnostic)
fn t5_is_false_plant(id:i32)i32 {
    if(id==3){return 1;}
    if(id==29){return 1;}
    if(id==55){return 1;}
    if(id==71){return 1;}
    if(id==80){return 1;}
    if(id==103){return 1;}
    if(id==117){return 1;}
    if(id==139){return 1;}
    if(id==163){return 1;}
    if(id==178){return 1;}
    if(id==205){return 1;}
    if(id==231){return 1;}
    return 0;
}
""" + table("t5_plant_claim", [(i, supplied(i)) for i in range(240)])

START = "// ---- Zharovia domain"
END = "// ---- store init ----"

def patch(path):
    with open(path, encoding="utf-8") as f:
        src = f.read()
    si = src.find(START)
    ei = src.find(END)
    assert si != -1 and ei != -1 and si < ei, "splice anchors missing in %s" % path
    # sanity: the span must contain the old t5_truth Zharovia formula
    span = src[si:ei]
    for marker in ("t5_truth", "t5_plant_claim", "t5_is_false_plant"):
        assert marker in span, "%s missing in span (%s)" % (marker, path)
    new = src[:si] + BLOCK + "\n" + src[ei:]
    assert new.count("fn t5_truth(") == 1 and new.count("fn t5_plant_claim(") == 1
    with open(path, "w", encoding="utf-8") as f:
        f.write(new)
    return len(span)

def main():
    legs = sys.argv[1:] or [
        os.path.join(WORK, "tnn", leg, "src", "t5_core.zag")
        for leg in ("legA", "legB", "legC")]
    for p in legs:
        n = patch(p)
        print("patched %s (replaced %d chars)" % (p, n))

if __name__ == "__main__":
    main()
