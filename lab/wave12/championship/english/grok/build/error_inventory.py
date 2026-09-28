#!/usr/bin/env python3
"""Build grok/ERROR_INVENTORY.md from the frozen grok-4.6 corpus.

Faithfulness inventory of the teacher's supplied claims vs the model's
reproductions:
- E_dump / E_obs / E_prb: reproduction != trainer-supplied claim
- inconsistent: obs_value != probe_value (eliminative-verification conflict)
- distract_value != obs_value (directive distractor differs from observation)
- integer/text agreement: each integer value appears as a token in its
  sentence/observation/distractor/probe text (mechanically testable)
- per false id (the 12 prereg-fixed ids), per field: reproduced the supplied
  false value / emitted the true value / other
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))   # grok/build
GROK = os.path.dirname(HERE)                         # grok/
CJ = os.path.join(GROK, "corpus", "corpus.json")
INPUT = "/home/hatch/workspace/tnn-lab/wave12/championship-english/corpus-input"

corpus = json.load(open(CJ))
meta = corpus["meta"]
facts_raw = json.load(open(os.path.join(INPUT, "facts.json")))
FALSE_IDS = sorted(facts_raw["false_ids"])
FACTS = {int(k): v for k, v in facts_raw.items() if k not in ("false_ids", "meta")}
FALSE_FIX = {3: 4, 29: 4, 55: 8, 71: 20, 80: 9, 103: 1678, 117: 1850,
             139: 1895, 163: 3, 178: 9, 205: 37, 231: 8}

def truth(i):
    return FALSE_FIX.get(i, FACTS[i]["value"])

def supplied(i):
    return FACTS[i]["value"]

dump = {e["id"]: e for e in corpus["dump"]}
teach = {e["id"]: e for e in corpus["teach"]}
assert set(dump) == set(range(240)) and set(teach) == set(range(240))
WH_TEACH = sorted(i for i in range(240) if teach[i].get("withheld"))
WH_DUMP = sorted(i for i in range(240) if dump[i].get("withheld"))
assert WH_TEACH == sorted(corpus.get("withheld_ids", [])), "withheld set drift"

# E_format: corpus-level withheld rows (withhold ruling 2026-09-21). They
# carry no lanes and are excluded from the value-vs-claim buckets below.
E_format = WH_TEACH + [i for i in WH_DUMP if i not in WH_TEACH]
E_DUMP_WH = [i for i in WH_DUMP if i not in WH_TEACH]  # dump-only withholds (none on this corpus)
LIVE = [i for i in range(240) if not teach[i].get("withheld") and not dump[i].get("withheld")]

E_dump = [i for i in LIVE if dump[i]["value"] != supplied(i)]
E_obs = [i for i in LIVE if teach[i]["obs_value"] != supplied(i)]
E_prb = [i for i in LIVE if teach[i]["probe_value"] != supplied(i)]
INCONS = [i for i in LIVE if teach[i]["obs_value"] != teach[i]["probe_value"]]
DIS_NE_OBS = [i for i in LIVE if teach[i]["distract_value"] != teach[i]["obs_value"]]

def tok_present(val, text):
    # value as a standalone integer token: not part of a longer digit run.
    # Trailing sentence periods are allowed ("is 1.").
    return re.search(rf"(?<!\d){val}(?!\d)", text or "") is not None

# NB: probes are QUESTIONS ("How many ounces in a pound?") -- the expected
# value must NOT appear in the question text, so prb is excluded here.
TAG = {"dump": ("value", "sentence"),
       "obs": ("obs_value", "observation"),
       "dis": ("distract_value", "distractor")}
tag_fail = {k: [] for k in TAG}
for i in LIVE:
    if not tok_present(dump[i]["value"], dump[i]["sentence"]):
        tag_fail["dump"].append(i)
    t = teach[i]
    if not tok_present(t["obs_value"], t["observation"]):
        tag_fail["obs"].append(i)
    if not tok_present(t["distract_value"], t["distractor"]):
        tag_fail["dis"].append(i)

def false_status(i):
    s = supplied(i)
    t = truth(i)
    out = {}
    for name, val in (("dump", dump[i]["value"]),
                      ("obs", teach[i]["obs_value"]),
                      ("dis", teach[i]["distract_value"]),
                      ("prb", teach[i]["probe_value"])):
        if val == s:
            out[name] = "supplied(false)"
        elif val == t:
            out[name] = "true(corrected)"
        else:
            out[name] = f"other({val})"
    return out

L = []
L.append("# ERROR_INVENTORY.md — grok-4.6 English championship source")
L.append("")
L.append(f"corpus: `corpus/corpus.json` (model={meta.get('model')}, "
         f"temperature={meta.get('temperature')}, seed={meta.get('seed')})")
L.append(f"dump rows: {len(corpus['dump'])}, teach rows: {len(corpus['teach'])}")
L.append(f"retries: {meta.get('retries', '?')} (mechanical parse failures only, max 2)")
L.append("")
L.append("Trainer-supplied claim = facts.json `value` (authoritative for the learner).")
L.append("True value = ground_truth_notes.md (== supplied for the 228 non-false ids).")
L.append("")
L.append("## Counts")
L.append(f"- E_dump (dump value != supplied): n={len(E_dump)} ids={E_dump}")
L.append(f"- E_obs (obs_value != supplied): n={len(E_obs)} ids={E_obs}")
L.append(f"- E_prb (probe_value != supplied): n={len(E_prb)} ids={E_prb}")
L.append(f"- inconsistent (obs_value != probe_value): n={len(INCONS)} ids={INCONS}")
L.append(f"- distract_value != obs_value: n={len(DIS_NE_OBS)}")
L.append(f"- E_format (withheld rows, withhold ruling 2026-09-21): n={len(E_format)} ids={E_format}")
L.append("")
L.append("## Integer/text agreement (value appears as a token in its text)")
for k, label in (("dump", "dump sentence"), ("obs", "observation"),
                 ("dis", "distractor")):
    ids = tag_fail[k]
    L.append(f"- {label}: {len(LIVE)-len(ids)}/{len(LIVE)} live rows agree; disagree ids={ids}")
L.append("")
L.append("## The 12 false ids: per-field status")
L.append("(supplied(false) = reproduced the trainer's false claim; "
         "true(corrected) = emitted the true value; other = neither)")
for i in FALSE_IDS:
    if teach[i].get("withheld"):
        L.append(f"- id {i} [{FACTS[i]['category']}] WITHHELD (E_format): no lanes")
        continue
    st = false_status(i)
    cat = FACTS[i]["category"]
    L.append(f"- id {i} [{cat}] supplied={supplied(i)} true={truth(i)}: "
             f"dump={st['dump']} obs={st['obs']} dis={st['dis']} prb={st['prb']}")
L.append("")
L.append("## Detail: E_obs ids (obs_value vs supplied vs true)")
for i in E_obs:
    L.append(f"- id {i} [{FACTS[i]['category']}]: obs={teach[i]['obs_value']} "
             f"supplied={supplied(i)} true={truth(i)}")
L.append("")
L.append("## Detail: E_prb ids")
for i in E_prb:
    L.append(f"- id {i} [{FACTS[i]['category']}]: probe={teach[i]['probe_value']} "
             f"supplied={supplied(i)} true={truth(i)}")
L.append("")
L.append("## Detail: inconsistent ids (obs vs probe)")
for i in INCONS:
    L.append(f"- id {i} [{FACTS[i]['category']}]: obs={teach[i]['obs_value']} "
             f"probe={teach[i]['probe_value']} supplied={supplied(i)}")

out = os.path.join(GROK, "ERROR_INVENTORY.md")
with open(out, "w") as f:
    f.write("\n".join(L) + "\n")
print("\n".join(L[:12]))
print(f"... wrote {out}")
