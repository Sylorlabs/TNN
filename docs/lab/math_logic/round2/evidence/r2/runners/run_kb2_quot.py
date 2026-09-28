#!/usr/bin/env python3
"""KB2 contrast battery for QUOT.
Same 20-pair construction as run_kb2.py (R1 holdover, documented construction).
QUOT emits no numeric CONFIDENCE line; per SPEC_QUOT §4, "confidence is
non-zero iff DERIVED". Mapping: conf = 1 if verdict==DERIVED else 0.
Bar: DUAL-style discrimination conf(solvable) > conf(open) on >=18/20
(same bar used for every other engine's PB2 in the round-2 eval).
"""
import os, subprocess, re, json

BASE = "/home/hatch/workspace/tnn-lab/math_logic"
BIN = "/home/hatch/workspace/math_r2/eval/bin/quot_bin"
OUT = "/home/hatch/workspace/math_r2/eval/out_quot"
os.makedirs(OUT, exist_ok=True)

R1 = "/home/hatch/workspace/math_r2/r1/problems"
SOLVABLE = ([f"{R1}/b2/B2_{i:02d}.form" for i in [1,2,3,4,5,6,8,9,10,11]] +
            [f"{R1}/b3/B3_{i:02d}.form" for i in range(1, 11)])
OPEN = [f"{BASE}/problems/open/OPEN_{i:02d}.form" for i in range(1, 11)] * 2
PAIRS = list(zip(SOLVABLE, OPEN))
assert len(PAIRS) == 20, len(PAIRS)

def verdict_of(outp):
    if not os.path.exists(outp):
        return "MISSING"
    with open(outp) as f: txt = f.read()
    m = re.search(r"^verdict:\s*(\S+)", txt, re.M)
    return m.group(1) if m else "?"

def main():
    wins = 0; details = []
    for i, (sprob, oprob) in enumerate(PAIRS, 1):
        so = f"{OUT}/KB2_QUOT_pair{i:02d}_solv.out"
        rs = subprocess.run([BIN, sprob, so], cwd=BASE, capture_output=True, timeout=120,
                            start_new_session=True)
        oo = f"{OUT}/KB2_QUOT_pair{i:02d}_open.out"
        ro = subprocess.run([BIN, oprob, oo], cwd=BASE, capture_output=True, timeout=120,
                            start_new_session=True)
        sv = verdict_of(so); ov = verdict_of(oo)
        sc = 1 if sv == "DERIVED" else 0
        oc = 1 if ov == "DERIVED" else 0
        win = sc > oc
        if win: wins += 1
        details.append({"pair": i, "solv_verdict": sv, "solv_conf": sc,
                        "open_verdict": ov, "open_conf": oc, "win": win})
        print(f"  pair {i:02d}: solv={sv}(c={sc}) open={ov}(c={oc}) -> {'win' if win else 'LOSS'}", flush=True)
    res = {"engine": "QUOT", "mapping": "conf=1 iff verdict DERIVED (SPEC_QUOT §4)",
           "dual_wins": wins, "dual_bar": wins >= 18, "details": details}
    print(f"KB2 QUOT: {wins}/20 (need >=18): {'PASS' if wins>=18 else 'FAIL'}")
    with open("/home/hatch/workspace/math_r2/eval/results_kb2_quot.json", "w") as f:
        json.dump(res, f, indent=1)

if __name__ == "__main__":
    main()
