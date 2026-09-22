#!/usr/bin/env python3
"""Generate one TOGETHER source corpus module from a frozen corpus.json.

Usage: gen_source_zag.py <corpus.json> <prefix> <out.zag>

Verifies the corpus.json structure matches Q2's exact protocol (240 teach
rows with the exact key set, ids covering 0..239), then emits
<prefix>_obs_at / <prefix>_prb_at / <prefix>_dis_at as inline if/else chains
(integer literals - no globals, no heap casts, deterministic) plus a
<prefix>_CORPUS_SHA256 const. Reruns are byte-identical.

Also prints the corpus's false_ids and meta for cross-corpus comparison.
"""
import hashlib
import json
import sys

CJ, PREFIX, OUT = sys.argv[1], sys.argv[2], sys.argv[3]

with open(CJ, "rb") as f:
    raw = f.read()
corpus = json.loads(raw)
sha = hashlib.sha256(raw).hexdigest()

n_teach = len(corpus["teach"])
assert n_teach == 240, f"teach rows: {n_teach} != 240"
for e in corpus["teach"]:
    assert set(e.keys()) == {"id", "obs_value", "observation",
                             "distract_value", "distractor",
                             "probe", "probe_value"}, f"teach key drift: {set(e.keys())}"
ids = sorted(e["id"] for e in corpus["teach"])
assert ids == list(range(240)), "teach ids do not cover 0..239"
by_id = {e["id"]: e for e in corpus["teach"]}
OBS = [by_id[i]["obs_value"] for i in range(240)]
PRB = [by_id[i]["probe_value"] for i in range(240)]
DIS = [by_id[i]["distract_value"] for i in range(240)]
assert all(isinstance(v, int) and v >= 0 for v in OBS + PRB + DIS), \
    "non-integer or negative leg value"


def accessor(name, vals):
    L = [f"fn {name}(id:i32)i32 {{"]
    for i, v in enumerate(vals):
        L.append(f"    if(id=={i}){{return {v};}}")
    L.append("    return -1;")
    L.append("}")
    return "\n".join(L)


L = []
L.append(f"// {PREFIX}_corpus.zag - GENERATED. Do not edit.")
L.append(f"// Built from {CJ} (sha256 below) by build/gen_source_zag.py.")
L.append("// Values are integer literals in if/else chains: deterministic, no heap,")
L.append("// no globals, no casts. Reruns of the generator are byte-identical.")
L.append('@import("t5_core.zag")')
L.append(f"const {PREFIX.upper()}_CORPUS_SHA256:[]u8=\"{sha}\";")
L.append("")
L.append(accessor(f"{PREFIX}_obs_at", OBS))
L.append("")
L.append(accessor(f"{PREFIX}_prb_at", PRB))
L.append("")
L.append(accessor(f"{PREFIX}_dis_at", DIS))
L.append("")

with open(OUT, "w") as f:
    f.write("\n".join(L))

meta = corpus.get("meta", {})
print(f"wrote {OUT}")
print(f"sha256={sha}")
print(f"model={meta.get('model')} temp={meta.get('temperature')} seed={meta.get('seed')}")
print(f"false_ids={corpus.get('false_ids')}")
print(f"retries={meta.get('retries')}")
