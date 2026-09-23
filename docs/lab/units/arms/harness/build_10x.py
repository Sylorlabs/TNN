#!/usr/bin/env python3
# build_10x.py — deterministic 10x corpus: 10-fold tiling of the 1x corpora.
# Each tile is the 1x file repeated verbatim; tile boundaries are recorded so
# arms can verify the tiling. Fully deterministic: no RNG, no timestamps.
# Usage: build_10x.py [r1-dir] [r10-dir]
import os, sys, json, hashlib

TILES = 10
FILES = ["prose.bin", "code.bin", "t1_prose.bin", "t1_code.bin",
         "t2_prose.bin", "t2_code.bin", "t3.bin", "churn_fresh.bin",
         "mem_vocab.txt", "mem_vocab_sorted.txt"]

def sha(b):
    return hashlib.sha256(b).hexdigest()

def main():
    src = sys.argv[1] if len(sys.argv) > 1 else os.path.join("corpora", "r1")
    dst = sys.argv[2] if len(sys.argv) > 2 else os.path.join("corpora", "r10")
    os.makedirs(dst, exist_ok=True)
    man = {"tiles": TILES, "source": os.path.abspath(src), "files": {}}
    for fn in FILES:
        data = open(os.path.join(src, fn), "rb").read()
        tiled = data * TILES
        open(os.path.join(dst, fn), "wb").write(tiled)
        man["files"][fn] = {
            "bytes": len(tiled),
            "sha256": sha(tiled),
            "tile_bytes": len(data),
            "tile_sha256": sha(data),
        }
        print(f"{fn}: {len(tiled)} bytes, tile sha {sha(data)[:16]}")
    json.dump(man, open(os.path.join(dst, "MANIFEST.json"), "w"), indent=2)
    print("wrote", os.path.join(dst, "MANIFEST.json"))

if __name__ == "__main__":
    main()
