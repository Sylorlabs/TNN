#!/usr/bin/env python3
"""PAR_DIVE section 4 prototype: is plan formation parallelizable?
Expands MOTIF-A (fixture t=2.0..5.15) from a compact spec two ways:
  PARALLEL     - each event computed independently from its index
                 (t0 = base + i*step, f = base_f * 2^(semi[i]/12))
  SEQUENTIAL   - carried state: running time t and running scale degree,
                 frequencies via cumulative interval deltas
Byte-diffs the two expansions, and diffs both against the fixture's own
motif lines. Deterministic; no RNG.
"""
import hashlib

BASE_T, STEP, DUR = 2.0, 0.4, 0.35
BASE_F = 440.0
SEMIS = [0, 4, 7, 4, 0, -3, -5, 0]          # absolute semitone offsets
DELTAS = [0, 4, 3, -3, -4, -3, -2, 5]        # cumulative interval deltas
AMP, TIM, GLIDE, VIBHZ, VIBC = 700, 6, "0.0", "5.5", "15"

def line(t, f):
    return f"EVENT {t:.1f} {DUR} {f:.2f} {AMP} {TIM} {GLIDE} {VIBHZ} {VIBC}\n"

def form_parallel():
    # every event an independent pure function of its index: any order works
    return "".join(line(BASE_T + STEP * i, BASE_F * 2 ** (s / 12))
                   for i, s in enumerate(SEMIS))

def form_sequential():
    # carried deterministic state: running time + running degree
    out, t, deg = [], BASE_T, 0
    for d in DELTAS:
        deg += d
        out.append(line(t, BASE_F * 2 ** (deg / 12)))
        t += STEP                       # state carry (redundant: t = BASE_T + i*STEP)
    return "".join(out)

def fixture_motif(path):
    keep = []
    with open(path) as f:
        for ln in f:
            if ln.startswith("EVENT"):
                p = ln.split()
                if 2.0 <= float(p[1]) < 5.2:
                    keep.append(ln)
    return "".join(keep)

par = form_parallel()
seq = form_sequential()
hp, hs = hashlib.sha256(par.encode()).hexdigest(), hashlib.sha256(seq.encode()).hexdigest()
print(f"parallel sha256:   {hp}")
print(f"sequential sha256: {hs}")
print("parallel == sequential (byte-identical):", par == seq)
fix = fixture_motif("/home/hatch/workspace/bytegen/fixture/plan_v1.txt")
print("parallel == fixture motif lines:", par == fix)
if par != fix:
    import difflib
    print("".join(difflib.unified_diff(fix.splitlines(True), par.splitlines(True)))[:2000])
