#!/usr/bin/env python3
"""Build sol legs' muse_corpus.zag from the FROZEN sol English corpus.

Mechanical port of tnn/build_gen.py (muse team):
- verifies sol/corpus/corpus.json against sol/corpus/SHA256.txt (FATAL on mismatch)
- re-verifies row shapes (240 dump + 240 teach)
- asserts meta.model == "gpt-5.6-sol" (wrong-corpus guard)
- emits muse_dump_at/muse_obs_at/muse_dis_at/muse_prb_at as inline
  if/else chains (integer literals — no globals, no heap casts,
  deterministic). Reruns must be byte-identical.

Accessor/file names are kept identical to the muse-native legs on purpose:
the sol legs are a mechanical port and the drivers reference these lanes.
Provenance (model + corpus sha) is stamped in the file header.
Usage: python3 build_gen.py  (writes all three leg src dirs)
"""
import hashlib
import json
import os
import sys

SOL = os.path.dirname(os.path.abspath(__file__))
CJ = os.path.join(SOL, "corpus", "corpus.json")
SH = os.path.join(SOL, "corpus", "SHA256.txt")

with open(CJ, "rb") as f:
    raw = f.read()
corpus = json.loads(raw)
expect = open(SH).read().strip()
got = hashlib.sha256(raw).hexdigest()
if got != expect:
    sys.exit(f"FATAL: corpus.json sha256 {got} != {expect}")
print(f"corpus.json verified sha256={got}", flush=True)

n_dump = len(corpus["dump"])
n_teach = len(corpus["teach"])
assert n_dump == 240 and n_teach == 240, "corpus must have 240+240 rows"
WITHHELD = sorted(corpus.get("withheld_ids", []))
for e in corpus["dump"]:
    assert set(e.keys()) == {"id", "value", "sentence"}
for e in corpus["teach"]:
    base = {"id", "obs_value", "observation",
            "distract_value", "distractor",
            "probe", "probe_value"}
    keys = set(e.keys())
    assert keys == base or keys == base | {"withheld", "withheld_reason"}, \
        f"bad teach row keys: {keys}"
    if e.get("withheld"):
        assert e["id"] in WITHHELD
assert sorted(e["id"] for e in corpus["teach"] if e.get("withheld")) == WITHHELD
meta = corpus["meta"]
assert meta["model"] == "gpt-5.6-sol", \
    f"wrong corpus: model={meta['model']}, expected gpt-5.6-sol"

DUMP = [e["value"] for e in corpus["dump"]]
OBS = [e["obs_value"] for e in corpus["teach"]]
DIS = [e["distract_value"] for e in corpus["teach"]]
PRB = [e["probe_value"] for e in corpus["teach"]]
WH = [1 if e.get("withheld") else 0 for e in corpus["teach"]]

def accessor(name, vals):
    L = [f"fn {name}(id:i32)i32 {{"]
    for i, v in enumerate(vals):
        L.append(f"    if(id=={i}){{return {v};}}")
    L.append("    return 0;")
    L.append("}")
    return "\n".join(L)

L = []
L.append("// muse_corpus.zag — GENERATED. Do not edit.")
L.append("// Built from the FROZEN sol English corpus (gpt-5.6-sol) by")
L.append("// sol/build_gen.py (mechanical port of tnn/build_gen.py).")
L.append(f"// corpus.json sha256: {expect}")
L.append(f"// model: {meta['model']}, seed: {meta['seed']}, "
         f"generated: {meta['generated_utc']}")
L.append("// Lane names kept identical to the muse-native legs (mechanical")
L.append("// port fidelity); the VALUES are sol's English-box corpus.")
L.append("// Values are integer literals in if/else chains: deterministic, no heap,")
L.append("// no globals, no casts. Reruns of the generator are byte-identical.")
L.append('@import("t5_core.zag")')
L.append("const MUSE_DUMP_N:i32=240;")
L.append(f'const MUSE_CORPUS_SHA256:[]u8="{expect}";')
L.append("")
L.append(accessor("muse_dump_at", DUMP))
L.append("")
L.append(accessor("muse_obs_at", OBS))
L.append("")
L.append(accessor("muse_dis_at", DIS))
L.append("")
L.append(accessor("muse_prb_at", PRB))
L.append("")
L.append("// muse_withheld_at(id): 1 iff the teach row is a corpus-level")
L.append("// WITHHELD fact (unparseable after the retry budget — parent")
L.append("// withhold ruling 2026-09-21). Withheld ids carry dead numeric")
L.append("// lanes (0); drivers must skip them via the withheld counter path")
L.append("// (muse_t_teach_one / q2_teach withheld machinery) and never read")
L.append("// the lanes. MUSE_WITHHELD_N counts them (0 on this corpus).")
L.append(accessor("muse_withheld_at", WH))
L.append("")
L.append(f"const MUSE_WITHHELD_N:i32={len(WITHHELD)};")
L.append("")

body = "\n".join(L)
for leg in ("legA", "legB", "legC"):
    out = os.path.join(SOL, "legs", leg, "src", "muse_corpus.zag")
    with open(out, "w") as f:
        f.write(body)
    print(f"wrote {out} ({os.path.getsize(out)} bytes)", flush=True)
print(f"MUSE_WITHHELD_N={len(WITHHELD)} withheld_ids={WITHHELD}", flush=True)
