#!/usr/bin/env python3
"""One-time recovery capture for teach batch 18 (ids 216-227).

CONTEXT: the main capture run (gen_corpus_sol.py, 2026-09-21) ended FATAL
on teach batch 18: 3 consecutive mechanical parse failures (non-numeric
DISTRACT_VALUE field), exhausting the max-2-retry budget. 39/40 batches
captured cleanly. This script performs ONE fresh capture of batch 18 only,
using the identical frozen prompt, model, temperature, seed, parser, and
429/503 pacing as the main run. The failed attempt-3 raw is preserved
untouched at corpus/raw/teach_batch18.txt; this attempt is written to
corpus/raw/teach_batch18_recovery.txt.

This is NOT a retry of a "wrong" value: all three failures were mechanical
format violations (unparseable fields), never value disagreements. If this
attempt also fails mechanically, the batch is declared unrecoverable and
the FATAL stands.
"""
import hashlib
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_corpus_sol as G

TAG = "teach"
BI = 18
IDS = list(range(BI * G.BATCH, (BI + 1) * G.BATCH))
OUT = os.path.join(G.RAW_DIR, "teach_batch18_recovery.txt")

print(f"recovering {TAG} batch {BI} (ids {IDS[0]}-{IDS[-1]})", flush=True)
prompt = G.read_prompt(TAG, BI)
raw = G.api_call(prompt)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(raw)
h = hashlib.sha256(raw.encode("utf-8")).hexdigest()
res, err = G.parse_teach(raw, IDS)
if err is not None:
    print(f"RECOVERY PARSE FAIL: {err}", flush=True)
    print(f"raw preserved at {OUT} sha256={h}", flush=True)
    sys.exit(1)
print(f"RECOVERY OK sha256={h} rows={len(res)}", flush=True)
