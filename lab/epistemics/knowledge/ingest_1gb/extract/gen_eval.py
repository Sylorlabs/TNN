#!/usr/bin/env python3
"""Generate deterministic evaluation key files from facts.bin.
- eval_keys.bin: 1000 keys sampled deterministically (every Nth record) for bquery
- rev_ids.txt: 100 fact IDs for revise test
- del_ids.txt: 100 fact IDs for delete test
All selections are deterministic (no RNG).
"""
import struct, os, sys

RUN = os.path.expanduser("~/workspace/tnn-lab/knowledge/ingest_1gb/run")

def main():
    facts = os.path.join(RUN, "facts.bin")
    # count records first
    n = 0
    with open(facts, "rb") as f:
        while True:
            hdr = f.read(7)
            if len(hdr) < 7:
                break
            klen = struct.unpack(">H", hdr[1:3])[0]
            tlen = struct.unpack(">I", hdr[3:7])[0]
            f.seek(klen + tlen, 1)
            n += 1
    print(f"total facts: {n}")
    step = max(1, n // 1000)
    # sample keys
    keys = []
    with open(facts, "rb") as f:
        i = 0
        while True:
            hdr = f.read(7)
            if len(hdr) < 7:
                break
            klen = struct.unpack(">H", hdr[1:3])[0]
            tlen = struct.unpack(">I", hdr[3:7])[0]
            key = f.read(klen)
            f.seek(tlen, 1)
            if i % step == 0 and len(keys) < 1000:
                keys.append(key)
            i += 1
    with open(os.path.join(RUN, "eval_keys.bin"), "wb") as o:
        for k in keys:
            o.write(struct.pack(">H", len(k)) + k)
    print(f"eval keys: {len(keys)}")
    # revise/delete IDs: deterministic spread
    rev_ids = [ (i * n) // 100 for i in range(100) ]
    del_ids = [ (i * n) // 100 + n // 200 for i in range(100) ]
    with open(os.path.join(RUN, "rev_ids.txt"), "w") as o:
        o.write("\n".join(map(str, rev_ids)))
    with open(os.path.join(RUN, "del_ids.txt"), "w") as o:
        o.write("\n".join(map(str, del_ids)))
    print("rev/del ID files written")

if __name__ == "__main__":
    main()
