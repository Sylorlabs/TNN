#!/usr/bin/env python3
"""Independent oracle for the bug-blindness crew.
Recomputes every scored metric from sealed keys + run logs.
Usage: python3 verify_bb.py   (run from the bug-blindness dir)
Exit 0 = all recomputed metrics match the verdict; nonzero = mismatch.
"""
import hashlib, json, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
fails = []

def check(name, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + name + (" — " + detail if detail else ""))
    if not cond:
        fails.append(name)

def sha_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

# ---- Q1: parity battery ----
LOG = os.path.join(BASE, "logs")
KEY = os.path.join(BASE, "battery", "parity", "answer_key_parity.txt")

rep_outs = [open(os.path.join(LOG, "bb1_parity_rep%d.out" % r)).read() for r in range(1, 6)]
digests = [hashlib.sha256(b.encode()).hexdigest() for b in rep_outs]
check("Q1 five reps byte-identical", len(set(digests)) == 1, digests[0][:12])

key = {}
for line in open(KEY):
    line = line.rstrip("\n")
    if line:
        name, verdict = line.split(" ", 1)
        key[name] = verdict
check("Q1 key has 38 entries", len(key) == 38, str(len(key)))

got = {}
for line in rep_outs[0].rstrip("\n").split("\n"):
    name, verdict = line.split(" ", 1)
    got[name] = verdict
check("Q1 output covers all 38 items", set(got) == set(key))

PARITY_CLASSES = ["E0001","E0002","E0010","E0203","UNKNOWN-IDENT","UNKNOWN-FN",
                  "ARITY","DUP-FN","DUP-TYPE","UNKNOWN-FIELD","NO-MAIN","BAD-INDEX"]
parity_items = [n for n, v in key.items()
                if v.startswith("BUG ") and v.split(" ")[1] in PARITY_CLASSES]
check("Q1 parity set is 24 items", len(parity_items) == 24, str(len(parity_items)))
parity_hit = sum(1 for n in parity_items if got[n] == key[n])
check("KB-D1C parity 24/24", parity_hit == 24, "%d/24" % parity_hit)

buggy = [n for n, v in key.items() if v.startswith("BUG")]
clean = [n for n, v in key.items() if v == "CLEAN"]
det = sum(1 for n in buggy if got[n].startswith("BUG"))
fa = sum(1 for n in clean if got[n].startswith("BUG"))
check("KB-D1 detection 30/30", det == 30, "%d/30" % det)
check("KB-D1 false alarms 0/8", fa == 0, "%d/8" % fa)
cp = sum(1 for n in buggy if got[n] == key[n])
check("KB-D2 class+line 30/30", cp == 30, "%d/30" % cp)

# ---- Q3 ----
r = json.load(open(os.path.join(LOG, "q3_report.json")))["summary"]
check("Q3a 5/10 -> KB-R1 FAIL", r["q3a_repaired"] == 5 and r["kb_r1"] == "FAIL",
      "repaired=%s bar=%s" % (r["q3a_repaired"], r["kb_r1"]))
check("Q3b 0/5 -> KB-R2 CONFIRMED", r["q3b_recover"] == 0 and r["kb_r2"] == "CONFIRMED")
check("Q3c 0/4", r["q3c_recover"] == 0)

# ---- Q4 ----
post = open(os.path.join(LOG, "bb1_q4_post_score.txt")).read().strip()
check("Q4 pre/post 8/8 + 8/8 (KB-T1 FAIL by ceiling+statelessness)",
      post.startswith("arity=8/8 uninit=8/8"), post[:40])
gen1 = open(os.path.join(LOG, "bb1_q4_gen_rep1.out")).read()
gen_ok = sum(1 for l in gen1.split("\n") if l.startswith("g") and "ok=True" in l)
check("Q4 generation probe 1/6 (honest miss)", gen_ok == 1, "%d/6" % gen_ok)

print()
if fails:
    print("MISMATCHES:", fails)
    sys.exit(1)
print("All recomputed metrics match VERDICT-BB.md.")
