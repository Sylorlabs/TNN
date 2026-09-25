#!/usr/bin/env python3
"""Independent Python resimulation of the F32 RSW Zag trainer.
Reads the frozen features.tsv, implements ideas/grok_forks.md Fork 1 exactly,
and compares final ledger state + per-row emitted C against the Zag outputs.
Any divergence = trainer bug. Exit 0 iff fully identical.
"""
import sys

FEAT = "/home/hatch/workspace/tnn-lab/deliberation_depth/monotonicity/training/features/features.tsv"
T = "/home/hatch/workspace/tnn-lab/deliberation_depth/monotonicity/training/fork_round/f32_rsw"

def tdiv(a, b):
    if b <= 0:
        return 0
    if a >= 0:
        return a // b
    return -((-a) // b)

def rho(k, n):
    return tdiv((k + 1) * 1000, n + 2)

def dslot(d):
    return {1: 0, 2: 1, 4: 2, 8: 3, 16: 4, 32: 5, 64: 6}.get(d, -1)

def key_of(f1, f5, f5p, d, dp, first):
    m = tdiv(f1, 200)
    m = min(4, max(0, m))
    my = f5
    if not first:
        df2 = (d - dp) * 1000 // 64
        if df2 < 1:
            df2 = 1
        num = max(0, f5 - f5p)
        my = tdiv(num * 1000, df2)
    my = min(1000, max(0, my))
    yld = tdiv(my, 400)
    yld = min(2, max(0, yld))
    return m * 3 + yld, m, yld

def main():
    # state
    cells = {(r, j): [0, 0] for r in range(15) for j in range(7)}  # n,k
    trans = {(r, j): [0]*6 for r in range(15) for j in range(7)}    # nstay,scstay,nall,scall,kall,kstay
    regime = [0]*15
    ghist = [[-1, -1, -1] for _ in range(15)]
    nswitch = [0]*15
    prev_id = None
    f5p = dp = f8p = 0
    cprev = cstar = 0
    relprev = correctprev = 0
    trace = []  # (id, depth, m, yld, regime, C, rel, correct)

    def pooled_n(r):
        return sum(cells[(r, j)][0] for j in range(7))

    def gamma(r):
        kd = sum(cells[(r, j)][1] for j in range(4, 7)); nd = sum(cells[(r, j)][0] for j in range(4, 7))
        ks = sum(cells[(r, j)][1] for j in range(0, 2)); ns = sum(cells[(r, j)][0] for j in range(0, 2))
        return rho(kd, nd) - rho(ks, ns)

    def emit(r, j, first, f3, f8):
        nonlocal cstar
        if first:
            cstar = rho(cells[(r, 0)][1], cells[(r, 0)][0])
            c = cstar
            return max(1, min(999, c))
        track = regime[r] == 1
        beta = 4 if track else 2
        s = 0
        for t in range(1, j + 1):
            nstay, scstay, nall, scall, kall, kstay = trans[(r, t)]
            delta = 0
            if nstay > 0 and nall > 0:
                e = tdiv(scstay, nstay) - tdiv(scall, nall)
                da = tdiv(kstay*1000, nstay) - tdiv(kall*1000, nall)
                delta = da - e - beta
            if track:
                s += delta
            elif delta < 0:
                s += delta
        if track:
            ms = min(s, 0)
            c = rho(cells[(r, j)][1], cells[(r, j)][0]) + ms
        else:
            c = cstar + s
        c = max(1, min(999, c))
        if f3 > 0 or f8 > f8p:
            c = min(c, cprev - 1)
        return c

    nrows = 0
    with open(FEAT) as f:
        for line in f:
            line = line.rstrip("\n").rstrip("\r")
            if not line:
                continue
            cols = line.split("\t")
            if int(cols[2]) == 1:
                continue
            iid, depth = cols[0], int(cols[3])
            j = dslot(depth)
            if j < 0:
                continue
            first = (prev_id is None) or (iid != prev_id)
            if first:
                relprev = correctprev = 0
                prev_id = iid
            f1, f3, f5, f8 = int(cols[7]), int(cols[9]), int(cols[11]), int(cols[14])
            rel = int(cols[5])
            correct = -1 if cols[6] == 'A' else int(cols[6])
            r, m, yld = key_of(f1, f5, f5p, depth, dp, first)
            reg0 = regime[r]
            c = emit(r, j, first, f3, f8)
            trace.append((iid, depth, m, yld, reg0, c, rel, correct))
            cnow = 1 if correct == 1 else 0
            if rel == 1:
                cells[(r, j)][0] += 1
                if cnow == 1:
                    cells[(r, j)][1] += 1
            if j >= 1 and relprev == 1:
                tr = trans[(r, j)]
                tr[2] += 1; tr[3] += cprev; tr[4] += correctprev
                if rel == 1:
                    tr[0] += 1; tr[1] += cprev; tr[5] += cnow
            if pooled_n(r) >= 32:
                g = gamma(r)
                ghist[r] = [ghist[r][1], ghist[r][2], g]
                if reg0 == 0:
                    if g >= 100 and all(x >= 0 for x in ghist[r]):
                        regime[r] = 1; nswitch[r] += 1
                elif g <= 60:
                    regime[r] = 0; nswitch[r] += 1
            f5p, dp, f8p = f5, depth, f8
            cprev = c
            relprev, correctprev = rel, cnow
            nrows += 1

    # compare state file
    errs = 0
    with open(f"{T}/params/f32_state_a.tsv") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            p = line.split(" ")
            if p[0] == "C":
                r, j, n, k = int(p[1]), int(p[2]), int(p[3]), int(p[4])
                if cells[(r, j)] != [n, k]:
                    print(f"C MISMATCH r={r} j={j}: py={cells[(r,j)]} zag={[n,k]}"); errs += 1
            elif p[0] == "T":
                r, j = int(p[1]), int(p[2]); vals = list(map(int, p[3:9]))
                if trans[(r, j)] != vals:
                    print(f"T MISMATCH r={r} j={j}: py={trans[(r,j)]} zag={vals}"); errs += 1
            elif p[0] == "Z":
                r = int(p[1]); vals = list(map(int, p[2:7]))
                py = [regime[r], nswitch[r]] + ghist[r]
                if py != vals:
                    print(f"Z MISMATCH r={r}: py={py} zag={vals}"); errs += 1
    # compare trace
    with open(f"{T}/params/f32_trace_a.tsv") as f:
        ztrace = [l.rstrip("\n").split("\t") for l in f if l.strip()]
    if len(ztrace) != len(trace):
        print(f"TRACE LEN MISMATCH py={len(trace)} zag={len(ztrace)}"); errs += 1
    else:
        for i, (py, z) in enumerate(zip(trace, ztrace)):
            zrow = (z[0], int(z[1]), int(z[2]), int(z[3]), int(z[4]), int(z[5]), int(z[6]), int(z[7]))
            if py != zrow:
                print(f"TRACE MISMATCH row {i}: py={py} zag={zrow}"); errs += 1
                if errs > 5:
                    break
    print(f"rows={nrows} errs={errs}")
    print("RESIM-IDENTICAL" if errs == 0 else "RESIM-DIVERGED")
    return 0 if errs == 0 else 1

sys.exit(main())
