#!/usr/bin/env python3
"""b4_ablation.py — B4 memory-contract proof.

Contract: final binary (exact-match INSTALL else WITHHOLD).
Ablated: same percepts through a contract-less gate (always INSTALL);
  judgment = the coarse WITHHOLD readout (from the stage-1 stub binary,
  which never installs). Graph-failed fixtures have no coarse judgment;
  installing them counts as a false install.

PASS iff:
  (1) contract changes install/withhold decisions on >=10% of the 275
      attack fixtures, AND
  (2) contract false-installs < ablated false-installs.
"""
import json

def load(p):
    return [json.loads(l) for l in open(p)]

def main():
    harness = load("build/final/harness.jsonl")
    attack = load("build/final/attack.jsonl")
    s1h = load("build/final/s1_harness.jsonl")
    s1a = load("build/final/s1_attack.jsonl")

    contract = {r["path"]: r for r in harness + attack}
    coarse = {r["path"]: r for r in s1h + s1a}

    atk_paths = [r["path"] for r in harness if r["variant"] == "adversarial"]
    atk_paths += [r["path"] for r in attack]
    assert len(atk_paths) == 275, len(atk_paths)

    n_change = 0
    c_fi = 0
    a_fi = 0
    for p in atk_paths:
        c = contract[p]
        s = coarse[p]
        truth = c["truth"]
        # contract decision
        c_inst = (c["disposition"] == "INSTALL")
        if c_inst and c["judgment"] != truth:
            c_fi += 1
        # ablated decision: always INSTALL, judgment = coarse readout
        cj = s.get("judgment")
        if cj is None or cj != truth:
            a_fi += 1
        # decision change: contract did NOT install, ablated does
        if not c_inst:
            n_change += 1

    print("attack fixtures: 275")
    print("decisions changed by contract: %d (%.1f%%)  bar: >=10%%" % (
        n_change, 100 * n_change / 275))
    print("contract false-installs: %d" % c_fi)
    print("ablated  false-installs: %d" % a_fi)
    b4 = (n_change / 275 >= 0.10) and (c_fi < a_fi)
    print("B4:", "PASS" if b4 else "FAIL")

if __name__ == "__main__":
    main()
