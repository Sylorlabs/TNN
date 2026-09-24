#!/usr/bin/env python3
"""LI-HARDEN round-3 Crew C driver: runs the quarantine battery.
- Admission battery: every fixture x every crawl window W, twice (byte-identical check).
- Exit battery: every exit fixture twice.
- Emits TSVs + summary. The decision path is the pure-Zag binary; this is plumbing.
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BIN = os.path.join(HERE, "quarantine_bin")
FIX = os.path.join(HERE, "fixtures")
FIXX = os.path.join(HERE, "fixtures_exit")

WINDOWS = [0, 1, 2, 4, 8, 16, 32, 64, 128, 999999]

def run(bin_args, bundle_path):
    with open(bundle_path, "rb") as f:
        data = f.read()
    p = subprocess.run([BIN] + bin_args, input=data, capture_output=True, timeout=120)
    if p.returncode != 0:
        raise RuntimeError(f"binary rc={p.returncode} args={bin_args} stderr={p.stderr[:200]}")
    return p.stdout.decode()

def verdict_of(out):
    for l in out.split("\n"):
        if l.startswith("V|quarantine|admit|"):
            return l.split("|")[4]
        if l.startswith("X|quarantine|exit|"):
            return l.split("|")[4]
    return "NO_VERDICT"

def main():
    cases = sorted(os.listdir(FIX))
    # ---- admission sweep ----
    admit_rows = []  # (case, window, rep, verdict, raw)
    det_ok = True
    for case in cases:
        bundle = os.path.join(FIX, case, "bundle.txt")
        for w in WINDOWS:
            outs = [run(["admit", str(w)], bundle) for _ in range(2)]
            if outs[0] != outs[1]:
                det_ok = False
                print(f"NONDETERMINISM: {case} W={w}", file=sys.stderr)
            v = verdict_of(outs[0])
            admit_rows.append((case, w, v))
    with open(os.path.join(HERE, "results_admit.tsv"), "w") as f:
        f.write("case\twindow\tverdict\n")
        for case, w, v in admit_rows:
            f.write(f"{case}\t{w}\t{v}\n")

    # ---- expected verdicts at full window ----
    kinds = {}
    for case in cases:
        with open(os.path.join(FIX, case, "kind.txt")) as fh:
            kinds[case] = fh.read().strip()
    full = {c: v for c, w, v in admit_rows if w == 999999}
    expect = {}
    for c in cases:
        if c == "W_S3":
            expect[c] = "QUARANTINED"
        elif c in ("Q_NQ", "Q_G1"):
            expect[c] = "WITHHOLD"
        else:
            expect[c] = "INSTALL"
    battery_ok = True
    for c in cases:
        if full[c] != expect[c]:
            battery_ok = False
            print(f"BATTERY MISS: {c} got {full[c]} expected {expect[c]}", file=sys.stderr)

    # ---- window tradeoff curve (fable's question) ----
    # honest set = cases expected to INSTALL at full window (kind FACT minus Q_NQ)
    honest = [c for c in cases if expect.get(c) == "INSTALL"]
    curve = []
    for w in WINDOWS:
        m = {c: v for c, ww, v in admit_rows if ww == w}
        fq = sum(1 for c in honest if m[c] == "QUARANTINED")
        curve.append((w, fq, len(honest), m.get("W_S3", "?")))
    with open(os.path.join(HERE, "results_window.tsv"), "w") as f:
        f.write("window\tfalse_quarantined\thonest_total\tfalse_q_rate\tw_s3\tpoisonable_surface_pages\n")
        for w, fq, n, ws3 in curve:
            f.write(f"{w}\t{fq}\t{n}\t{fq/n:.4f}\t{ws3}\t{w}\n")

    # ---- exit battery ----
    xcases = sorted(os.listdir(FIXX))
    xdet_ok = True
    xok = True
    with open(os.path.join(HERE, "results_exit.tsv"), "w") as f:
        f.write("case\texpect\tgot\tpass\n")
        for case in xcases:
            bundle = os.path.join(FIXX, case, "bundle.txt")
            outs = [run(["exit"], bundle) for _ in range(2)]
            if outs[0] != outs[1]:
                xdet_ok = False
                print(f"NONDETERMINISM(exit): {case}", file=sys.stderr)
            got = verdict_of(outs[0])
            exp = open(os.path.join(FIXX, case, "expect.txt")).read().strip()
            ok = "PASS" if got == exp else "FAIL"
            if ok == "FAIL":
                xok = False
                print(f"EXIT MISS: {case} got {got} expected {exp}", file=sys.stderr)
            f.write(f"{case}\t{exp}\t{got}\t{ok}\n")

    # ---- summary ----
    print("=== QUARANTINE BATTERY SUMMARY ===")
    print(f"determinism admit: {'OK' if det_ok else 'FAIL'}; exit: {'OK' if xdet_ok else 'FAIL'}")
    print(f"admission battery @full window: {'PASS' if battery_ok else 'FAIL'} "
          f"({sum(1 for c in cases if full[c]==expect[c])}/{len(cases)})")
    print(f"exit battery: {'PASS' if xok else 'FAIL'} ({len(xcases)} cases)")
    print("--- crawl-window tradeoff (fable's question) ---")
    print("W\tfalseQ\thonest\tFQR\tW_S3\tsurface")
    for w, fq, n, ws3 in curve:
        print(f"{w}\t{fq}\t{n}\t{fq/n:.3f}\t{ws3}\t{w}")
    # per-case flip depth
    print("--- flip depth (W at which each honest case first INSTALLs) ---")
    for c in honest:
        fd = next((w for w in WINDOWS
                   if next(v for cc, ww, v in admit_rows if cc == c and ww == w) == "INSTALL"),
                  None)
        print(f"{c}\t{fd}")

if __name__ == "__main__":
    main()
