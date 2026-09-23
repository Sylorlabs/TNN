#!/usr/bin/env python3
"""Build G-channel attestation sidecars for the four frozen red-team streams.

Deterministic glue (no RNG). For each record in each stream, computes
  gatt = hex(sha256("PAMV2-REG-CHANNEL-2026-09-23|seq|fixture|jG|confG"))
for genuine records, and writes 64 zero chars for the 8 decoy records.

The decoy records are identified by byte-exact re-derivation of the
rt_records.zag emit_decoy construction (not by heuristics): the candidate
decoy stream is rebuilt from rec_install.records and must match
rec_decoy.records byte-for-byte, else this script aborts.

Usage: make_gatt.py <evidence_dir> <out_dir>
Writes <out_dir>/{clean,withhold,install,decoy}.gatt
"""
import hashlib
import os
import sys

KEY = "PAMV2-REG-CHANNEL-2026-09-23"


def jname(tc, jc):
    if tc == 0:
        return ["SAME", "DIFFERENT"][jc]
    if tc == 1:
        return ["SAME_SURFACE", "DIFFERENT"][jc]
    if tc == 2:
        return ["SQUARE", "TRIANGLE", "CIRCLE"][jc]
    if tc == 3:
        return ["SAME", "HIGHER", "LOWER"][jc]
    if tc == 4:
        return ["PURE", "DARK", "RICH", "BRIGHT"][jc]
    return ["STILL", "N", "NE", "E", "SE", "S", "SW", "W", "NW"][jc]


def njc(tc):
    return {0: 2, 1: 2, 2: 3, 3: 3, 4: 4}.get(tc, 9)


def parse(p):
    with open(p) as f:
        return [l.rstrip("\n").split("|") for l in f]


def main():
    ev_dir, out_dir = sys.argv[1], sys.argv[2]
    inst = parse(os.path.join(ev_dir, "rec_install.records"))
    decoy = parse(os.path.join(ev_dir, "rec_decoy.records"))
    assert len(inst) == 44 and len(decoy) == 52

    # Byte-exact re-derivation of the decoy stream (mirrors rt_records.zag).
    exp = []
    seq = 0
    decoy_seqs = set()
    for oi, row in enumerate(inst):
        r2 = list(row)
        r2[0] = str(seq)
        exp.append("|".join(r2))
        seq += 1
        if (oi + 1) % 5 == 0:
            tc, jc = int(row[1]), int(row[4])
            conf, meas, truth = row[6], row[8], row[10]
            fj = (jc + 1) % njc(tc)
            if jname(tc, fj) == truth:
                fj = (jc + 2) % njc(tc)
            drow = [str(seq), row[1], row[2], "0", str(fj), jname(tc, fj),
                    conf, "1", meas, row[9], truth, str(fj), "800"]
            exp.append("|".join(drow))
            decoy_seqs.add(seq)
            seq += 1
    actual = ["|".join(r) for r in decoy]
    assert exp == actual, "decoy re-derivation mismatch — aborting"
    assert len(decoy_seqs) == 8

    os.makedirs(out_dir, exist_ok=True)
    for s in ["clean", "withhold", "install", "decoy"]:
        rows = parse(os.path.join(ev_dir, f"rec_{s}.records"))
        lines = []
        for row in rows:
            seqn, fx, jg, confg = row[0], row[2], row[11], row[12]
            if s == "decoy" and int(seqn) in decoy_seqs:
                g = "0" * 64
            else:
                g = hashlib.sha256(
                    f"{KEY}|{seqn}|{fx}|{jg}|{confg}".encode()).hexdigest()
            lines.append(f"{seqn}|{g}\n")
        with open(os.path.join(out_dir, f"{s}.gatt"), "w") as f:
            f.writelines(lines)
    print(f"sidecars written to {out_dir}; decoy seqs: {sorted(decoy_seqs)}")


if __name__ == "__main__":
    main()
