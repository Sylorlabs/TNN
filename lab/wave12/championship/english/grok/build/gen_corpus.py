#!/usr/bin/env python3
"""Championship ENGLISH-box corpus generation (source: grok-4.6, OPPORTUNISTIC leg).

Governed by the frozen English corpus-input (2026-09-21):
- Prompts read VERBATIM from the 40 frozen batch files
  (batch00_dump.txt ... batch19_teach.txt; sha256 of each in SHA256SUMS.txt).
- Claim reference = facts.json supplied values (228 world-true + 12
  deliberately false; false_ids [3,29,55,71,80,103,117,139,163,178,205,231]).
- Model: grok-4.6 via UnoRouter chat/completions, temperature=0, seed=42.
- Batches retried ONLY on mechanical parse failure (max 2, logged) — NEVER
  retried because values were wrong (wrong values are the experiment).
- 429/503: paced 90s waits, max ~2h cumulative, then STOP (BLOCKED).
- Every raw response byte captured + sha256'd; corpus.json is the frozen artifact.
Output: corpus/corpus.json (Q2 structure), corpus/SHA256.txt, corpus/raw/,
corpus/SHA256SUMS.txt.
"""
import hashlib
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error

sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
from dynamic_credentials import add_surrogate_to_request, read_json_response

HERE = os.path.dirname(os.path.abspath(__file__))  # grok/build
ROOT = os.path.dirname(HERE)                        # grok
INPUT = "/home/hatch/workspace/tnn-lab/wave12/championship-english/corpus-input"
FACTS_PATH = os.path.join(INPUT, "facts.json")
CORPUS_DIR = os.path.join(ROOT, "corpus")
RAW_DIR = os.path.join(CORPUS_DIR, "raw")

BASE = "https://api.unorouter.com/v1"
MODEL = "grok-4.6"
TEMPERATURE = 0
SEED = 42
BATCH = 12
N_BATCHES = 20

EXPECTED_PROMPTS_SHA = ("ac5d7d3155f9a90dc60f4f3ec529a3c6125a0469ce5862c7193fb261441b8b7d")
EXPECTED_FACTS_SHA = "4f1ba933a75a0f9e488ae170366afe7f514aec425f92432f5b0e0b49c4bfede5"

# ---- frozen reference data ----
_facts_raw = json.load(open(FACTS_PATH))
FALSE_IDS = set(_facts_raw["false_ids"])
FACTS = {int(k): v for k, v in _facts_raw.items()
         if k not in ("false_ids", "meta")}
assert set(FACTS) == set(range(240)), "facts.json id set drift"

def t5_plant_claim(i):
    """Supplied (trainer's) value — authoritative claim for the learner."""
    return FACTS[i]["value"]

def t5_cat(i):
    if i < 48: return "alpha-pos"
    if i < 96: return "word-len"
    if i < 144: return "pub-year"
    return "count-fact"

assert all(FACTS[i]["category"] == t5_cat(i) for i in range(240)), "cat boundary drift"
assert sorted(FALSE_IDS) == [3,29,55,71,80,103,117,139,163,178,205,231], "false_ids drift"

# ---- frozen integrity checks (fail fast on drift) ----
with open(FACTS_PATH, "rb") as f:
    _h = hashlib.sha256(f.read()).hexdigest()
assert _h == EXPECTED_FACTS_SHA, f"facts.json sha mismatch: {_h}"

_m = re.search(r"## PROMPT-A-EN \(fact dump\)\n```\n(.*?)```",
               open(os.path.join(INPUT, "ENGLISH_PROMPT_SET.md")).read(), re.DOTALL)
_pa = _m.group(1)
_m = re.search(r"## PROMPT-B-EN \(teaching sequence\)\n```\n(.*?)```",
               open(os.path.join(INPUT, "ENGLISH_PROMPT_SET.md")).read(), re.DOTALL)
_pb = _m.group(1)
_h = hashlib.sha256((_pa.rstrip("\n") + "\n" + _pb.rstrip("\n")).encode()).hexdigest()
assert _h == EXPECTED_PROMPTS_SHA, f"prompt template sha mismatch: {_h}"
print(f"frozen integrity OK: facts.json sha256={EXPECTED_FACTS_SHA[:16]}..., "
      f"prompt templates sha256={EXPECTED_PROMPTS_SHA[:16]}...", flush=True)

def batch_ids(bi):
    return list(range(bi * BATCH, (bi + 1) * BATCH))

def read_prompt(tag, bi):
    """Read the frozen batch prompt file VERBATIM."""
    p = os.path.join(INPUT, f"batch{bi:02d}_{tag}.txt")
    with open(p) as f:
        prompt = f.read()
    # mechanical: verify the fact lines match facts.json supplied values
    fact_lines = [ln for ln in prompt.split("\n")
                  if re.match(r"^\d+ \| ", ln)]
    ids = batch_ids(bi)
    assert len(fact_lines) == len(ids), f"{tag} batch {bi}: fact line count drift"
    for ln, i in zip(fact_lines, ids):
        want = f"{i} | {t5_cat(i)} | {t5_plant_claim(i)} | {FACTS[i]['claim_text']}"
        assert ln.strip() == want, f"{tag} batch {bi} fact line drift: {ln!r} != {want!r}"
    return prompt

