#!/usr/bin/env python3
"""R-36 battery runner: build, 3x batt, 3x m36, seed-reuse detector test, SHA-compare."""
import hashlib
import os
import subprocess
import sys

WORK = os.path.expanduser("~/workspace/r36_repair")
ZNC = os.path.expanduser("~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1")
MATERIAL = "bd1b7914f731ac24c0823828702f642ef45807fe90b230f81fe13444f554ee73"
RUNS = os.path.join(WORK, "runs")


def sha(b):
    return hashlib.sha256(b).hexdigest()


def run_bin(args, ledger_dir):
    os.makedirs(ledger_dir, exist_ok=True)
    ledger = os.path.join(ledger_dir, "ledger.tsv")
    p = subprocess.run(
        [os.path.join(WORK, "r36_probe")] + args + [MATERIAL, ledger],
        capture_output=True, cwd=WORK, timeout=900)
    return p.returncode, p.stdout, ledger


def main():
    os.makedirs(RUNS, exist_ok=True)
    # build
    print("== build ==", flush=True)
    b = subprocess.run([ZNC, "r36_probe.zag", "-o", "r36_probe"],
                       capture_output=True, text=True, cwd=WORK, timeout=600)
    print(b.stdout[-500:] if b.stdout else "", flush=True)
    print(b.stderr[-500:] if b.stderr else "", flush=True)
    assert os.path.exists(os.path.join(WORK, "r36_probe")), "build failed"

    sums = []
    # batt 3x, fresh ledger per run
    batt_shas = []
    for i in (1, 2, 3):
        rc, out, ledger = run_bin(["batt"], os.path.join(WORK, f"batt_run{i}"))
        assert rc == 0, f"batt run{i}: rc={rc}\n{out.decode()[-800:]}"
        fn = os.path.join(RUNS, f"batt_{i}.txt")
        with open(fn, "wb") as f:
            f.write(out)
        h = sha(out)
        batt_shas.append(h)
        sums.append(f"{h}  batt_{i}.txt")
        print(f"batt run{i}: rc=0 sha={h[:16]} ledger={ledger}", flush=True)
    assert batt_shas[0] == batt_shas[1] == batt_shas[2], "batt NOT byte-identical"
    print("batt: 3x byte-identical", flush=True)

    # m36 3x, fresh ledger per run
    m36_shas = []
    for i in (1, 2, 3):
        rc, out, ledger = run_bin(["m36"], os.path.join(WORK, f"m36_run{i}"))
        assert rc == 0, f"m36 run{i}: rc={rc}\n{out.decode()[-800:]}"
        fn = os.path.join(RUNS, f"m36_{i}.txt")
        with open(fn, "wb") as f:
            f.write(out)
        h = sha(out)
        m36_shas.append(h)
        sums.append(f"{h}  m36_{i}.txt")
        print(f"m36 run{i}: rc=0 sha={h[:16]} ledger={ledger}", flush=True)
    assert m36_shas[0] == m36_shas[1] == m36_shas[2], "m36 NOT byte-identical"
    print("m36: 3x byte-identical", flush=True)

    # detector test: repeat batt with the SAME ledger as batt_run1
    print("== seed-reuse detector test ==", flush=True)
    rc, out, ledger = run_bin(["batt"], os.path.join(WORK, "batt_run1"))
    fn = os.path.join(RUNS, "reuse_refusal.txt")
    with open(fn, "wb") as f:
        f.write(out)
    sums.append(f"{sha(out)}  reuse_refusal.txt")
    txt = out.decode()
    print(f"reuse run: rc={rc}", flush=True)
    print(txt, flush=True)
    assert rc != 0, "detector test FAILED: repeated seed did not refuse (rc=0)"
    assert "REFUSED_SEED_REUSE" in txt, "detector test FAILED: no loud refusal"
    assert "R36_BATT_DONE" not in txt, "detector test FAILED: battery ran despite reuse"
    print("detector: loud refusal confirmed", flush=True)

    with open(os.path.join(RUNS, "SHA256SUMS"), "w") as f:
        f.write("\n".join(sums) + "\n")
    print("wrote runs/SHA256SUMS", flush=True)


if __name__ == "__main__":
    main()
