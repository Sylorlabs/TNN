#!/usr/bin/env python3
"""Resume the enwiki en1 split after page 13942 (daemon-restart recovery).

Replays split_wiki.py's exact page-boundary detection over the bz2 stream,
discards the first SKIP pages (already written), then writes pages numbered
from SKIP onward as en1_n%08d.xml into wiki_full/shard_00/wikipedia/.
Output is byte-identical to what an uninterrupted split_wiki.py run would
have produced for pages >= SKIP. Zero RNG. Deterministic.

Usage: bzcat en1.bz2 | python3 resume_wiki_en1.py <outdir> [skip]
"""
import os
import sys

CHUNK = 1 << 24

def main():
    outdir = sys.argv[1]
    skip = int(sys.argv[2]) if len(sys.argv) > 3 else 13943
    head = b"<mediawiki>\n"
    tail = b"</mediawiki>\n"
    buf = b""
    n_pages = 0
    n_written = 0
    inp = sys.stdin.buffer

    def write_page(page, idx):
        name = f"en1_n{idx:08d}.xml"
        with open(os.path.join(outdir, name), "wb") as f:
            f.write(head)
            f.write(page)
            f.write(b"\n")
            f.write(tail)

    eof = False
    while not eof:
        c = inp.read(CHUNK)
        if not c:
            eof = True
        buf += c
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
                break
            e += 7
            if n_pages >= skip:
                write_page(buf[s:e], n_pages)
                n_written += 1
            n_pages += 1
            pos = e
        if pos > 0:
            buf = buf[pos:]
        if len(buf) > (1 << 28):
            sys.stderr.write("page exceeds 256MB, aborting\n")
            sys.exit(1)
    print(f"pages seen: {n_pages}, written: {n_written} (from {skip})", flush=True)

if __name__ == "__main__":
    main()
