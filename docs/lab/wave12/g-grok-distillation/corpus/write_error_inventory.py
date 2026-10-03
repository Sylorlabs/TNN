#!/usr/bin/env python3
"""Write corpus/ERROR_INVENTORY.md from the frozen grok corpus.json.

Mechanical only: compares grok outputs against t5_plant_claim inputs.
Never retries or edits corpus.json.

G-GROK delta vs Q2's writer: D1 is CANCELLED (planting dead), so the
"installed-by-D1" overlap is replaced by "consistent errors the teaching
route installs" (both legs agree on a wrong value -> D2 installs it).
"""
import hashlib
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS = os.path.join(HERE, "corpus.json")

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

with open(CORPUS, "rb") as f:
    raw = f.read()
corpus = json.loads(raw)
assert hashlib.sha256(raw).hexdigest() == open(
    os.path.join(HERE, "SHA256.txt")).read().strip(), "corpus.json hash mismatch"

DUMP = [e["value"] for e in corpus["dump"]]
OBS = [e["obs_value"] for e in corpus["teach"]]
PRB = [e["probe_value"] for e in corpus["teach"]]
CLAIM = [t5_plant_claim(i) for i in range(240)]

E_dump = [i for i in range(240) if DUMP[i] != CLAIM[i]]
E_obs = [i for i in range(240) if OBS[i] != CLAIM[i]]
E_prb = [i for i in range(240) if PRB[i] != CLAIM[i]]
INCONS = [i for i in range(240) if OBS[i] != PRB[i]]
CAUGHT = [i for i in INCONS if OBS[i] != CLAIM[i] or PRB[i] != CLAIM[i]]
# consistent errors: both legs agree on a value != input claim -> teaching installs
CONSISTENT_INSTALL = [i for i in range(240)
                      if OBS[i] == PRB[i] and OBS[i] != CLAIM[i]]
mech = corpus["meta"]["retries"]
n_dump_retry = sum(1 for r in mech if r["tag"] == "dump")
n_teach_retry = sum(1 for r in mech if r["tag"] == "teach")

L = []
L.append("# G-GROK corpus — LLM error inventory (championship rescope)")
L.append("")
L.append(f"Model: `{corpus['meta']['model']}`, temperature={corpus['meta']['temperature']}, seed={corpus['meta']['seed']}.")
L.append(f"Prompt sha256: `{corpus['meta']['prompts_sha256']}` (extracted from frozen Q2 prereg).")
L.append(f"Corpus sha256: `{open(os.path.join(HERE,'SHA256.txt')).read().strip()}`.")
L.append("")
L.append("Mechanical (parse/format) errors — retried per prereg §3, never for semantics:")
L.append(f"- dump batches: {n_dump_retry} parse failures (retried per prereg §3)")
L.append(f"- teach batches: {n_teach_retry} parse failures (retried per prereg §3)")
L.append(f"  retry details: {[(r['tag'], r['batch'], r['attempt']) for r in mech]}")
L.append("")
L.append(f"## E_dump (n={len(E_dump)}): dump value != input claim")
for i in E_dump:
    tag = " [DELIBERATE FALSE]" if i in FALSE_IDS else ""
    L.append(f"- id {i}: input={CLAIM[i]} llm={DUMP[i]} truth={t5_truth(i)}{tag}")
L.append("")
L.append(f"## E_obs (n={len(E_obs)}): teaching observation leg != input claim")
for i in E_obs:
    L.append(f"- id {i}: input={CLAIM[i]} obs={OBS[i]} truth={t5_truth(i)}")
L.append("")
L.append(f"## E_prb (n={len(E_prb)}): teaching probe leg != input claim")
for i in E_prb:
    L.append(f"- id {i}: input={CLAIM[i]} probe={PRB[i]} truth={t5_truth(i)}")
L.append("")
L.append(f"## inconsistent obs/probe legs (n={len(INCONS)}): withheld by D2 teaching")
for i in INCONS:
    L.append(f"- id {i}: obs={OBS[i]} probe={PRB[i]} input={CLAIM[i]} truth={t5_truth(i)}")
L.append("")
L.append(f"## CAUGHT_ERR (n={len(CAUGHT)}): withheld AND at least one leg wrong")
for i in CAUGHT:
    L.append(f"- id {i}: obs={OBS[i]} probe={PRB[i]} input={CLAIM[i]} truth={t5_truth(i)}")
L.append("")
L.append(f"## CONSISTENT_INSTALL (n={len(CONSISTENT_INSTALL)}): both legs agree on a wrong value")
L.append("The D2 teaching route INSTALLS these (eliminative verification passes on")
L.append("agreement); only disagreement is withheld. D1 is cancelled — there is no")
L.append("planted comparison; this is the K-Q2 live-watch evidence.")
for i in CONSISTENT_INSTALL:
    tag = " [DELIBERATE FALSE]" if i in FALSE_IDS else ""
    L.append(f"- id {i}: legs={OBS[i]} input={CLAIM[i]} truth={t5_truth(i)}{tag}")
L.append("")
L.append("## K-Q2 outcome")
L.append("D1 is CANCELLED (planting dead) — K-Q2 as originally framed (teaching")
L.append("catches what planting installs) cannot fire comparatively. The live-watch")
L.append(f"evidence: CAUGHT_ERR n={len(CAUGHT)} (withheld), CONSISTENT_INSTALL")
L.append(f"n={len(CONSISTENT_INSTALL)} (installed by teaching despite being wrong).")

with open(os.path.join(HERE, "ERROR_INVENTORY.md"), "w") as f:
    f.write("\n".join(L) + "\n")
print(f"wrote ERROR_INVENTORY.md: E_dump={len(E_dump)} E_obs={len(E_obs)} "
      f"E_prb={len(E_prb)} incons={len(INCONS)} caught={len(CAUGHT)} "
      f"consistent_install={len(CONSISTENT_INSTALL)}")
