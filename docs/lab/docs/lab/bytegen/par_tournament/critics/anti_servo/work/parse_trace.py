#!/usr/bin/env python3
"""Parse render_c trace logs: adapts, vetoes, holds, dsum(FS), engagement, adapt blocks."""
import sys, re, math

def parse(path):
    adapts = vetoes = holds = n = 0
    dsum = 0.0
    gprev = None
    rgprev = None
    adapt_blocks = []   # (rg, rb, g, m, T)
    gate_opens = []
    latches = []
    for line in open(path, errors="replace"):
        m = re.match(r"C rg=(\d+) rb=(\d+) g=(\d+) m=(\d+) T=(\d+) st=(\d+)", line)
        if m:
            rg, rb, g, mm, T, st = map(int, m.groups())
            n += 1
            if st == 1:
                adapts += 1
                adapt_blocks.append((rg, rb, g, mm, T))
            elif st == 2:
                vetoes += 1
            elif st == 3:
                holds += 1
            if rgprev is not None and rg != rgprev:
                gprev = None  # region-boundary unity reset: not servo movement
            rgprev = rg
            if gprev is not None and g != gprev:
                dsum += abs(g - gprev) / 65536.0
            gprev = g
            continue
        m2 = re.match(r"C blocks=(\d+) vetoes=(\d+) adapts=(\d+) latched=(\d+) kept=(\d+)", line)
        if m2:
            nb, nv, na, nl, nk = map(int, m2.groups())
        m3 = re.search(r"C gate (OPEN|CLOSED|PRE-OPEN) rg=(\d+)( rb=(\d+))?", line)
        if m3:
            gate_opens.append((m3.group(1), int(m3.group(2)), m3.group(4)))
        if "LATCHED" in line or "ABSTAIN" in line or "nominal" in line:
            latches.append(line.strip())
    engage = adapts / n if n else 0.0
    return dict(n=n, adapts=adapts, vetoes=vetoes, holds=holds, dsum=dsum,
                engage=engage, adapt_blocks=adapt_blocks, gate=gate_opens,
                latch=latches)

if __name__ == "__main__":
    for p in sys.argv[1:]:
        r = parse(p)
        print(f"{p}: n={r['n']} adapts={r['adapts']} vetoes={r['vetoes']} holds={r['holds']} "
              f"dsum={r['dsum']:.2f} engage={r['engage']:.3f}")
        if r['adapt_blocks'] and len(sys.argv) == 2:
            for b in r['adapt_blocks'][:12]:
                print("   adapt rg=%d rb=%d g=%d m=%d T=%d" % b)
        if r['gate']:
            print("   gate:", r['gate'][:8])
        for l in r['latch'][:6]:
            print("   latch:", l[:100])
