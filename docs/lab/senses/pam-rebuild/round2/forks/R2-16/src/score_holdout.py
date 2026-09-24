#!/usr/bin/env python3
"""score_holdout.py -- R2-16 B-holdout scorer (prereg bar 5).

Scores a holdout union ledger against fixtures_holdout/gen_ledger.jsonl.
Reports per-family (10 families x 1000) false-install counts and 95%
Wilson UCBs, plus the pooled FI and pooled UCB.

Also supports scoring the abl_bank 1-NN disposition (for the bar-3
holdout-gap condition) via --abl <bank.json>.

Usage:
  score_holdout.py <ledger> <list> [--abl <bank.json>]
"""
import json, re, os, sys, math

HERE = os.path.dirname(os.path.abspath(__file__))
FORK = os.path.normpath(os.path.join(HERE, ".."))

JMAP = {
    "colordisc": {"SAME": 0, "DIFFERENT": 1},
    "colorconst": {"SAME_SURFACE": 0, "DIFFERENT": 1},
    "shapetrans": {"CIRCLE": 0, "TRIANGLE": 1, "SQUARE": 2},
    "pitchdisc": {"SAME": 0, "HIGHER": 1, "LOWER": 2},
    "timbredisc": {"PURE": 0, "BRIGHT": 1, "DARK": 2, "RICH": 3},
    "motiondir": {"STILL": 0, "N": 1, "NE": 2, "E": 3, "SE": 4, "S": 5,
                  "SW": 6, "W": 7, "NW": 8},
}
FAM_ORDER = ["R2H16-COL-1", "R2H16-CCN-1", "R2H16-CCN-2", "R2H16-SHP-1",
             "R2H16-SHP-2", "R2H16-PTC-1", "R2H16-PTC-2", "R2H16-TMB-1",
             "R2H16-TMB-2", "R2H16-MOT-1"]
LED_PAT = re.compile(
    r'fixture=r2fx_t(\d+)_i(\d+)_f(\d+)\s+task=(\w+)\s+judgment=(\S+)'
    r'\s+conf=(\d+)\s+challenge=\S+\s+outcome=(\S+)\s+disp=(\w+)')

def wilson_ucb(k, n, z=1.96):
    if n == 0:
        return 1.0
    p = k / n
    den = 1 + z * z / n
    ctr = p + z * z / (2 * n)
    mgn = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (ctr + mgn) / den

def main():
    ledger_path, list_path = sys.argv[1], sys.argv[2]
    abl_bank = None
    if "--abl" in sys.argv:
        abl_bank = json.load(open(sys.argv[sys.argv.index("--abl") + 1]))

    truth = {}
    fam_of = {}
    with open(os.path.join(FORK, "fixtures_holdout", "gen_ledger.jsonl")) as f:
        for line in f:
            d = json.loads(line)
            truth[d["id"]] = d["truth"]
            fam_of[d["id"]] = d["family"]
    with open(list_path) as f:
        paths = [l.strip() for l in f]
    rows = []
    with open(ledger_path, "rb") as f:
        for raw in f:
            m = LED_PAT.search(raw.decode("utf-8", "replace"))
            if m:
                t, i, fam, task, jname, conf, out, disp = m.groups()
                rows.append({"task": task, "idx": int(i), "jname": jname,
                             "conf": int(conf), "disp": disp})
    assert len(rows) == len(paths), (len(rows), len(paths))
    fam_fi = {f: 0 for f in FAM_ORDER}
    fam_n = {f: 0 for f in FAM_ORDER}
    total_fi = 0
    for r, p in zip(rows, paths):
        oid = re.match(r'.*/(r2h16_R2H16-[A-Z]+-\d+_\d+)\.r2fx$', p).group(1)
        t = truth[oid]
        fam = fam_of[oid]
        jid = JMAP[r["task"]].get(r["jname"], -1)
        tid = JMAP[r["task"]].get(t, -1)
        correct = (jid == tid and jid >= 0)
        if abl_bank is None:
            is_fi = (r["disp"] == "INSTALL" and not correct)
        else:
            b = abl_bank[r["task"]]
            best_d, best_lab = None, None
            for lab, vals in (("true", b["true"]), ("false", b["false"])):
                for v in vals:
                    d = abs(r["conf"] - v)
                    if best_d is None or d < best_d:
                        best_d, best_lab = d, lab
                    elif d == best_d and lab == "false":
                        best_lab = "false"
            is_fi = (best_lab == "true" and not correct)
        fam_n[fam] += 1
        if is_fi:
            fam_fi[fam] += 1
            total_fi += 1
    n = len(rows)
    mode = "abl_bank" if abl_bank else "full"
    print("holdout %s: n=%d FI=%d (%.3f%%)" % (mode, n, total_fi, 100.0 * total_fi / n))
    print("pooled UCB: %.4f%%" % (100.0 * wilson_ucb(total_fi, n)))
    for fam in FAM_ORDER:
        k, nn = fam_fi[fam], fam_n[fam]
        print("  %s: %d/%d = %.3f%%  UCB=%.4f%%" %
              (fam, k, nn, 100.0 * k / nn if nn else 0, 100.0 * wilson_ucb(k, nn)))
    print("RESULT mode=%s fi=%d n=%d pooled_ucb=%.6f" %
          (mode, total_fi, n, wilson_ucb(total_fi, n)))

if __name__ == "__main__":
    main()
