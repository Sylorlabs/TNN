#!/usr/bin/env python3
"""v3 reference adapter (NON-CONTENDER, context only).
Converts the SG battery to prose_learn3's input format, runs `prose_learn3 sg m2`,
parses PROBE verdict lines, and writes an SG-style verdict file.
Usage: adapt_v3.py <battery_dir> <v3_binary> <workdir> <verdicts_out>"""
import json, os, re, subprocess, sys

bdir, v3bin, work, out = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
inp = os.path.join(work, "inputs")
os.makedirs(inp, exist_ok=True)

teach = [ln.rstrip("\n").split("\t", 1) for ln in open(f"{bdir}/teach_sg.txt")]
probes = [ln.rstrip("\n").split("\t") for ln in open(f"{bdir}/probe_sg.txt")]
expected = json.load(open(f"{bdir}/expected_sg.json"))

with open(f"{inp}/train_sg.txt", "w") as f:
    for n, (sid, text) in enumerate(teach):
        f.write(f"{n}\t{text}\n")
with open(f"{inp}/test_sg.txt", "w") as f:
    for m, (sid, text, cls) in enumerate(probes):
        f.write(f"{m}\t{expected[sid]['verdict']}\t{text}\t{cls}\n")
open(f"{inp}/false_ids_sg.txt", "w").write("")
idmap = {str(m): sid for m, (sid, _, _) in enumerate(probes)}
json.dump(idmap, open(os.path.join(work, "idmap.json"), "w"))

r = subprocess.run([v3bin, "sg", "m2"], cwd=work, capture_output=True, text=True)
open(os.path.join(work, "v3_stdout.txt"), "w").write(r.stdout)
open(os.path.join(work, "v3_stderr.txt"), "w").write(r.stderr)
print("v3 rc:", r.returncode, file=sys.stderr)

verdicts = {}
for m in re.finditer(r"PROBE id=(\d+) verdict=(\S+)", r.stdout):
    verdicts[idmap[m.group(1)]] = m.group(2)
print(f"parsed {len(verdicts)}/{len(probes)} probe verdicts", file=sys.stderr)
with open(out, "w") as f:
    for sid, _, _ in probes:
        f.write(f"{sid}\t{verdicts.get(sid, 'MISSING')}\n")
