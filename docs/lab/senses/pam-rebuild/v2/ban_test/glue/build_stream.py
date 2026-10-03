#!/usr/bin/env python3
"""Build the frozen R2-4 replay stream for bantest.zag.

Reads (read-only):
  <lab>/senses/pam-rebuild/round2/forks/R2-4/evidence/clean/sweep.jsonl
  <lab>/senses/pam-rebuild/round2/forks/R2-4/evidence/clean/records.txt
Joins on seq; asserts 11,840 rows, identical seq sets.

Emits (one line per trial):
  seq|tcode|fixture|fprog|jcode|conf|fpred|meas|mrgF
where fprog/fpred are the POST-DELIBERATION fields (final_prog/final_pred),
mirroring the autopsy replay method (0 mismatches / 11,840 vs
gate_dispositions.txt). The gate's decision path never sees truth: no truth
column is emitted. Scoring joins truth back in score.py.

Deterministic: no RNG, no dict-ordering dependence (rows sorted by seq).
"""
import json, os, sys

LAB = os.path.expanduser("~/workspace/tnn-lab")
EV = LAB + "/senses/pam-rebuild/round2/forks/R2-4/evidence/clean"

def main():
    out_path = sys.argv[1] if len(sys.argv) > 1 else "stream.txt"
    recs = {}
    with open(EV + "/records.txt") as f:
        for line in f:
            p = line.rstrip("\n").split("|")
            assert len(p) == 11, line[:80]
            seq = int(p[0])
            recs[seq] = {
                "tcode": int(p[1]), "fixture": p[2], "jcode": int(p[4]),
                "conf_rec": int(p[6]), "meas": int(p[8]),
            }
    sw = {}
    with open(EV + "/sweep.jsonl") as f:
        for line in f:
            r = json.loads(line)
            sw[r["seq"]] = r
    assert len(recs) == 11840 and len(sw) == 11840, (len(recs), len(sw))
    assert set(recs) == set(sw), "seq set mismatch"
    # cross-checks against the frozen record fields
    for seq in sorted(sw):
        r, s = recs[seq], sw[seq]
        assert r["conf_rec"] == s["conf"], seq
        assert r["meas"] == s["measure"], seq
        assert r["jcode"] >= 0
    with open(out_path, "w") as o:
        for seq in sorted(sw):
            r, s = recs[seq], sw[seq]
            o.write("%d|%d|%s|%d|%d|%d|%d|%d|%d\n" % (
                seq, r["tcode"], r["fixture"], int(s["final_prog"]),
                r["jcode"], s["conf"], int(s["final_pred"]),
                r["meas"], int(s["mrgF"])))
    print("wrote %s (11840 rows)" % out_path)

if __name__ == "__main__":
    main()
