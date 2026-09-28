#!/usr/bin/env python3
"""Kill criterion (i) adjudication for H1 vs fixed-64B baseline (B-64).

Definition (coordinator operationalization, frozen in VERDICT.md):
  reuse hit rate = fraction of ingested units whose content exactly matches an
  already-live stored span (content-keyed, offset-independent).

Protocol:
  - Single ingest of each corpus (prose.bin, code.bin), units walked in order.
  - Live-store slots: equal for both arms, capacity ample (no evictions), so
    "already-live" = every previously-ingested unit.
  - H1 spans: from the arm's own dry segmentation (spans-1x-<corpus> mode).
  - B-64 spans: fixed 64-byte chunks (deterministic rule, no rebuild needed).
"""
import hashlib, sys

CROOT = "/home/hatch/workspace/tnn-lab/units/arms/harness/corpora/r1"

def h1_spans(path):
    spans = []
    with open(path) as f:
        for line in f:
            if line.startswith("SPAN,"):
                _, off, ln = line.strip().split(",")
                spans.append((int(off), int(ln)))
    return spans

def b64_spans(n):
    spans = []
    off = 0
    while off < n:
        ln = min(64, n - off)
        spans.append((off, ln))
        off += 64
    return spans

def tile_check(spans, n, name):
    # spans must tile [0, n) contiguously in order
    pos = 0
    for off, ln in spans:
        assert off == pos, f"{name}: gap/overlap at {pos} vs {off}"
        assert ln > 0, f"{name}: empty span at {off}"
        pos += ln
    assert pos == n, f"{name}: spans cover {pos}, file is {n}"
    print(f"{name}: tiling OK ({len(spans)} spans, {n} bytes)")

def reuse_rate(data, spans):
    seen = set()
    hits = 0
    for off, ln in spans:
        h = hashlib.sha256(data[off:off+ln]).digest()
        if h in seen:
            hits += 1
        else:
            seen.add(h)
    return hits, len(spans), hits / len(spans)

for corpus, fname in (("prose", "prose.bin"), ("code", "code.bin")):
    data = open(f"{CROOT}/{fname}", "rb").read()
    n = len(data)
    h1 = h1_spans(f"/tmp/spans_{corpus}.txt")
    b64 = b64_spans(n)
    tile_check(h1, n, f"H1-{corpus}")
    tile_check(b64, n, f"B64-{corpus}")
    hh, ht, hr = reuse_rate(data, h1)
    bh, bt, br = reuse_rate(data, b64)
    print(f"H1  {corpus}: hits={hh} total={ht} rate={hr*100:.3f}%")
    print(f"B64 {corpus}: hits={bh} total={bt} rate={br*100:.3f}%")
    print(f"  H1 - B64 = {(hr-br)*100:+.3f} pp ; kill-(i) bar = B64+10pp = {(br*100)+10:.3f}% ; fires = {hr <= br + 0.10}")
    print()
