#!/usr/bin/env python3
"""Build generated Zag sources for the hy3 ENGLISH championship box.

1. hy3_corpus.zag — corpus accessors from the frozen corpus.json
   (verified against corpus/SHA256.txt; FATAL on mismatch). Mechanical port
   of ~/workspace/championship/muse_team/tnn/build_gen.py:
   hy3_dump_at / hy3_obs_at / hy3_dis_at / hy3_prb_at as inline if/else
   chains (integer literals — no globals, no heap casts, deterministic).
   Reruns are byte-identical.

2. English domain block — t5_cat / t5_truth / t5_plant_claim /
   t5_is_false_plant replacing the Zharovia domain section of t5_core.zag:
     t5_cat(id):          0=alpha-pos (0-47), 1=word-len (48-95),
                          2=pub-year (96-143), 3=count-fact (144-239)
     t5_truth(id):        real-world TRUE value (facts.json supplied value
                          for the 228 non-false ids; TRUE_TABLE for the 12
                          false ids, parsed from the frozen
                          ground_truth_notes.md and mechanically verified)
     t5_plant_claim(id):  trainer's SUPPLIED value (facts.json "value";
                          authoritative for the model)
     t5_is_false_plant:   unchanged (same 12 ids as Q2)

Usage: python3 build_gen.py   (writes into tnn/leg{ A,B,C}/src + tnn/shared)
"""
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))          # hy3/tnn
HY3 = os.path.dirname(HERE)                                 # hy3/
CORPUS_JSON = os.path.join(HY3, "corpus", "corpus.json")
CORPUS_SHA = os.path.join(HY3, "corpus", "SHA256.txt")
INPUT = os.path.abspath(os.path.join(HY3, "..", "corpus-input"))
FACTS_JSON = os.path.join(INPUT, "facts.json")
GT_NOTES = os.path.join(INPUT, "ground_truth_notes.md")
MUSE_SRC = "/home/hatch/workspace/tnn-lab/wave12/championship/muse-native/trial/tnn"

CAT_NAMES = ["alpha-pos", "word-len", "pub-year", "count-fact"]

# ---------------------------------------------------------------- facts

def load_facts():
    d = json.load(open(FACTS_JSON))
    supplied, cats, claims, false = {}, {}, {}, {}
    for k, v in d.items():
        if k in ("false_ids", "meta"):
            continue
        i = int(k)
        supplied[i] = int(v["value"])
        cats[i] = v["category"]
        claims[i] = v["claim_text"]
        false[i] = bool(v["false"])
    assert len(supplied) == 240, f"facts.json: {len(supplied)} facts"
    false_ids = sorted(int(x) for x in d["false_ids"])
    assert false_ids == [3, 29, 55, 71, 80, 103, 117, 139, 163, 178, 205, 231], \
        f"unexpected false_ids {false_ids}"
    for i in false_ids:
        assert false[i], f"false id {i} not flagged"
    # category boundaries
    for i in range(240):
        want = 0 if i < 48 else (1 if i < 96 else (2 if i < 144 else 3))
        assert cats[i] == CAT_NAMES[want], f"id {i}: {cats[i]}"
    return supplied, cats, claims, false, false_ids


