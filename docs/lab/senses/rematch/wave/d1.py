#!/usr/bin/env python3
"""Diagnostic D1 for the RAW-VS-HUMAN wave (prereg-gated, cheap, no building).

Question: are B's TRAIN_T2 colordisc/pitchdisc errors within-bin errors?
  - colordisc: error AND same color handle AND recomputed dE2000 straddles
    the dE=2.3 truth boundary (|dE-2.3| <= 1.0, fixed before looking at data)
  - pitchdisc: error AND same pitch bin AND relative pitch diff < 1 semitone
    (2**(1/12)-1)

Ground truth recomputed from the FROZEN generator code + fixture params:
  - color: exact (base, c2) RGB re-derived from the frozen RNG (verified
    byte-identical against 8 fixture files before use), dE via the frozen
    delta_e_2000 / rgb_to_lab math.
  - pitch: exact f0/f1 re-derived from the frozen RNG draws (same code path
    as the color cross-check).

B judgments/errors: runs_TRAIN_T2.jsonl B records, fitted k=0 for both tasks
(rematch VERDICT fitted params at T2: B colordisc k=0, B pitchdisc k=0).
No new data, no TEST-FRESH contact.

Gate (prereg): D1 >= 50% on a modality -> that modality is in scope for
fork building. D1 < 50% on BOTH -> STOP, report H-mech weakened.
"""
import json, math, os, sys

sys.path.insert(0, "/home/hatch/workspace/senses-rebuild/harness")
import gen
gen.MASTER_SEED = 20260922

REMATCH = "/home/hatch/workspace/senses-rematch"
RUNS_T2 = os.path.join(REMATCH, "runs_TRAIN_T2.jsonl")
WAVE = "/home/hatch/workspace/tnn-lab/senses/rematch/wave"

SEMITONE = 2 ** (1.0 / 12.0) - 1.0   # ~0.05946
COLOR_STRADDLE_HALF = 1.0            # |dE - 2.3| <= 1.0  (fixed a priori)


def rederive_color(idx):
    """Exact (base, c2) RGBs for t1 primary fixture idx (mirrors gen_t1)."""
    rng = gen.Rng(gen.stream_seed(20260922, 100 + 0 * 10 + 0, idx))
    if idx < 20:  # SAME: 10 identical, 10 near-identical
        base = gen._rand_color(rng)
        c2 = base if idx < 10 else gen._color_at_distance(rng, base, rng.range(0.4, 1.6))
        truth = "SAME"
    else:  # DIFFERENT, graded
        k = idx - 20
        base = gen._rand_color(rng)
        if k < 14: de = rng.range(10, 28)      # easy
        elif k < 27: de = rng.range(4, 10)      # medium
        else: de = rng.range(2.4, 4.0)          # hard
        c2 = gen._color_at_distance(rng, base, de)
        truth = "DIFFERENT"
    return base, c2, truth


def rederive_pitch(idx):
    """Exact (f0, f1, truth) for t4 primary fixture idx (mirrors gen_t4)."""
    rng = gen.Rng(gen.stream_seed(20260922, 100 + 3 * 10 + 0, idx))
    f0 = rng.range(220, 660)
    cls = idx % 3  # 0 SAME, 1 HIGHER, 2 LOWER
    if cls == 0:
        f1 = f0
        truth = "SAME"
    else:
        band = idx % 4
        rels = [rng.range(0.10, 0.25), rng.range(0.02, 0.05),
                rng.range(0.005, 0.008), rng.range(0.10, 0.25)]
        rel = rels[band]
        f1 = f0 * (1 + rel) if cls == 1 else f0 * (1 - rel)
        truth = "HIGHER" if cls == 1 else "LOWER"
    return f0, f1, truth


