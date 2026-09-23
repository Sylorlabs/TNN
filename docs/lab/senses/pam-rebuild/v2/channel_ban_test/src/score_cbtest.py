#!/usr/bin/env python3
"""STEP 6 — Channel-ban test scoring glue (PREREG_CHANNEL_BAN_TEST.md §5, §6).

Pure-Zag harness (src/cbtest.zag) emits per-row verdicts and contingency
counts. This script ONLY:
  1. parses the run outputs,
  2. independently recomputes every row from the frozen evidence files and
     VOIDS on any mismatch (KB3 evidence fidelity),
  3. recomputes every VS contingency table from the R rows and VOIDS on any
     mismatch,
  4. derives false installs / truth acceptance / I(V;Y) bits from the counts,
  5. verifies the 3 run digests are byte-identical (KB2),
  6. writes out/cbtest_scores.json.

No mechanism, no judgment, no RNG. Usage:
  score_cbtest.py run1.txt run2.txt run3.txt
"""
import hashlib
import json
import math
import os
import sys

TN = os.path.expanduser("~/workspace/tnn-lab")
CHAN2 = os.path.join(TN, "kb", "autopsy", "channels2")
TESTD = os.path.join(TN, "senses", "pam-rebuild", "v2", "channel_ban_test")
OUTD = os.path.join(TESTD, "out")


def rows(path):
    with open(path) as f:
        return [l.rstrip("\n").split("\t") for l in f if l.strip()]


def mi_2x2(c):
    # c = [n00, n01, n10, n11] (rows V, cols Y) -> I(V;Y) bits
    N = sum(c)
    mi = 0.0
    for v in (0, 1):
        for y in (0, 1):
            n = c[v * 2 + y]
            if n:
                pv = (c[v * 2] + c[v * 2 + 1]) / N
                py = (c[y] + c[2 + y]) / N
                mi += (n / N) * math.log2((n / N) / (pv * py))
    return mi


def build_expected():
    """Rebuild the expected battery straight from the evidence files."""
    def base(s):
        return s[:-4] if s.endswith(".pcm") else s
    truth = [r for r in rows(os.path.join(CHAN2, "out_tcp", "truth_rows.txt")) if r[0] == "A"]
    c2v = [r for r in rows(os.path.join(CHAN2, "out_tcp", "run1", "verdicts.txt"))
           if r[0] == "TEST" and r[1] == "A"]
    c3v = [r for r in rows(os.path.join(CHAN2, "out_c3", "run1", "verdicts.txt"))
           if r[0] == "TEST" and r[1] == "A"]
    c1 = rows(os.path.join(CHAN2, "out_c1scout", "run1", "truth_rows.txt"))
    ymap = {(r[1], r[2], r[3]): int(r[4]) for r in truth}
    c2map = {(r[2], r[3], r[4]): int(r[6]) for r in c2v}
    c3map = {(r[2], r[3], r[4]): int(r[6]) for r in c3v}
    c1map = {base(r[0]): (r[1], r[2], int(r[3])) for r in c1}
    exp = []
    for (task, variant, logical) in sorted(ymap.keys()):
        y = ymap[(task, variant, logical)]
        c2 = c2map[(task, variant, logical)]
        c3 = c3map[(task, variant, logical)]
        pa = 1 if task == "pitchdisc" else 0
        aj = 0
        if pa:
            j, a, cy = c1map[base(logical)]
            assert cy == y
            aj = 1 if j == a else 0
        va = 1 if (pa == 1 and aj == 1) else 0
        vb2, vb3 = c2, c3
        vor2 = 1 if (va or vb2) else 0
        vor3 = 1 if (va or vb3) else 0
        vand2 = 1 if (va and vb2) else 0
        vand3 = 1 if (va and vb3) else 0
        exp.append((y, c2, c3, pa, aj, va, vb2, vb3, vor2, vor3, vand2, vand3))
    return exp


