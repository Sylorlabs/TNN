#!/usr/bin/env python3
"""run_c1scout.py — KB4 C1-scout run glue (PREREG_FROZEN_TCP.md §9).

Python is glue only: file prep, subprocess orchestration, hashing.
Estimation (c1scout_pitch), channel rule (c1scout_channel), and test
counts (score_c1scout) are pure Zag. Zero RNG. truth.json is NEVER
opened here — only by score_c1scout.py at score time.

For each pitchdisc fixture (15 calibration primaries + 15 test
adversarials, from the frozen blob manifest):
  analytic = c1scout_pitch(fixture)        (Zag)
  J        = frozen sense A binary output  (frozen instrument)
  verdict  = c1scout_channel(analytic, J)  (Zag, test rows only)

Writes out_c1scout/runN/{analytic_judgments.txt, calibration.txt,
verdicts.txt}; checks run1/run2 byte-identical (SHA256).

Usage: python3 run_c1scout.py [run_ids...]   (default: 1 2)
"""
import hashlib
import json
import os
import subprocess
import sys

TN = os.path.expanduser("~/workspace/tnn-lab")
CHAN = os.path.join(TN, "kb", "autopsy", "channels2")
FIXROOT = os.path.join(TN, "senses", "rebuild", "harness", "fixtures")
SENSE_A = os.path.join(TN, "senses", "rebuild", "a_raw", "sense")
ANALYTIC = os.path.join(CHAN, "src", "c1scout_pitch")
CHANNEL = os.path.join(CHAN, "src", "c1scout_channel")

SENSE_A_SHA = "68db15216d9dc75a10839212ac5349195248f5ae113a7e37dc336795db8e35a1"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def run_analytic(path):
    q = subprocess.run([ANALYTIC, path], capture_output=True, text=True, timeout=120)
    if q.returncode != 0:
        raise RuntimeError("analytic rc=%d: %s" % (q.returncode, q.stdout.strip()[:200]))
    out = {}
    for line in q.stdout.splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            out[k] = v
    if "judgment" not in out:
        raise RuntimeError("no judgment line: %r" % q.stdout[:200])
    return out["judgment"], out.get("f0_mhz", "?"), out.get("f1_mhz", "?")


def run_sense(path):
    q = subprocess.run([SENSE_A, "pitchdisc", path], capture_output=True, text=True, timeout=1800)
    if q.returncode != 0:
        raise RuntimeError("sense rc=%d: %s" % (q.returncode, q.stdout.strip()[:200]))
    j = None
    for line in q.stdout.splitlines():
        if line.startswith("judgment="):
            j = line[len("judgment="):]
    if j is None:
        raise RuntimeError("no judgment line: %r" % q.stdout[:200])
    return j


def run_channel(analytic, j):
    q = subprocess.run([CHANNEL, analytic, j], capture_output=True, text=True, timeout=60)
    if q.returncode != 0:
        raise RuntimeError("channel rc=%d: %s" % (q.returncode, q.stdout.strip()[:200]))
    v = None
    for line in q.stdout.splitlines():
        if line.startswith("verdict="):
            v = line[len("verdict="):]
    if v not in ("INSTALL", "WITHHOLD"):
        raise RuntimeError("bad verdict: %r" % q.stdout[:200])
    return v


def logical_name(relpath):
    # t4_pitchdisc/primary/p000.pcm -> pitchdisc/p000
    base = os.path.basename(relpath)
    if base.endswith(".pcm"):
        base = base[:-4]
    return "pitchdisc/" + base


def main():
    runs = [int(x) for x in sys.argv[1:]] or [1, 2]
    # Frozen-instrument gate (§1): sense A binary SHA must match.
    got = sha256_file(SENSE_A)
    if got != SENSE_A_SHA:
        raise RuntimeError("sense A SHA mismatch: %s (expected %s) — HALT" % (got, SENSE_A_SHA))
    print("sense A SHA OK: %s" % got[:16])

    man = json.load(open(os.path.join(CHAN, "inputs_tcp", "blob_manifest.json")))
    rows = [r for r in man if r["task"] == "pitchdisc"]
    rows.sort(key=lambda r: (r["split"], r["stim_idx"]))
    cal = [r for r in rows if r["split"] == "calibration"]
    tst = [r for r in rows if r["split"] == "test"]
    assert len(cal) == 15 and len(tst) == 15, (len(cal), len(tst))

    for run in runs:
        outdir = os.path.join(CHAN, "out_c1scout", "run%d" % run)
        os.makedirs(outdir, exist_ok=True)
        aj_path = os.path.join(outdir, "analytic_judgments.txt")
        cal_path = os.path.join(outdir, "calibration.txt")
        ver_path = os.path.join(outdir, "verdicts.txt")
        with open(aj_path, "w") as faj, open(cal_path, "w") as fcal, open(ver_path, "w") as fver:
            for r in cal + tst:
                src = os.path.join(FIXROOT, r["relpath"])
                analytic, f0, f1 = run_analytic(src)
                j = run_sense(src)
                logic = logical_name(r["relpath"])
                faj.write("%s\t%s\tf0_mhz=%s\tf1_mhz=%s\n" % (logic, analytic, f0, f1))
                if r["split"] == "calibration":
                    fcal.write("CAL\tA\tpitchdisc\tprimary\t%s\t%s\t%s\n" % (logic, analytic, j))
                else:
                    v = run_channel(analytic, j)
                    fver.write("TEST\tA\tpitchdisc\tadversarial\t%s\t%s\t%s\t%s\n"
                               % (logic, analytic, j, v))
        print("run%d: %d cal + %d test rows" % (run, len(cal), len(tst)))

    # Byte-identical rerun check.
    if len(runs) >= 2:
        files = ["analytic_judgments.txt", "calibration.txt", "verdicts.txt"]
        ok = True
        for fn in files:
            hs = [sha256_file(os.path.join(CHAN, "out_c1scout", "run%d" % r, fn)) for r in runs]
            same = all(h == hs[0] for h in hs)
            print("%s: %s %s" % (fn, hs[0][:16], "IDENTICAL" if same else "MISMATCH"))
            ok = ok and same
        if not ok:
            raise RuntimeError("rerun byte-identity FAILED — run void")
        print("2x reruns byte-identical: PASS")


if __name__ == "__main__":
    main()
