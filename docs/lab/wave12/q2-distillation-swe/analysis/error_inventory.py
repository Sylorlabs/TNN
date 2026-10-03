#!/usr/bin/env python3
"""Q2-SWE faithfulness inventory — mechanical §7 error extraction.

Source: corpus/corpus.json (frozen, swe-1-6-slow:free ONLY) + the frozen
Zharovia domain spec (corpus_gen.py DOMAIN docstring) + the frozen prompt set
(championship/q2_prompt_set.md, hash-verified).
No retries for wrong values. All comparisons are mechanical.
Writes corpus/ERROR_INVENTORY.md.
"""
import json
import os
import re
import hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CORPUS = os.path.join(ROOT, "corpus", "corpus.json")

def t5_cat(i):
    if i < 48: return 0
    if i < 72: return 1
    if i < 108: return 2
    if i < 156: return 3
    if i < 192: return 4
    return 5

def t5_truth(i):
    c = t5_cat(i)
    x = [i, i-48, i-72, i-108, i-156, i-192][c]
    m = [12, 8, 100, 200, 48, 36][c]
    r = [(x*7+3) % m, (x*5+1) % m, (x*11+7) % m,
         (x*13+2) % m, (x*9+5) % m, (x*17+4) % m][c]
    return [0, 0, 1800, 1700, 0, 0][c] + r

FALSE_IDS = {3, 29, 55, 71, 80, 103, 117, 139, 163, 178, 205, 231}

def t5_plant_claim(i):
    if i in FALSE_IDS:
        c = t5_cat(i)
        m = [12, 8, 100, 200, 48, 36][c]
        b = [0, 0, 1800, 1700, 0, 0][c]
        return b + ((t5_truth(i) - b + 1) % m)
    return t5_truth(i)

def t5_range(i):
    c = t5_cat(i)
    b = [0, 0, 1800, 1700, 0, 0][c]
    m = [12, 8, 100, 200, 48, 36][c]
    return b, b + m - 1

with open(CORPUS) as f:
    corpus = json.load(f)
meta = corpus["meta"]
DUMP = corpus["dump"]
TEACH = corpus["teach"]

lines = []
lines.append("# Q2-SWE faithfulness inventory")
lines.append("")
lines.append(f"Source model: {meta['model']} (frozen corpus, seed unsupported).")
lines.append(f"corpus.json sha256: {open(os.path.join(ROOT,'corpus','SHA256.txt')).read().strip()}")
lines.append("")
lines.append("All comparisons are mechanical against the frozen prompt set and the")
lines.append("frozen Zharovia domain spec. No retries were made for wrong values.")
lines.append("")

# ---------- §7 E_dump ----------
lines.append("## §7 E_dump (240/240)")
dump_err = 0
dump_err_ids = []
for e in DUMP:
    i = e["id"]
    if e["value"] != t5_plant_claim(i):
        dump_err += 1
        dump_err_ids.append(i)
lines.append(f"items deviating from the planted claim: {dump_err}/240")
if dump_err_ids:
    lines.append(f"deviating ids: {dump_err_ids}")
lines.append("")

# ---------- §7 E_obs ----------
lines.append("## §7 E_obs (240/240)")
obs_err = 0
obs_err_ids = []
for e in TEACH:
    i = e["id"]
    if e["obs_value"] != t5_truth(i):
        obs_err += 1
        obs_err_ids.append(i)
lines.append(f"items where the LLM's observed value != world observation: {obs_err}/240")
if obs_err_ids:
    lines.append(f"deviating ids: {obs_err_ids}")
lines.append("")

# ---------- §7 E_prb ----------
lines.append("## §7 E_prb (240/240)")
prb_err = 0
prb_err_ids = []
for e in TEACH:
    i = e["id"]
    if e["probe_value"] != t5_truth(i):
        prb_err += 1
        prb_err_ids.append(i)
