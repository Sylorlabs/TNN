#!/usr/bin/env python3
"""Build curated legs' muse_corpus.zag from the FROZEN curated English corpus.

Mechanical port of sol/build_gen.py (curated box):
- verifies curated_corpus.json against CURATED_SHA256.txt (FATAL on mismatch)
- re-verifies row shapes (240 dump + 240 teach)
- asserts meta.model == "curated-english" (wrong-corpus guard)
- asserts withheld rows carry dead lanes + withheld_ids match
- emits muse_dump_at/muse_obs_at/muse_dis_at/muse_prb_at/muse_withheld_at as
  inline if/else chains (integer literals — no globals, no heap casts,
  deterministic). Reruns must be byte-identical.
Usage: python3 build_gen.py  (writes shared + all three leg src dirs)
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CJ = os.path.join(HERE, "..", "curated_corpus.json")
SH = os.path.join(HERE, "..", "CURATED_SHA256.txt")

with open(CJ, "rb") as f:
    raw = f.read()
corpus = json.loads(raw)
expect = open(SH).read().strip()
got = hashlib.sha256(raw).hexdigest()
if got != expect:
    sys.exit(f"FATAL: curated_corpus.json sha256 {got} != {expect}")
print(f"curated_corpus.json verified sha256={got}", flush=True)

n_dump = len(corpus["dump"])
n_teach = len(corpus["teach"])
assert n_dump == 240 and n_teach == 240, "corpus must have 240+240 rows"
WITHHELD = sorted(corpus.get("withheld_ids", []))
for e in corpus["dump"]:
    assert set(e.keys()) == {"id", "value", "sentence", "curated",
                             "withhold_reason"}
for e in corpus["teach"]:
    base = {"id", "obs_value", "observation",
            "distract_value", "distractor",
            "probe", "probe_value",
            "curated", "withhold_reason", "text_source",
            "distractor_selection", "distractor_votes"}
    assert set(e.keys()) == base, f"bad teach row keys: {set(e.keys())}"
    if not e["curated"]:
        assert e["id"] in WITHHELD, f"withheld row {e['id']} not in withheld_ids"
        assert e["obs_value"] == 0 and e["distract_value"] == 0 \
            and e["probe_value"] == 0, "withheld row must carry dead lanes"
        assert e["withhold_reason"], "withheld row needs a reason"
    else:
        assert e["id"] not in WITHHELD
        assert e["withhold_reason"] is None
for e in corpus["dump"]:
    if not e["curated"]:
        assert e["id"] in WITHHELD and e["value"] == 0
assert sorted(e["id"] for e in corpus["teach"] if not e["curated"]) == WITHHELD
meta = corpus["meta"]
assert meta["model"] == "curated-english", \
    f"wrong corpus: model={meta['model']}, expected curated-english"

DUMP = [e["value"] for e in corpus["dump"]]
OBS = [e["obs_value"] for e in corpus["teach"]]
DIS = [e["distract_value"] for e in corpus["teach"]]
PRB = [e["probe_value"] for e in corpus["teach"]]
WH = [0 if e["curated"] else 1 for e in corpus["teach"]]


def accessor(name, vals):
    L = [f"fn {name}(id:i32)i32 {{"]
    for i, v in enumerate(vals):
        L.append(f"    if(id=={i}){{return {v};}}")
    L.append("    return 0;")
    L.append("}")
    return "\n".join(L)


L = []
L.append("// muse_corpus.zag — GENERATED. Do not edit.")
L.append("// Built from the FROZEN curated English corpus (pure-Muse native")
L.append("// curation crew, 232 adopted / 8 withheld) by tnn/build_gen.py")
L.append("// (mechanical port of sol/build_gen.py).")
L.append(f"// curated_corpus.json sha256: {expect}")
L.append(f"// model: {meta['model']}, generated: {meta['generated_utc']}")
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
L.append("// WITHHELD fact (curation crew: fact disagreement across the 5")
L.append("// sources — agree-before-add). Withheld ids carry dead numeric")
L.append("// lanes (0); drivers skip them via the withheld counter path")
L.append("// (muse_t_teach_one / q2_teach withheld machinery) and never read")
L.append("// the lanes.")
L.append(accessor("muse_withheld_at", WH))
L.append("")
L.append(f"const MUSE_WITHHELD_N:i32={len(WITHHELD)};")
L.append("")

body = "\n".join(L)
dests = [os.path.join(HERE, "shared", "muse_corpus.zag")]
for leg in ("legA", "legB", "legC"):
    dests.append(os.path.join(HERE, leg, "src", "muse_corpus.zag"))
for out in dests:
    with open(out, "w") as f:
        f.write(body)
    print(f"wrote {out} ({os.path.getsize(out)} bytes)", flush=True)
print(f"MUSE_WITHHELD_N={len(WITHHELD)} withheld_ids={WITHHELD}", flush=True)
