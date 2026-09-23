#!/usr/bin/env python3
"""FALLBACK freeze for the grok-4.6 corpus: capture + freeze with withhold marking.

Used ONLY if gen_corpus.py main() exits FATAL on a batch (unparseable after
the mechanical retry budget). Reuses gen_corpus.py's parsers/constants but
replaces the FATAL-on-exhaustion policy with the parent-authorized withhold
ruling (2026-09-21): the batch's 12 ids are marked {"withheld": true,
"withheld_reason": ...} in corpus.json — never salvage-parsed, never
trainer-repaired — and capture continues with the remaining batches.

Same frozen prompts/model/seed; paced retries on 429/503/524 (mechanical
parse retries max 2 per batch, logged). Raw bytes of the last failed attempt
are preserved in corpus/raw/.

On success this produces corpus/corpus.json identical in structure to
gen_corpus.py main()'s output (plus withheld marks + withheld_ids), then
runs finalize_corpus.py.
"""
import hashlib
import json
import os
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_corpus as gc

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CORPUS_DIR = os.path.join(ROOT, "corpus")
RAW_DIR = os.path.join(CORPUS_DIR, "raw")
os.makedirs(RAW_DIR, exist_ok=True)


def capture(tag, parse_fn):
    merged, retries_log, withheld = {}, [], {}
    for bi in range(gc.N_BATCHES):
        ids = gc.batch_ids(bi)
        prompt = gc.read_prompt(tag, bi)
        raw_path = os.path.join(RAW_DIR, f"{tag}_batch{bi:02d}.txt")
        done = False
        if os.path.exists(raw_path):
            with open(raw_path) as f:
                raw = f.read()
            res, err = parse_fn(raw, ids)
            if err is None:
                merged.update(res)
                print(f"[{tag} batch {bi}] resumed from raw (parses)", flush=True)
                done = True
        attempt = 0
        while not done:
            raw = gc.api_call(prompt)
            with open(raw_path, "w") as f:
                f.write(raw)
            h = hashlib.sha256(raw.encode()).hexdigest()
            res, err = parse_fn(raw, ids)
            if err is None:
                merged.update(res)
                print(f"[{tag} batch {bi}] ok sha256={h[:16]}", flush=True)
                done = True
            else:
                attempt += 1
                retries_log.append({"tag": tag, "batch": bi, "attempt": attempt,
                                    "error": err, "raw_sha256": h})
                print(f"[{tag} batch {bi}] PARSE FAIL (attempt {attempt}): {err}",
                      flush=True)
                if attempt > 2:
                    reason = (f"withhold ruling 2026-09-21: unparseable after "
                              f"2 mechanical retries; last error: {err}; "
                              f"last raw sha256={h}")
                    for i in ids:
                        withheld[i] = reason
                    print(f"[{tag} batch {bi}] WITHHELD ids {ids[0]}..{ids[-1]}",
                          flush=True)
                    done = True
    return merged, retries_log, withheld


def main():
    t0 = time.time()
    dump, log_a, wh_dump = capture("dump", gc.parse_dump)
    teach, log_b, wh_teach = capture("teach", gc.parse_teach)
    assert not wh_dump, "dump batches withheld — investigate, do not freeze"

    corpus = {
        "meta": {
            "model": gc.MODEL, "temperature": gc.TEMPERATURE, "seed": gc.SEED,
            "batch": gc.BATCH,
            "prereg": "wave12/championship-english/corpus-input/ENGLISH_PROMPT_SET.md",
            "prompts_sha256": gc.EXPECTED_PROMPTS_SHA,
            "facts_sha256": gc.EXPECTED_FACTS_SHA,
            "prompt_batch_sha256": gc.PROMPT_SHA,
            "input_claim": "facts.json supplied values (228 world-true + 12 "
                           "deliberately false)",
            "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "retries": log_a + log_b,
            "format_layout": dict(gc.FORMAT_STATS),
            "procedure_note": "prompts read verbatim from frozen batch files; "
                              "single-line block layout accepted mechanically "
                              "(same rules as Q2 step37)",
        },
        "input_claims": {str(i): gc.t5_plant_claim(i) for i in range(240)},
        "false_ids": sorted(gc.FALSE_IDS),
        "withheld_ids": sorted(wh_teach),
        "dump": [{"id": i, "value": dump[i]["value"],
                  "sentence": dump[i]["sentence"]} for i in range(240)],
        "teach": ([{"id": i, "obs_value": teach[i]["obs_value"],
                    "observation": teach[i]["observation"],
                    "distract_value": teach[i]["distract_value"],
                    "distractor": teach[i]["distractor"],
                    "probe": teach[i]["probe"],
                    "probe_value": teach[i]["probe_value"]}
                   for i in range(240) if i not in wh_teach] +
                  [{"id": i, "withheld": True, "withheld_reason": wh_teach[i]}
                   for i in sorted(wh_teach)]),
    }
    corpus["teach"].sort(key=lambda e: e["id"])
    inv = {"E_dump": [], "E_obs": [], "E_prb": [],
           "inconsistent": [], "sentence_missing_value": [], "E_format": []}
    for i in range(240):
        if i in wh_teach:
            inv["E_format"].append(i)
            continue
        want = gc.t5_plant_claim(i)
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

    with open(os.path.join(CORPUS_DIR, "corpus.json"), "w") as f:
        json.dump(corpus, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"corpus.json written with {len(wh_teach)} withheld ids "
          f"({time.time()-t0:.0f}s)", flush=True)
    r = subprocess.run([sys.executable,
                        os.path.join(HERE, "finalize_corpus.py")])
    if r.returncode != 0:
        raise SystemExit("finalize_corpus.py failed")


if __name__ == "__main__":
    main()
