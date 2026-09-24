#!/usr/bin/env python3
"""Independent audit scorer for fork C battery transcripts.
Recomputes per-bar rates from case-file EXPECT fields + transcript lines.
Usage: audit_c.py <cases-dir> <transcript>"""
import sys, re, os

cases_dir, transcript = sys.argv[1], sys.argv[2]

# Parse manifest -> ordered case file list
manifest = sys.argv[3]
mfiles = [l.strip().split("/")[0] for l in open(manifest) if l.strip()]
# manifest lines are like "m1/m1-catch-001.txt" or bare filenames
mfiles = [l.strip() for l in open(manifest) if l.strip()]
mfiles = [m.split("/")[-1] for m in mfiles]

# Parse case files: id -> (bar, expect, is_gold)
cases = {}
for fn in mfiles:
    cid, bar, expect, gold = None, None, None, False
    with open(os.path.join(cases_dir, fn)) as f:
        for line in f:
            line = line.rstrip("\n")
            if line.startswith("CASE:"): cid = line[5:].strip()
            elif line.startswith("BAR:"): bar = line[4:].strip()
            elif line.startswith("EXPECT:"): expect = line[7:].strip()
    if cid:
        gold = "gold" in fn
        cases[cid] = (bar, expect, gold)

# Parse transcript
verdicts, pairs = {}, {}
for line in open(transcript):
    line = line.rstrip("\n")
    if line.startswith("VERDICT "):
        p = line.split()
        verdicts[p[1]] = p[2]
    elif line.startswith("PAIR "):
        p = line.split()
        # PAIR <case> <SAME|DIVERGE> expect=<..>
        res = p[2]
        exp = p[3].split("=", 1)[1] if len(p) > 3 and "=" in p[3] else None
        pairs[p[1]] = (res, exp)

bars = {"m1": [0, 0, 0, 0], "m2": [0, 0], "m3": [0, 0],
        "m4": [0, 0], "m5": [0, 0], "m6": [0, 0]}
# m1: [catch_n, catch_ok, gold_n, gold_ok]; others: [n, ok]
errors = []
for cid, (bar, expect, gold) in sorted(cases.items()):
    if bar in ("m2", "m3"):
        if cid not in pairs:
            errors.append(f"MISSING PAIR {cid}")
            continue
        res, pexp = pairs[cid]
        if pexp != expect:
            errors.append(f"PAIR-EXPECT-MISMATCH {cid}: file={expect} line={pexp}")
        bars[bar][0] += 1
        if res == expect:
            bars[bar][1] += 1
        else:
            errors.append(f"PAIR-FAIL {cid}: got {res} expect {expect}")
    else:
        if cid not in verdicts:
            errors.append(f"MISSING VERDICT {cid}")
            continue
        v = verdicts[cid]
        if bar == "m1":
            bars["m1"][0 if not gold else 2] += 1
            if v == expect:
                bars["m1"][1 if not gold else 3] += 1
            else:
                errors.append(f"M1-FAIL {cid}: got {v} expect {expect}")
        else:
            bars[bar][0] += 1
            if v == expect:
                bars[bar][1] += 1
            else:
                errors.append(f"{bar.upper()}-FAIL {cid}: got {v} expect {expect}")

print(f"cases parsed: {len(cases)}, verdicts: {len(verdicts)}, pairs: {len(pairs)}")
m1 = bars["m1"]
print(f"M1 catch: {m1[1]}/{m1[0]}  gold-ok: {m1[3]}/{m1[2]} (false-withhold {(m1[2]-m1[3])}/{m1[2]})")
for b in ("m2", "m3", "m4", "m5", "m6"):
    n, ok = bars[b]
    print(f"{b.upper()}: {ok}/{n} = {ok/n*100:.1f}%" if n else f"{b.upper()}: n=0")
print(f"errors: {len(errors)}")
for e in errors[:20]:
    print(" ", e)
