#!/usr/bin/env python3
"""Verify vgate hash-chained ledgers and cross-check against gate stdout.

Usage: verify_ledger.py <ledger_path> <gate_stdout_path>

Checks:
  1. Each link: prev_hex matches the previous link's hash (genesis prev = 32 zero bytes).
  2. Each link: hash_hex == sha256(prev_raw32 || canonical_bytes).
  3. Disposition counts in the ledger canonicals match the gate stdout counts.
Prints a one-line verdict; exit 0 iff all checks pass.
"""
import hashlib
import sys
from collections import Counter


def main():
    ledger_path, stdout_path = sys.argv[1], sys.argv[2]
    with open(ledger_path, "rb") as f:
        links = [ln.rstrip(b"\n") for ln in f if ln.strip()]
    prev = bytes(32)
    led_disps = Counter()
    for i, ln in enumerate(links):
        parts = ln.split(b"|", 2)
        assert len(parts) == 3, f"link {i}: bad shape"
        prev_hex, hash_hex, canonical = parts
        assert bytes.fromhex(prev_hex.decode()) == prev, f"link {i}: chain break"
        h = hashlib.sha256(prev + canonical).hexdigest()
        assert h == hash_hex.decode(), f"link {i}: hash mismatch"
        # canonical = record_line|DISP=<d>|DETAIL=<det>
        disp = canonical.split(b"|DISP=")[1].split(b"|DETAIL=")[0].decode()
        led_disps[disp] += 1
        prev = bytes.fromhex(h)
    out_disps = Counter()
    n_out = 0
    with open(stdout_path, "rb") as f:
        for ln in f:
            ln = ln.rstrip(b"\n")
            if not ln:
                continue
            flds = ln.split(b"|")
            assert len(flds) == 6, f"stdout line with {len(flds)} fields"
            out_disps[flds[3].decode()] += 1
            n_out += 1
    assert n_out == len(links), f"count mismatch: stdout={n_out} ledger={len(links)}"
    assert led_disps == out_disps, f"disp mismatch: {led_disps} vs {out_disps}"
    installs = sum(v for k, v in out_disps.items()
                   if k in ("PROVISIONAL_INSTALL", "PERMANENT_INSTALL",
                            "ACCEPT_INSTALL", "REVISE_INSTALL"))
    print(f"OK links={len(links)} chain=valid installs={installs} "
          f"disps={dict(sorted(out_disps.items()))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
