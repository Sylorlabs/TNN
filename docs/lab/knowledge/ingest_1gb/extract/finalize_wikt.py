#!/usr/bin/env python3
"""Post-extraction: concatenate worker chunks, validate, filter, report.

Steps:
1. Concatenate run/wikt.bin (pages 1-5M) + run/wikt_d1..d4.bin (5M-EOF)
   in page order -> run/wikt_raw_full.bin
2. Structurally validate wikt_raw_full.bin (parse all records, count)
3. Run filter_degenerate.py -> run/wikt_clean.bin
4. Print final counts and SHAs

Usage: finalize_wikt.py
"""
import hashlib, os, struct, subprocess, sys

RUN = os.path.expanduser("~/workspace/tnn-lab/knowledge/ingest_1gb/run")
EXT = os.path.expanduser("~/workspace/tnn-lab/knowledge/ingest_1gb/extract")

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            ch = f.read(1 << 20)
            if not ch:
                break
            h.update(ch)
    return h.hexdigest()

def count_records(path):
    with open(path, "rb") as f:
        data = f.read()
    p, n = 0, len(data)
    cnt = {1: 0, 2: 0}
    while p < n:
        kind = data[p]
        klen = struct.unpack(">H", data[p+1:p+3])[0]
        tlen = struct.unpack(">I", data[p+3:p+7])[0]
        rec_len = 7 + klen + tlen
        if p + rec_len > n:
            raise ValueError(f"truncated record at offset {p}")
        cnt[kind] = cnt.get(kind, 0) + 1
        p += rec_len
    if p != n:
        raise ValueError(f"trailing bytes: {n - p}")
    return cnt, n

def main():
    chunks = [os.path.join(RUN, "wikt.bin")] + \
             [os.path.join(RUN, f"wikt_d{i}.bin") for i in (1, 2, 3, 4)]
    for c in chunks:
        if not os.path.exists(c):
            print(f"MISSING: {c}", flush=True)
            sys.exit(1)
        print(f"chunk {os.path.basename(c)}: {os.path.getsize(c)} bytes", flush=True)

    raw = os.path.join(RUN, "wikt_raw_full.bin")
    print("concatenating...", flush=True)
    with open(raw, "wb") as o:
        for c in chunks:
            with open(c, "rb") as f:
                while True:
                    ch = f.read(1 << 20)
                    if not ch:
                        break
                    o.write(ch)
    print(f"raw: {os.path.getsize(raw)} bytes sha={sha256(raw)}", flush=True)

    print("validating structure...", flush=True)
    cnt, total = count_records(raw)
    print(f"raw records: kind1={cnt[1]}, kind2={cnt[2]}, total={cnt[1]+cnt[2]}", flush=True)

    clean = os.path.join(RUN, "wikt_clean.bin")
    print("filtering degenerate...", flush=True)
    r = subprocess.run([sys.executable, os.path.join(EXT, "filter_degenerate.py"),
                        raw, clean], capture_output=True, text=True)
    print(r.stdout, flush=True)
    if r.returncode != 0:
        print(r.stderr, flush=True)
        sys.exit(1)
    print(f"clean: {os.path.getsize(clean)} bytes sha={sha256(clean)}", flush=True)
    cnt2, _ = count_records(clean)
    print(f"clean records: kind1={cnt2[1]}, kind2={cnt2[2]}, total={cnt2[1]+cnt2[2]}", flush=True)

if __name__ == "__main__":
    main()