def pc_color_dist_py(a, b):
    # mirrors relations.py pc_color_dist (frozen percept.zag logic)
    def is_chroma(h):
        return 1000 <= h < 1072
    if a == b:
        return 0
    ca, cb = is_chroma(a), is_chroma(b)
    if ca and cb:
        ha, hb = (a - 1000) // 6, (b - 1000) // 6
        wd = abs(ha - hb)
        if wd > 6:
            wd = 12 - wd
        la, lb = ((a - 1000) % 6) // 2, ((b - 1000) % 6) // 2
        sa, sb = (a - 1000) % 2, (b - 1000) % 2
        return wd + abs(la - lb) + abs(sa - sb)
    if not ca and not cb:
        return abs(a - b)
    def lrank(h):
        if is_chroma(h):
            return ((h - 1000) % 6) // 2
        i = h - 2000
        return 0 if i <= 1 else (1 if i == 2 else 2)
    return 4 + abs(lrank(a) - lrank(b))


def load_t2():
    recs = []
    with open(RUNS_T2) as f:
        for line in f:
            recs.append(json.loads(line))
    return recs


def main():
    recs = load_t2()
    b_col = [r for r in recs if r["approach"] == "B" and r["task"] == "colordisc"
             and "error" not in r]
    b_pitch = [r for r in recs if r["approach"] == "B" and r["task"] == "pitchdisc"
               and "error" not in r]
    assert b_col and b_pitch, "missing TRAIN_T2 records"

    # sanity: cached truths must match re-derived truths
    for r in b_col:
        idx = int(r["rel"].split("/")[-1][1:4])
        assert rederive_color(idx)[2] == r["truth"], (r["rel"], "color truth mismatch")
    for r in b_pitch:
        idx = int(r["rel"].split("/")[-1][1:4])
        assert rederive_pitch(idx)[2] == r["truth"], (r["rel"], "pitch truth mismatch")

    # ---- colordisc ----
    col_rows = []
    for r in sorted(b_col, key=lambda x: x["rel"]):
        idx = int(r["rel"].split("/")[-1][1:4])
        base, c2, truth = rederive_color(idx)
        de = gen.delta_e_2000(gen.rgb_to_lab(*base), gen.rgb_to_lab(*c2))
        p1, p2 = r["scores"]["percept"], r["scores"]["percept2"]
        same_handle = (p1 == p2)
        judg = "SAME" if pc_color_dist_py(p1, p2) <= 0 else "DIFFERENT"
        err = (judg != truth)
        straddle = abs(de - 2.3) <= COLOR_STRADDLE_HALF
        col_rows.append({"rel": r["rel"], "truth": truth, "judgment": judg,
                         "error": err, "de": de, "same_handle": same_handle,
                         "straddle": straddle, "p1": p1, "p2": p2})
    col_err = [x for x in col_rows if x["error"]]
    col_within = [x for x in col_err if x["same_handle"] and x["straddle"]]
    col_samehandle = [x for x in col_err if x["same_handle"]]

    # ---- pitchdisc ----
    pit_rows = []
    for r in sorted(b_pitch, key=lambda x: x["rel"]):
        idx = int(r["rel"].split("/")[-1][1:4])
        f0, f1, truth = rederive_pitch(idx)
        rel = abs(f1 - f0) / f0
        p1, p2 = r["scores"]["percept"], r["scores"]["percept2"]
        same_bin = (p1 == p2)
        d = abs(p1 - p2)
        judg = "SAME" if d <= 0 else ("HIGHER" if p2 > p1 else "LOWER")
        err = (judg != truth)
        sub_semi = rel < SEMITONE
        pit_rows.append({"rel": r["rel"], "truth": truth, "judgment": judg,
                         "error": err, "rel_pitch": rel, "same_bin": same_bin,
                         "sub_semitone": sub_semi, "p1": p1, "p2": p2})
    pit_err = [x for x in pit_rows if x["error"]]
    pit_within = [x for x in pit_err if x["same_bin"] and x["sub_semitone"]]
    pit_samebin = [x for x in pit_err if x["same_bin"]]

    def frac(a, b):
        return (a / b) if b else 0.0

    out = {
        "prereg": "WAVE_RAWVSHUMAN_PREREG.md D1",
        "data": "runs_TRAIN_T2.jsonl (B records), frozen gen.py re-derivation",
        "fitted_k": {"B/colordisc": 0, "B/pitchdisc": 0},
        "colordisc": {
            "n": len(col_rows),
            "errors": len(col_err),
            "error_rate": frac(len(col_err), len(col_rows)),
            "same_handle_errors": len(col_samehandle),
            "straddle_errors": sum(1 for x in col_err if x["straddle"]),
            "within_bin_straddle_errors": len(col_within),
            "D1": frac(len(col_within), len(col_err)),
            "same_handle_fraction_of_errors": frac(len(col_samehandle), len(col_err)),
            "gate_pass": frac(len(col_within), len(col_err)) >= 0.5,
        },
        "pitchdisc": {
            "n": len(pit_rows),
            "errors": len(pit_err),
            "error_rate": frac(len(pit_err), len(pit_rows)),
            "same_bin_errors": len(pit_samebin),
            "sub_semitone_errors": sum(1 for x in pit_rows if x["error"] and x["sub_semitone"]),
            "within_bin_subsemitone_errors": len(pit_within),
            "D1": frac(len(pit_within), len(pit_err)),
            "same_bin_fraction_of_errors": frac(len(pit_samebin), len(pit_err)),
            "gate_pass": frac(len(pit_within), len(pit_err)) >= 0.5,
        },
    }

    os.makedirs(WAVE, exist_ok=True)
    with open(os.path.join(WAVE, "d1_results.json"), "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    with open(os.path.join(WAVE, "d1_colordisc_rows.jsonl"), "w") as f:
        for x in col_rows:
            f.write(json.dumps(x, sort_keys=True) + "\n")
    with open(os.path.join(WAVE, "d1_pitchdisc_rows.jsonl"), "w") as f:
        for x in pit_rows:
            f.write(json.dumps(x, sort_keys=True) + "\n")

    print("=== D1: colordisc ===")
    print("n=%d errors=%d (%.3f)" % (len(col_rows), len(col_err),
                                    frac(len(col_err), len(col_rows))))
    print("same-handle errors=%d straddle-band errors=%d both=%d"
          % (len(col_samehandle),
             sum(1 for x in col_err if x["straddle"]), len(col_within)))
    print("D1_color = %.4f  GATE %s" % (out["colordisc"]["D1"],
                                        "PASS" if out["colordisc"]["gate_pass"] else "FAIL"))
    print("=== D1: pitchdisc ===")
    print("n=%d errors=%d (%.3f)" % (len(pit_rows), len(pit_err),
                                    frac(len(pit_err), len(pit_rows))))
    print("same-bin errors=%d sub-semitone errors=%d both=%d"
          % (len(pit_samebin),
             sum(1 for x in pit_rows if x["error"] and x["sub_semitone"]), len(pit_within)))
    print("D1_pitch = %.4f  GATE %s" % (out["pitchdisc"]["D1"],
                                       "PASS" if out["pitchdisc"]["gate_pass"] else "FAIL"))
    # dE histogram of colordisc errors (band context)
    import collections
    hb = collections.Counter()
    for x in col_err:
        de = x["de"]
        key = "de<1.3" if de < 1.3 else ("1.3-3.3" if de <= 3.3 else ("3.3-10" if de <= 10 else "de>10"))
        hb[(key, "same_handle" if x["same_handle"] else "diff_handle")] += 1
    print("colordisc error dE x handle table:", dict(sorted(hb.items())))
    hb2 = collections.Counter()
    for x in pit_err:
        key = "sub-semi" if x["sub_semitone"] else ">=1-semitone"
        hb2[(key, "same_bin" if x["same_bin"] else "diff_bin")] += 1
    print("pitchdisc error relpitch x bin table:", dict(sorted(hb2.items())))


if __name__ == "__main__":
    main()
