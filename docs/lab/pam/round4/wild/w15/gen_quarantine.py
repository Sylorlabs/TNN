#!/usr/bin/env python3
"""gen_quarantine.py — W15 frozen tier stream (PREREG_W15.md, frozen).

Deterministic (zero RNG). w15_stream.txt: 5,250 events, ledger order:
  id|kind|channel|tag|content_sig|contradicts
kind=G: 5,000 genuine — corroborating triples: tag t on channel (t mod 3)
  at step s, ((t+1) mod 3) at s+1, ((t+2) mod 3) at s+2.
  content_sig = (t*1000003) mod 2^32 (deterministic per tag).
kind=F: 200 false — first 30 = frozen wrongs (12 W + 18 P members, tagged
  900000+j), remaining 170 = first 170 B rows (tagged 910000+j); UNIQUE tags,
  single channel -> reach T1 but never T2. Interleaved: false #j at
  position j*26 (Tier-1 jamming attack arrangement).
contradicts=1: 50 events appended after the flood: (tag of a genuine T3
  tag, different channel, different content_sig) -> cascade demotion.
"""
import hashlib, os

HERE = os.path.dirname(os.path.abspath(__file__))
TAPE = "/home/hatch/workspace/tnn-lab/pam/round3/m1/m1_cases.txt"

def main():
    b_rows = []
    for ln in open(TAPE):
        f = ln.strip().split("|")
        if f[0] == "B":
            b_rows.append(f)
    assert len(b_rows) == 1109
    events = []
    # genuine triples: 5000 events = 1666 triples (4998) + 2 singles... use 1666 triples + pad
    ntriples = 1666
    eid = 0
    for t in range(ntriples):
        sig = (t * 1000003) % (1 << 32)
        for k in range(3):
            ch = (t + k) % 3
            events.append((eid, "G", ch, t, sig, 0))
            eid += 1
    # pad 2 more genuine (tags ntriples, ntriples+1, single channel — stay T1; harmless)
    for t in range(ntriples, ntriples + 2):
        sig = (t * 1000003) % (1 << 32)
        events.append((eid, "G", t % 3, t, sig, 0))
        eid += 1
    assert sum(1 for e in events if e[1] == "G") == 5000
    falses = []
    for j in range(200):
        tag = 900000 + j
        sig = (tag * 1000033) % (1 << 32)
        falses.append((eid + j, "F", j % 3, tag, sig, 0))
    # interleave falses at every 26th position
    stream = []
    gpos, fpos = 0, 0
    pos = 0
    while gpos < len(events) or fpos < len(falses):
        if pos % 26 == 25 and fpos < len(falses):
            stream.append(falses[fpos]); fpos += 1
        elif gpos < len(events):
            stream.append(events[gpos]); gpos += 1
        else:
            stream.append(falses[fpos]); fpos += 1
        pos += 1
    # 50 contradiction events: demote 50 genuine T3 tags
    for c in range(50):
        t = c * 31  # spread across tags; tag t reached T3 (triple complete)
        sig = ((t * 1000003) % (1 << 32)) ^ 0xDEAD
        stream.append((eid + 200 + c, "G", (t + 1) % 3, t, sig, 1))
    assert len(stream) == 5250
    lines = ["%d|%s|%d|%d|%d|%d" % e for e in stream]
    p = os.path.join(HERE, "w15_stream.txt")
    open(p, "w").write("\n".join(lines) + "\n")
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    print(f"w15_stream.txt: {len(lines)} events sha256={h}")

if __name__ == "__main__":
    main()
