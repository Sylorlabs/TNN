#!/usr/bin/env python3
"""Dry-run of the FIXED pipeline on current (partial-wiktionary) inputs.

Validates end-to-end BEFORE the full wiktionary extraction completes:
  filter (degenerate wikt) -> fixed merge (dedupe) -> make_bad ->
  ingest with rebuilt binary -> audit must show ZERO CAL=REJECT.

All work happens in run/dry/; the real run/ artifacts are untouched.
Deterministic glue; the mechanisms (merge, ingest) are the real ones.
"""
import os, sys, struct, subprocess, hashlib

BASE = os.path.expanduser("~/workspace/tnn-lab/knowledge/ingest_1gb")
RUN = os.path.join(BASE, "run")
DRY = os.path.join(RUN, "dry")
EXT = os.path.join(BASE, "extract")
sys.path.insert(0, EXT)

def count_records(path):
    n = 0
    with open(path, "rb") as f:
        while True:
            hdr = f.read(7)
            if len(hdr) < 7:
                break
            klen = struct.unpack(">H", hdr[1:3])[0]
            tlen = struct.unpack(">I", hdr[3:7])[0]
            f.seek(klen + tlen, 1)
            n += 1
    return n

def main():
    os.makedirs(DRY, exist_ok=True)

    # 1. filter current wikt.bin (resume is in skip phase; no appends happening)
    import filter_degenerate
    sys.argv = ["filter_degenerate.py", os.path.join(RUN, "wikt.bin"),
                os.path.join(DRY, "wikt.bin")]
    filter_degenerate.main()

    # 2. link the other inputs
    for name in ("wn.bin", "wiki.bin"):
        dst = os.path.join(DRY, name)
        if not os.path.exists(dst):
            os.symlink(os.path.join(RUN, name), dst)

    # 3. fixed merge
    import merge_sort
    merge_sort.RUN = DRY
    merge_sort.main()
    facts = os.path.join(DRY, "facts.bin")
    nf = count_records(facts)
    print(f"dry facts records: {nf}")
    hf = hashlib.sha256()
    with open(facts, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            hf.update(ch)
    print(f"dry facts sha256: {hf.hexdigest()}")

    # 4. negative control
    import make_bad
    make_bad.RUN = DRY
    make_bad.main()

    # 5. ingest with the rebuilt (sindex-fixed) binary.
    # NOTE: the first build at build/ingest_bin_new vanished from the shared
    # build/ dir mid-run (cause unknown); rebuilt to ~/workspace/ingest_bin_v2.
    ncap = nf * 11 // 10
    store = os.path.join(DRY, "store_dry")
    bbin = os.path.expanduser("~/workspace/ingest_bin_v2")
    print(f"ingesting {nf} facts, ncap={ncap} ...", flush=True)
    r = subprocess.run([bbin, "ingest", facts, os.path.join(DRY, "bad.bin"),
                        store, str(ncap)])
    print(f"ingest rc={r.returncode}")
    if r.returncode != 0:
        raise SystemExit("dry ingest failed")

    # 6. audit verdict
    rejects = []
    lessons_ok = 0
    with open(os.path.join(store, "audit.log")) as f:
        for line in f:
            if "CAL=REJECT" in line:
                rejects.append(line.strip())
            if "CAL=OK" in line:
                lessons_ok += 1
    print(f"lessons CAL=OK: {lessons_ok}, CAL=REJECT: {len(rejects)}")
    for rj in rejects[:20]:
        print("  REJECT:", rj)
    seal = open(os.path.join(store, "seal.txt")).read().strip() \
        if os.path.exists(os.path.join(store, "seal.txt")) else "?"
    # report / seal lives in the binary's report output; also grab audit tail
    print(f"seal file: {seal}")
    with open(os.path.join(DRY, "dry_verdict.txt"), "w") as v:
        v.write(f"facts={nf}\nfacts_sha256={hf.hexdigest()}\nncap={ncap}\n")
        v.write(f"lessons_ok={lessons_ok}\ncal_reject={len(rejects)}\n")
        for rj in rejects:
            v.write(f"reject: {rj}\n")
    print("DRY RUN COMPLETE" if not rejects else "DRY RUN SHOWS REJECTS")

if __name__ == "__main__":
    main()
