#!/usr/bin/env python3
"""Generate corrected slot-based E2/E3 fixtures from slot2pos.bin.
Deterministic (zero randomness). Outputs JSON-ish TSV files:
  e2_targets.tsv: slot, facts_pos, key, old_text_sha, new_text
  e3_targets.tsv: slot, facts_pos, key
  neighbors.tsv: target_slot, phase(e2/e3), neighbor_slot, key, text_sha
"""
import struct, hashlib, os

BASE = os.path.expanduser("~/workspace/tnn-lab/knowledge/ingest_1gb")
AUD = os.path.join(BASE, "audit")
N = 2597057

def load_slot2pos():
    d = open(os.path.join(AUD, "slot2pos.bin"), "rb").read()
    n = struct.unpack("<i", d[:4])[0]
    assert n == N, n
    return struct.unpack("<%di" % n, d[4:4+4*n])

def read_facts_record(f, pos):
    """Read the pos-th record from facts.bin file object (sequential)."""
    # We walk sequentially; caller iterates in increasing pos order.
    raise NotImplementedError

def main():
    s2p = load_slot2pos()
    # deterministic target selection
    rev_slots = [(i * N) // 100 for i in range(100)]
    del_slots = [((i * N) // 100 + 12985) % N for i in range(100)]
    assert len(set(rev_slots)) == 100
    assert len(set(del_slots)) == 100
    assert not (set(rev_slots) & set(del_slots)), "overlap!"
    # neighbors: 5 each side, clamped, skipping any target slot
    targets = set(rev_slots) | set(del_slots)
    def neighbors(s):
        out = []
        d = 1
        while len(out) < 10 and d < N:
            for c in (s - d, s + d):
                if 0 <= c < N and c not in targets and c not in out:
                    out.append(c)
                    if len(out) == 10:
                        break
            d += 1
        return sorted(out)
    # collect all slots we need records for
    need = {}
    for i, s in enumerate(rev_slots):
        need[s] = ("rev", i)
    for i, s in enumerate(del_slots):
        need[s] = ("del", i)
    neigh = {}
    for s in rev_slots:
        for nb in neighbors(s):
            neigh[nb] = ("e2", s)
    for s in del_slots:
        for nb in neighbors(s):
            neigh[nb] = ("e3", s)
    for nb in neigh:
        if nb not in need:
            need[nb] = ("neigh", None)
    # walk facts.bin once, in increasing position order
    by_pos = sorted(((s2p[s], s) for s in need), key=lambda x: x[0])
    recs = {}
    with open(os.path.join(BASE, "run", "facts.bin"), "rb") as f:
        cur = 0
        bi = 0
        while bi < len(by_pos):
            want_pos, slot = by_pos[bi]
            # skip to want_pos
            while cur < want_pos:
                h = f.read(7)
                klen = struct.unpack(">H", h[1:3])[0]
                tlen = struct.unpack(">I", h[3:7])[0]
                f.seek(klen + tlen, 1)
                cur += 1
            h = f.read(7)
            assert len(h) == 7
            klen = struct.unpack(">H", h[1:3])[0]
            tlen = struct.unpack(">I", h[3:7])[0]
            key = f.read(klen)
            text = f.read(tlen)
            assert len(key) == klen and len(text) == tlen
            recs[slot] = (key, text)
            cur += 1
            bi += 1
    # write fixtures
    with open(os.path.join(AUD, "e2_targets.tsv"), "w") as o:
        for i, s in enumerate(rev_slots):
            key, text = recs[s]
            newtext = ("AUDIT-REVISED slot=%d seq=%d key=%s" % (s, i, key.decode())).encode()
            o.write("%d\t%d\t%s\t%s\t%s\n" % (
                s, s2p[s], key.decode(),
                hashlib.sha256(text).hexdigest()[:16],
                newtext.decode()))
    with open(os.path.join(AUD, "e3_targets.tsv"), "w") as o:
        for i, s in enumerate(del_slots):
            key, text = recs[s]
            o.write("%d\t%d\t%s\t%s\n" % (
                s, s2p[s], key.decode(), hashlib.sha256(text).hexdigest()[:16]))
    with open(os.path.join(AUD, "neighbors.tsv"), "w") as o:
        for nb, (phase, ts) in sorted(neigh.items()):
            key, text = recs[nb]
            o.write("%d\t%s\t%d\t%s\t%s\n" % (
                ts, phase, nb, key.decode(), hashlib.sha256(text).hexdigest()[:16]))
    # also stash full expected texts for neighbor verification (sha only in tsv;
    # store texts in a side file keyed by slot)
    with open(os.path.join(AUD, "neighbor_texts.tsv"), "w") as o:
        for nb in sorted(neigh):
            key, text = recs[nb]
            o.write("%d\t%s\t%s\n" % (nb, key.decode(), text.decode('utf-8', 'replace').replace("\t", " ").replace("\n", " ")))
    print("fixtures written: rev=%d del=%d neighbors=%d" % (len(rev_slots), len(del_slots), len(neigh)))

if __name__ == "__main__":
    main()
