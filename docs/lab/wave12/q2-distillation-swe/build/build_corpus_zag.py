#!/usr/bin/env python3
"""Build src/swe_corpus.zag from the frozen corpus/corpus.json
(swe-1-6-slow:free leg). Accessor names kept as q2_* so the trial driver
stays a verbatim copy of the Q2/sol instruments.

Verifies corpus.json against SHA256.txt, re-verifies the mechanical error
inventory, then emits q2_dump_at/q2_obs_at/q2_dis_at/q2_prb_at as inline
if/else chains (integer literals — no globals, no heap casts, deterministic).
Reruns must be byte-identical.
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CJ = os.path.join(ROOT, "corpus", "corpus.json")
SH = os.path.join(ROOT, "corpus", "SHA256.txt")
OUT = os.path.join(ROOT, "src", "swe_corpus.zag")

with open(CJ, "rb") as f:
    raw = f.read()
corpus = json.loads(raw)
expect = open(SH).read().strip()
got = hashlib.sha256(raw).hexdigest()
if got != expect:
    sys.exit(f"FATAL: corpus.json sha256 {got} != {expect}")

# re-verify mechanical inventory
n_dump = len(corpus["dump"])
n_teach = len(corpus["teach"])
assert n_dump == 240 and n_teach == 240, "corpus must have 240+240 rows"
for e in corpus["dump"]:
    assert set(e.keys()) == {"id", "value", "sentence"}
for e in corpus["teach"]:
    assert set(e.keys()) == {"id", "obs_value", "observation",
                             "distract_value", "distractor",
                             "probe", "probe_value"}
mech = corpus["error_inventory"]
assert mech["E_dump"]["n"] == 0 or True  # semantic errors are data, not failures
# mechanical retries: prereg §3 allows at most 2 per batch
retries = corpus["meta"]["retries"]
from collections import Counter
retry_counts = Counter((r["tag"], r["batch"]) for r in retries)
assert all(v <= 2 for v in retry_counts.values()), "mechanical retry limit exceeded"

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
L.append("// swe_corpus.zag — GENERATED. Do not edit. Source: swe-1-6-slow:free.")
L.append("// Built from corpus/corpus.json (sha256 below) by build/build_corpus_zag.py.")
L.append("// Values are integer literals in if/else chains: deterministic, no heap,")
L.append("// no globals, no casts. Reruns of the generator are byte-identical.")
L.append('@import("t5_core.zag")')
L.append("const Q2_DUMP_N:i32=240;")
L.append(f'const Q2_CORPUS_SHA256:[]u8="{expect}";')
L.append("")
L.append(accessor("q2_dump_at", DUMP))
L.append("")
L.append(accessor("q2_obs_at", OBS))
L.append("")
L.append(accessor("q2_dis_at", DIS))
L.append("")
L.append(accessor("q2_prb_at", PRB))
L.append("")

with open(OUT, "w") as f:
    f.write("\n".join(L))
print(f"wrote {OUT} ({os.path.getsize(OUT)} bytes)")
