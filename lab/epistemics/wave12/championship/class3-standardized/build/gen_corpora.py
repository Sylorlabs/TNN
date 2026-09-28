#!/usr/bin/env python3
"""Build src/corpus_<src>.zag from each frozen corpus.json (class3-standardized).

Same numeric-leg format as q2-distillation-step37/build/build_corpus_zag.py:
q2_dump_at/q2_obs_at/q2_dis_at/q2_prb_at as integer if/else chains.
Verifies sha256 against each corpus/SHA256.txt. Reruns byte-identical.
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
WAVE12 = "/home/hatch/workspace/tnn-lab/wave12"

SOURCES = {
    "grok": "g-grok-distillation",
    "sol": "q2-distillation-sol",
    "step": "q2-distillation-step37",
    "swe": "q2-distillation-swe",
}

def accessor(name, vals):
    L = [f"fn {name}(id:i32)i32 {{"]
    for i, v in enumerate(vals):
        L.append(f"    if(id=={i}){{return {v};}}")
    L.append("    return 0;")
    L.append("}")
    return "\n".join(L)

for src, dirname in SOURCES.items():
    cdir = os.path.join(WAVE12, dirname, "corpus")
    cj = os.path.join(cdir, "corpus.json")
    sh = os.path.join(cdir, "SHA256.txt")
    with open(cj, "rb") as f:
        raw = f.read()
    corpus = json.loads(raw)
    expect = open(sh).read().strip().split()[0]
    got = hashlib.sha256(raw).hexdigest()
    if got != expect:
        sys.exit(f"FATAL: {src} corpus.json sha256 {got} != {expect}")
    n_dump = len(corpus["dump"])
    n_teach = len(corpus["teach"])
    assert n_dump == 240 and n_teach == 240, f"{src}: corpus must have 240+240 rows"
    for k, v in corpus["error_inventory"].items():
        assert v["n"] == 0, f"{src}: error inventory {k} = {v['n']} != 0"
    DUMP = [e["value"] for e in corpus["dump"]]
    OBS = [e["obs_value"] for e in corpus["teach"]]
    DIS = [e["distract_value"] for e in corpus["teach"]]
    PRB = [e["probe_value"] for e in corpus["teach"]]
    out = []
    out.append(f"// corpus_{src}.zag — GENERATED. Do not edit. Source: {corpus['meta'].get('model')}.")
    out.append(f"// Built from {dirname}/corpus/corpus.json (sha256 {got}) by class3-standardized/build/gen_corpora.py.")
    out.append("// Values are integer literals in if/else chains: deterministic, no heap,")
    out.append("// no globals, no casts. Reruns of the generator are byte-identical.")
    out.append('@import("t5_core.zag")')
    out.append(f"const Q2_CORPUS_SHA256_{src.upper()}:[]u8=\"{got}\";")
    out.append(accessor("q2_dump_at", DUMP))
    out.append(accessor("q2_obs_at", OBS))
    out.append(accessor("q2_dis_at", DIS))
    out.append(accessor("q2_prb_at", PRB))
    opath = os.path.join(ROOT, "src", f"corpus_{src}.zag")
    with open(opath, "w") as f:
        f.write("\n".join(out) + "\n")
    print(f"wrote {opath} ({os.path.getsize(opath)} bytes) sha256={got[:16]}")
