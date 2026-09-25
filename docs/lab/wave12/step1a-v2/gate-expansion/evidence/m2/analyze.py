#!/usr/bin/env python3
"""Analyze M2 battery results: per-module verdicts, K-CATCH, K-DET."""
import os, re, hashlib, sys

E2M = os.path.expanduser("~/workspace/tnn-lab/wave12/step1a-v2/gate-expansion/evidence/m2")
MODULES = ["p01_getrandom","p02_clock","p03_urandom","p04_uninit","p05_envflag",
           "p06_aslr","p07_rdtsc","p08_hashorder","p09_innocent_tables",
           "p10_machineid","p11_argv","p12_invoke_discard",
           "c01_clean","c02_phrasing","c03_seeded","c04_fileio",
           "c05_instrcount","c06_fixedmap"]
ROUNDS = ["r1","r2","r3"]
CATCH_SET = ["p01_getrandom","p02_clock","p03_urandom","p04_uninit","p05_envflag",
             "p06_aslr","p07_rdtsc","p08_hashorder","p09_innocent_tables","p11_argv"]
CLEAN = ["c01_clean","c02_phrasing","c03_seeded","c04_fileio","c05_instrcount","c06_fixedmap"]

def parse(mod, rnd):
    p = f"{E2M}/runs/{rnd}/{mod}.driver.log"
    if not os.path.exists(p):
        return None
    log = open(p).read()
    verdict = re.search(r"M2-VERDICT (\S+) (PASS|FAIL)", log)
    hashes = re.findall(r"^hash (\d+) ([0-9a-f]{64}) len=(\d+) class=(\d+)", log, re.M)
    div = re.search(r"div_runs=([\d,]+)", log)
    fdo = re.search(r"first_diff_vs_run0_at=(\d+)", log)
    return {"verdict": verdict.group(2) if verdict else "MISSING",
            "hashes": hashes,
            "div": div.group(1) if div else "",
            "fdo": fdo.group(1) if fdo else ""}

res = {rnd: {m: parse(m, rnd) for m in MODULES} for rnd in ROUNDS}
have = [r for r in ROUNDS if res[r]["p01_getrandom"] is not None]

print("=== per-module verdicts (r1) ===")
for m in MODULES:
    p = res["r1"][m]
    print(f"{m:20s} {p['verdict']:4s} div={p['div'] or '-':40s} fdo={p['fdo'] or '-'}")

print("\n=== K-CATCH (denominator 10) ===")
# Counting rule (frozen): FAIL on a dirty plant = CAUGHT; P09 must PASS
# (correctly-passed counts); P08 AT-RISK counts normally.
caught = [m for m in CATCH_SET if res["r1"][m]["verdict"] == "FAIL"]
p09_ok = res["r1"]["p09_innocent_tables"]["verdict"] == "PASS"
p08_miss = res["r1"]["p08_hashorder"]["verdict"] == "PASS"  # dirty but passed
kcatch = len(caught) + (1 if p09_ok else 0)
print(f"caught dirty: {len(caught)}/8: {caught}")
print(f"P09 correct-pass: {p09_ok}")
print(f"P08 AT-RISK miss: {p08_miss}")
print(f"K-CATCH: {kcatch}/10")

if len(have) == 3:
    print("\n=== K-DET: clean-control schedule reports byte-identical r1==r2==r3 ===")
    det_ok = 0
    for m in CLEAN:
        logs = [open(f"{E2M}/runs/{rnd}/{m}.driver.log","rb").read() for rnd in ROUNDS]
        same = logs[0] == logs[1] == logs[2]
        print(f"{m:16s} {'IDENTICAL 3/3' if same else 'DIFFER'}")
        det_ok += same
    print(f"K-DET: {det_ok}/6 clean controls byte-identical across 3 rounds")

    print("\n=== cross-round verdict stability ===")
    for m in MODULES:
        vs = [res[r][m]["verdict"] for r in ROUNDS]
        if len(set(vs)) > 1:
            print(f"{m}: {vs}  <-- UNSTABLE")
else:
    print(f"\n(K-DET needs r1/r2/r3; have: {have})")

print("\n=== expected-outcome check ===")
expect = {"p01_getrandom":"FAIL","p02_clock":"FAIL","p03_urandom":"FAIL",
          "p04_uninit":"FAIL","p05_envflag":"FAIL","p06_aslr":"FAIL",
          "p07_rdtsc":"FAIL","p08_hashorder":"PASS","p09_innocent_tables":"PASS",
          "p11_argv":"FAIL",
          "c01_clean":"PASS","c02_phrasing":"PASS","c03_seeded":"PASS",
          "c04_fileio":"PASS","c05_instrcount":"PASS","c06_fixedmap":"PASS"}
bad = [(m, res["r1"][m]["verdict"], e) for m, e in expect.items()
       if res["r1"][m]["verdict"] != e]
print("mismatches vs frozen expectation:", bad if bad else "NONE")
