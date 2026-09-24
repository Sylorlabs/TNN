#!/usr/bin/env python3
"""Score FS-GR2 CH-MOT-5 frozen battery per task spec.
- MOTIONDIR ADV (task=motiondir, n=630): FI = disp=INSTALL and judgment != truth
- MOTIONDIR CTRL (task=motiondir, n=200): recall = (disp=INSTALL and judgment==truth)/200
- NO-REGRESSION: other five tasks' lines byte-identical to FS-GR1 committed raws
- Resolve rate: non-UNRESOLVED fraction on motiondir ctrl
Usage: score_mot5.py adv|ctrl <claim.tsv> <my_raw.txt> <gr1_raw.txt>
"""
import sys, math, os

def parse_kv(line):
    d = {}
    for tok in line.split():
        if "=" in tok:
            k, v = tok.split("=", 1)
            d[k] = v
    return d

def truth_of(fixture_path):
    tline = open(fixture_path + ".truth").read().strip()
    return tline.split("=", 1)[1] if "=" in tline else tline

def wilson_ucb(p, n, z=1.96):
    if n == 0:
        return 1.0
    z2 = z * z
    num = p + z2 / (2 * n) + z * math.sqrt(p * (1 - p) / n + z2 / (4 * n * n))
    return num / (1 + z2 / n)

def main():
    tag, claim_path, my_raw, gr1_raw = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    claims = [l.rstrip("\n").split("\t") for l in open(claim_path) if l.strip()]
    raws = [l.rstrip("\n") for l in open(my_raw) if l.strip()]
    assert len(claims) == len(raws), f"claims {len(claims)} != raws {len(raws)}"
    rows = []
    for (cpath, _cclaim), rline in zip(claims, raws):
        kv = parse_kv(rline)
        # sanity: fixture id stem corresponds to claim path stem
        rows.append({"path": cpath, "task": kv["task"], "judgment": kv["judgment"],
                     "challenge": kv["challenge"], "outcome": kv["outcome"],
                     "disp": kv["disp"], "line": rline})
    for r in rows:
        r["truth"] = truth_of(r["path"])

    mot = [r for r in rows if r["task"] == "motiondir"]
    print(f"[{tag}] motiondir rows: {len(mot)} (expect 630 adv / 200 ctrl)")
    fi = [r for r in mot if r["disp"] == "INSTALL" and r["judgment"] != r["truth"]]
    n = len(mot)
    rate = len(fi) / n if n else 0.0
    print(f"[{tag}] motiondir FI: {len(fi)}/{n}  rate={rate:.4f}  Wilson95_UCB={wilson_ucb(rate, n):.4f}")
    if tag == "ctrl":
        rec = sum(1 for r in mot if r["disp"] == "INSTALL" and r["judgment"] == r["truth"])
        print(f"[{tag}] motiondir recall: {rec}/{n} = {rec/n:.4f}")
    elif tag == "adv":
        inst = sum(1 for r in mot if r["disp"] == "INSTALL")
        print(f"[{tag}] motiondir INSTALL count (any): {inst}/{n}")
    unresolved = sum(1 for r in mot if r["outcome"] == "UNRESOLVED")
    print(f"[{tag}] motiondir UNRESOLVED: {unresolved}/{n}  resolve_rate={(n-unresolved)/n if n else 0:.4f}")

    # no-regression: other five tasks byte-identical to FS-GR1 committed raw
    gr1_lines = [l.rstrip("\n") for l in open(gr1_raw) if l.strip()]
    my_other = [r["line"] for r in rows if r["task"] != "motiondir"]
    gr1_other = [l for l in gr1_lines if parse_kv(l)["task"] != "motiondir"]
    same = (len(my_other) == len(gr1_other)) and all(a == b for a, b in zip(my_other, gr1_other))
    print(f"[{tag}] other-five byte-identity vs FS-GR1: {'PASS' if same else 'FAIL'} "
          f"(mine={len(my_other)}, gr1={len(gr1_other)})")
    if not same:
        for i, (a, b) in enumerate(zip(my_other, gr1_other)):
            if a != b:
                print(f"  first diff at other-task line {i}:\n    mine: {a}\n    gr1 : {b}")
                break

if __name__ == "__main__":
    main()