def parse_true_table(supplied, cats, claims, false):
    """TRUE values parsed from the frozen ground_truth_notes.md (3 line
    formats), mechanically verified against derivations where available."""
    notes = open(GT_NOTES).read()
    true = {}
    for m in re.finditer(
            r'^- id (\d+): letter ([A-Z]) -> position (\d+) '
            r'\(supplied (\d+)( FALSE)?\)', notes, re.M):
        true[int(m.group(1))] = int(m.group(3))
    for m in re.finditer(
            r'^- id (\d+): "(.*?)" has (\d+) letters '
            r'\(supplied (\d+)( FALSE)?\)', notes, re.M):
        i = int(m.group(1))
        assert i not in true, f"dup parse {i}"
        true[i] = int(m.group(3))
    for m in re.finditer(
            r'^- id (\d+): .*? -- (\d+) \(FALSE: true (\d+)\) --', notes, re.M):
        i = int(m.group(1))
        assert i not in true, f"dup parse {i}"
        assert int(m.group(2)) == supplied[i], f"id {i}: supplied drift"
        true[i] = int(m.group(3))
    for m in re.finditer(r'^- id (\d+): .*? -- (\d+) --', notes, re.M):
        i = int(m.group(1))
        if i not in true:
            true[i] = int(m.group(2))
    missing = [i for i in range(240) if i not in true]
    assert not missing, f"true table missing ids {missing}"
    # mechanical verification: alpha-pos / word-len derivations
    for i in range(240):
        mech = None
        if cats[i] == "alpha-pos":
            mech = ord(claims[i].upper()) - ord("A") + 1
        elif cats[i] == "word-len":
            mech = len(claims[i])
        if mech is not None:
            assert mech == true[i], \
                f"id {i}: derived {mech} != notes-true {true[i]}"
            if not false[i]:
                assert mech == supplied[i], \
                    f"id {i}: derived {mech} != supplied {supplied[i]}"
    # non-false: true == supplied (builder's mechanical assertion)
    for i in range(240):
        if not false[i]:
            assert true[i] == supplied[i], \
                f"id {i}: non-false true {true[i]} != supplied {supplied[i]}"
    # false: true != supplied, and the 12-set matches
    fset = {i for i in range(240) if false[i]}
    assert fset == {3, 29, 55, 71, 80, 103, 117, 139, 163, 178, 205, 231}
    for i in fset:
        assert true[i] != supplied[i], f"false id {i}: true==supplied"
    print(f"TRUE table verified: 240 ids, 12 false overrides "
          f"{sorted((i, true[i]) for i in fset)}", flush=True)
    return true

# ---------------------------------------------------------------- corpus.zag

def build_corpus_zag(corpus, sha):
    n_dump = len(corpus["dump"])
    n_teach = len(corpus["teach"])
    assert n_dump == 240 and n_teach == 240, "corpus must have 240+240 rows"
    for e in corpus["dump"]:
        assert set(e.keys()) == {"id", "value", "sentence"}
    for e in corpus["teach"]:
        assert set(e.keys()) == {"id", "obs_value", "observation",
                                 "distract_value", "distractor",
                                 "probe", "probe_value"}
    meta = corpus["meta"]
    assert meta["model"] == "hy3:free", "wrong corpus: not the hy3 freeze"

    DUMP = [e["value"] for e in corpus["dump"]]
    OBS = [e["obs_value"] for e in corpus["teach"]]
    DIS = [e["distract_value"] for e in corpus["teach"]]
    PRB = [e["probe_value"] for e in corpus["teach"]]

    def accessor(name, vals):
        L = [f"fn {name}(id:i32)i32 {{"]
        for i, v in enumerate(vals):
            L.append(f"    if(id=={i}){{return {v};}}")
        L.append("    return 0;")
        L.append("}")
        return "\n".join(L)

    L = []
    L.append("// hy3_corpus.zag — GENERATED. Do not edit.")
    L.append("// Built from hy3/corpus/corpus.json (sha256 below) by tnn/build_gen.py.")
    L.append("// Mechanical port of the muse_team tnn/build_gen.py.")
    L.append("// Values are integer literals in if/else chains: deterministic, no heap,")
    L.append("// no globals, no casts. Reruns of the generator are byte-identical.")
    L.append('@import("t5_core.zag")')
    L.append("const HY3_DUMP_N:i32=240;")
    L.append(f'const HY3_CORPUS_SHA256:[]u8="{sha}";')
    L.append("")
    L.append(accessor("hy3_dump_at", DUMP))
    L.append("")
    L.append(accessor("hy3_obs_at", OBS))
    L.append("")
    L.append(accessor("hy3_dis_at", DIS))
    L.append("")
    L.append(accessor("hy3_prb_at", PRB))
    L.append("")
    return "\n".join(L)

# ---------------------------------------------------------------- domain block