def parse_run(path):
    rlines, vs, kb3 = [], {}, None
    with open(path) as f:
        for line in f:
            p = line.rstrip("\n").split(" ")
            if not p or not p[0]:
                continue
            if p[0] == "R":
                rlines.append(tuple(int(x) for x in p[1:]))
            elif p[0] == "VS":
                vs[(p[1], p[2])] = [int(x) for x in p[3:7]]
            elif p[0] == "KB3SUMS":
                kb3 = [int(x) for x in p[1:5]]
    return rlines, vs, kb3


def main():
    run_paths = sys.argv[1:]
    assert len(run_paths) == 3, "need exactly 3 run files (KB2)"
    digests = []
    parsed = []
    for rp in run_paths:
        with open(rp, "rb") as f:
            digests.append(hashlib.sha256(f.read()).hexdigest())
        parsed.append(parse_run(rp))
    kb2 = (digests[0] == digests[1] == digests[2])
    assert kb2, "KB2 FAIL: runs not byte-identical: %s" % digests

    rlines, vs, kb3 = parsed[0]
    assert kb3 == [52, 92, 87, 15], "KB3SUMS mismatch: %s" % kb3

    exp = build_expected()
    assert len(rlines) == len(exp) == 92, (len(rlines), len(exp))
    for i, (rl, ex) in enumerate(zip(rlines, exp)):
        assert rl[0] == i, (i, rl[0])
        assert rl[1:] == ex, "row %d mismatch: got %s want %s" % (i, rl[1:], ex)

    # recompute every VS table from the R rows
    names = ["A", "B2", "B3", "COR2", "COR3", "CAND2", "CAND3"]
    vidx = {n: 6 + k for k, n in enumerate(names)}
    recomputed = {}
    for vname in names:
        for scope, pred in (("F", lambda r: True),
                            ("P", lambda r: r[4] == 1),
                            ("T", lambda r: r[4] == 0)):
            c = [0, 0, 0, 0]
            for rl in rlines:
                if pred(rl):
                    c[rl[vidx[vname]] * 2 + rl[1]] += 1
            recomputed[(vname, scope)] = c
            assert vs[(vname, scope)] == c, "VS %s %s mismatch" % (vname, scope)

    variants = {}
    for vname in names:
        for scope in ("F", "P", "T"):
            c = recomputed[(vname, scope)]
            n10, n11 = c[2], c[3]
            n_y1 = c[1] + c[3]
            variants["%s/%s" % (vname, scope)] = {
                "n": sum(c),
                "contingency_n00_n01_n10_n11": c,
                "installs": n10 + n11,
                "false_installs": n10,
                "true_installs": n11,
                "truth_acceptance": (n11 / n_y1) if n_y1 else None,
                "bits_I_V_Y": round(mi_2x2(c), 6),
            }
    # channel-level bits on the full battery (A/B2/B3 series == C1/C2/C3 channels)
    channels = {}
    for vname, ch in (("A", "C1-class"), ("B2", "C2-class"), ("B3", "C3-class")):
        channels[ch] = {s: variants["%s/%s" % (vname, s)]["bits_I_V_Y"] for s in ("F", "P", "T")}

    os.makedirs(OUTD, exist_ok=True)
    result = {
        "prereg": "PREREG_CHANNEL_BAN_TEST.md (frozen; commit 3ffb4962)",
        "kb2_byte_identical_3x": kb2,
        "run_sha256": digests[0],
        "kb3_evidence_fidelity": "PASS (92 rows, KB3SUMS [52,92,87,15], all rows + VS tables match evidence)",
        "kb4_zero_rng": "PASS (source audit: no RNG in cbtest.zag)",
        "variants": variants,
        "channel_bits": channels,
    }
    with open(os.path.join(OUTD, "cbtest_scores.json"), "w") as f:
        json.dump(result, f, indent=1)
    with open(os.path.join(OUTD, "cbtest.sha256"), "w") as f:
        f.write(digests[0] + "  3x byte-identical runs\n")
    print(json.dumps({
        "kb2": kb2, "digest": digests[0][:16] + "...",
        "A/F": variants["A/F"], "B2/F": variants["B2/F"], "B3/F": variants["B3/F"],
        "COR2/F": variants["COR2/F"], "COR3/F": variants["COR3/F"],
        "channel_bits_F": {k: v["F"] for k, v in channels.items()},
    }, indent=1))


if __name__ == "__main__":
    main()
