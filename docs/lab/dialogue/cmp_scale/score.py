#!/usr/bin/env python3
"""Score cmp_scale runs.

Reads oracle.jsonl + one or more run logs, reports per-family per-scale:
  exact accuracy (binary PASS/FAIL) and decisive accuracy (oracle rules).

Decisive rules (frozen in PREREG_CMP_SCALE.md):
  yn/ba/idk : response == expected exactly
  winner    : winner's canonical name in response AND a direction word of
              the right (dim,dir) class in response.
"""
import json
import os
import re
import sys

DIR_WORDS = {
    ("H", "max"): ["taller", "tallest", "higher"],
    ("H", "min"): ["shorter", "shortest", "lower"],
    ("T", "min"): ["first"],
    ("T", "max"): ["last"],
}

T_RE = re.compile(r"^(?:NOVEL=1 )?T (\S+) (\d+) (PASS|FAIL)$")


def load_oracle(path):
    o = {}
    with open(path) as f:
        for line in f:
            r = json.loads(line)
            o[(r["id"], r["turn"])] = r
    return o


def load_log(path):
    """(id, turn) -> (pass_bool, response)."""
    res = {}
    cur = None
    with open(path) as f:
        for line in f:
            line = line.rstrip("\n")
            m = T_RE.match(line)
            if m:
                did, turn, pf = m.group(1), int(m.group(2)), m.group(3)
                cur = (did, turn)
                res[cur] = [pf == "PASS", None]
            elif line.startswith("A ") and cur is not None:
                res[cur][1] = line[2:]
                cur = None
    return {k: tuple(v) for k, v in res.items()}


def decisive(ok_oracle, resp):
    dec = ok_oracle["dec"]
    if dec in ("yn", "ba", "idk"):
        return resp == ok_oracle["expected"]
    if dec == "winner":
        w = ok_oracle["winner"]
        words = DIR_WORDS[(ok_oracle["dim"], ok_oracle["dir"])]
        return (w in resp) and any(x in resp for x in words)
    raise ValueError(dec)


def main():
    root = os.path.dirname(os.path.abspath(__file__))
    oracle = load_oracle(os.path.join(root, "oracle.jsonl"))
    logs = sys.argv[1:]
    # aggregate over all logs given (e.g. 4 chunks of 100x)
    agg = {}
    digests = []
    for lp in logs:
        res = load_log(lp)
        with open(lp) as f:
            for line in f:
                if line.startswith("DIGEST "):
                    digests.append(line.split()[1])
        for k, (p, resp) in res.items():
            assert k not in agg, f"duplicate probe {k} across logs"
            agg[k] = (p, resp)
    fams = {}
    for (did, turn), (p, resp) in agg.items():
        o = oracle.get((did, turn))
        if o is None:
            print(f"WARN: no oracle for {did} turn {turn}")
            continue
        fam = o["family"]
        d = fams.setdefault(fam, {"n": 0, "exact": 0, "dec": 0})
        d["n"] += 1
        d["exact"] += 1 if p else 0
        d["dec"] += 1 if decisive(o, resp if resp is not None else "") else 0
    print(f"{'family':12s} {'n':>5s} {'exact':>7s} {'decisive':>8s}")
    tn = te = td = 0
    for fam in sorted(fams):
        d = fams[fam]
        tn += d["n"]; te += d["exact"]; td += d["dec"]
        print(f"{fam:12s} {d['n']:5d} {d['exact']/d['n']:7.3f} "
              f"{d['dec']/d['n']:8.3f}")
    print(f"{'TOTAL':12s} {tn:5d} {te/tn:7.3f} {td/tn:8.3f}")
    if digests:
        print("DIGESTS:", " ".join(digests),
              "all-equal" if len(set(digests)) == 1 else "MISMATCH")


if __name__ == "__main__":
    main()
