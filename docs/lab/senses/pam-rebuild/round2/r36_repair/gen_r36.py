#!/usr/bin/env python3
"""R-36 generator: extract the M-36 fixture class from rt_jklm/drive36.zag and
emit r36_probe.zag from r36_harness.tmpl.

The M-36 fixture class (per PREREG_R36 §5) = drive36.zag::run_m parameters:
  - attacker seed (whi, wlo) hardcoded in run_m
  - trial count (precompute loop bound)
  - id base (in-run phase)
Extracted by regex and ASSERTED against the documented class values; any drift
fails loudly instead of silently generating a different fixture class.
"""
import re
import sys
import hashlib
import shutil
import os

WORK = os.path.expanduser("~/workspace/r36_repair")
TNNLAB = os.path.expanduser("~/workspace/tnn-lab")
DRIVE36 = os.path.join(TNNLAB, "senses/pam-rebuild/round2/rt_jklm/drive36.zag")
TMPL = os.path.join(WORK, "r36_harness.tmpl")
OUT = os.path.join(WORK, "r36_probe.zag")

PREREG_SHA = "506fc0927100e76b3d1c00874dfe42239c6bef63"

# documented M-36 class values (PREREG_R36 §5 / RT-JKLM verdict)
EXP_SEED_HI = "305419896"
EXP_SEED_LO = "2596069104"
EXP_TRIALS = "120"
EXP_IDBASE = "8000"


def extract_run_m(src):
    # isolate run_m body: from "fn run_m(" to the next top-level "fn "
    m = re.search(r"fn run_m\(bs:\[\]u8\) void \{(.*?)\n\}\n\nfn ", src, re.S)
    assert m, "run_m not found in drive36.zag"
    body = m.group(1)
    seed_hi = re.search(r"let whi:u64 = (\d+);", body).group(1)
    seed_lo = re.search(r"let wlo:u64 = (\d+);", body).group(1)
    trials = re.search(r"while\(t < (\d+)\)", body).group(1)
    idbase = re.search(r"let id:i64 = (\d+) \+ t;", body).group(1)
    return seed_hi, seed_lo, trials, idbase


def main():
    with open(DRIVE36) as f:
        src = f.read()
    seed_hi, seed_lo, trials, idbase = extract_run_m(src)
    print(f"extracted M-36 class: seed=({seed_hi},{seed_lo}) trials={trials} idbase={idbase}")
    assert seed_hi == EXP_SEED_HI, f"seed_hi drift: {seed_hi}"
    assert seed_lo == EXP_SEED_LO, f"seed_lo drift: {seed_lo}"
    assert trials == EXP_TRIALS, f"trials drift: {trials}"
    assert idbase == EXP_IDBASE, f"idbase drift: {idbase}"
    print("M-36 fixture class params match the documented class (no drift).")

    with open(TMPL) as f:
        tmpl = f.read()
    for ph in ("{PREREG_SHA}", "{M36A_SEED_HI}", "{M36A_SEED_LO}",
               "{M36A_TRIALS}", "{M36A_IDBASE}"):
        assert ph in tmpl, f"placeholder {ph} missing from template"
    out = tmpl.replace("{PREREG_SHA}", PREREG_SHA)
    out = out.replace("{M36A_SEED_HI}", seed_hi)
    out = out.replace("{M36A_SEED_LO}", seed_lo)
    out = out.replace("{M36A_TRIALS}", trials)
    out = out.replace("{M36A_IDBASE}", idbase)
    assert re.search(r"\{[A-Z0-9_]+\}", out) is None, "unsubstituted placeholder remains"
    with open(OUT, "w") as f:
        f.write(out)
    h = hashlib.sha256(out.encode()).hexdigest()
    print(f"wrote {OUT}: {len(out)} bytes, sha256={h}")

    # substrate copies next to the probe (import resolves relative to importer)
    for name in ("R33_NATIVE_SHA256_V2.zag", "R33_NATIVE_IO_V1.zag"):
        srcp = os.path.join(TNNLAB, "toolchain", name)
        dstp = os.path.join(WORK, name)
        shutil.copyfile(srcp, dstp)
        print(f"copied substrate {name}")


if __name__ == "__main__":
    main()
