#!/usr/bin/env python3
"""gen_launder.py — W7 frozen laundering fixture set (PREREG_W7.md, frozen).

Deterministic (zero RNG). 200 entries:
  ids 0..99:   LAUNDERED (true GEN, claimed EXT)
  ids 100..199: GENUINE  (true EXT, claimed EXT)
Signals (0..1000 unless noted), counter-indexed deterministic formulas:
  sig_c: content similarity to frozen GEN profile.
         laundered: 550 + (id*37 mod 401)  -> 550..950
         genuine:    50 + (id*53 mod 601)  -> 50..650
  sig_b: behavioral anomaly (bulk arrival, zero edit history).
         laundered: 700 + (id*29 mod 251)  -> 700..950
         genuine:    50 + (id*41 mod 401)  -> 50..450
  sig_a: external attestation count (0..4).
         laundered: 0
         genuine:   1 + (id mod 3)         -> 1..3
Writes:
  launder_signals.txt: id|sig_c|sig_b|sig_a   (ONLY file the instrument reads)
  launder_truth.txt:   id|true_origin|claimed_label (scorer only)
"""
import hashlib, os

HERE = os.path.dirname(os.path.abspath(__file__))

def main():
    sig_lines, truth_lines = [], []
    for i in range(200):
        if i < 100:
            origin, claimed = "GEN", "EXT"
            sig_c = 550 + (i * 37 % 401)
            sig_b = 700 + (i * 29 % 251)
            sig_a = 0
        else:
            origin, claimed = "EXT", "EXT"
            sig_c = 50 + (i * 53 % 601)
            sig_b = 50 + (i * 41 % 401)
            sig_a = 1 + (i % 3)
        assert 0 <= sig_c <= 1000 and 0 <= sig_b <= 1000 and 0 <= sig_a <= 4
        sig_lines.append(f"{i}|{sig_c}|{sig_b}|{sig_a}")
        truth_lines.append(f"{i}|{origin}|{claimed}")
    sp = os.path.join(HERE, "launder_signals.txt")
    tp = os.path.join(HERE, "launder_truth.txt")
    open(sp, "w").write("\n".join(sig_lines) + "\n")
    open(tp, "w").write("\n".join(truth_lines) + "\n")
    for p in (sp, tp):
        h = hashlib.sha256(open(p, "rb").read()).hexdigest()
        print(f"{os.path.basename(p)}: {len(open(p).readlines())} rows sha256={h}")

if __name__ == "__main__":
    main()
