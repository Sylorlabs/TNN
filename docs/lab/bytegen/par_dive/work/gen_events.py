#!/usr/bin/env python3
"""Build the COMPLETE plan-scripted transient event list from plan_v1.txt.
Independent construction for PAR_DIVE §0(a) re-verification.
Events: note onsets, note offsets, release onsets (offset - min(150ms, dur/2)),
vibrato-cycle extrema (tr=(2k+1)/(4*fv) for fv>0), bed fade edges.
"""
import sys
plan = sys.argv[1]
evs = []
with open(plan) as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        p = line.split()
        if p[0] == 'BED':
            t0, t1 = float(p[1]), float(p[2])
            evs += [t0, t1]  # 25 ms raised-cosine edge fades
        elif p[0] == 'EVENT':
            t0, dur = float(p[1]), float(p[2])
            vib_hz = float(p[7])
            off = t0 + dur
            rel = min(0.150, dur / 2.0)
            evs += [t0, off, off - rel]
            if vib_hz > 0.001:
                k = 0
                while True:
                    tr = (2 * k + 1) / (4.0 * vib_hz)
                    if tr >= dur:
                        break
                    evs.append(t0 + tr)
                    k += 1
evs = sorted(evs)
print(f"total timestamps: {len(evs)}", file=sys.stderr)
for e in evs:
    print(f"{e:.6f}")
