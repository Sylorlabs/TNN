#!/usr/bin/env python3
"""RSI-8 Round 2 (R5) build: assemble + compile all five TNN binaries.

Assembly (identical prelude convention): build/tables_gen.zag +
src/policy_engine.zag.inc + src/<name>.zag -> work/r5/<name>_full.zag,
then compile with the pinned toolchain into work/r5/<bin>.

Binaries: afdisc, deliberation (adaptive D1, RUN_PREREG5), proposer,
subject, problems (D-PROBLEMS scan + adaptive deliberation, new).
"""
import subprocess, sys, os

BASE = os.path.expanduser("~/workspace/tnn-lab/rsi/autonomous_run_2")
ZNC = os.path.expanduser("~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1")
R5 = f"{BASE}/work/r5"
os.makedirs(R5, exist_ok=True)

BINARIES = {
    "afdisc": "afdisc",
    "deliberation": "deliberation",
    "proposer": "proposer",
    "subject": "subject",
    "problems": "problems",
}

def build(name, srcfile):
    full = f"{R5}/{name}_full.zag"
    tg = open(f"{BASE}/build/tables_gen.zag").read()
    inc = open(f"{BASE}/src/policy_engine.zag.inc").read()
    src = open(f"{BASE}/src/{srcfile}").read()
    open(full, "w").write(tg + inc + src)
    out = f"{R5}/{BINARIES[name]}"
    r = subprocess.run([ZNC, full, "-o", out], capture_output=True, text=True)
    if r.returncode != 0:
        print(f"BUILD FAIL {name}:\n{r.stderr[-3000:]}")
        return False
    print(f"built {out} ({os.path.getsize(out)} bytes)")
    return True

ok = True
which = sys.argv[1:] or list(BINARIES)
for name in which:
    if not build(name, f"{name}.zag"):
        ok = False
sys.exit(0 if ok else 1)
