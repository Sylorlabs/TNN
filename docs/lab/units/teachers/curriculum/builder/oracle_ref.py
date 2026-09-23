#!/usr/bin/env python3
"""oracle_ref.py — reference implementation of the arm-5 oracle answer function.

CORPUS PREP / HARNESS REFERENCE ONLY. Not an AI decision path: a pure,
deterministic function of (slice bytes, inventory, queried span).

ORACLE_ANSWER([s, e)) = YES  iff
  (a) canonical(slice_bytes[s:e]) is in the slice's ground-truth inventory
      unit set, AND
  (b) [s, e) exactly equals a candidate occurrence (start, start+len) from the
      G-V1 extraction pass over the slice bytes.

Notes (all frozen in OPERATIONALIZATION.md §2):
- (b) makes the oracle occurrence-level: querying "the" inside "there" is NO.
- A span exactly covering a candidate occurrence whose unit fell below
  REC_BAR is NO (not inventoried).
- Out-of-range spans are malformed input; the harness rejects them before
  calling this function (never silently answered).
"""
from build_curriculum import scan_prose, scan_code, canonical


def oracle_answer(slice_bytes: bytes, corpus: str, inventory_units: set,
                  s: int, e: int) -> bool:
    if not (0 <= s < e <= len(slice_bytes)):
        raise ValueError("span out of range")
    unit = canonical(slice_bytes[s:e], corpus)
    if unit not in inventory_units:
        return False
    scan = scan_prose(slice_bytes) if corpus == "shakespeare" \
        else scan_code(slice_bytes)
    for (os_, raw) in scan:
        if os_ == s and os_ + len(raw) == e and canonical(raw, corpus) == unit:
            return True
    return False
