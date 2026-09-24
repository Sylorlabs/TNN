#!/usr/bin/env python3
"""D1 battery adversarial fixture generator (build crew B-D1, 2026-09-24).
Deterministic parameter sweeps, zero RNG. Generates Class A/B/C fixtures
per D1B_DESIGN.md §3. Output: d1_adv_fixtures.txt (pipe-separated).

Columns: id|cls|scene|conf|meas|t
  cls: A (static injection), B (driver-level spoof), C (fusion-layer injection)
  scene: cycles TMB-5 / COL-4 / PTC-4 (TMB-5 = P10-covered, others = blind spots)
  t: hidden true presence bit (world ground truth; 1-c, the lie, for B/C)

The (conf,meas) sweep matches the D-1 probe (d1probe.zag) so Class A/B are
directly comparable: conf=700+10*(j%30), meas=2200+500*((j*7)%10).
Claim c = 1 iff meas>=4000 (gate-derivable); t = 1-c for spoofs (the lie).
"""
import os

DEST = os.path.expanduser("~/workspace/pam_round2/d1_build/d1_adv_fixtures.txt")
SCENES = ["TMB-5", "COL-4", "PTC-4"]

def gen(cls, n, start_id):
    rows = []
    for j in range(n):
        gid = start_id + j
        conf = 700 + 10 * (j % 30)
        meas = 2200 + 500 * ((j * 7) % 10)
        scene = SCENES[j % 3]
        c = 1 if meas >= 4000 else 0
        t = 1 - c  # spoof lies about the binary presence
        rows.append((gid, cls, scene, conf, meas, t))
    return rows

def main():
    rows = []
    rows += gen("A", 120, 0)
    rows += gen("B", 120, 1000)
    rows += gen("C", 60, 2000)
    assert len(rows) == 300
    # determinism self-check: regenerate and compare
    rows2 = gen("A", 120, 0) + gen("B", 120, 1000) + gen("C", 60, 2000)
    assert rows == rows2, "generator not deterministic"
    with open(DEST, "w") as fh:
        for (gid, cls, scene, conf, meas, t) in rows:
            fh.write(f"{gid}|{cls}|{scene}|{conf}|{meas}|{t}\n")
    print(f"wrote {len(rows)} fixtures -> {DEST}")
    # summary
    for cls in "ABC":
        sub = [r for r in rows if r[1] == cls]
        by_scene = {s: sum(1 for r in sub if r[2] == s) for s in SCENES}
        print(f"class {cls}: n={len(sub)} scenes={by_scene}")

if __name__ == "__main__":
    main()
