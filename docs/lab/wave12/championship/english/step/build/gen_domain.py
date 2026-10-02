#!/usr/bin/env python3
"""Generate the English domain section for t5_core.zag (step team).

Reads frozen championship-english/corpus-input/facts.json:
- t5_cat: boundaries 48/96/144 (alpha-pos/word-len/pub-year/count-fact)
- t5_truth(id): real-world TRUE value
    - alpha-pos: ord(letter)-ord('A')+1 (mechanical from claim_text)
    - word-len: len(word) (mechanical from claim_text)
    - pub-year / count-fact: supplied value, except the 12 false plants
      (corrections from ground_truth_notes.md, asserted below)
- t5_plant_claim(id): trainer-SUPPLIED value (228 true + 12 false)
- t5_is_false_plant: unchanged (same 12 ids as Q2)

Splices the section into legs/tnn/{legA,legB,legC}/src/t5_core.zag,
replacing the Zharovia domain block. Reruns are byte-identical.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))          # step/build
STEP = os.path.dirname(HERE)                                # step
CORPUS_IN = "/home/hatch/workspace/tnn-lab/wave12/championship-english/corpus-input"
LEGS = os.path.join(STEP, "legs", "tnn")

_fj = json.load(open(os.path.join(CORPUS_IN, "facts.json")))
FALSE_IDS = sorted(_fj["false_ids"])
assert FALSE_IDS == [3, 29, 55, 71, 80, 103, 117, 139, 163, 178, 205, 231]

# true-value corrections for the 12 false plants (ground_truth_notes.md);
# every other id: true == supplied (asserted mechanically below).
CORRECTIONS = {3: 4, 29: 4, 55: 8, 71: 20, 80: 9, 103: 1678,
               117: 1850, 139: 1895, 163: 3, 178: 9, 205: 37, 231: 8}

SUP, TRUE, CAT = {}, {}, {}
for k, v in _fj.items():
    if k in ("false_ids", "meta"):
        continue
    i = int(k)
    SUP[i] = v["value"]
    CAT[i] = v["category"]
    claim = v["claim_text"]
    if v["category"] == "alpha-pos":
        t = ord(claim) - 64
    elif v["category"] == "word-len":
        t = len(claim)
    else:
        t = CORRECTIONS.get(i, v["value"])
    TRUE[i] = t
    if v["false"]:
        assert t != v["value"] and t == CORRECTIONS[i], f"false id {i}"
    else:
        assert t == v["value"], f"non-false id {i}: true {t} != supplied {v['value']}"

def chain(name, vals):
    L = [f"fn {name}(id:i32)i32 {{"]
    for i in range(240):
        L.append(f"    if(id=={i}){{return {vals[i]};}}")
    L.append("    return 0;")
    L.append("}")
    return "\n".join(L)

SEC = []
SEC.append("// ---- English domain: world truth (harness-side; arms never see it) ----")
SEC.append("// 4 categories: 0=alpha-pos (ids 0-47), 1=word-len (48-95),")
SEC.append("// 2=pub-year (96-143), 3=count-fact (144-239).")
SEC.append("// t5_truth(id) = real-world TRUE value; t5_plant_claim(id) =")
SEC.append("// trainer-SUPPLIED value (228 true + 12 deliberately false plants,")
SEC.append("// same ids as Q2). Generated from frozen facts.json by")
SEC.append("// step/build/gen_domain.py (reruns byte-identical).")
SEC.append("fn t5_cat(id:i32)i32 {")
SEC.append("    if(id<48){return 0;}")
SEC.append("    if(id<96){return 1;}")
SEC.append("    if(id<144){return 2;}")
SEC.append("    return 3;")
SEC.append("}")
SEC.append("// 12 deliberately false plants (prereg-fixed; same ids as Q2)")
SEC.append("fn t5_is_false_plant(id:i32)i32 {")
for fid in FALSE_IDS:
    SEC.append(f"    if(id=={fid}){{return 1;}}")
SEC.append("    return 0;")
SEC.append("}")
SEC.append(chain("t5_truth", TRUE))
SEC.append(chain("t5_plant_claim", SUP))
SEC.append("")
SECTION = "\n".join(SEC)

START = "// ---- Zharovia domain"
END = "// ---- store init ----"
for leg in ("legA", "legB", "legC"):
    p = os.path.join(LEGS, leg, "src", "t5_core.zag")
    with open(p) as f:
        text = f.read()
    si = text.index(START)
    ei = text.index(END)
    # the Q1-delta comment block in legB/legC sits between domain and store
    # init; keep everything from END onward intact.
    new = text[:si] + SECTION + text[ei:]
    assert "t5_mod" not in new and "t5_base" not in new and "t5_idx" not in new, leg
    with open(p, "w") as f:
        f.write(new)
    print(f"spliced English domain into {leg}/src/t5_core.zag")
print("domain splice OK")
