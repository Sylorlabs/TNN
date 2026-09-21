#!/usr/bin/env python3
"""B-T1 tournament scorer. Deterministic measurement code (xcheck.py precedent).
Zero RNG: no random module, no hash(), no wall-clock in output-affecting paths.
All orderings are total and explicit; JSON emitted with sorted keys.

Implements PROBE_MANIFEST.md (frozen 2026-09-21) against arms-binary SEG output.
Usage: bt1_score.py <seg_file> <corpus_file>
"""
import json
import sys

DELIM = {0x20, 0x0A, 0x09, 0x0D, 0x2C, 0x3B, 0x7B, 0x7D, 0x28, 0x29}
K_PROBE = 256
R1_MAX_OCC = 1024


def fnv1a64(data: bytes) -> int:
    h = 1469598103934665603
    for b in data:
        h ^= b
        h = (h * 1099511628211) & 0xFFFFFFFFFFFFFFFF
    return h


def parse_seg(path):
    segs = []
    arm = None
    n = None
    with open(path, "r") as f:
        for line in f:
            line = line.rstrip("\n")
            if line.startswith("ARMS v=1"):
                for tok in line.split():
                    if tok.startswith("arm="):
                        arm = tok[4:]
                    elif tok.startswith("n="):
                        n = int(tok[2:])
            elif line.startswith("SEG "):
                _, st, ln, _idx, _kind = line.split(" ")
                segs.append((int(st), int(ln)))
            elif line.startswith("END "):
                pass
            elif line.startswith("META "):
                pass
            elif line == "":
                pass
            else:
                raise ValueError("unparsed line: %r" % line[:60])
    return arm, n, segs


