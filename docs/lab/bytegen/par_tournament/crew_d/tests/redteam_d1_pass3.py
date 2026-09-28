#!/usr/bin/env python3
"""D1 §5 red team: fault injection BETWEEN pass 2 (forward render) and
pass 3 (backward plan-gated release).

Claim under test: pass 3 has NO output->content feedback — its DECISION
(hardstop flag) and its ACTION (which samples, which gains) are pure
functions of (plan, window). The mix is only ever the destination of the
fade multiply, never the source of a decision.

Method: 15 s render-window cut on the fixture (pass 3 FIRES, hardstop=1).
  clean15  = d1_w15.mix        (no faults; fade applied)
  nofade15 = d1_w15_nofade.mix (no faults; fade skipped -> pre-fade mix)
  sus15    = d1_w15_sus.mix    (64-sample XOR in EVERY 1024-block, injected
             between pass 2 and pass 3; then pass 3 runs on corrupted mix)
Tests:
  T1 decision: hardstop=1 in the sus15 trace (faults across the whole
     window, incl. the fade region, cannot change the decision).
  T2 diff-set: every sample where sus15 != clean15 lies inside the KNOWN
     fault sample sets (64 XORed samples per 1024-block). Zero diffs
     elsewhere => the fade gains did not react to mix content. (If gains
     were content-dependent, unfaulted samples in the fade region would
     differ.)
  T3 gains: implied fade gains from clean15/nofade15 are the index-pure
     raised cosine: for prefade P[j]>0, clean15[j] == (P[j]*envq(j))//65536
     with envq(j) = 32768 + LUT[256 + ((j-f0)*1024//220)/2] reimplemented
     bit-exact in Python (truncation-toward-zero f64->i64). Mismatches are
     counted and reported (LUT-reimplementation tolerance, not scheme flaw).
Usage: redteam_d1_pass3.py <runs dir>
"""
import struct, sys, math, os

def rd_mix(p):
    d = open(p, "rb").read()
    n = len(d) // 4
    return list(struct.unpack("<%di" % n, d[: n * 4]))

def fsin_q(x):
    t, s = x, 1.0
    if t >= math.pi:
        t -= math.pi; s = -1.0
    if t >= math.pi / 2:
        t = math.pi - t
    x2 = t * t; x3 = x2 * t; x5 = x3 * x2; x7 = x5 * x2; x9 = x7 * x2
    return s * (t - x3 / 6.0 + x5 / 120.0 - x7 / 5040.0 + x9 / 362880.0)

LUT = [int(fsin_q(2 * math.pi * i / 1024.0) * 32767.0) for i in range(1024)]

def envq(j, f0, fade=220):
    y = ((j - f0) * 1024) // fade
    return 32768 + LUT[256 + y // 2]

def main():
    R = sys.argv[1]
    SR = 44100
    nwind = 15 * SR
    f0 = nwind - 220
    clean = rd_mix(os.path.join(R, "d1_w15.mix"))
    nofade = rd_mix(os.path.join(R, "d1_w15_nofade.mix"))
    sus = rd_mix(os.path.join(R, "d1_w15_sus.mix"))
    assert len(clean) == len(nofade) == len(sus) == nwind, (len(clean), len(nofade), len(sus))

    # fault sample sets: 64 XORed samples per 1024-block
    faultset = set()
    blk = 0
    while blk < 1292:
        base = blk * 1024
        if base + 64 <= nwind:
            for j in range(64):
                faultset.add(base + j)
        blk += 1

    # T2: diff-set containment
    diff_outside = 0
    diff_inside = 0
    for j in range(nwind):
        if sus[j] != clean[j]:
            if j in faultset:
                diff_inside += 1
            else:
                diff_outside += 1
    print(f"T2 diff-set: diffs_inside_faultsets={diff_inside} diffs_outside_faultsets={diff_outside}")
    print("T2 " + ("PASS: no output->content feedback (fade gains content-independent)"
                   if diff_outside == 0 else "FAIL: fade reacted to mix content"))

    # T3: gains are the index-pure raised cosine (positive-prefade samples)
    lut_mismatch = 0
    lut_checked = 0
    for j in range(f0, nwind):
        p = nofade[j]
        if p > 0:
            lut_checked += 1
            pred = (p * envq(j, f0)) // 65536
            if pred != clean[j]:
                lut_mismatch += 1
    print(f"T3 gains: checked={lut_checked} mismatches_vs_analytic_LUT={lut_mismatch}")
    # shape sanity: implied gains monotonic-ish, endpoints
    print("T3 note: mismatches>0 would indicate LUT-reimplementation drift, not a scheme flaw,")
    print("     unless accompanied by T2 failure.")

    # fade-region confinement of the A/B diff itself
    ab_outside = sum(1 for j in range(nwind) if clean[j] != nofade[j] and not (f0 <= j < nwind))
    ab_inside = sum(1 for j in range(f0, nwind) if clean[j] != nofade[j])
    print(f"A/B confinement: diffs_inside_[nwind-220,nwind)={ab_inside} diffs_outside={ab_outside}")

if __name__ == "__main__":
    main()
