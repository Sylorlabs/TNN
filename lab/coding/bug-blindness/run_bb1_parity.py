#!/usr/bin/env python3
"""Q1 parity battery runner: 38 items, 5 reps, byte-identical outputs.
Bars: KB-D1C (parity rate over 24 parity items, >=0.85),
      KB-D1 (>=0.70 detection over 30 buggy, <=0.25 false alarms over 8 clean),
      KB-D2 (class precision >=0.60 over detected buggy)."""
import subprocess, hashlib, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
INSPECT = os.path.join(BASE, "inspect")
BAT = os.path.join(BASE, "battery", "parity")
KEY = os.path.join(BAT, "answer_key_parity.txt")
LOG = os.path.join(BASE, "logs")

PARITY_CLASSES = ["E0001","E0002","E0010","E0203","UNKNOWN-IDENT","UNKNOWN-FN",
                  "ARITY","DUP-FN","DUP-TYPE","UNKNOWN-FIELD","NO-MAIN","BAD-INDEX"]

def load_key():
    d = {}
    with open(KEY) as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            name, verdict = line.split(" ", 1)
            d[name] = verdict
    return d

def run_rep(rep):
    out = []
    names = sorted(n[:-4] for n in os.listdir(BAT) if n.endswith(".zag"))
    for name in names:
        p = subprocess.run([INSPECT, os.path.join(BAT, name + ".zag")],
                           capture_output=True, text=True, timeout=30)
        out.append(name + " " + p.stdout.strip())
    blob = "\n".join(out) + "\n"
    with open(os.path.join(LOG, "bb1_parity_rep%d.out" % rep), "w") as f:
        f.write(blob)
    return blob

def main():
    key = load_key()
    assert len(key) == 38, "key must have 38 entries, has %d" % len(key)
    blobs = [run_rep(r) for r in range(1, 6)]
    digests = [hashlib.sha256(b.encode()).hexdigest() for b in blobs]
    with open(os.path.join(LOG, "bb1_parity_digests.txt"), "w") as f:
        for r, d in enumerate(digests, 1):
            f.write("rep%d %s\n" % (r, d))
    det = len(set(digests)) == 1
    print("five-rep digests identical:", det)
    for r, d in enumerate(digests, 1):
        print("  rep%d" % r, d)

    lines = blobs[0].rstrip("\n").split("\n")
    got = {}
    for line in lines:
        name, verdict = line.split(" ", 1)
        got[name] = verdict

    # per-class parity table
    print("\n== KB-D1C parity (24 items, 12 classes x2) ==")
    print("%-14s %6s %6s" % ("class", "hit", "n"))
    par_hits = 0
    par_n = 0
    gaps = []
    for cls in PARITY_CLASSES:
        members = [n for n in key if n.startswith("p") and key[n].split()[1] == cls]
        h = sum(1 for n in members if got[n] == key[n])
        par_hits += h
        par_n += len(members)
        print("%-14s %6d %6d" % (cls, h, len(members)))
        if h < len(members):
            gaps.append((cls, h, len(members),
                         [(n, key[n], got[n]) for n in members if got[n] != key[n]]))
    parity_rate = par_hits / par_n
    print("parity rate: %d/%d = %.4f  (bar >= 0.85)" % (par_hits, par_n, parity_rate))
    print("KB-D1C:", "PASS" if parity_rate >= 0.85 else "FAIL")
    for cls, h, n, det_items in gaps:
        print("  GAP %s %d/%d:" % (cls, h, n))
        for name, exp, g in det_items:
            print("    %s expected %s got %s" % (name, exp, g))

    # KB-D1: detection over 30 buggy, false alarms over 8 clean
    buggy = [n for n in key if key[n] != "CLEAN"]
    clean = [n for n in key if key[n] == "CLEAN"]
    detected = sum(1 for n in buggy if got[n].startswith("BUG"))
    fa = sum(1 for n in clean if got[n] != "CLEAN")
    det_rate = detected / len(buggy)
    fa_rate = fa / len(clean)
    print("\n== KB-D1 full battery (38) ==")
    print("detection: %d/%d = %.4f (bar >= 0.70)" % (detected, len(buggy), det_rate))
    print("false alarms: %d/%d = %.4f (bar <= 0.25)" % (fa, len(clean), fa_rate))
    print("KB-D1:", "PASS" if (det_rate >= 0.70 and fa_rate <= 0.25) else "FAIL")

    # KB-D2: class precision over detected buggy
    class_ok = sum(1 for n in buggy if got[n].startswith("BUG") and got[n] == key[n])
    prec = class_ok / detected if detected else 0.0
    print("\n== KB-D2 class precision ==")
    print("exact class+line: %d/%d detected = %.4f (bar >= 0.60)" % (class_ok, detected, prec))
    print("KB-D2:", "PASS" if prec >= 0.60 else "FAIL")

    # stretch table
    print("\n== stretch (6, beyond-compiler) ==")
    for n in sorted(k for k in key if k.startswith("s")):
        mark = "OK " if got[n] == key[n] else "MISS"
        print("  %s %-4s expected %-22s got %s" % (n, mark, key[n], got[n]))

    # misses / false alarms detail
    print("\n== misses ==")
    for n in sorted(buggy):
        if not got[n].startswith("BUG"):
            print("  %s expected %s got %s" % (n, key[n], got[n]))
    print("== false alarms ==")
    for n in sorted(clean):
        if got[n] != "CLEAN":
            print("  %s got %s" % (n, got[n]))
    print("== class errors (detected, wrong class/line) ==")
    for n in sorted(buggy):
        if got[n].startswith("BUG") and got[n] != key[n]:
            print("  %s expected %s got %s" % (n, key[n], got[n]))

    with open(os.path.join(LOG, "bb1_parity_score.txt"), "w") as f:
        f.write("parity %d/%d %.4f KB-D1C %s\n" % (par_hits, par_n, parity_rate,
              "PASS" if parity_rate >= 0.85 else "FAIL"))
        f.write("detect %d/%d %.4f fa %d/%d %.4f KB-D1 %s\n" % (
            detected, len(buggy), det_rate, fa, len(clean), fa_rate,
            "PASS" if (det_rate >= 0.70 and fa_rate <= 0.25) else "FAIL"))
        f.write("classprec %d/%d %.4f KB-D2 %s\n" % (class_ok, detected, prec,
              "PASS" if prec >= 0.60 else "FAIL"))
        f.write("digests_identical %s\n" % det)
    return 0 if det else 1

if __name__ == "__main__":
    sys.exit(main())
