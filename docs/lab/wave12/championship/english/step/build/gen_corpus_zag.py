#!/usr/bin/env python3
"""Build legs/tnn/<leg>/src/step_corpus.zag from the FROZEN step English corpus.

Mechanical port of the muse_team tnn/build_gen.py:
- verifies step/corpus/corpus.json against step/corpus/SHA256.txt (FATAL on mismatch)
- re-verifies row shapes (240 dump + 240 teach)
- asserts meta.model == "step-3.7-flash:free"
- emits step_dump_at/step_obs_at/step_dis_at/step_prb_at as inline
  if/else chains (integer literals — no globals, no heap casts,
  deterministic). Reruns must be byte-identical.
Usage: python3 gen_corpus_zag.py   (writes all three legs' src/step_corpus.zag)
"""
import hashlib
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))  # step/build
STEP = os.path.dirname(HERE)                        # step
CJ = os.path.join(STEP, "corpus", "corpus.json")
SH = os.path.join(STEP, "corpus", "SHA256.txt")

with open(CJ, "rb") as f:
    raw = f.read()
corpus = json.loads(raw)
expect = open(SH).read().strip()
got = hashlib.sha256(raw).hexdigest()
if got != expect:
    raise SystemExit(f"FATAL: corpus.json sha256 {got} != {expect}")
print(f"corpus.json verified sha256={got}", flush=True)

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
assert meta["model"] == "step-3.7-flash:free", "wrong corpus: not the step freeze"

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
L.append("// step_corpus.zag — GENERATED. Do not edit.")
L.append("// Built from step/corpus/corpus.json (sha256 below) by build/gen_corpus_zag.py.")
L.append("// Mechanical port of the muse_team tnn/build_gen.py.")
L.append("// Values are integer literals in if/else chains: deterministic, no heap,")
L.append("// no globals, no casts. Reruns of the generator are byte-identical.")
L.append('@import("t5_core.zag")')
L.append("const STEP_DUMP_N:i32=240;")
L.append(f'const STEP_CORPUS_SHA256:[]u8="{expect}";')
L.append("")
L.append(accessor("step_dump_at", DUMP))
L.append("")
L.append(accessor("step_obs_at", OBS))
L.append("")
L.append(accessor("step_dis_at", DIS))
L.append("")
L.append(accessor("step_prb_at", PRB))
L.append("")

body = "\n".join(L)
for leg in ("legA", "legB", "legC"):
    out = os.path.join(STEP, "legs", "tnn", leg, "src", "step_corpus.zag")
    with open(out, "w") as f:
        f.write(body)
    print(f"wrote {out} ({os.path.getsize(out)} bytes)")
