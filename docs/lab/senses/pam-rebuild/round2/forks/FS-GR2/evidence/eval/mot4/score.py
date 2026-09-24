#!/usr/bin/env python3
"""FS-GR2 MOT-4 scorer.

Parses raw lines as k=v pairs:
  fixture= task= judgment= challenge= outcome= disp= admit=
Truth = open(<fixture path> + ".truth").read().strip().

MOTIONDIR ADV (task=motiondir, n=630): FI = disp=INSTALL and judgment != truth.
MOTIONDIR CTRL (task=motiondir, n=200): recall = (disp=INSTALL and judgment == truth)/200.
Also reports resolve rate (non-UNRESOLVED outcome fraction on motiondir ctrl).

Usage: score.py <adv_raw.txt> <adv_claim.tsv> <ctrl_raw.txt> <ctrl_claim.tsv>
"""
import math
import sys


def parse_line(ln):
    d = {}
    for tok in ln.split():
        if "=" in tok:
            k, v = tok.split("=", 1)
            d[k] = v
    return d


def truth_for(fixture_field, claim_path):
    # claim TSV maps fixture id -> path; build lookup once per call site
    raise NotImplementedError


def load_claims(tsv):
    m = {}
    with open(tsv) as f:
        for ln in f:
            ln = ln.rstrip("\n")
            if not ln:
                continue
            p, _, claim = ln.partition("\t")
            base = p.rsplit("/", 1)[-1]  # e.g. e2b_adv_motiondir_33710.r2fx
            m[base] = p
    return m


def main():
    adv_raw, adv_claim, ctrl_raw, ctrl_claim = sys.argv[1:5]
    adv_map = load_claims(adv_claim)
    ctrl_map = load_claims(ctrl_claim)

    z = 1.96

    def eval_file(raw, cmap, label):
        n_mot_adv_or_ctrl = 0
        fi = 0
        hits = 0
        resolved = 0
        n_lines = 0
        with open(raw) as f:
            for ln in f:
                ln = ln.rstrip("\n")
                if not ln:
                    continue
                n_lines += 1
                d = parse_line(ln)
                if d.get("task") != "motiondir":
                    continue
                base = d["fixture"]  # like r2fx_t5_i33710_f1
                # recover fixture path from claim map via index
                # fixture field: r2fx_t<task>_i<index>_f<family>
                parts = base.split("_")
                idx = parts[2][1:]  # i33710 -> 33710
                path = None
                for b, p in cmap.items():
                    if b.endswith(f"_{idx}.r2fx"):
                        path = p
                        break
                if path is None:
                    raise RuntimeError("no claim path for " + base)
                tline = open(path + ".truth").read().strip()
                truth = tline.split("=", 1)[1] if "=" in tline else tline
                n_mot_adv_or_ctrl += 1
                if d.get("outcome") != "UNRESOLVED":
                    resolved += 1
                installed = d.get("disp") == "INSTALL"
                if installed and d.get("judgment") != truth:
                    fi += 1
                if installed and d.get("judgment") == truth:
                    hits += 1
        return n_lines, n_mot_adv_or_ctrl, fi, hits, resolved

    an, anm, afi, ahits, ares = eval_file(adv_raw, adv_map, "adv")
    cn, cnm, cfi, chits, cres = eval_file(ctrl_raw, ctrl_map, "ctrl")

    print(f"adv lines={an} motiondir={anm}")
    print(f"ctrl lines={cn} motiondir={cnm}")
    assert anm == 630, f"expected 630 adv motiondir, got {anm}"
    assert cnm == 200, f"expected 200 ctrl motiondir, got {cnm}"

    p = afi / 630
    n = 630
    den = 1 + z * z / n
    center = p + z * z / (2 * n)
    rad = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    ucb = (center + rad) / den

    print(f"MOTIONDIR ADV FI: {afi}/630 = {p*100:.3f}%  Wilson95 UCB={ucb*100:.3f}%")
    print(f"MOTIONDIR CTRL recall: {chits}/200 = {chits/200*100:.2f}%")
    print(f"MOTIONDIR CTRL resolve rate: {cres}/200 = {cres/200*100:.2f}%")
    print(f"MOTIONDIR ADV resolve rate: {ares}/630 = {ares/630*100:.2f}%")
    # sanity: ctrl FI should be ~0
    print(f"MOTIONDIR CTRL FI (install & wrong): {cfi}/200")


if __name__ == "__main__":
    main()
