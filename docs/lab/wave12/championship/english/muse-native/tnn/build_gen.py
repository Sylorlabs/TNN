#!/usr/bin/env python3
"""Build tnn/shared/muse_corpus.zag from the FROZEN muse_team corpus.

Mechanical port of q2-distillation/build/build_corpus_zag.py:
- verifies corpus/corpus.json against corpus/SHA256.txt (FATAL on mismatch)
- re-verifies row shapes (240 dump + 240 teach)
- emits muse_dump_at/muse_obs_at/muse_dis_at/muse_prb_at as inline
  if/else chains (integer literals — no globals, no heap casts,
  deterministic). Reruns must be byte-identical.
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))  # tnn
CJ = os.path.join(HERE, "..", "corpus", "corpus.json")
SH = os.path.join(HERE, "..", "corpus", "SHA256.txt")
# output path from argv[1]; default tnn/shared/muse_corpus.zag
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "shared", "muse_corpus.zag")
os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)

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
for e in corpus["dump"]:
    assert set(e.keys()) == {"id", "value", "sentence"}
for e in corpus["teach"]:
    assert set(e.keys()) == {"id", "obs_value", "observation",
                             "distract_value", "distractor",
                             "probe", "probe_value"}
meta = corpus["meta"]
assert meta["model"] == "muse-native-english", "wrong corpus: not the muse-native-english freeze"

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
L.append("// muse_corpus.zag — GENERATED. Do not edit.")
L.append("// Built from muse_team/corpus/corpus.json (sha256 below) by tnn/build_gen.py.")
L.append("// Mechanical port of q2_distillation/build/build_corpus_zag.py.")
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

with open(OUT, "w") as f:
    f.write("\n".join(L))
print(f"wrote {OUT} ({os.path.getsize(OUT)} bytes)")
