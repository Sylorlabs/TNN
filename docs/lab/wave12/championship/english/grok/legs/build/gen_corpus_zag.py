#!/usr/bin/env python3
"""Build legs/{legA,legB,legC}/src/corpus.zag from the FROZEN grok-4.6 corpus.

Mechanical port of tnn/build_gen.py (muse):
- verifies grok/corpus/corpus.json against grok/corpus/SHA256SUMS.txt
  (FATAL on mismatch)
- re-verifies row shapes (240 dump + 240 teach)
- asserts meta.model == "grok-4.6"
- emits grok_dump_at/grok_obs_at/grok_dis_at/grok_prb_at as inline
  if/else chains (integer literals — no globals, no heap casts,
  deterministic). Reruns must be byte-identical.
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))   # grok/legs/build
GROK = os.path.dirname(os.path.dirname(HERE))        # grok/
CJ = os.path.join(GROK, "corpus", "corpus.json")
SH = os.path.join(GROK, "corpus", "SHA256SUMS.txt")

with open(CJ, "rb") as f:
    raw = f.read()
corpus = json.loads(raw)
got = hashlib.sha256(raw).hexdigest()
expect = None
for line in open(SH):
    parts = line.strip().split()
    if len(parts) == 2 and parts[1] in ("corpus.json", "./corpus.json"):
        expect = parts[0]
assert expect, "no corpus.json line in SHA256SUMS.txt"
if got != expect:
    sys.exit(f"FATAL: corpus.json sha256 {got} != {expect}")
print(f"corpus.json verified sha256={got}", flush=True)

n_dump = len(corpus["dump"])
n_teach = len(corpus["teach"])
assert n_dump == 240 and n_teach == 240, "corpus must have 240+240 rows"
WITHHELD_TEACH = []
for e in corpus["dump"]:
    ks = set(e.keys())
    assert ks == {"id", "value", "sentence"} or \
        ks == {"id", "withheld", "withheld_reason"}, f"bad dump row keys: {ks}"
for e in corpus["teach"]:
    ks = set(e.keys())
    if ks == {"id", "obs_value", "observation", "distract_value",
              "distractor", "probe", "probe_value"}:
        pass
    elif ks == {"id", "withheld", "withheld_reason"}:
        assert e["withheld"] is True, "withheld must be true"
        WITHHELD_TEACH.append(e["id"])
    else:
        raise AssertionError(f"bad teach row keys: {ks}")
assert WITHHELD_TEACH == sorted(WITHHELD_TEACH), "withheld ids not ascending"
meta = corpus["meta"]
assert meta["model"] == "grok-4.6", f"wrong corpus: model={meta['model']!r}"
# withhold ruling (parent-authorized 2026-09-21): cross-check the corpus
# records the withheld set identically.
corpus_wh = set(corpus.get("withheld_ids", []))
assert set(WITHHELD_TEACH) == corpus_wh, \
    f"teach withheld {sorted(WITHHELD_TEACH)} != corpus withheld_ids {sorted(corpus_wh)}"

def lane(e, key):
    # withheld rows carry no lanes; their dead lanes are never read (drivers
    # skip withheld ids before touching the accessors). Emit 0 as a dummy.
    return e[key] if not e.get("withheld") else 0

DUMP = [e["value"] for e in corpus["dump"]]
OBS = [lane(e, "obs_value") for e in corpus["teach"]]
DIS = [lane(e, "distract_value") for e in corpus["teach"]]
PRB = [lane(e, "probe_value") for e in corpus["teach"]]
for name, vals in (("dump", DUMP), ("obs", OBS), ("dis", DIS), ("prb", PRB)):
    assert all(isinstance(v, int) for v in vals), f"{name} has non-int values"

def accessor(name, vals):
    L = [f"fn {name}(id:i32)i32 {{"]
    for i, v in enumerate(vals):
        L.append(f"    if(id=={i}){{return {v};}}")
    L.append("    return 0;")
    L.append("}")
    return "\n".join(L)

L = []
L.append("// corpus.zag — GENERATED. Do not edit.")
L.append("// Built from grok/corpus/corpus.json (sha256 below) by legs/build/gen_corpus_zag.py.")
L.append("// Mechanical port of tnn/build_gen.py (muse) to the grok-4.6 English box.")
L.append("// Values are integer literals in if/else chains: deterministic, no heap,")
L.append("// no globals, no casts. Reruns of the generator are byte-identical.")
L.append('@import("t5_core.zag")')
L.append("const GROK_DUMP_N:i32=240;")
L.append(f'const GROK_CORPUS_SHA256:[]u8="{expect}";')
L.append("")
L.append(accessor("grok_dump_at", DUMP))
L.append("")
L.append(accessor("grok_obs_at", OBS))
L.append("")
L.append(accessor("grok_dis_at", DIS))
L.append("")
L.append(accessor("grok_prb_at", PRB))
L.append("")
L.append("// grok_withheld_at(id): 1 iff the teach row is a corpus-level")
L.append("// WITHHELD row (withhold ruling 2026-09-21: unparseable after the")
L.append("// mechanical retry budget; never salvage-parsed, never repaired).")
L.append("// Drivers skip withheld ids before touching the lanes above, so the")
L.append("// dead lanes above (0 for withheld ids) are never read.")
L.append("// GROK_WITHHELD_N counts them.")
L.append("fn grok_withheld_at(id:i32)i32 {")
for i in WITHHELD_TEACH:
    L.append(f"    if(id=={i}){{return 1;}}")
L.append("    return 0;")
L.append("}")
L.append("")
L.append(f"const GROK_WITHHELD_N:i32={len(WITHHELD_TEACH)};")
L.append("")

text = "\n".join(L)
for leg in ("legA", "legB", "legC"):
    out = os.path.join(HERE, "..", leg, "src", "corpus.zag")
    with open(out, "w") as f:
        f.write(text)
    print(f"wrote {out} ({os.path.getsize(out)} bytes)")
