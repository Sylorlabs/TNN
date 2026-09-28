#!/usr/bin/env python3
"""Analyzer-level re-verification of D1's 15 s window-cut A/B pair
(d1_boundary_fade.wav vs d1_boundary_nofade.wav), rendered from
plans/plan_excerpt_d1.txt at a 15 s render window.

Checks (all at the sample level, no listening):
  E1 end transient: |last sample| and max |sample| over the final 220
     samples for fade vs nofade (nofade must show the hard-stop transient,
     fade must end ~0).
  E2 confinement: diffs(fade, nofade) lie entirely within [n-220, n);
     count them (dive: 219-214, the shortfall is integer truncation).
  E3 end slope: mean |d| over the last 220 samples (fade << nofade).
  E4 CHOP-1 style: count single-sample steps >= 0.35 FS anywhere in the
     last 1 s of each file (the dive's finding: frozen CHOP-1 does not
     discriminate sub-0.35 end-steps; the extension is proven here).
Usage: verify_d1_edgeAB.py <fade.wav> <nofade.wav>
"""
import struct, sys

def rd_wav(p):
    d = open(p, "rb").read()
    raw = d[44:]
    n = len(raw) // 2
    return list(struct.unpack("<%dh" % n, raw[: n * 2]))

def main():
    fade = rd_wav(sys.argv[1])
    nofade = rd_wav(sys.argv[2])
    assert len(fade) == len(nofade), (len(fade), len(nofade))
    n = len(fade)
    f0 = n - 220
    FS = 32768.0

    print(f"samples={n} ({n/44100:.1f}s)")
    # E1
    print(f"E1 end transient: fade |last|={abs(fade[-1])/FS:.4f} FS, "
          f"max|last220|={max(abs(x) for x in fade[f0:])/FS:.4f} FS")
    print(f"E1 end transient: nofade |last|={abs(nofade[-1])/FS:.4f} FS, "
          f"max|last220|={max(abs(x) for x in nofade[f0:])/FS:.4f} FS")
    # E2
    diffs = [j for j in range(n) if fade[j] != nofade[j]]
    outside = [j for j in diffs if j < f0]
    print(f"E2 confinement: total_diffs={len(diffs)} diffs_outside_[n-220,n)={len(outside)} "
          f"(expect 0 outside)")
    # E3
    def meanslope(x):
        return sum(abs(x[j+1]-x[j]) for j in range(f0, n-1)) / (219.0 * FS)
    print(f"E3 mean|d| last220: fade={meanslope(fade):.5f} FS  nofade={meanslope(nofade):.5f} FS")
    # E4
    def chop1(x):
        return sum(1 for j in range(n-44100, n-1) if abs(x[j+1]-x[j]) >= 0.35*FS)
    print(f"E4 CHOP-1(0.35FS) steps in last 1s: fade={chop1(fade)} nofade={chop1(nofade)}")

if __name__ == "__main__":
    main()
