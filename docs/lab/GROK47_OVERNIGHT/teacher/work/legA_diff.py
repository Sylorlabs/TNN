#!/usr/bin/env python3
"""LEG A: byte-compare grok-4.7 numeric legs vs frozen grok-4.6 corpora.

Compares dump/obs/dis/probe integer legs of evidence/grok47_corpus/corpus.json
against:
  A) wave12/g-grok-distillation/corpus/corpus.json (numeric-channel reference)
  B) wave12/championship-english/grok/corpus/corpus.json (English reference)
Reports per-leg diff ids and counts. Exit 0 if obs+probe are 0-diff vs BOTH.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPORT = os.path.dirname(HERE)
NEW = os.path.join(REPORT, "evidence", "grok47_corpus", "corpus.json")
W12 = "/home/hatch/workspace/tnn-lab/wave12"
REFS = {
    "g-grok-distillation": os.path.join(W12, "g-grok-distillation", "corpus", "corpus.json"),
    "english-grok": os.path.join(W12, "championship-english", "grok", "corpus", "corpus.json"),
}

def legs(cj):
    c = json.load(open(cj))
    return ({e["id"]: e["value"] for e in c["dump"]},
            {e["id"]: e["obs_value"] for e in c["teach"]},
            {e["id"]: e["distract_value"] for e in c["teach"]},
            {e["id"]: e["probe_value"] for e in c["teach"]})

nd, no, nx, np_ = legs(NEW)
fail = False
for name, path in REFS.items():
    rd, ro, rx, rp_ = legs(path)
    diffs = {}
    for legname, a, b in (("dump", nd, rd), ("obs", no, ro), ("dis", nx, rx), ("probe", np_, rp_)):
        d = [i for i in range(240) if a[i] != b[i]]
        diffs[legname] = d
        print(f"[{name}] {legname}: {len(d)}/240 diffs" + (f" ids={d}" if d else ""))
    if diffs["obs"] or diffs["probe"]:
        fail = True
        print(f"[{name}] *** OBS/PROBE DIFFERS — digest divergence expected ***")
    else:
        print(f"[{name}] obs+probe byte-identical (0/240)")
print()
if fail:
    print("LEG A RESULT: DIFFERENT numeric legs — investigate mechanism")
    sys.exit(1)
print("LEG A RESULT: numeric legs byte-identical vs frozen grok-4.6 (both corpora) → NO-DIFFERENTIATION predicted")
