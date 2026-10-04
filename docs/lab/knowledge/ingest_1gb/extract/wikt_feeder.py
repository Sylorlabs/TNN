#!/usr/bin/env python3
"""Decompress the wiktionary dump once to a plain XML file.

A single sequential bz2 decompression (~1.6GB -> ~6GB). Workers then parse
the decompressed file directly, avoiding 4x redundant decompression.
"""
import bz2

SRC = "/home/hatch/workspace/tnn-lab/knowledge/ingest_1gb/corpus/enwiktionary-latest-pages-articles.xml.bz2"
DST = "/home/hatch/workspace/wikt_full.xml"

def main():
    n = 0
    with bz2.open(SRC, "rb") as f, open(DST, "wb") as o:
        while True:
            ch = f.read(1 << 20)
            if not ch:
                break
            o.write(ch)
            n += len(ch)
            if n % (1 << 30) == 0:
                print(f"feeder ... {n >> 30} GB", flush=True)
    print(f"feeder done: {n} bytes", flush=True)

if __name__ == "__main__":
    main()
