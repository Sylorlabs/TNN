#!/usr/bin/env python3
"""G2 B6 part 2: independent Python FNV-1a-64 ledger re-verification.

Re-parses every batch record from stdout (fixture order, all fields),
re-chains from genesis L_0 = FNV-1a-64("G2-PRP-1") per prereg 2.4, and
compares each per-record 'chain=' value and the SUMMARY 'ledger_final='
against the binary's emitted values. Independent of the Zag binary.
Usage: ledger_verify.py <batch_output.txt> [...]
"""
import sys

FNV_INIT = 14695981039346656037
FNV_PRIME = 1099511628211
MASK = 0xFFFFFFFFFFFFFFFF

TASKS = ["colordisc", "colorconst", "shapetrans",
         "pitchdisc", "timbredisc", "motiondir"]
TID = {t: i + 1 for i, t in enumerate(TASKS)}
JCODE = {  # task-keyed; must match parse_truth() in g2_sense.zag exactly
    ("colordisc", "SAME"): 0, ("colordisc", "DIFFERENT"): 1,
    ("colorconst", "SAME_SURFACE"): 0, ("colorconst", "DIFFERENT"): 1,
    ("shapetrans", "CIRCLE"): 0, ("shapetrans", "SQUARE"): 1,
    ("shapetrans", "TRIANGLE"): 2,
    ("pitchdisc", "SAME"): 0, ("pitchdisc", "HIGHER"): 1,
    ("pitchdisc", "LOWER"): 2,
    ("timbredisc", "PURE"): 0, ("timbredisc", "DARK"): 1,
    ("timbredisc", "RICH"): 2, ("timbredisc", "BRIGHT"): 3,
    ("motiondir", "STILL"): 0, ("motiondir", "N"): 1,
    ("motiondir", "NE"): 2, ("motiondir", "E"): 3,
    ("motiondir", "SE"): 4, ("motiondir", "S"): 5,
    ("motiondir", "SW"): 6, ("motiondir", "W"): 7,
    ("motiondir", "NW"): 8,
}

def fnv_str(s):
    h = FNV_INIT
    for ch in s:
        h = ((h ^ ord(ch)) * FNV_PRIME) & MASK
    return h

def fnv_bytes(h, data):
    for b in data:
        h = ((h ^ b) * FNV_PRIME) & MASK
    return h

def verify(path):
    with open(path, "rb") as f:
        out = f.read()
    recs = []
    cur = {}
    for line in out.decode("utf-8", "replace").splitlines():
        if "=" not in line:
            continue
        k, v = line.split("=", 1)
        cur[k] = v
        if k == "chain":
            recs.append(cur)
            cur = {}
    summ = cur
    h = fnv_str("G2-PRP-1")
    genesis = h
    ok = True
    bad_recs = 0
    for r in recs:
        tid = TID[r["task"]]
        jc = JCODE[(r["task"], r["judgment"])]
        disp = 1 if r["disposition"] == "INSTALL" else 0
        norm = int(r["residual_norm"])
        ph = int(r["pred_hash"], 16)
        oh = int(r["obs_hash"], 16)
        rv = [(int(x) & 0xFF) for x in r["residuals"].split(",")]
        assert len(rv) == 256, "record has %d residual bytes" % len(rv)
        rec = bytes([tid & 0xFF, jc & 0xFF, disp & 0xFF,
                     norm & 0xFF, (norm >> 8) & 0xFF])
        rec += ph.to_bytes(8, "little") + oh.to_bytes(8, "little")
        assert len(rec) == 21
        rec += bytes(rv)
        assert len(rec) == 277
        h = fnv_bytes(h, rec)
        if "%016x" % h != r["chain"]:
            ok = False
            bad_recs += 1
    final = "%016x" % h
    if final != summ.get("ledger_final", ""):
        ok = False
    print("%s: genesis=%016x records=%d ledger_final(binary)=%s "
          "ledger_final(recompute)=%s per-record-match=%d/%d -> %s"
          % (path, genesis, len(recs), summ.get("ledger_final"),
             final, len(recs) - bad_recs, len(recs),
             "PASS" if ok else "FAIL"))
    return ok, len(recs), final

if __name__ == "__main__":
    results = [verify(p) for p in sys.argv[1:]]
    sys.exit(0 if all(r[0] for r in results) else 1)