def domain_block(true, supplied, false_ids):
    def chain(name, vals):
        L = [f"fn {name}(id:i32)i32 {{"]
        for i in range(240):
            L.append(f"    if(id=={i}){{return {vals[i]};}}")
        L.append("    return 0;")
        L.append("}")
        return "\n".join(L)

    L = []
    L.append("// ---- ENGLISH domain: world truth (harness-side; arms never see the formula) ----")
    L.append("// Categories: 0=alpha-pos (ids 0-47), 1=word-len (48-95),")
    L.append("// 2=pub-year (96-143), 3=count-fact (144-239).")
    L.append("// t5_truth = real-world TRUE value (facts.json supplied value for the")
    L.append("// 228 non-false ids; the 12 false-id TRUE values parsed from the frozen")
    L.append("// ground_truth_notes.md and mechanically verified).")
    L.append("// t5_plant_claim = trainer's SUPPLIED value (facts.json \"value\"),")
    L.append("// authoritative for the model: 228 real-world-true + 12 deliberately false.")
    L.append("// GENERATED by tnn/build_gen.py — do not hand-edit.")
    L.append("fn t5_cat(id:i32)i32 {")
    L.append("    if(id<48){return 0;}")
    L.append("    if(id<96){return 1;}")
    L.append("    if(id<144){return 2;}")
    L.append("    return 3;")
    L.append("}")
    L.append(chain("t5_truth", true))
    L.append("// 12 deliberately false plants (prereg-fixed; same ids as Q2)")
    Fl = ["fn t5_is_false_plant(id:i32)i32 {"]
    for i in false_ids:
        Fl.append(f"    if(id=={i}){{return 1;}}")
    Fl.append("    return 0;")
    Fl.append("}")
    L.append("\n".join(Fl))
    L.append(chain("t5_plant_claim", supplied))
    return "\n".join(L) + "\n"


def splice_t5_core(block):
    """Copy t5_core.zag from the muse-native legB src (it carries the
    documented Q1 delta t5_claim_of, which legA's copy lacks), replacing the
    Zharovia domain section with the English domain block."""
    src = open(os.path.join(MUSE_SRC, "legB", "src", "t5_core.zag")).read()
    start_mark = "// ---- Zharovia domain:"
    end_mark = "// ---- store init ----"
    si = src.index(start_mark)
    ei = src.index(end_mark)
    # back up to the start of the comment line
    si = src.rindex("\n", 0, si) + 1
    new = src[:si] + block + "\n" + src[ei:]
    assert "t5_mod" not in new and "t5_base" not in new and "t5_idx" not in new, \
        "Zharovia helpers leaked through"
    assert "Zharovia" not in new
    return new

# ---------------------------------------------------------------- main

def main():
    with open(CORPUS_JSON, "rb") as f:
        raw = f.read()
    corpus = json.loads(raw)
    expect = open(CORPUS_SHA).read().strip()
    got = hashlib.sha256(raw).hexdigest()
    if got != expect:
        sys.exit(f"FATAL: corpus.json sha256 {got} != {expect}")
    print(f"corpus.json verified sha256={got}", flush=True)

    supplied, cats, claims, false, false_ids = load_facts()
    true = parse_true_table(supplied, cats, claims, false)

    czag = build_corpus_zag(corpus, expect)
    for leg in ("legA", "legB", "legC"):
        out = os.path.join(HERE, leg, "src", "hy3_corpus.zag")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w") as f:
            f.write(czag)
        print(f"wrote {out} ({os.path.getsize(out)} bytes)", flush=True)

    core = splice_t5_core(domain_block(true, supplied, false_ids))
    for leg in ("legA", "legB", "legC"):
        out = os.path.join(HERE, leg, "src", "t5_core.zag")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w") as f:
            f.write(core)
        print(f"wrote {out} ({os.path.getsize(out)} bytes)", flush=True)

    # stash the verified tables for the analysis scripts
    tables = {"true": {str(i): true[i] for i in range(240)},
              "supplied": {str(i): supplied[i] for i in range(240)},
              "false_ids": false_ids}
    tp = os.path.join(HERE, "gen", "english_tables.json")
    os.makedirs(os.path.dirname(tp), exist_ok=True)
    with open(tp, "w") as f:
        json.dump(tables, f, indent=1)
        f.write("\n")
    print(f"wrote {tp}", flush=True)


if __name__ == "__main__":
    main()
