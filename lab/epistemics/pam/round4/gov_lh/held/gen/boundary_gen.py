#!/usr/bin/env python3
# boundary_gen.py — adversarial boundary percepts (glue; predicate stays in Zag).
# For each frontier window (rc, rm): 8 CORRECT TMB percepts from exemplar
# 10983 (conf 718, meas 2618) at |Dconf| = rc +/- 1 and |Dmeas| = rm +/- 1,
# both sides of each boundary, both axes. Run through f5_sweep at that window;
# record BLOCKED/ALLOWED per percept.
import os, subprocess

CREW = os.path.expanduser("~/workspace/pam_gov_lh/crew6_held")
SRC = os.path.join(CREW, "src")
GEN = os.path.join(CREW, "gen")
EV = os.path.join(CREW, "evidence")
BIN = os.path.join(SRC, "bin", "f5_sweep")
EX = os.path.expanduser("~/workspace/tnn-lab/senses/pam-rebuild/round2/f5_tightened/exemplars.tsv")

# (rc, rm) representative frontier windows (unique Pareto points)
WINDOWS = [(9, 15), (150, 245), (150, 500), (150, 1000)]
E_CONF, E_MEAS = 718, 2618  # exemplar 10983, the max-conf/min-meas corner

Z64 = "0" * 64

def fixture_line(tag, conf, meas):
    f = [Z64, Z64, tag, "3", f"rt4_TMB-5_{tag}.r24", "2", "1", "RICH",
         str(conf), "0", str(meas), Z64, "RICH", "1", str(conf),
         "DISP=ACCEPT_INSTALL", "DETAIL=det_bnd", "SET=NEAR"]
    return "|".join(f) + "\n"

def classify(rc, rm, line):
    p = os.path.join(GEN, "bnd_one.txt")
    with open(p, "w") as f:
        f.write(line)
    r = subprocess.run([BIN, p, EX, str(rc), str(rm)], capture_output=True)
    assert r.returncode == 0, r.stderr[:200]
    out = r.stdout.decode()
    assert "CORRUPT" not in out, out
    if "\tBLOCKED\t" in out:
        return "BLOCKED"
    assert "\tALLOWED\t" in out, out
    return "ALLOWED"

def main():
    os.makedirs(EV, exist_ok=True)
    rows = []
    i = 0
    for rc, rm in WINDOWS:
        specs = [
            ("conf", "plus", "inside", E_CONF + (rc - 1), E_MEAS),
            ("conf", "plus", "outside", E_CONF + (rc + 1), E_MEAS),
            ("conf", "minus", "inside", E_CONF - (rc - 1), E_MEAS),
            ("conf", "minus", "outside", E_CONF - (rc + 1), E_MEAS),
            ("meas", "plus", "inside", E_CONF, E_MEAS + (rm - 1)),
            ("meas", "plus", "outside", E_CONF, E_MEAS + (rm + 1)),
            ("meas", "minus", "inside", E_CONF, E_MEAS - (rm - 1)),
            ("meas", "minus", "outside", E_CONF, E_MEAS - (rm + 1)),
        ]
        for axis, side, pos, conf, meas in specs:
            i += 1
            tag = f"B{i:04d}"
            verdict = classify(rc, rm, fixture_line(tag, conf, meas))
            rows.append((rc, rm, axis, side, pos, conf, meas, verdict))
            dconf = abs(conf - E_CONF)
            dmeas = abs(meas - E_MEAS)
            print(f"rc={rc:3d} rm={rm:4d} {axis:4s} {side:5s} {pos:7s} conf={conf} meas={meas} (|dc|={dconf},|dm|={dmeas}) -> {verdict}")
    with open(os.path.join(EV, "boundary_percepts.tsv"), "w") as f:
        f.write("rc\trm\taxis\tside\tposition\tconf\tmeas\texemplar_conf\texemplar_meas\tverdict\n")
        for rc, rm, axis, side, pos, conf, meas, verdict in rows:
            f.write(f"{rc}\t{rm}\t{axis}\t{side}\t{pos}\t{conf}\t{meas}\t{E_CONF}\t{E_MEAS}\t{verdict}\n")
    print("wrote evidence/boundary_percepts.tsv")

if __name__ == "__main__":
    main()
