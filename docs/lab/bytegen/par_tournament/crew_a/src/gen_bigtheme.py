#!/usr/bin/env python3
"""gen_bigtheme.py — deterministic large theme for A-fmt (no RNG).
4000 directives: STRUCT+INST (exercises INST path), then EVENTs with every
7th a RESPOND (nominal lies cycle 880/460/220). Spans 600 s.
Usage: gen_bigtheme.py <out> [n_directives]
"""
import sys

out = sys.argv[1]
N = int(sys.argv[2]) if len(sys.argv) > 2 else 4000

L = []
L.append("# A-fmt big theme: deterministic, no RNG")
L.append("SR 44100")
L.append("DUR_S 600")
L.append("BED 0.0 600.0 110 250")
L.append("STRUCT motifA NOTES 440.00 554.37 659.25 554.37 440.00 369.99 329.63 440.00 STEP 0.4 DUR 0.35 AMP 700 TIMBRE 6 GLIDE 0.0 VIB 5.5 15")
L.append("INST motifA 2.0")
L.append("INST motifA 24.0")

def freq(i):
    semis = (i * 7) % 24
    return 220.0 * (2.0 ** (semis / 12.0))

noms = [880.0, 460.0, 220.0]
ri = 0
for i in range(N):
    t0 = 30.0 + i * 0.14
    if i % 7 == 6:
        w0 = t0 - 2.0; w1 = t0 - 1.0
        nom = noms[ri % 3]; ri += 1
        L.append(f"RESPOND {t0:.2f} 1.0 {w0:.2f} {w1:.2f} 700 6 {nom:.1f}")
    else:
        f = freq(i)
        L.append(f"EVENT {t0:.2f} 0.35 {f:.2f} 700 6 0.0 5.5 15")

with open(out, "w") as fh:
    fh.write("\n".join(L) + "\n")
print(f"wrote {out}: {len(L)} lines, {N} generated directives", file=sys.stderr)
