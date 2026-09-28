#!/usr/bin/env python3
"""MUSE-TNN gate: mechanically freeze the native Muse corpus.

Imports parse_dump / parse_teach and the domain (t5_plant_claim, FALSE_IDS,
t5_cat, CATS, BATCH) from Q2's gen_corpus.py — never reimplements them.
Parses all 40 raw batches, builds corpus.json + SHA256.txt mirroring Q2's
structure, sha256s every raw byte. Any parse failure is REPORTED loudly;
no batch is dropped or edited.
"""
import hashlib
import json
import os
import sys
import time

sys.path.insert(0, "/home/hatch/workspace/tnn-lab/wave12/q2-distillation/build")
import gen_corpus as Q2  # noqa: E402  (parse_*, t5_plant_claim, FALSE_IDS, t5_cat, CATS, BATCH)

RAW_DIR = "/home/hatch/workspace/championship/muse_team/raw"
CORPUS_DIR = "/home/hatch/workspace/championship/muse_team/corpus"

N_BATCHES = 240 // Q2.BATCH  # 20

def check_all_present():
    missing = []
    for tag in ("dump", "teach"):
        for bi in range(N_BATCHES):
            p = os.path.join(RAW_DIR, f"{tag}_batch{bi:02d}.txt")
            if not os.path.exists(p):
                missing.append(f"{tag}_batch{bi:02d}.txt")
    return missing

def freeze():
    missing = check_all_present()
    if missing:
        print(f"GATE NOT CLEAR: {len(missing)} files missing", flush=True)
        return 1, missing

    merged_dump, merged_teach = {}, {}
    failures = []
    raw_hashes = {}
    for bi in range(N_BATCHES):
        ids = list(range(bi * Q2.BATCH, (bi + 1) * Q2.BATCH))
        for tag, parse_fn, merged in (("dump", Q2.parse_dump, merged_dump),
                                      ("teach", Q2.parse_teach, merged_teach)):
            p = os.path.join(RAW_DIR, f"{tag}_batch{bi:02d}.txt")
            with open(p, "rb") as f:
                raw = f.read()
            raw_hashes[f"{tag}_batch{bi:02d}.txt"] = hashlib.sha256(raw).hexdigest()
            res, err = parse_fn(raw.decode("utf-8"), ids)
            if err is not None:
                failures.append({"file": f"{tag}_batch{bi:02d}.txt",
                                 "error": err,
                                 "sha256": raw_hashes[f"{tag}_batch{bi:02d}.txt"]})
            else:
                merged.update(res)

    if failures:
        print("PARSE FAILURES — corpus NOT frozen; corrected files awaited:", flush=True)
        for fl in failures:
            print(f"  {fl['file']}: {fl['error']} (sha256={fl['sha256'][:16]})", flush=True)
        return 2, failures
    assert len(merged_dump) == 240 and len(merged_teach) == 240

    corpus = {
        "meta": {
            "model": "muse-native",
            "temperature": "n/a — native generation, no temperature parameter",
            "seed": "n/a",
            "batch": Q2.BATCH,
            "prereg": "~/workspace/championship/q2_prompt_set.md (frozen, sha256-verified)",
            "prompts_sha256": "eff5f91f03076ea0be29bd94bc39f941e5dcf9abbeb7b6d13fd55ed8fcca6991",
            "input_claim": "t5_plant_claim(id): trainer's intended Zharovia records "
                           "(228 world-true + 12 deliberately false); the producer is NOT "
                           "told which 12 are false and knows nothing of Zharovia beyond the prompt",
            "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "producer": "parent coordinator's native subagents (MUSE team), not API calls",
        },
        "input_claims": {str(i): Q2.t5_plant_claim(i) for i in range(240)},
        "false_ids": sorted(Q2.FALSE_IDS),
        "dump": [{"id": i, "value": merged_dump[i]["value"],
                 "sentence": merged_dump[i]["sentence"]} for i in range(240)],
        "teach": [{"id": i, "obs_value": merged_teach[i]["obs_value"],
                  "observation": merged_teach[i]["observation"],
                  "distract_value": merged_teach[i]["distract_value"],
                  "distractor": merged_teach[i]["distractor"],
                  "probe": merged_teach[i]["probe"],
                  "probe_value": merged_teach[i]["probe_value"]} for i in range(240)],
    }
    # mechanical error inventory (§7, same five buckets as Q2)
    inv = {"E_dump": [], "E_obs": [], "E_prb": [],
           "inconsistent": [], "sentence_missing_value": []}
    for i in range(240):
        want = Q2.t5_plant_claim(i)
        if merged_dump[i]["value"] != want:
            inv["E_dump"].append(i)
        if merged_teach[i]["obs_value"] != want:
            inv["E_obs"].append(i)
        if merged_teach[i]["probe_value"] != want:
            inv["E_prb"].append(i)
        if merged_teach[i]["obs_value"] != merged_teach[i]["probe_value"]:
            inv["inconsistent"].append(i)
        if str(merged_dump[i]["value"]) not in merged_dump[i]["sentence"]:
            inv["sentence_missing_value"].append(i)
    corpus["error_inventory"] = {k: {"n": len(v), "ids": v} for k, v in inv.items()}

    os.makedirs(CORPUS_DIR, exist_ok=True)
    with open(os.path.join(CORPUS_DIR, "corpus.json"), "w") as f:
        json.dump(corpus, f, indent=1, ensure_ascii=False)
        f.write("\n")
    with open(os.path.join(CORPUS_DIR, "corpus.json"), "rb") as f:
        sha = hashlib.sha256(f.read()).hexdigest()
    with open(os.path.join(CORPUS_DIR, "SHA256.txt"), "w") as f:
        f.write(sha + "\n")
    with open(os.path.join(RAW_DIR, "SHA256SUMS.txt"), "w") as f:
        for bi in range(N_BATCHES):
            for tag in ("dump", "teach"):
                fn = f"{tag}_batch{bi:02d}.txt"
                f.write(raw_hashes[fn] + f"  {fn}\n")

    print(f"FROZEN: corpus.json sha256={sha}", flush=True)
    print("error inventory: " + ", ".join(
        f"{k}={v['n']}" for k, v in corpus["error_inventory"].items()), flush=True)
    return 0, {"corpus_sha256": sha, "inventory": corpus["error_inventory"],
               "raw_hashes": raw_hashes}

if __name__ == "__main__":
    code, _ = freeze()
    sys.exit(code)
