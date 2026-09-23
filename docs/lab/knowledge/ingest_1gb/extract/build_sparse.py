#!/usr/bin/env python3
"""Build sparse.idx for a store (workaround for sindex parse bug at scale).
Format: [4B LE nentries][entries...]
Each entry: [2B BE klen][8B LE goff][key bytes]
One entry per id where id % 1024 == 0.
Blob record: [1B kind][4B LE id][2B BE klen][4B LE tlen][key][text]
"""
import struct, os, sys

CHUNK = 33488896
EVERY = 1024

def main():
    outdir = sys.argv[1]
    nchunks = len([f for f in os.listdir(outdir) if f.startswith("blob_")])
    entries = []
    for ci in range(nchunks):
        path = os.path.join(outdir, f"blob_{ci:06d}.dat")
        with open(path, "rb") as f:
            data = f.read()
        off = 0
        n = len(data)
        first_in_chunk = True
        while off < n:
            if off + 11 > n:
                break
            kind = data[off]
            if kind == 0:
                break
            fid = struct.unpack("<i", data[off+1:off+5])[0]
            klen = struct.unpack(">H", data[off+5:off+7])[0]
            tlen = struct.unpack("<i", data[off+7:off+11])[0]
            key = data[off+11:off+11+klen]
            # sparse entry every 1024th, PLUS first key of each chunk
            # (workaround: ig_lookup doesn't cross chunk boundaries on rl==0)
            if fid % EVERY == 0 or first_in_chunk:
                goff = ci * CHUNK + off
                entries.append((key, goff))
                first_in_chunk = False
            off += 11 + klen + tlen
        print(f"  chunk {ci}: off={off}", flush=True)
    entries.sort()
    with open(os.path.join(outdir, "sparse.idx"), "wb") as o:
        o.write(struct.pack("<i", len(entries)))
        for key, goff in entries:
            o.write(struct.pack(">H", len(key)))
            o.write(struct.pack("<q", goff))
            o.write(key)
    print(f"sparse.idx: {len(entries)} entries")

if __name__ == "__main__":
    main()
