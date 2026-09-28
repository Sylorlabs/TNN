#!/usr/bin/env python3
"""Independent reimplementation of the UNGROUNDED mdl path from
units/r0/impl/arms/arms.zag (mdl_fit + mdl_next + arm_adaptive_mdl emission).

Mirrors the Zag logic exactly:
- FNV-1a 64 with u64 wraparound; slot = h & 0xFFFFF (MS=2^20)
- linear-probe insert/compare by (h, L, bytes), count++, first=insert pos
- candidates: count>=4 and savings=(L-1)*count-(L+3) > 0
- final rank: mergesort-by (score desc, len desc, count desc, bytes asc), stable
- top 256 motifs; head/next chains; greedy longest-match at each pos,
  tie on length -> HIGHEST e (lowest score-rank, per Zag mdl_next traversal order)
- emission: motif kind 'm' id=best-e; literal kind 'r' id=byte, len=1
"""
import sys

P = 1099511628211
M64 = 0xFFFFFFFFFFFFFFFF
MS = 1 << 20
MM = MS - 1


def mdl_segments(buf: bytes, maxlen: int):
    n = len(buf)
    # hash table: slot -> [h, L, count, first]
    mh = [0] * MS
    ml = [0] * MS
    mc = [0] * MS
    mf = [-1] * MS
    nentries = 0
    full = False
    for i in range(n):
        h = 1469598103934665603
        for L in range(1, maxlen + 1):
            if i + L > n:
                break
            h = ((h ^ buf[i + L - 1]) * P) & M64
            if L >= 2 and not full:
                slot = h & MM
                while True:
                    if mf[slot] < 0:
                        mh[slot] = h
                        ml[slot] = L
                        mc[slot] = 1
                        mf[slot] = i
                        nentries += 1
                        if nentries >= MS:
                            full = True
                        break
                    if (mh[slot] == h and ml[slot] == L
                            and buf[mf[slot]:mf[slot] + L] == buf[i:i + L]):
                        mc[slot] += 1
                        break
                    slot = (slot + 1) & MM
    # candidates
    cands = []  # (slot, sav, L, count, first)
    for s in range(MS):
        if mf[s] >= 0 and mc[s] >= 4:
            L = ml[s]
            sav = (L - 1) * mc[s] - (L + 3)
            if sav > 0:
                cands.append((s, sav, L, mc[s], mf[s]))
    # final rank: (score desc, len desc, count desc, bytes asc), stable.
    # Zag uses bottom-up mergesort with strict comparator; Python sorted() with
    # tuple key + stability reproduces it (bytes comparison = bytes_less).
    keyed = sorted(
        enumerate(cands),
        key=lambda t: (
            -t[1][1], -t[1][2], -t[1][3],
            buf[t[1][4]:t[1][4] + t[1][2]],
            t[0],  # stability: original slot-ascending order
        ),
    )
    top = keyed[:256]
    nmot = len(top)
    mlen = [top[e][1][2] for e in range(nmot)]
    mfirst = [top[e][1][4] for e in range(nmot)]
    head = [-1] * 256
    nxt = [-1] * nmot
    for e in range(nmot):
        fb = buf[mfirst[e]]
        nxt[e] = head[fb]
        head[fb] = e
    segs = []
    pos = 0
    while pos < n:
        best = -1
        bestlen = 0
        e = head[buf[pos]]
        while e >= 0:  # descending e (head = max e; chain goes down)
            L = mlen[e]
            if (L > bestlen and pos + L <= n
                    and buf[mfirst[e]:mfirst[e] + L] == buf[pos:pos + L]):
                best = e
                bestlen = L
            e = nxt[e]
        if best >= 0:
            segs.append((pos, bestlen, best, "m"))
            pos += bestlen
        else:
            segs.append((pos, 1, buf[pos], "r"))
            pos += 1
    return segs


def main():
    inp, maxlen = sys.argv[1], int(sys.argv[2])
    buf = open(inp, "rb").read()
    segs = mdl_segments(buf, maxlen)
    out = ["ARMS v=1 arm=x n=%d" % len(buf)]
    for st, ln, idx, kind in segs:
        out.append("SEG %d %d %d %s" % (st, ln, idx, kind))
    out.append("END chunks=%d" % len(segs))
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
