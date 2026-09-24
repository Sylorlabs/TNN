#!/usr/bin/env python3
"""D8 TARGET_MISMATCH_PROBE certification (H2 run-2).

Runs the pure-Zag target-mismatch scorer over the hand-checked fixture suite,
each fixture twice, asserting:
  1. byte-identical output across the 2 runs (KB-DET), and
  2. exact match to the hand-computed expectation (prereg D8: "(v) computation
     matches hand-checked fixtures exactly").

Hand-checked expectations (SCORER_SPEC.md):
  f1_planted    -> SCORER,(v),1,CHASE,0,SHAM,0,MISMATCHES,1
  f2_all_match  -> SCORER,(v),0,CHASE,0,SHAM,0,MISMATCHES,0
  f3_no_target  -> SCORER,(v),0,CHASE,0,SHAM,0,MISMATCHES,0
  f4_chase      -> SCORER,(v),0,CHASE,1,SHAM,0,MISMATCHES,1
  f5_sham       -> SCORER,(v),0,CHASE,0,SHAM,1,MISMATCHES,1
  f6_no_windows -> SCORER,(v),0,CHASE,0,SHAM,0,MISMATCHES,1
  f7_empty_basis-> SCORER,(v),0,CHASE,0,SHAM,0,MISMATCHES,0
"""
import os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCORER = os.path.join(HERE, "scorer_bin")
FIX = os.path.join(HERE, "fixtures_d8")

EXPECTED = {
    "f1_planted":    "SCORER,(v),1,CHASE,0,SHAM,0,MISMATCHES,1",
    "f2_all_match":  "SCORER,(v),0,CHASE,0,SHAM,0,MISMATCHES,0",
    "f3_no_target":  "SCORER,(v),0,CHASE,0,SHAM,0,MISMATCHES,0",
    "f4_chase":      "SCORER,(v),0,CHASE,1,SHAM,0,MISMATCHES,1",
    "f5_sham":       "SCORER,(v),0,CHASE,0,SHAM,1,MISMATCHES,1",
    "f6_no_windows": "SCORER,(v),0,CHASE,0,SHAM,0,MISMATCHES,1",
    "f7_empty_basis":"SCORER,(v),0,CHASE,0,SHAM,0,MISMATCHES,0",
}

def main():
    assert os.path.exists(SCORER), f"scorer binary missing: {SCORER}"
    all_ok = True
    for name, exp in EXPECTED.items():
        path = os.path.join(FIX, name + ".txt")
        with open(path) as f:
            data = f.read()
        outs = []
        for _ in range(2):
            r = subprocess.run([SCORER], input=data, capture_output=True, text=True)
            if r.returncode != 0:
                print(f"{name}: SCORER FAILED rc={r.returncode}: {r.stderr[:200]}")
                all_ok = False
                break
            outs.append(r.stdout.strip())
        else:
            det = outs[0] == outs[1]
            match = outs[0] == exp
            ok = det and match
            all_ok = all_ok and ok
            print(f"{name}: {'PASS' if ok else 'FAIL'} "
                  f"(det={'OK' if det else 'FAIL'}, got={outs[0]!r}, exp={exp!r})")
    print(f"D8 {'PASS' if all_ok else 'FAIL'}: scorer certified"
          if all_ok else "D8 FAIL: scorer NOT certified")
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())
