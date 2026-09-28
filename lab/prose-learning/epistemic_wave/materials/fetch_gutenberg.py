#!/usr/bin/env python3
"""Fetch Project Gutenberg plain texts for the leg-(e) corpus (2026-09-22).

Deterministic network fetch stage. Walks Gutenberg ebook IDs in strictly
ascending order starting at --start-id, downloads the plain-text edition
https://www.gutenberg.org/cache/epub/{id}/pg{id}.txt, keeps the text only
if it is English-language (parsed from the Project Gutenberg header's
"Language:" line), and saves the RAW response bytes unmodified to
{outdir}/{id:06d}.txt. Stops after --target-texts English texts are saved.

No RNG, no shuffle, no seed anywhere. Retries are a fixed count (3) with
no backoff jitter. The fetch log records id, byte count, and sha256 of
the saved bytes so the sampler stage (and anyone re-running it) can
verify inputs byte-identically.

Usage:
  python3 fetch_gutenberg.py --start-id 1 --target-texts 25 \
      --outdir materials/gutenberg_raw --log materials/gutenberg_raw/fetch_log.txt
"""

import argparse
import hashlib
import os
import sys
import urllib.request
import urllib.error

BASE = "https://www.gutenberg.org/cache/epub/{eid}/pg{eid}.txt"
RETRIES = 3
TIMEOUT_S = 90


def fetch_bytes(url):
    last = None
    for _ in range(RETRIES):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "TNN-lab-corpus/1.0"})
            with urllib.request.urlopen(req, timeout=TIMEOUT_S) as r:
                return r.read()
        except Exception as e:  # noqa: BLE001 - fixed retry count, deterministic
            last = e
    raise last


def header_is_english(raw: bytes) -> bool:
    # Parse the Project Gutenberg header (everything before the START marker)
    # for a "Language:" line. Require it to name English.
    head = raw[:20000].decode("utf-8", errors="replace")
    for line in head.splitlines():
        if line.startswith("*** START OF"):
            break
        low = line.strip().lower()
        if low.startswith("language:"):
            return "english" in low
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start-id", type=int, default=1)
    ap.add_argument("--target-texts", type=int, default=25)
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--log", required=True)
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    kept = 0
    eid = args.start_id
    # Safety bound: never scan more than 20000 IDs for a batch.
    log_lines = []
    while kept < args.target_texts and eid < args.start_id + 20000:
        url = BASE.format(eid=eid)
        try:
            raw = fetch_bytes(url)
        except Exception as e:  # noqa: BLE001
            log_lines.append(f"{eid}\tFETCH_FAIL\t{type(e).__name__}")
            eid += 1
            continue
        if not header_is_english(raw):
            log_lines.append(f"{eid}\tSKIP_NONENGLISH\t{len(raw)}")
            eid += 1
            continue
        sha = hashlib.sha256(raw).hexdigest()
        path = os.path.join(args.outdir, f"{eid:06d}.txt")
        with open(path, "wb") as f:
            f.write(raw)
        log_lines.append(f"{eid}\tOK\t{len(raw)}\t{sha}")
        kept += 1
        eid += 1

    with open(args.log, "w", encoding="utf-8") as f:
        f.write("# fetch_gutenberg.py log, 2026-09-22. Columns: ebook_id, status, bytes, sha256.\n")
        f.write(f"# start_id={args.start_id} target_texts={args.target_texts} kept={kept}\n")
        f.write("\n".join(log_lines) + "\n")
    print(f"kept={kept} log={args.log}")
    return 0 if kept >= args.target_texts else 1


if __name__ == "__main__":
    sys.exit(main())