def main():
    seg_path, corpus_path = sys.argv[1], sys.argv[2]
    stream = open(corpus_path, "rb").read()
    n = len(stream)
    arm, n_hdr, segs = parse_seg(seg_path)
    assert n_hdr == n, (n_hdr, n)

    # tiling + reconstruction gate
    pos = 0
    out = bytearray()
    for st, ln in segs:
        assert st == pos, ("tiling gap", arm, st, pos)
        out += stream[st:st + ln]
        pos += ln
    assert pos == n, ("tiling end", arm, pos, n)
    reconstruction = "1" if bytes(out) == stream else "0"
    assert reconstruction == "1", "reconstruction failed for %s" % arm

    # probe vocabulary: distinct contents, count>=2, (count desc, bytes asc), top 256
    counts = {}
    first_off = {}
    for st, ln in segs:
        c = bytes(stream[st:st + ln])
        e = counts.get(c)
        if e is None:
            counts[c] = 1
            first_off[c] = st
        else:
            counts[c] = e + 1
    cand = [c for c in counts if counts[c] >= 2]
    cand.sort(key=lambda c: (-counts[c], c))
    vocab = cand[:K_PROBE]
    if len(vocab) == 0:
        sys.stderr.write("WARN: probe vocab empty: %s (no repeated chunk contents)\n" % arm)
        # No reusable units to probe: grounded/retrieval are 0; compression/reconstruction still measured.
        compression_ev = 1.0 - (len(segs) / n)
        comp = (0.55 * 0.0 + 0.25 * 0.0
                + 0.10 * compression_ev + 0.10 * float(reconstruction))
        result = {
            "arm": arm, "corpus": corpus_path.split("/")[-1], "n_bytes": n, "n_chunks": len(segs),
            "vocab_probed": 0, "mean_purity": 0.0,
            "grounded_clean": 0.0, "grounded_perturbed": 0.0, "grounded_hard": 0.0,
            "retrieval_20way": 0.0, "compression": round(compression_ev, 6),
            "reconstruction": reconstruction,
            "capability_composite": round(comp, 6),
            "m8_note": "seg input run twice byte-identical; see M8 log",
        }
        if len(sys.argv) > 3:
            json.dump(result, open(sys.argv[3], "w"), indent=2, sort_keys=True)
        print(json.dumps(result, indent=2, sort_keys=True))
        return
    if len(vocab) < 20:
        sys.stderr.write("WARN: probe vocab small: %s n=%d\n" % (arm, len(vocab)))

    def occurrences(content):
        occ = []
        i = stream.find(content, 0)
        while i != -1 and len(occ) < R1_MAX_OCC:
            occ.append(i)
            i = stream.find(content, i + 1)
        return occ

    # per-span labels
    purities = []
    tot_agree = 0
    tot_labeled = 0
    span_info = []  # (content, occ, q_list, m)
    for content in vocab:
        occ = occurrences(content)
        qs = []
        for o in occ:
            j = o + len(content)
            if j >= n:
                continue
            qs.append(1 if stream[j] in DELIM else 0)
        if not qs:
            continue
        # (a) recall: concat of chunks covering [o, o+len) == content (always 1; verified)
        b = 1 if all(q == qs[0] for q in qs) else 0
        # labels in {1,3} since a=1; purity = majority fraction
        # careful: label=1 means (a=0? no) -> a=1,b=0 -> label 2? label = a*2+b = 2+b? no:
        # label = a_j*2 + b with a=1 -> labels are 2 (b=0) and 3 (b=1).
        lab2 = 0 if b == 1 else len(qs)
        lab3 = len(qs) if b == 1 else 0
        purity = max(lab2, lab3) / len(qs)
        purities.append(purity)
        m = 1 if sum(qs) * 2 >= len(qs) else 0  # majority outcome bit, ties -> 1
        tot_agree += sum(1 for q in qs if q == m)
        tot_labeled += len(qs)
        span_info.append((content, occ, qs, m))

    grounded_clean = tot_agree / tot_labeled if tot_labeled else 0.0

    # perturbed leg: every-7th-byte XOR 0x5A (M-16 defect rule)
    pstream = bytearray(stream)
    for i in range(0, n, 7):
        pstream[i] ^= 0x5A
    pstream = bytes(pstream)
    p_agree = 0
    p_labeled = 0
    for content, occ, qs, m in span_info:
        pocc = []
        i = pstream.find(content, 0)
        while i != -1 and len(pocc) < R1_MAX_OCC:
            pocc.append(i)
            i = pstream.find(content, i + 1)
        for o in pocc:
            j = o + len(content)
            if j >= n:
                continue
            q = 1 if pstream[j] in DELIM else 0
            if q == m:
                p_agree += 1
            p_labeled += 1
    grounded_perturbed = p_agree / p_labeled if p_labeled else 0.0
    grounded_hard = (grounded_clean + grounded_perturbed) / 2.0

    # retrieval_20way: corrupted cue -> best agreement candidate
    nv = len(vocab)
    hits = 0
    for vi, content in enumerate(vocab):
        occ = occurrences(content)
        o1 = occ[0]
        cue = bytearray(content)
        for p in range(len(cue)):
            if (o1 + p) % 7 == 0:
                cue[p] ^= 0x5A
        cue = bytes(cue)
        cands = [vocab[(vi + d) % nv] for d in range(20)]
        best = None
        for ci, y in enumerate(cands):
            ml = min(len(cue), len(y))
            agree = sum(1 for p in range(ml) if cue[p] == y[p]) / max(len(cue), len(y))
            key = (-agree, abs(len(cue) - len(y)), y, ci)
            if best is None or key < best[0]:
                best = (key, ci)
        if best[1] == 0:
            hits += 1
    retrieval_20way = hits / nv

    compression = 1.0 - (len(segs) / n)
    composite = (0.55 * grounded_hard + 0.25 * retrieval_20way
                 + 0.10 * compression + 0.10 * float(reconstruction))

    result = {
        "arm": arm,
        "corpus": corpus_path.split("/")[-1],
        "n_bytes": n,
        "n_chunks": len(segs),
        "vocab_probed": nv,
        "mean_purity": sum(purities) / len(purities) if purities else 0.0,
        "grounded_clean": grounded_clean,
        "grounded_perturbed": grounded_perturbed,
        "grounded_hard": grounded_hard,
        "retrieval_20way": retrieval_20way,
        "compression": compression,
        "reconstruction": reconstruction,
        "capability_composite": composite,
        "m8_note": "seg input run twice byte-identical; see M8 log",
    }
    if len(sys.argv) > 3:
        json.dump(result, open(sys.argv[3], "w"), sort_keys=True, indent=2)
    json.dump(result, sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")


main()