PROMPT_SHA = {}
for tag in ("dump", "teach"):
    for bi in range(N_BATCHES):
        p = os.path.join(INPUT, f"batch{bi:02d}_{tag}.txt")
        PROMPT_SHA[f"{tag}_batch{bi:02d}"] = hashlib.sha256(open(p, "rb").read()).hexdigest()

# ---- API ----
_rate_limit_t0 = None

def api_call(prompt):
    global _rate_limit_t0
    payload = {"model": MODEL,
               "messages": [{"role": "user", "content": prompt}],
               "temperature": TEMPERATURE, "seed": SEED, "stream": False}
    last = None
    for attempt in range(1, 11):
        try:
            req = urllib.request.Request(
                BASE + "/chat/completions", data=json.dumps(payload).encode(), method="POST")
            req.add_header("Content-Type", "application/json")
            add_surrogate_to_request(req, "custom.unorouter",
                                     allowed_hosts=("api.unorouter.com", "unorouter.com"))
            with urllib.request.urlopen(req, timeout=240) as resp:
                body = read_json_response(resp)
            return body["choices"][0]["message"]["content"]
        except urllib.error.HTTPError as e:
            last = e
            code = e.code
            if code in (429, 503):
                if _rate_limit_t0 is None:
                    _rate_limit_t0 = time.time()
                elapsed = time.time() - _rate_limit_t0
                if elapsed > 2 * 3600:
                    raise RuntimeError(
                        f"STOP: 429/503 persists after ~2h of paced retries — BLOCKED")
                print(f"  {code} rate-limit (paced wait 90s; elapsed "
                      f"{elapsed/60:.0f}m/120m)", flush=True)
                time.sleep(90)
                continue
            print(f"  HTTP error {code} (attempt {attempt}/10)", flush=True)
            time.sleep(10 * attempt)
        except Exception as e:
            last = e
            print(f"  transient API error (attempt {attempt}/10): "
                  f"{type(e).__name__}: {e}", flush=True)
            time.sleep(10 * attempt)
    raise RuntimeError(f"api_call failed after 10 attempts: {last}")

# ---- parsing (mechanical; same rules as step37) ----
DUMP_SINGLE = re.compile(
    r"^ID:\s*(\d+)\s+VALUE:\s*(-?\d+)\s+SENTENCE:\s*(.+)$")
TEACH_SINGLE = re.compile(
    r"^ID:\s*(\d+)\s+OBS_VALUE:\s*(-?\d+)\s+OBSERVATION:\s*(.+?)"
    r"\s+DISTRACT_VALUE:\s*(-?\d+)\s+DISTRACTOR:\s*(.+?)"
    r"\s+PROBE:\s*(.+?)\s+PROBE_VALUE:\s*(-?\d+)\s*$")
FORMAT_STATS = {"single_line": 0, "multi_line": 0, "unparsed": 0}

def parse_blocks(text, fields, single_pat=None, single_fields=None):
    chunks = re.split(r"\n\s*\n", text.strip())
    out = []
    for ch in chunks:
        lines = ch.split("\n")
        if single_pat is not None and len(lines) == 1:
            line = lines[0].strip()
            keys_ok = all(line.count(f + ":") == 1 for f in single_fields)
            m = single_pat.match(line) if keys_ok else None
            if m:
                d = dict(zip(single_fields, (g.strip() for g in m.groups())))
                FORMAT_STATS["single_line"] += 1
                out.append(d)
                continue
            FORMAT_STATS["unparsed"] += 1
        else:
            FORMAT_STATS["multi_line"] += 1
        d, cur = {}, None
        for line in lines:
            m = re.match(r"^([A-Z_]+):\s*(.*)$", line.strip())
            if m and m.group(1) in fields:
                cur = m.group(1)
                d[cur] = m.group(2).strip()
            elif cur is not None:
                d[cur] = (d[cur] + " " + line.strip()).strip()
        out.append(d)
    return out

def parse_dump(text, ids):
    blocks = parse_blocks(text, {"ID", "VALUE", "SENTENCE"},
                          DUMP_SINGLE, ["ID", "VALUE", "SENTENCE"])
    if len(blocks) != len(ids):
        return None, f"block count {len(blocks)} != {len(ids)}"
    res = {}
    for b in blocks:
        try:
            i, v = int(b["ID"]), int(b["VALUE"])
        except (KeyError, ValueError) as e:
            return None, f"bad ID/VALUE: {e} in {b}"
        if "SENTENCE" not in b or not b["SENTENCE"]:
            return None, f"missing SENTENCE for id {i}"
        if i in res:
            return None, f"duplicate id {i}"
        res[i] = {"value": v, "sentence": b["SENTENCE"]}
    if set(res) != set(ids):
        return None, f"id set mismatch: got {sorted(res)} want {sorted(ids)}"
    return res, None

