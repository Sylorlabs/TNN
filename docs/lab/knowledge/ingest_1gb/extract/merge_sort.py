#!/usr/bin/env python3
"""Merge the per-source .bin files into one key-sorted facts.bin.
External merge sort (chunk sort + k-way merge). Deterministic.
Also writes run/merge_stats.txt (record counts, duplicate-key count).
Record: [1B kind][2B key_len BE][4B text_len BE][key][text]
"""
import struct, os, sys, heapq, tempfile

RUN = os.path.expanduser("~/workspace/tnn-lab/knowledge/ingest_1gb/run")
CHUNK = 500000

def read_records(path):
    with open(path, "rb") as f:
        data = f.read()
    p = 0
    n = len(data)
    while p < n:
        kind = data[p]
        klen = struct.unpack(">H", data[p+1:p+3])[0]
        tlen = struct.unpack(">I", data[p+3:p+7])[0]
        key = data[p+7:p+7+klen]
        rec = data[p:p+7+klen+tlen]
        p += 7 + klen + tlen
        yield key, rec

def main():
    srcs = [os.path.join(RUN, x) for x in ("wn.bin", "wiki.bin", "wikt.bin")]
    for s in srcs:
        if not os.path.exists(s):
            raise SystemExit(f"missing {s}")
    tmpd = tempfile.mkdtemp(prefix="mergesort_", dir=RUN)
    runs = []
    buf = []
    total = 0
    def flush():
        buf.sort(key=lambda r: r[0])
        rp = os.path.join(tmpd, f"run{len(runs):04d}.bin")
        with open(rp, "wb") as o:
            for _, rec in buf:
                o.write(struct.pack(">I", len(rec)) + rec)
        runs.append(rp)
        buf.clear()
    for s in srcs:
        for key, rec in read_records(s):
            buf.append((key, rec))
            total += 1
            if len(buf) >= CHUNK:
                flush()
                print(f"  ... sorted {total} records", flush=True)
    if buf:
        flush()
    # k-way merge
    outp = os.path.join(RUN, "facts.bin")
    files = [open(r, "rb") for r in runs]
    heap = []
    dupes = 0
    prev_key = None
    written = 0
    for i, fh in enumerate(files):
        hdr = fh.read(4)
        if hdr:
            ln = struct.unpack(">I", hdr)[0]
            rec = fh.read(ln)
            kind = rec[0]
            klen = struct.unpack(">H", rec[1:3])[0]
            key = rec[7:7+klen]
            heapq.heappush(heap, (key, i, rec))
    with open(outp, "wb") as out:
        while heap:
            key, i, rec = heapq.heappop(heap)
            if key == prev_key:
                # duplicate key: drop this record (keep the first occurrence,
                # which the stable chunk sort + run-ordered k-way merge pops
                # first). The stream still advances below.
                dupes += 1
            else:
                prev_key = key
                out.write(rec)
                written += 1
            fh = files[i]
            hdr = fh.read(4)
            if hdr:
                ln = struct.unpack(">I", hdr)[0]
                rec2 = fh.read(ln)
                klen2 = struct.unpack(">H", rec2[1:3])[0]
                key2 = rec2[7:7+klen2]
                heapq.heappush(heap, (key2, i, rec2))
    for fh in files:
        fh.close()
    with open(os.path.join(RUN, "merge_stats.txt"), "w") as st:
        st.write(f"input_records={total}\nwritten={written}\nduplicate_keys={dupes}\nruns={len(runs)}\n")
    print(f"merged: {written} records, {dupes} duplicate keys, {len(runs)} runs")
    # cleanup temp runs
    for r in runs:
        os.remove(r)
    os.rmdir(tmpd)

if __name__ == "__main__":
    main()
