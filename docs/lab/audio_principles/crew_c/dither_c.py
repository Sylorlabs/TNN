#!/usr/bin/env python3
"""Crew C dither-stability spot check (prereg 5.3, control analog).

20 intent renders (P00-P06, E00-E06, R00-R05, manifest order) are re-run
with a deterministic x1.001 gain applied to the PCM samples, then re-scored
with the frozen scorer. Hit-verdict stability must be >= 19/20.
A byte-keyed lookup / brittle scorer flips under dither; a real measurement
is stable. Deterministic; no RNG.
"""
import hashlib
import json
import os
import struct
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
W = os.path.join(HERE, sys.argv[1] if len(sys.argv) > 1 else "test_wavs")
CONTROL = os.path.join(HERE, "control")
SCORER = os.path.join(HERE, "scorer_c.py")
MANIFEST = json.load(open(os.path.join(HERE, "TEST_MANIFEST_C.json")))
BATTERY = { (r["axis"], r["idx"]): r["hit"]
            for r in json.load(open(os.path.join(W, "RESULTS_C.json")))
            if r["arm"] == "intent" }

os.makedirs(W, exist_ok=True)
argv_log = open(os.path.join(W, "ARGV_LOG.jsonl"), "a")

items = ([("P", i, MANIFEST["pitch"]["targets"][i]) for i in range(7)] +
         [("E", i, MANIFEST["envelope"]["targets"][i]) for i in range(7)] +
         [("R", i, MANIFEST["rhythm"]["targets"][i]) for i in range(6)])
assert len(items) == 20

rows = []
for axis, idx, desc in items:
    tag = f"dither_{axis}{idx:02d}"
    p = os.path.join(W, f"{tag}.wav")
    argv_log.write(json.dumps({"wav": p, "argv": [CONTROL, p, desc]}) + "\n")
    r = subprocess.run([CONTROL, p, desc], capture_output=True)
    assert r.returncode == 0, (desc, r.returncode)
    with open(p, "r+b") as f:
        data = bytearray(f.read())
    n = struct.unpack("<I", data[40:44])[0] // 2
    for k in range(n):
        v = struct.unpack("<h", data[44 + 2 * k:46 + 2 * k])[0]
        v2 = int(round(v * 1.001))
        v2 = max(-32768, min(32767, v2))
        struct.pack_into("<h", data, 44 + 2 * k, v2)
    with open(p, "wb") as f:
        f.write(data)
    r = subprocess.run([sys.executable, SCORER, p, desc],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[:200]
    s = json.loads(r.stdout)
    orig_hit = BATTERY[(axis, idx)]
    rows.append({"axis": axis, "idx": idx, "descriptor": desc,
                 "orig_hit": orig_hit, "dither_hit": s["hit"],
                 "stable": bool(orig_hit) == bool(s["hit"])})
    os.unlink(p)
    print(f"{tag}: orig={orig_hit} dither={s['hit']}", flush=True)

argv_log.close()
stable = sum(r["stable"] for r in rows)
out = {"n": 20, "stable": stable, "bar": ">=19/20",
       "pass": stable >= 19, "rows": rows}
with open(os.path.join(W, "DITHER_C.json"), "w") as f:
    json.dump(out, f, indent=1)
print(f"dither stability: {stable}/20 pass={stable >= 19}")
