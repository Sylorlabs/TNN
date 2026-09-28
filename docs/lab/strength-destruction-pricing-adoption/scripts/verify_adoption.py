#!/usr/bin/env python3
"""Verify the adopted deliberative-pricing sources.

Checks that strength_core.zag and strength_checker.zag contain all required
adopted elements (constants, functions, personality fail-closed logic) and
reports SHA256 for the evidence manifest. Deterministic; no network; no RNG.
"""
import hashlib, os, sys

SRC = os.path.dirname(os.path.abspath(__file__)) + "/../src"

REQUIRED_CORE = [
    "ST_OP_DELIBERATE=23",
    "ST_PRICE_DELIB=5",
    "ST_DELIB_HIST=1",
    "ST_DELIB_FRESH=2",
    "fn st_deliberate(",
    "fn st_deliberate_dryrun(",
    "fn st_delib_ncites(",
    "fn st_delib_maxjustify(",
    "fn st_delib_reason(",
    "fn st_deliberation_price(",
    "fn st_price(",
    "ST_REFUSED_NODELIB",
    "delib_pers",
    "price_mode",
]

REQUIRED_CHECKER = [
    "fn ck_verify_deliberate(",
    "fn ck_verify_delib_binding(",
    "ST_OP_DELIBERATE",
    "ST_PRICE_DELIB",
]

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

def main():
    fails = 0
    core = open(os.path.join(SRC, "strength_core.zag")).read()
    checker = open(os.path.join(SRC, "strength_checker.zag")).read()
    for token in REQUIRED_CORE:
        if token not in core:
            print(f"FAIL core missing: {token}")
            fails += 1
    for token in REQUIRED_CHECKER:
        if token not in checker:
            print(f"FAIL checker missing: {token}")
            fails += 1
    # personality fail-closed: st_price must compare recorded pers to current
    if "st_aw(s,di,3)==s.*.delib_pers" not in core:
        print("FAIL core: personality binding check not found in st_price")
        fails += 1
    if "st_aw(s,di,3)==s.*.delib_pers" not in checker:
        print("FAIL checker: personality binding check not found")
        fails += 1
    print(f"core SHA256:   {sha256(os.path.join(SRC, 'strength_core.zag'))}")
    print(f"checker SHA256: {sha256(os.path.join(SRC, 'strength_checker.zag'))}")
    if fails == 0:
        print("VERIFY_ADOPTION PASS")
    else:
        print(f"VERIFY_ADOPTION FAIL ({fails})")
    return 1 if fails else 0

if __name__ == "__main__":
    sys.exit(main())
