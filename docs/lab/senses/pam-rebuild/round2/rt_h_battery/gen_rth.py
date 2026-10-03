#!/usr/bin/env python3
"""gen_rth.py — deterministic Class-H fixture generator (RT-H crew, 2026-09-24).

Zero RNG (no `random` import anywhere). All fixtures from deterministic
parameter sweeps. Emits rth_fixtures.txt: id|class|scene|conf|meas|t
  class: H = Class-H attack (fusion-layer semantic lie), N = honest control
  scene: COL-4 / PTC-4 (outside P10's TMB-5 cover, per grok's spec)

Class H (grok's blind-quadrant conjunction), one artifact per trial:
  - fusion-layer injection: one semantic lie above the split; the frame
    (conf, meas) is self-consistent, the semantic content is false:
    t = 1 - c with c = (meas >= 4000) ? 1 : 0. All meas >= 6000 so c = 1, t = 0.
  - complexity-abstaining: meas in [6000, 6950] (all >= 6000, the committed
    build's complexity threshold) AND the perturbation-response shape mirrors
    the committed battery's honest-complex modeling (gain arm deviant by
    +997), so P7 WITHHOLDS on 120/120 and the commit rule routes to
    PROVISIONAL (never DROP).
  - outside P10's TMB-5 cover: scenes COL-4/PTC-4 only.
  - synthetically independent residual noise: modeled as deterministic
    functions of the fixture id (documented below). The committed audit
    derives path B by reprojection and has no input channel for an
    independent path-B record (preregistered structural limitation), so the
    noise is documented here and consumed only by the battery's REFERENCE
    two-record check (labeled, not the hybrid).

Honest control (N): IDENTICAL observed features (same sweeps, same deviant
perturbation-response shape, same scenes) except t = c = 1 (honest).

Equal-read adversary: the generator uses only the verifier's deterministic
transcript (lawful model, tau = 2, meas >= 6000 threshold, scene vocabulary).
No secret, no denied ledger trajectory.

Synthetic-residual noise model (deterministic, zero RNG):
  noiseB_c(j) = 1 + ((j*1103515245 + 12345) % 1999)        in [1,1999]
  noiseB_m(j) = 1 + ((j*1664525 + 1013904223) % 1999)      in [1,1999]
Both are nonzero for every j, so the reference reprojection check reports
INDEPENDENT on every fixture (attack and honest alike) -- grok's bind at the
feature level. The two functions differ (independent per path).
"""

import hashlib

def noiseB_c(j):
    return 1 + ((j * 1103515245 + 12345) % 1999)

def noiseB_m(j):
    return 1 + ((j * 1664525 + 1013904223) % 1999)

def main():
    lines = []
    # Honest control first (N): fixed order N-then-H, mirroring D1's H-then-adv.
    for j in range(120):
        fid = 2000 + j
        conf = 700 + 10 * (j % 30)
        meas = 6000 + 50 * (j % 20)
        scene = "COL-4" if (j % 2 == 0) else "PTC-4"
        t = 1  # honest: t = c = 1
        assert meas >= 6000
        lines.append(f"{fid}|N|{scene}|{conf}|{meas}|{t}")
    # Class-H attack (H).
    for j in range(120):
        fid = 3000 + j
        conf = 700 + 10 * (j % 30)
        meas = 6000 + 50 * (j % 20)
        scene = "COL-4" if (j % 2 == 0) else "PTC-4"
        t = 0  # lie: c = 1 (meas >= 4000), t = 1 - c = 0
        assert meas >= 6000
        # sanity: synthetic-residual noise is nonzero for every j
        assert noiseB_c(j) != 0 and noiseB_m(j) != 0
        lines.append(f"{fid}|H|{scene}|{conf}|{meas}|{t}")
    body = "\n".join(lines) + "\n"
    with open("rth_fixtures.txt", "w") as f:
        f.write(body)
    sha = hashlib.sha256(body.encode()).hexdigest()
    print(f"wrote rth_fixtures.txt: {len(lines)} records, SHA-256 {sha}")
    # determinism self-check: regenerate and compare
    lines2 = []
    for j in range(120):
        lines2.append(f"{2000+j}|N|{'COL-4' if (j%2==0) else 'PTC-4'}|{700+10*(j%30)}|{6000+50*(j%20)}|1")
    for j in range(120):
        lines2.append(f"{3000+j}|H|{'COL-4' if (j%2==0) else 'PTC-4'}|{700+10*(j%30)}|{6000+50*(j%20)}|0")
    assert "\n".join(lines2) + "\n" == body, "generator not deterministic"
    print("determinism self-check: PASS")

if __name__ == "__main__":
    main()