def parse_teach(text, ids):
    blocks = parse_blocks(
        text, {"ID", "OBS_VALUE", "OBSERVATION", "DISTRACT_VALUE",
               "DISTRACTOR", "PROBE", "PROBE_VALUE"},
        TEACH_SINGLE, ["ID", "OBS_VALUE", "OBSERVATION", "DISTRACT_VALUE",
                       "DISTRACTOR", "PROBE", "PROBE_VALUE"])
    if len(blocks) != len(ids):
        return None, f"block count {len(blocks)} != {len(ids)}"
    res = {}
    for b in blocks:
        try:
            i = int(b["ID"])
            ov, dv, pv = int(b["OBS_VALUE"]), int(b["DISTRACT_VALUE"]), int(b["PROBE_VALUE"])
        except (KeyError, ValueError) as e:
            return None, f"bad numeric field: {e} in {b}"
        for f in ("OBSERVATION", "DISTRACTOR", "PROBE"):
            if f not in b or not b[f]:
                return None, f"missing {f} for id {i}"
        if i in res:
            return None, f"duplicate id {i}"
        res[i] = {"obs_value": ov, "observation": b["OBSERVATION"],
                  "distract_value": dv, "distractor": b["DISTRACTOR"],
                  "probe": b["PROBE"], "probe_value": pv}
    if set(res) != set(ids):
        return None, f"id set mismatch: got {sorted(res)} want {sorted(ids)}"
    return res, None

# ---- driver ----
def run_artifact(tag, parse_fn, only=None):
    os.makedirs(RAW_DIR, exist_ok=True)
    merged, retries_log = {}, []
    rng = [only] if only is not None else range(N_BATCHES)
    for bi in rng:
        ids = batch_ids(bi)
        prompt = read_prompt(tag, bi)
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
            raw = api_call(prompt)
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
                    raise SystemExit(
                        f"FATAL: {tag} batch {bi} unparseable after 2 retries: {err}")
    return merged, retries_log

def main():
    only = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[1] == "--only-batch" else None
    tag = sys.argv[3] if len(sys.argv) > 3 else None
    if only is not None:
        dump, log_a = run_artifact("dump", parse_dump, only=only)
        print(f"smoke batch {only}: dump ok ({len(dump)} facts)", flush=True)
        return
    t0 = time.time()
    dump, log_a = run_artifact("dump", parse_dump)
    teach, log_b = run_artifact("teach", parse_teach)

    corpus = {
        "meta": {
            "model": MODEL, "temperature": TEMPERATURE, "seed": SEED,
            "batch": BATCH,
            "prereg": "wave12/championship-english/corpus-input/ENGLISH_PROMPT_SET.md",
            "prompts_sha256": EXPECTED_PROMPTS_SHA,
            "facts_sha256": EXPECTED_FACTS_SHA,
            "prompt_batch_sha256": PROMPT_SHA,
            "input_claim": "facts.json supplied values (228 world-true + 12 "
                           "deliberately false)",
            "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "retries": log_a + log_b,
            "format_layout": dict(FORMAT_STATS),
            "procedure_note": "prompts read verbatim from frozen batch files; "
                              "single-line block layout accepted mechanically "
                              "(same rules as Q2 step37)",
        },
        "input_claims": {str(i): t5_plant_claim(i) for i in range(240)},
        "false_ids": sorted(FALSE_IDS),
        "dump": [{"id": i, "value": dump[i]["value"],
                  "sentence": dump[i]["sentence"]} for i in range(240)],
        "teach": [{"id": i, "obs_value": teach[i]["obs_value"],
                   "observation": teach[i]["observation"],
                   "distract_value": teach[i]["distract_value"],
                   "distractor": teach[i]["distractor"],
                   "probe": teach[i]["probe"],
                   "probe_value": teach[i]["probe_value"]} for i in range(240)],
    }
    # LLM-error inventory (mechanical)
    inv = {"E_dump": [], "E_obs": [], "E_prb": [],
           "inconsistent": [], "sentence_missing_value": []}
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

    with open(os.path.join(CORPUS_DIR, "corpus.json"), "w") as f:
        json.dump(corpus, f, indent=1, ensure_ascii=False)
        f.write("\n")
    with open(os.path.join(CORPUS_DIR, "corpus.json"), "rb") as f:
        sha = hashlib.sha256(f.read()).hexdigest()
    with open(os.path.join(CORPUS_DIR, "SHA256.txt"), "w") as f:
        f.write(sha + "\n")
    with open(os.path.join(RAW_DIR, "SHA256SUMS.txt"), "w") as f:
        for bi in range(N_BATCHES):
            for tg in ("dump", "teach"):
                p = os.path.join(RAW_DIR, f"{tg}_batch{bi:02d}.txt")
                with open(p, "rb") as rf:
                    f.write(hashlib.sha256(rf.read()).hexdigest() +
                            f"  {tg}_batch{bi:02d}.txt\n")
    print(f"corpus.json sha256={sha}", flush=True)
    print(f"error inventory: " +
          ", ".join(f"{k}={v['n']}" for k, v in corpus["error_inventory"].items()),
          flush=True)
    print(f"done in {time.time()-t0:.0f}s", flush=True)

if __name__ == "__main__":
    main()
