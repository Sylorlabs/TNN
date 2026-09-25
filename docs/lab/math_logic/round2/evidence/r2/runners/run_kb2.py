#!/usr/bin/env python3
"""KB2 contrast battery (R1 holdover).
R1 manifest unrecoverable (searched prereg, verdict, build reports, scripts).
R2 construction (documented deviation): 20 pairs.
  Pairs 1-10:  (B2 DERIVED solvable, OPEN open)   B2_01-06,B2_08-12 x OPEN_01-10
  Pairs 11-20: (B3 DERIVED solvable, OPEN open)   B3_01-10 x OPEN_01-10
DUAL bar: conf(solvable) > conf(open) on >=18/20.
ONE bar:  conf(solvable)>0 AND conf(open)=0 on every pair.
(Also measured for HYB, REF-FIRST, NFEE, LEARN-FORM for the record.)
"""
import os, subprocess, re, json

BASE = "/home/hatch/workspace/tnn-lab/math_logic"
BIN = "/home/hatch/workspace/math_r2/eval/bin"
EV = "/home/hatch/workspace/math_r2/eval"
OUT = f"{EV}/out"

R1 = "/home/hatch/workspace/math_r2/r1/problems"
SOLVABLE = ([f"{R1}/b2/B2_{i:02d}.form" for i in [1,2,3,4,5,6,8,9,10,11]] +
            [f"{R1}/b3/B3_{i:02d}.form" for i in range(1, 11)])
OPEN = [f"{BASE}/problems/open/OPEN_{i:02d}.form" for i in range(1, 11)] * 2  # 20 opens (OPEN_01-10 reused)
PAIRS = list(zip(SOLVABLE, OPEN))  # 20 pairs
assert len(PAIRS) == 20, len(PAIRS)

ENGINES = {
    "ONE-R1": f"{BIN}/one_bin", "DUAL-R1": f"{BIN}/dual_bin",
    "HYB": f"{BIN}/hyb_bin", "REF-FIRST": f"{BIN}/reffirst_bin",
    "NFEE": f"{BIN}/nfee_bin", "LEARN-FORM": f"{BIN}/one_bin",
}

def conf_of(outp):
    with open(outp) as f: txt = f.read()
    m = re.search(r"^CONFIDENCE:\s*(\S+)", txt, re.M)
    v = re.search(r"^VERDICT:\s*(\S+)", txt, re.M)
    return (int(m.group(1)) if m else -1, v.group(1) if v else "?")

def main():
    res = {}
    for ename, binary in ENGINES.items():
        print(f"=== KB2 {ename} ===", flush=True)
        wins = 0; one_pass = True; details = []
        for i, (sprob, oprob) in enumerate(PAIRS, 1):
            # solvable
            so = f"{OUT}/KB2_{ename}_pair{i:02d}_solv.out"
            subprocess.run([binary, sprob, so], cwd=BASE, capture_output=True, timeout=120)
            # open
            oo = f"{OUT}/KB2_{ename}_pair{i:02d}_open.out"
            subprocess.run([binary, oprob, oo], cwd=BASE, capture_output=True, timeout=120)
            sc, sv = conf_of(so); oc, ov = conf_of(oo)
            dual_win = sc > oc
            one_ok = (sc > 0 and oc == 0)
            if dual_win: wins += 1
            if not one_ok: one_pass = False
            details.append({"pair": i, "solv_conf": sc, "solv_verdict": sv,
                            "open_conf": oc, "open_verdict": ov,
                            "dual_win": dual_win, "one_ok": one_ok})
        res[ename] = {"dual_wins": wins, "dual_bar": wins >= 18,
                      "one_allpass": one_pass, "details": details}
        print(f"  DUAL-bar: {wins}/20 (need >=18): {'PASS' if wins>=18 else 'FAIL'}", flush=True)
        print(f"  ONE-bar: allpass={one_pass}: {'PASS' if one_pass else 'FAIL'}", flush=True)
    with open(f"{EV}/results_kb2.json", "w") as f:
        json.dump(res, f, indent=1)

if __name__ == "__main__":
    main()
