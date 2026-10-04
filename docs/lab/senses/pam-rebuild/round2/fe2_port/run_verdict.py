#!/usr/bin/env python3
"""FE2 verdict harness (frozen PREREG_FE2_PORT.md §5-§7).
Runs fe2 on fresh held-out indices 24..47 (11 families x 24), 3x byte-identical;
scores vs truth; applies frozen kill bars vs the canonical R2-4 sense baseline;
runs the COL-5 defense-scope negative control; writes VERDICT_FE2.md."""
import sys, os, subprocess, hashlib, json, re, datetime

HERE = os.path.expanduser("~/workspace/pam_round2/fe2_port")
BUILD = os.path.join(HERE, "build")
FE2 = os.path.join(BUILD, "fe2")
HELD = os.path.join(HERE, "heldout")
COL5D = os.path.join(HERE, "heldout_col5")
BASE = json.load(open(os.path.join(BUILD, "baseline.json")))

FAMS = ["PTC-4","PTC-5","TMB-4","TMB-5","COL-4","CCN-3","CCN-4","SHP-4","SHP-5","MOT-4","MOT-5"]
EXT = {"PTC-4":"pcm","PTC-5":"pcm","TMB-4":"pcm","TMB-5":"pcm","COL-4":"img",
       "CCN-3":"img","CCN-4":"img","SHP-4":"img","SHP-5":"img","MOT-4":"vid","MOT-5":"vid"}

