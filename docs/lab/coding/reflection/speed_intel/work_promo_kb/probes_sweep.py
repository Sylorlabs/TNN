#!/usr/bin/env python3
"""Probe sweep: run plan mode over the 24 GEN specs, report scored/probes.
Usage: probes_sweep.py <kb_main> <kb.dat> [extra_arg ...]
"""
import subprocess, sys

kb_main, kbdat, extra = sys.argv[1], sys.argv[2], sys.argv[3:]
specs = []
for line in open("kb/tests/specs.txt"):
    line = line.rstrip("\n")
    if line.startswith("GEN\t"):
        p = line.split("\t")
        specs.append((p[1], p[2]))
tot_sc = tot_pr = tot_tp = 0
print("%-4s %-12s %6s %6s %7s" % ("spec", "family", "scored", "probes", "tprobes"))
for sid, spec in specs:
    p = subprocess.run([kb_main, "plan", kbdat, spec] + extra,
                       capture_output=True, timeout=30)
    out = p.stdout.decode(errors="replace").strip()
    fam = [l for l in out.split("\n") if l.startswith("PLAN family=")][0].split("family=")[1].split()[0]
    sl = [l for l in out.split("\n") if l.startswith("PLAN scored=")][0]
    sc = int(sl.split("scored=")[1].split()[0])
    pr = int(sl.split("probes=")[1].split()[0])
    tb = int(sl.split("tprobes=")[1].split()[0]) if "tprobes=" in sl else 0
    tot_sc += sc; tot_pr += pr; tot_tp += tb
    print("%-4s %-12s %6d %6d %7d" % (sid, fam, sc, pr, tb))
n = len(specs)
print("avg scored/query=%.2f probes/query=%.2f tprobes/query=%.2f total/query=%.2f" % (
    tot_sc/n, tot_pr/n, tot_tp/n, (tot_pr+tot_tp)/n))
