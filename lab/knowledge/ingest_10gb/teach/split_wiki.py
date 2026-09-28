#!/usr/bin/env python3
"""Split a MediaWiki XML stream into one well-formed file per <page> (streaming).

Reads bz2-decompressed XML from stdin in chunks (bounded memory), writes
<mediawiki>\\n<page>...</page>\\n</mediawiki>\\n per page into shard dirs.
One page per file is REQUIRED: the frozen clean.py emits wikibooks keys as
wb:{slug}:{n} with n restarting per page, so multi-page files produce
duplicate keys (verified 2026-09-23). Unique slug per page keeps keys unique.

Usage: bzcat dump.bz2 | python3 split_wiki.py <outbase> <stem> [pages_per_shard]
       [skip_n] [start_n]
Writes <outbase>/shard_<nn>/wikipedia/<stem>_n<n:08d>.xml
If skip_n>0, the first skip_n pages are counted but not written (fast resume);
numbering starts at start_n (default 0). Use skip_n=start_n to continue a
killed split without rewriting existing files.
Prints pages, shards.
Zero RNG. Deterministic.
"""
import os
import sys

CHUNK = 1 << 24  # 16MB

def main():
    outbase = sys.argv[1]
    stem = sys.argv[2]
    pps = int(sys.argv[3]) if len(sys.argv) > 3 else 50000
    skip_n = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    start_n = int(sys.argv[5]) if len(sys.argv) > 5 else 0
    seen = 0  # pages seen in stream (for skip)
    head = b"<mediawiki>\n"
    tail = b"</mediawiki>\n"
    buf = b""
    n_pages = start_n
    cur_shard = -1
    cur_dir = None
    inp = sys.stdin.buffer

    def ensure_shard():
        nonlocal cur_shard, cur_dir
        shard = n_pages // pps
        if shard != cur_shard:
            cur_shard = shard
            cur_dir = os.path.join(outbase, f"shard_{shard:02d}", "wikipedia")
            os.makedirs(cur_dir, exist_ok=True)

    def write_page(page):
        nonlocal n_pages, seen
        seen += 1
        if seen <= skip_n:
            return  # resume: count but don't rewrite
        ensure_shard()
        name = f"{stem}_n{n_pages:08d}.xml"
        with open(os.path.join(cur_dir, name), "wb") as f:
            f.write(head)
            f.write(page)
            f.write(b"\n")
            f.write(tail)
        n_pages += 1

    eof = False
    while not eof:
        # accumulate small pipe reads into a >=1MB buffer: bzcat trickles
        # (~9KB/read under CPU contention) and per-read Python overhead
        # dominated at 6 pages/sec. Amortize by batching reads.
        chunks = []
        total = 0
        while total < (1 << 20):
            c = inp.read(CHUNK - total)
            if not c:
                break
            chunks.append(c)
            total += len(c)
        if not chunks:
            eof = True
            continue
        c = b"".join(chunks)
        buf += c
        # extract complete <page>...</page> elements
        pos = 0
        while True:
            s = buf.find(b"<page>", pos)
            s2 = buf.find(b"<page ", pos)
            if s2 >= 0 and (s < 0 or s2 < s):
                s = s2
                gt = buf.find(b">", s)
                if gt < 0:
                    break
            elif s >= 0:
                gt = s + 5
            else:
                break
            e = buf.find(b"</page>", gt)
            if e < 0:
                break  # incomplete; need more data
            e += 7
            write_page(buf[s:e])
            pos = e
        # keep unprocessed tail (from pos); drop processed head
        # keep enough to not lose a split "<page" marker: retain from pos
        # but if pos==0 and buf is huge without a complete page, keep it all
        # (a single page could exceed CHUNK; keep accumulating)
        if pos > 0:
            buf = buf[pos:]
        # safety: if buf grows beyond 256MB without a complete page, abort
        if len(buf) > (1 << 28):
            sys.stderr.write("page exceeds 256MB, aborting\n")
            sys.exit(1)
    # trailing buf should contain no complete pages; ignore
    print(f"pages: {n_pages}, shards used: {cur_shard + 1}")

if __name__ == "__main__":
    main()
