#!/usr/bin/env python3
"""Verify the self-PAM composition.

Checks (all must pass):
  1. build.py succeeds.
  2. smoke_bin runs twice; stdout byte-identical (cmp clean).
  3. smoke stdout matches the expected 11-step disposition sequence.
  4. stderr digests match across the two runs.
  5. g1probe_bin runs twice; stdout byte-identical; registration values sane
     (name selfpam-fact-gate, disjoint srcs 0/1, valid=1; same-span pair
     admits, different-span pair withholds on the probe spans).
  6. No RNG tokens in the Zag decision sources.

Python here only moves files and checks bytes — it never decides a verdict.
"""
import hashlib
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, "build")

EXPECTED = [
    (1, "PROVISIONAL_INSTALL"),
    (2, "PERMANENT_INSTALL"),
    (3, "CORROBORATED"),
    (4, "CHALLENGER_PROV"),
    (5, "REVISED_INSTALL"),
    (6, "CONFLICT_WITHHELD"),
    (7, "NEGATIVE_EVIDENCE"),
    (8, "SUPPRESSED"),
    (9, "WITHHELD"),
    (10, "WITHHELD"),
    (11, "WITHHELD"),
]

failures = []


def check(name, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + name + (f" ({detail})" if detail and not cond else ""))
    if not cond:
        failures.append(name)


def run(path):
    r = subprocess.run([path], capture_output=True)
    return r.returncode, r.stdout, r.stderr


def main():
    r = subprocess.run([sys.executable, os.path.join(HERE, "build.py")],
                       capture_output=True, text=True)
    check("build.py succeeds", r.returncode == 0, r.stderr[-500:] + r.stdout[-500:])

    smoke = os.path.join(BUILD, "smoke_bin")
    rc1, out1, err1 = run(smoke)
    rc2, out2, err2 = run(smoke)
    check("smoke rc==0 both runs", rc1 == 0 and rc2 == 0, f"rc={rc1},{rc2}")
    check("smoke stdout byte-identical (cmp clean)", out1 == out2,
          f"len {len(out1)} vs {len(out2)}")
    check("smoke stderr byte-identical", err1 == err2)

    lines = out1.decode().strip().split("\n")
    got = []
    ok_shape = True
    for ln in lines:
        m = re.fullmatch(r"(\d+)\|([A-Z_]+)", ln.strip())
        if not m:
            ok_shape = False
            break
        got.append((int(m.group(1)), m.group(2)))
    check("smoke output shape 11 lines", ok_shape and len(got) == 11, f"{len(got)} lines")
    check("smoke disposition sequence as expected", got == EXPECTED,
          f"got={got}")

    m1 = re.fullmatch(rb"steps=11 digest=([0-9a-f]{64})\n", err1.strip() + b"\n")
    check("smoke stderr digest well-formed", m1 is not None, err1[:120].decode(errors="replace"))
    if m1:
        stream = "".join(n + "\n" for _, n in EXPECTED).encode()
        expect_hex = hashlib.sha256(stream).hexdigest()
        check("smoke digest matches sha256 of disposition stream",
              m1.group(1).decode() == expect_hex)

    probe = os.path.join(BUILD, "g1probe_bin")
    prc1, pout1, _ = run(probe)
    prc2, pout2, _ = run(probe)
    check("g1probe rc==0", prc1 == 0 and prc2 == 0)
    check("g1probe stdout byte-identical", pout1 == pout2)
    pt = pout1.decode()
    check("g1probe name=selfpam-fact-gate", "name=selfpam-fact-gate" in pt, pt[:200])
    check("g1probe disjoint srcs", "formation_src=0\ngate_src=1" in pt, pt[:200])
    check("g1probe valid=1", "\nvalid=1\n" in pt, pt[:200])
    check("g1probe same-span admits", "judge_same_span jf=" in pt and " withhold=0\njudge_diff_span" in pt, pt)
    check("g1probe diff-span withholds", pt.rstrip().endswith("withhold=1"), pt[-120:])

    rng_hits = []
    for fn in ["admit_claim.zag", "codec.zag", "corr.zag", "g1_candidate.zag",
               "main_smoke.zag", "main_g1probe.zag"]:
        src = open(os.path.join(HERE, fn)).read()
        for tok in ["rand(", "Random", "srand", "Math.random", "random()"]:
            if tok in src:
                rng_hits.append(f"{fn}:{tok}")
    check("no RNG tokens in decision sources", not rng_hits, ",".join(rng_hits))

    if failures:
        print(f"\n{len(failures)} FAILURES: {failures}")
        sys.exit(1)
    print("\nALL CHECKS PASS")


if __name__ == "__main__":
    main()
