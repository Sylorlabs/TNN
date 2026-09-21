#!/usr/bin/env python3
"""Freeze the muse-native ENGLISH corpus: parse 40 raw batch files, build
corpus.json (Q2 structure), SHA256.txt, SHA256SUMS.txt.

Parsers imported from Q2's gen_corpus (never reimplemented). Domain truth
(t5_plant_claim = trainer-SUPPLIED values, FALSE_IDS) read from the FROZEN
facts.json -- never reimplemented. Any parse failure aborts loudly; no batch
is dropped or edited.
"""
import hashlib
import json
import os
import sys
import time

sys.path.insert(0, "/home/hatch/workspace/tnn-lab/wave12/q2-distillation/build")
import gen_corpus as Q2  # noqa: E402  (parse_dump, parse_teach)

WORK = os.path.dirname(os.path.abspath(__file__))
INPUT = os.path.join(WORK, "..", "corpus-input")
RAW = os.path.join(WORK, "corpus", "raw")
CORPUS = os.path.join(WORK, "corpus")

PROMPTS_SHA = "ac5d7d3155f9a90dc60f4f3ec529a3c6125a0469ce5862c7193fb261441b8b7d"

with open(os.path.join(INPUT, "facts.json"), encoding="utf-8") as f:
    FACTS = json.load(f)
assert FACTS["meta"]["prompts_sha256"] == PROMPTS_SHA, "prompts sha drift"
FALSE_IDS = FACTS["false_ids"]
assert FALSE_IDS == [3, 29, 55, 71, 80, 103, 117, 139, 163, 178, 205, 231]

def t5_plant_claim(i):
    return int(FACTS[str(i)]["value"])

N_BATCHES = 20
BATCH = 12

def main():
    missing = []
    for tag in ("dump", "teach"):
        for bi in range(N_BATCHES):
            p = os.path.join(RAW, "%s_batch%02d.txt" % (tag, bi))
            if not os.path.exists(p):
                missing.append(p)
    if missing:
        sys.exit("GATE NOT CLEAR: %d files missing: %s" % (len(missing), missing))

    merged_dump, merged_teach, failures, raw_hashes = {}, {}, [], {}
    for bi in range(N_BATCHES):
        ids = list(range(bi * BATCH, (bi + 1) * BATCH))
        for tag, parse_fn, merged in (("dump", Q2.parse_dump, merged_dump),
                                      ("teach", Q2.parse_teach, merged_teach)):
            p = os.path.join(RAW, "%s_batch%02d.txt" % (tag, bi))
            with open(p, "rb") as f:
                raw = f.read()
            raw_hashes["%s_batch%02d.txt" % (tag, bi)] = \
                hashlib.sha256(raw).hexdigest()
            res, err = parse_fn(raw.decode("utf-8"), ids)
            if err is not None:
                failures.append({"file": "%s_batch%02d.txt" % (tag, bi),
                                 "error": err})
            else:
                merged.update(res)
    if failures:
        for fl in failures:
            print("PARSE FAIL %s: %s" % (fl["file"], fl["error"]), flush=True)
        sys.exit("PARSE FAILURES -- corpus NOT frozen")
    assert len(merged_dump) == 240 and len(merged_teach) == 240, \
        "id coverage: dump=%d teach=%d" % (len(merged_dump), len(merged_teach))

    corpus = {
        "meta": {
            "model": "muse-native-english",
            "temperature": "n/a -- native generation, no temperature parameter",
            "seed": "n/a -- deterministic native source, no seed",
            "batch": BATCH,
            "prereg": ("~/workspace/tnn-lab/wave12/championship-english/"
                       "corpus-input/ENGLISH_PROMPT_SET.md (frozen, sha256-verified)"),
            "prompts_sha256": PROMPTS_SHA,
            "retries": [],
            "input_claim": ("t5_plant_claim(id): trainer's intended English "
                            "records (228 world-true + 12 deliberately false); "
                            "the producer is NOT told which 12 are false and "
                            "transcribes the given value exactly, never "
                            "correcting from prior knowledge"),
            "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "producer": ("native Muse subagents acting AS the source "
                         "(ENGLISH BOX SOURCE TEAM), no API calls"),
        },
        "input_claims": {str(i): t5_plant_claim(i) for i in range(240)},
        "false_ids": list(FALSE_IDS),
        "dump": [{"id": i, "value": merged_dump[i]["value"],
                  "sentence": merged_dump[i]["sentence"]} for i in range(240)],
        "teach": [{"id": i, "obs_value": merged_teach[i]["obs_value"],
                   "observation": merged_teach[i]["observation"],
                   "distract_value": merged_teach[i]["distract_value"],
                   "distractor": merged_teach[i]["distractor"],
                   "probe": merged_teach[i]["probe"],
                   "probe_value": merged_teach[i]["probe_value"]}
                  for i in range(240)],
    }
    inv = {"E_dump": [], "E_obs": [], "E_prb": [],
           "inconsistent": [], "sentence_missing_value": []}
    for i in range(240):
        want = t5_plant_claim(i)
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
    corpus["error_inventory"] = {k: {"n": len(v), "ids": v}
                                 for k, v in inv.items()}

    os.makedirs(CORPUS, exist_ok=True)
    cj = os.path.join(CORPUS, "corpus.json")
    with open(cj, "w", encoding="utf-8") as f:
        json.dump(corpus, f, indent=1, ensure_ascii=False)
        f.write("\n")
    with open(cj, "rb") as f:
        sha = hashlib.sha256(f.read()).hexdigest()
    with open(os.path.join(CORPUS, "SHA256.txt"), "w") as f:
        f.write(sha + "\n")
    sums = []
    for bi in range(N_BATCHES):
        for tag in ("dump", "teach"):
            fn = "%s_batch%02d.txt" % (tag, bi)
            sums.append("%s  raw/%s" % (raw_hashes[fn], fn))
    sums.append("%s  corpus.json" % sha)
    with open(os.path.join(CORPUS, "SHA256SUMS.txt"), "w") as f:
        f.write("\n".join(sums) + "\n")
    print("frozen: 240/240 parse, 0 failures")
    print("corpus.json sha256:", sha)
    print("error_inventory:", {k: v["n"] for k, v in
                               corpus["error_inventory"].items()})

if __name__ == "__main__":
    main()