def run_fe2(fam, paths):
    p = subprocess.run([FE2, fam] + paths, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr

def truth_of(path):
    return open(path + ".truth").read().strip().split("=", 1)[1].strip()

# ---- 3x byte-identical full held-out runs ----
digests = []
runblobs = []
for r in range(3):
    blob = []
    for fam in FAMS:
        paths = [os.path.join(HELD, f"rt3_{fam}_{i:04d}.{EXT[fam]}") for i in range(24, 48)]
        rc, out, err = run_fe2(fam, paths)
        assert rc == 0, f"run {r} {fam} rc={rc} err={err[:200]}"
        assert len(out.strip().split(chr(10))) == 24, f"run {r} {fam} line count"
        blob.append(f"# {fam}\n" + out)
    full = "".join(blob).encode()
    digests.append(hashlib.sha256(full).hexdigest())
    runblobs.append(full)
    open(os.path.join(BUILD, f"predictions_run{r+1}.txt"), "wb").write(full)
    print(f"run {r+1} digest: {digests[r]}", flush=True)

det_ok = (digests[0] == digests[1] == digests[2])
print("3x byte-identical:", det_ok, flush=True)
assert det_ok, "NON-DETERMINISM"

# ---- score run 1 vs truth ----
scores, per_fam = {}, {}
for fam in FAMS:
    ok = 0; rows = []
    for i in range(24, 48):
        path = os.path.join(HELD, f"rt3_{fam}_{i:04d}.{EXT[fam]}")
        t = truth_of(path)
        m = re.search(r"prediction=([A-Z_]+)", runblobs[0].decode().split(f"# {fam}\n")[1].split("\n")[i-24])
        pred = m.group(1)
        c = 1 if pred == t else 0
        ok += c
        rows.append((i, t, pred, c))
    scores[fam] = ok
    per_fam[fam] = rows

# ---- frozen kill bars (PREREG §6) ----
results = {}
for fam in FAMS:
    fe2, base = scores[fam], BASE[fam]["correct"]
    a = fe2 >= 20
    b = fe2 >= base
    c = (base >= 20) or (fe2 - base >= 4)
    surv = a and b and c
    results[fam] = (fe2, base, a, b, c, surv)
n_surv = sum(1 for f in FAMS if results[f][5])
useful = n_surv >= 9

# ---- COL-5 negative control ----
col5_path = os.path.join(COL5D, "rt3_COL-5_0024.img")
rc, out, err = run_fe2("COL-5", [col5_path])
col5_ok = (rc == 3 and "defense-scope" in err and out == "")
print(f"COL-5 control: rc={rc} defense-scope-refusal={col5_ok}", flush=True)

# ---- verdict doc ----
L = []
L.append("# VERDICT_FE2 — FE2 separator port, Crew 1 (Round 3)")
L.append("")
L.append(f"Date: {datetime.date.today().isoformat()} (America/Los_Angeles)")
L.append("Prereg: PREREG_FE2_PORT.md (frozen, committed alone as f8e4dfa5d444b30f8668d0bf445e64dcb69af539)")
L.append("Held-out manifest SHA-256: 60d4a912432bbc92ba04e200cf34fe117f9726f996b24c5fd8c5d95c6030682a")
L.append("Held-out indices: 24..47 (24 fixtures/family, 264 total; indices 0..23 build self-checks only)")
L.append("Baseline: canonical R2-4 sense_r24 (SHA-256 a71a11f16dcb0883e09107ddf3e13afb1ac32dc5b312c54cf724d82b8723b159)")
L.append("")
L.append("## Determinism")
for r, d in enumerate(digests):
    L.append(f"- run {r+1} predictions SHA-256: `{d}`")
L.append(f"- 3x byte-identical: **{'PASS' if det_ok else 'FAIL'}**")
L.append("")
L.append("## Per-separator verdict (frozen bars: FE2>=20/24, FE2>=baseline, lead>=4/24 if baseline<20/24)")
L.append("")
L.append("| family | FE2 (held-out 24-47) | sense baseline | bar-a (>=20) | bar-b (>=base) | bar-c (lead>=4) | verdict |")
L.append("|---|---|---|---|---|---|---|")
for fam in FAMS:
    fe2, base, a, b, c, surv = results[fam]
    L.append(f"| {fam} | {fe2}/24 | {base}/24 | {'Y' if a else 'n'} | {'Y' if b else 'n'} | {'Y' if c else 'n'} | **{'SURVIVE' if surv else 'KILL'}** |")
L.append("")
L.append(f"## Program usefulness: {n_surv}/11 separators survive -> **{'USEFUL' if useful else 'NOT USEFUL'}** (bar: >=9/11)")
L.append("")
L.append("## COL-5 defense-scope control")
L.append(f"- `fe2 COL-5 <fixture>` -> exit code {rc} (expected 3), stderr carries the defense-scope refusal: **{'PASS' if col5_ok else 'FAIL'}**")
L.append("- COL-5 was not ported; its machine-checked Bayes ceiling (15.5/24 = 64.6% < 80% bar) keeps it defense-scope per the frozen prereg.")
L.append("")
L.append("## Implementation notes")
L.append("- Pure Zag, zero RNG. Audio families use /8 true-time decimation with a fixed-point (x1024) 5-term Taylor sin correlator bank; peak locations, harmonic ratios, and the full-spectrum centroid are preserved (verified: FE2 predictions match the float64 FE1 audit on all 264 frozen fixtures, indices 0..23).")
L.append("- Image/video families use exact integer comparisons (cross-multiplication for IoU/direction, scaled-integer thresholds); CCN inversion uses banker's rounding, matching the FE1 reference.")
with open(os.path.join(BUILD, "VERDICT_FE2.md"), "w") as f:
    f.write("\n".join(L) + "\n")

json.dump({"scores": scores, "baseline": BASE,
           "results": {f: {"fe2": v[0], "base": v[1], "survive": v[5]} for f, v in results.items()},
           "n_survive": n_surv, "useful": useful, "digests": digests,
           "col5_control": {"rc": rc, "ok": col5_ok}},
          open(os.path.join(BUILD, "verdict.json"), "w"), indent=1)

print(f"\nSURVIVE: {n_surv}/11  USEFUL: {useful}", flush=True)
for fam in FAMS:
    fe2, base, a, b, c, surv = results[fam]
    print(f"  {fam}: FE2 {fe2}/24 vs base {base}/24 -> {'SURVIVE' if surv else 'KILL'}", flush=True)