lines.append(f"items where the LLM's probe value != world observation: {prb_err}/240")
if prb_err_ids:
    lines.append(f"deviating ids: {prb_err_ids}")
lines.append("")

# ---------- inconsistencies: dump vs obs vs probe ----------
lines.append("## inconsistencies (dump vs obs vs probe)")
inc = 0
inc_ids = []
for i in range(240):
    d = DUMP[i]["value"]
    o = TEACH[i]["obs_value"]
    p = TEACH[i]["probe_value"]
    if not (d == o == p):
        inc += 1
        inc_ids.append(i)
lines.append(f"ids where dump/obs/probe are not all equal: {inc}/240")
lines.append("Note: for false ids the planted claim differs from the world value")
lines.append("by design, so dump != obs == probe is the EXPECTED pattern there.")
lines.append("")

# ---------- sentence-value checks ----------
lines.append("## sentence-value checks")
sv_fail = 0
sv_fail_ids = []
for e in DUMP:
    i = e["id"]
    nums = [int(x) for x in re.findall(r"\d+", e["sentence"])]
    if e["value"] not in nums:
        sv_fail += 1
        sv_fail_ids.append(i)
for e in TEACH:
    i = e["id"]
    # observation and distractor are statements; the probe is a question
    # (it does not contain the answer value by design)
    for field, txtfield in (("obs_value", "observation"),
                            ("distract_value", "distractor")):
        nums = [int(x) for x in re.findall(r"\d+", e[txtfield])]
        if e[field] not in nums:
            sv_fail += 1
            sv_fail_ids.append((i, field))
lines.append(f"text/value mismatches: {sv_fail}")
if sv_fail_ids:
    lines.append(f"failing (id[, field]): {sv_fail_ids}")
lines.append("")

# ---------- per-ID table: the 12 false ids ----------
lines.append("## per-ID table: the 12 false ids")
lines.append("")
lines.append("claim_in = planted claim shown in the dump prompt (the distractor,")
lines.append("INTENTIONAL deviation from world truth); truth = world observation;")
lines.append("obs/distract/probe = values asserted by the model in the teach item.")
lines.append("A teach deviation is UNINTENDED iff it differs from the intended")
lines.append("witness pattern (obs == truth, probe == truth, distract == claim_in).")
lines.append("")
lines.append("| id | claim_in | truth | obs | distract | probe | intended | unintended |")
lines.append("|---:|---:|---:|---:|---:|---:|---|---|")
for i in sorted(FALSE_IDS):
    ci = t5_plant_claim(i)
    tr = t5_truth(i)
    o = TEACH[i]["obs_value"]
    d = TEACH[i]["distract_value"]
    p = TEACH[i]["probe_value"]
    intended = (o == tr and p == tr and d == ci)
    un = []
    if o != tr: un.append("obs")
    if p != tr: un.append("probe")
    if d != ci: un.append("distract")
    lines.append(f"| {i} | {ci} | {tr} | {o} | {d} | {p} |"
                 f" {'yes' if intended else 'NO'} | {','.join(un) or 'none'} |")
lines.append("")
lines.append("Range check: every asserted numeric value lies within the fact's")
rng_fail = 0
for e in TEACH:
    i = e["id"]
    lo, hi = t5_range(i)
    for field in ("obs_value", "distract_value", "probe_value"):
        if not (lo <= e[field] <= hi):
            rng_fail += 1
            lines.append(f"  OUT OF RANGE: id {i} field {field} value {e[field]}")
lines.append(f"out-of-range assertions: {rng_fail}")
lines.append("")

with open(os.path.join(ROOT, "corpus", "ERROR_INVENTORY.md"), "w") as f:
    f.write("\n".join(lines))
print(f"E_dump deviations: {dump_err}/240")
print(f"E_obs deviations: {obs_err}/240")
print(f"E_prb deviations: {prb_err}/240")
print(f"inconsistencies: {inc}/240")
print(f"sentence-value mismatches: {sv_fail}")
print("corpus/ERROR_INVENTORY.md written")
