#!/usr/bin/env python3
"""Fork C blind-battery adapter. Deterministic. Zero RNG.
Reads frozen battery, emits fork C store + cases + manifest.
"""
import os, sys

BAT = os.path.expanduser("~/workspace/selfpam_r2/attacks/frozen_battery/battery")
OUT = os.path.expanduser("~/workspace/selfpam_r2/attacks/c_attack")
os.makedirs(OUT + "/cases", exist_ok=True)

def read_tsv(name):
    rows = []
    for line in open(os.path.join(BAT, name), encoding="utf-8"):
        line = line.rstrip("\n")
        if line:
            rows.append(line.split("|"))
    return rows

# ---- store: STORE|S001|text|WORLD|E0 -> S001|WORLD|text ----
store_rows = read_tsv("STORE.tsv")
with open(OUT + "/store.txt", "w", encoding="utf-8") as f:
    for p in store_rows:
        # p = [STORE, S001, text, WORLD, E0]
        f.write(f"{p[1]}|{p[3]}|{p[2]}\n")

# ---- traces: item -> list of (step, op, detail, text) ----
traces = {}
for p in read_tsv("TRACE.tsv"):
    # TRACE|CF-001|1|recall|S001|text
    traces.setdefault(p[1], []).append((int(p[2]), p[3], p[4], p[5] if len(p) > 5 else ""))
for k in traces:
    traces[k].sort()

def conclude_text(item_id):
    """Return the conclude-step text for an item, or ''."""
    for step, op, detail, text in traces.get(item_id, []):
        if op == "conclude":
            return text
    return ""

def mkcase(cid, bar, draft=None, a=None, b=None, expect="", rule="", delib=""):
    lines = [f"CASE: {cid}", f"BAR: {bar}"]
    if a is not None:
        lines.append(f"A: {a}")
        lines.append(f"B: {b}")
    else:
        lines.append(f"DRAFT: {draft}")
    lines.append(f"EXPECT: {expect}")
    lines.append(f"RULE: {rule}")
    lines.append("ENTCTX: ")
    lines.append(f"DELIB: {delib}")
    lines.append("")
    return "\n".join(lines)

manifest = []
nc = 0

def add_case(cid, *args, **kwargs):
    global nc
    fn = f"cases/{cid}.txt"
    with open(os.path.join(OUT, fn), "w", encoding="utf-8") as f:
        f.write(mkcase(cid, *args, **kwargs))
    manifest.append(fn)
    nc += 1

# ---- M1: CONF (CATCH->WITHHOLD) + GOLD (KEEP->INSTALL), DELIB empty ----
for p in read_tsv("CONF.tsv"):
    # ITEM|CONF|CF-001|text|CATCH
    add_case(p[2], "m1", draft=p[3], expect="WITHHOLD",
             rule=f"blind M1 confab {p[2]}", delib="")
for p in read_tsv("GOLD.tsv"):
    add_case(p[2] + "-m1", "m1", draft=p[3], expect="INSTALL",
             rule=f"blind M1 gold {p[2]}", delib="")

# ---- M6: GOLD (KEEP->INSTALL), BAR=m6 ----
for p in read_tsv("GOLD.tsv"):
    add_case(p[2] + "-m6", "m6", draft=p[3], expect="INSTALL",
             rule=f"blind M6 gold {p[2]}", delib="")

# ---- M2: pairs_ss + pairs_flip (DIVERGE) ----
for p in read_tsv("pairs_ss.tsv"):
    # PAIR|SS|P-SS-001|rule|A|B|DIVERGE
    add_case(p[2], "m2", a=p[4], b=p[5], expect="DIVERGE",
             rule=f"blind M2 ss {p[3]}", delib="")
for p in read_tsv("pairs_flip.tsv"):
    add_case(p[2], "m2", a=p[4], b=p[5], expect="DIVERGE",
             rule=f"blind M2 flip {p[3]}", delib="")

# ---- M3: pairs_sm (STABLE) ----
for p in read_tsv("pairs_sm.tsv"):
    add_case(p[2], "m3", a=p[4], b=p[5], expect="SAME",
             rule=f"blind M3 sm {p[3]}", delib="")

# ---- M4: ALIBI (CATCH->WITHHOLD), DELIB = fabricated conclude ----
for p in read_tsv("ALIBI.tsv"):
    # ITEM|ALIBI|AB-001|text|CATCH
    concl = conclude_text(p[2])
    add_case(p[2], "m4", draft=p[3], expect="WITHHOLD",
             rule=f"blind M4 alibi {p[2]}", delib=concl)

# ---- M5: RECUR (CATCH->WITHHOLD), DELIB empty (tests GEN provenance only) ----
for p in read_tsv("RECUR.tsv"):
    add_case(p[2], "m5", draft=p[3], expect="WITHHOLD",
             rule=f"blind M5 recur {p[2]}", delib="")

# ---- extras: SMUGGLE, CALIB, UTYPE, POINTER as m1 (CATCH->WITHHOLD) ----
for p in read_tsv("SMUGGLE.tsv"):
    add_case(p[2], "m1", draft=p[3], expect="WITHHOLD",
             rule=f"blind M1-ext smuggle {p[2]}", delib="")
for p in read_tsv("CALIB.tsv"):
    add_case(p[2], "m1", draft=p[3], expect="WITHHOLD",
             rule=f"blind M1-ext calib {p[2]}", delib="")
for p in read_tsv("UTYPE.tsv"):
    # ITEM|UTYPE|UT-001|text|WITHHOLD-AS-FACT? check GT
    add_case(p[2], "m1", draft=p[3], expect="WITHHOLD",
             rule=f"blind M1-ext utype {p[2]}", delib="")
for p in read_tsv("POINTER.tsv"):
    add_case(p[2], "m1", draft=p[3], expect="WITHHOLD",
             rule=f"blind M1-ext pointer {p[2]}", delib="")

with open(OUT + "/manifest.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(manifest) + "\n")

print(f"cases: {nc}")
print(f"manifest lines: {len(manifest)}")
