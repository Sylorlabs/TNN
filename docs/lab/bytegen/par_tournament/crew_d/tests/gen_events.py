#!/usr/bin/env python3
"""Generate the COMPLETE CHOP-3 event list per PREREG_PAR_DIVE.md section 0:
onsets + offsets + release-tail onsets (offset - 150 ms) + predicted vibrato
extrema (every half vibrato period inside each vibrato-bearing event).
Deterministic; no audio read. Usage: gen_events.py <plan> > events_full.txt
"""
import sys

def parse(plan_path):
    events = []
    for line in open(plan_path):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        p = line.split()
        if p[0] == "EVENT" and len(p) >= 9:
            t0, dur = float(p[1]), float(p[2])
            vibhz = float(p[7]) if len(p) > 7 else 0.0
            events.append((t0, dur, vibhz))
    return events

def main():
    evs = parse(sys.argv[1])
    ts = []
    for (t0, dur, vibhz) in evs:
        off = t0 + dur
        ts.append(t0)            # onset
        ts.append(off)           # offset
        ts.append(off - 0.150)   # release-tail onset (150 ms release)
        if vibhz > 0.001:
            half = 0.5 / vibhz
            k = 1
            while k * half < dur:
                ts.append(t0 + k * half)  # predicted vibrato extremum
                k += 1
    ts = sorted(set(round(t, 4) for t in ts if t >= 0))
    for t in ts:
        print(f"{t:.4f}")
    print(f"# total {len(ts)}", file=sys.stderr)

if __name__ == "__main__":
    main()
