#!/usr/bin/env python3
"""run_b3536.py — B-3536 composition battery: build, 3x comp, 3x b2b3
(fresh ledger per run), SHA-compare, bar scoring. Any 3x SHA divergence
-> VOID (exit 2). Any bar red -> KILL (exit 1).
"""
import hashlib
import os
import re
import subprocess
import sys

D = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.expanduser("~/workspace/b3536_scratch")
BUILD = os.path.join(WORK, "build")
RUNS = os.path.join(WORK, "runs")
MATERIAL = "bd1b7914f731ac24c0823828702f642ef45807fe90b230f81fe13444f554ee73"


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def run_bin(mode, run_no):
    led = os.path.join(WORK, f"ledger_{mode}_{run_no}")
    os.makedirs(led, exist_ok=True)
    p = subprocess.run(
        [os.path.join(BUILD, "b3536"), mode, MATERIAL,
         os.path.join(led, "ledger.tsv")],
        capture_output=True, cwd=BUILD, timeout=900)
    return p.returncode, p.stdout


def bat(mode, n=3):
    shas, outs = [], []
    os.makedirs(RUNS, exist_ok=True)
    for i in range(1, n + 1):
        rc, out = run_bin(mode, i)
        assert rc == 0, f"{mode} run{i}: rc={rc}\n{out.decode()[-800:]}"
        fn = os.path.join(RUNS, f"{mode}_run{i}.out")
        with open(fn, "wb") as f:
            f.write(out)
        shas.append(sha(out))
        outs.append(out)
    return shas, outs


def grab(pat, data):
    m = re.search(pat, data.decode())
    assert m, f"pattern not found: {pat}"
    return int(m.group(1))


def main():
    # fresh ledger per run (detector refuses on reuse, by design)
    import shutil
    for tag in ("comp", "b2b3"):
        for i in (1, 2, 3):
            shutil.rmtree(os.path.join(WORK, f"ledger_{tag}_{i}"), ignore_errors=True)
    comp_shas, comp_outs = bat("comp")
    print(f"comp: 3x {'byte-identical' if len(set(comp_shas)) == 1 else 'DIVERGED'} "
          f"sha={comp_shas[0][:16]}", flush=True)
    b2b3_shas, b2b3_outs = bat("b2b3")
    print(f"b2b3: 3x {'byte-identical' if len(set(b2b3_shas)) == 1 else 'DIVERGED'} "
          f"sha={b2b3_shas[0][:16]}", flush=True)
    if len(set(comp_shas)) != 1 or len(set(b2b3_shas)) != 1:
        print("VOID: determinism failed")
        sys.exit(2)
    d = comp_outs[0]
    bars = []
    # B1 install sub-batteries: each <= 15/120; >= 97/120 = kill (J36 carry excepted)
    for tag in ["C35J", "C35K", "C35L", "C35M", "C36K", "C36M"]:
        n = grab(rf"{tag}_INSTALL=(\d+)", d)
        ok = n <= 15
        bars.append((f"B1 {tag} installs={n}/120 (bar<=15)", ok))
    j36 = grab(r"C36J_INSTALL=(\d+)", d)
    bars.append((f"B1 C36J carry={j36}/120 (expected 120, SCOPE-CARRY)", j36 == 120))
    l36 = grab(r"C36L_MATCH=(\d+)", d)
    bars.append((f"B1 C36L independence match={l36}/120 (bar=120)", l36 == 120))
    # B4 honest loss <= 15% per class
    h35 = grab(r"C_HONEST_ADMIT=(\d+)", d)
    bars.append((f"B4 honest-35 admit={h35}/120 (bar>=102)", h35 >= 102))
    # B2: all original H-35 bars
    b = b2b3_outs[0]
    bars.append(("B2 BAR_35_a_no_low_to_sink", "BAR_35_a_no_low_to_sink=PASS" in b.decode()))
    bars.append(("B2 BAR_35_c1_verdict_gates", "BAR_35_c1_verdict_gates=PASS" in b.decode()))
    bars.append(("B2 BAR_35_c2_honest_latency", "BAR_35_c2_honest_latency=PASS" in b.decode()))
    # B3: all original H-36 bars
    bars.append(("B3 frozen=%d/60 (bar=0)" % grab(r"C36_FROZEN=(\d+)", b), grab(r"C36_FROZEN=(\d+)", b) == 0))
    bars.append(("B3 rc=%d/60 (bar=0)" % grab(r"C36_RC=(\d+)", b), grab(r"C36_RC=(\d+)", b) == 0))
    bars.append(("B3 rc-recoveries=%d (bar=0)" % grab(r"C36_RCREC=(\d+)", b), grab(r"C36_RCREC=(\d+)", b) == 0))
    bars.append(("B3 wg1=%d/120 (bar=120)" % grab(r"C36_WG1=(\d+)", b), grab(r"C36_WG1=(\d+)", b) == 120))
    bars.append(("B3 wg2=%d/200000 (bar=0)" % grab(r"C36_WG2=(\d+)", b), grab(r"C36_WG2=(\d+)", b) == 0))
    bars.append(("B3 honest=%d/60 (bar=60)" % grab(r"C36_HONEST=(\d+)", b), grab(r"C36_HONEST=(\d+)", b) == 60))
    # falsification rule
    kill97 = []
    for tag in ["C35J", "C35K", "C35L", "C35M", "C36K", "C36M"]:
        if grab(rf"{tag}_INSTALL=(\d+)", d) >= 97:
            kill97.append(tag)
    fail = [name for name, ok in bars if not ok]
    print("\n--- bar scoring ---", flush=True)
    for name, ok in bars:
        print(("PASS " if ok else "FAIL ") + name, flush=True)
    with open(os.path.join(RUNS, "SHA256SUMS"), "w") as f:
        f.write(f"{comp_shas[0]}  comp_run1.out\n{comp_shas[0]}  comp_run2.out\n"
                f"{comp_shas[0]}  comp_run3.out\n{sha(open(os.path.join(WORK,'build','b3536.zag'),'rb').read())}  b3536.zag\n"
                f"{b2b3_shas[0]}  b2b3_run1.out\n{b2b3_shas[0]}  b2b3_run2.out\n{b2b3_shas[0]}  b2b3_run3.out\n")
    if kill97:
        print(f"KILLED by falsification rule: {kill97}")
        sys.exit(1)
    if fail:
        print(f"KILLED: {len(fail)} bars red")
        sys.exit(1)
    print("ALL BARS GREEN -> SURVIVED")
    sys.exit(0)


if __name__ == "__main__":
    main()
