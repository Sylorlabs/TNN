#!/usr/bin/env python3
"""Finalize the grok-4.7 corpus: merge lane partials -> evidence/grok47_corpus/corpus.json.

Same corpus.json schema as the frozen captures:
  meta (model, temperature, seed, batch, prereg, facts_sha, prompt batch shas,
        input_claim, generated_utc, retries, format_layout, procedure_note),
  input_claims, false_ids, dump[240], teach[240], error_inventory.
"""
import hashlib
import json
import os
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPORT = os.path.dirname(HERE)
EV = os.path.join(REPORT, "evidence", "grok47_corpus")
RAW_DIR = os.path.join(EV, "raw")
PARTIAL_DIR = os.path.join(HERE, "partial")
INPUT = "/home/hatch/workspace/tnn-lab/wave12/championship-english/corpus-input"
FACTS_PATH = os.path.join(INPUT, "facts.json")
FACTS_SHA = "4f1ba933a75a0f9e488ae170366afe7f514aec425f92432f5b0e0b49c4bfede5"
N_BATCHES = 20

_facts_raw = json.load(open(FACTS_PATH))
FALSE_IDS = sorted(_facts_raw["false_ids"])
FACTS = {int(k): v for k, v in _facts_raw.items() if k not in ("false_ids", "meta")}

def t5_plant_claim(i):
    return FACTS[i]["value"]

prompt_sha = {}
for tag in ("dump", "teach"):
    for bi in range(N_BATCHES):
        p = os.path.join(INPUT, f"batch{bi:02d}_{tag}.txt")
        prompt_sha[f"{tag}_batch{bi:02d}"] = hashlib.sha256(open(p, "rb").read()).hexdigest()

dump, teach = {}, {}
retries = []
truncs = []
for tag, store in (("dump", dump), ("teach", teach)):
    for bi in range(N_BATCHES):
        pp = os.path.join(PARTIAL_DIR, f"{tag}_batch{bi:02d}.json")
        if not os.path.exists(pp):
            raise SystemExit(f"FATAL: missing partial {pp}")
        d = json.load(open(pp))
        store.update({int(k): v for k, v in d["facts"].items()})
        retries.extend(d.get("retries", []))
        truncs.extend(d.get("truncations", []))
print(f"transport truncations voided/recaptured: {len(truncs)}")
assert len(dump) == 240 and len(teach) == 240, (len(dump), len(teach))

corpus = {
    "meta": {
        "model": "grok-4.7",
        "gateway": "api.experientiallabs.ai (experientiallabs; frozen protocol used UnoRouter)",
        "temperature": 0,
        "seed": 42,
        "batch": 12,
        "prereg": "tnn-lab/docs/lab/GROK47_OVERNIGHT/teacher/PREREG.md",
        "facts_sha256": FACTS_SHA,
        "prompt_batch_sha256": prompt_sha,
        "input_claim": "facts.json supplied values (228 world-true + 12 deliberately false)",
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "retries": retries,
        "transport_truncations": truncs,
        "procedure_note": "frozen English-box capture protocol; prompts verbatim; "
                          "retries only on mechanical parse failure (max 2), "
                          "never on wrong values",
    },
    "input_claims": {str(i): t5_plant_claim(i) for i in range(240)},
    "false_ids": FALSE_IDS,
    "dump": [{"id": i, "value": dump[i]["value"], "sentence": dump[i]["sentence"]}
             for i in range(240)],
    "teach": [{"id": i, "obs_value": teach[i]["obs_value"],
               "observation": teach[i]["observation"],
               "distract_value": teach[i]["distract_value"],
               "distractor": teach[i]["distractor"],
               "probe": teach[i]["probe"],
               "probe_value": teach[i]["probe_value"]} for i in range(240)],
}

inv = {"E_dump": [], "E_obs": [], "E_prb": [], "inconsistent": [],
       "sentence_missing_value": []}
for i in range(240):
    want = t5_plant_claim(i)
    if dump[i]["value"] != want:
        inv["E_dump"].append(i)
    if teach[i]["obs_value"] != want:
        inv["E_obs"].append(i)
    if teach[i]["probe_value"] != want:
        inv["E_prb"].append(i)
    if teach[i]["obs_value"] != teach[i]["probe_value"]:
        inv["inconsistent"].append(i)
    if str(dump[i]["value"]) not in dump[i]["sentence"]:
        inv["sentence_missing_value"].append(i)
corpus["error_inventory"] = {k: {"n": len(v), "ids": v} for k, v in inv.items()}

os.makedirs(RAW_DIR, exist_ok=True)
with open(os.path.join(EV, "corpus.json"), "w") as f:
    json.dump(corpus, f, indent=1, ensure_ascii=False)
    f.write("\n")
with open(os.path.join(EV, "corpus.json"), "rb") as f:
    sha = hashlib.sha256(f.read()).hexdigest()
with open(os.path.join(EV, "SHA256.txt"), "w") as f:
    f.write(sha + "\n")
with open(os.path.join(RAW_DIR, "SHA256SUMS.txt"), "w") as f:
    for bi in range(N_BATCHES):
        for tg in ("dump", "teach"):
            p = os.path.join(RAW_DIR, f"{tg}_batch{bi:02d}.txt")
            with open(p, "rb") as rf:
                f.write(hashlib.sha256(rf.read()).hexdigest() + f"  {tg}_batch{bi:02d}.txt\n")
print(f"corpus.json sha256={sha}")
print("error inventory: " + ", ".join(f"{k}={v['n']}" for k, v in corpus["error_inventory"].items()))
