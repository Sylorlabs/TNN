#!/usr/bin/env python3
"""Championship ENGLISH corpus generation (source: gpt-5.6-sol via UnoRouter).

English box ("square", classes 1-4): replaces the toy Zharovia facts with
real English data. Corpus is FROZEN in corpus-input/ (2026-09-21); this
script reads the 40 frozen batch prompts BYTE-EXACTLY and sends them to
gpt-5.6-sol, temp=0, seed=42.

Adapted from q2-distillation-step37/build/gen_corpus.py (proven pattern).
- Prompts are the 40 FROZEN batch files (not extracted from any prereg).
  Prompts sha256 (canonical templates): ac5d7d3155f9a90dc60f4f3ec529a3c6125a0469ce5862c7193fb261441b8b7d
  (verified against build_english_corpus.py source before run).
- Claim reference: facts.json SUPPLIED values (trainer-authoritative,
  228 world-true + 12 deliberately false; ground truth lives in
  ground_truth_notes.md, used only by the scorer, never by this script).
- Batches retried ONLY on mechanical parse failure (max 2, logged) — NEVER
  retried because values were wrong (wrong values are the experiment).
- 429/503: 90s waits, max ~21 retries (SWE-run precedent); do not hammer.
- Every raw response byte captured + sha256'd; corpus.json is frozen output.
"""
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
from dynamic_credentials import add_surrogate_to_request, read_json_response

SOL_DIR = os.path.dirname(os.path.abspath(__file__))          # .../sol
CHAMP_DIR = os.path.dirname(SOL_DIR)                          # .../championship-english
INPUT_DIR = os.path.join(CHAMP_DIR, "corpus-input")            # frozen input
CORPUS_DIR = os.path.join(SOL_DIR, "corpus")
RAW_DIR = os.path.join(CORPUS_DIR, "raw")

BASE = "https://api.unorouter.com/v1"
MODEL = "gpt-5.6-sol"
TEMPERATURE = 0
SEED = 42
BATCH = 12

EXPECTED_PROMPTS_SHA = "ac5d7d3155f9a90dc60f4f3ec529a3c6125a0469ce5862c7193fb261441b8b7d"

# ---- claim reference: facts.json SUPPLIED values (trainer-authoritative) ----
with open(os.path.join(INPUT_DIR, "facts.json")) as f:
    FACTS = json.load(f)
FALSE_IDS = set(int(x) for x in FACTS["false_ids"])
assert FALSE_IDS == {3, 29, 55, 71, 80, 103, 117, 139, 163, 178, 205, 231}, \
    "facts.json false_ids drift — aborting"

def t5_plant_claim(i):
    return int(FACTS[str(i)]["value"])

def t5_cat(i):
    if i < 48: return 0
    if i < 96: return 1
    if i < 144: return 2
    return 3

CATS = ["alpha-pos", "word-len", "pub-year", "count-fact"]

# sanity: facts.json categories line up with the id boundaries
for i in range(240):
    assert FACTS[str(i)]["category"] == CATS[t5_cat(i)], f"category drift at {i}"

# ---- frozen prompt verification ----
def read_prompt(tag, bi):
    p = os.path.join(INPUT_DIR, f"batch{bi:02d}_{tag}.txt")
    with open(p, "r", encoding="utf-8") as f:
        return f.read()

# verify canonical-template sha from the builder (independent of batch files)
def canonical_sha():
    src = open(os.path.join(INPUT_DIR, "build_english_corpus.py")).read()
    ns = {}
    for name in ("PROMPT_A_EN", "PROMPT_B_EN"):
        m = re.search(name + r'\s*=\s*("""|\'\'\')(.*?)\1', src, re.DOTALL)
        assert m, f"{name} not found in frozen builder"
        ns[name] = m.group(2)
    return hashlib.sha256(
        (ns["PROMPT_A_EN"] + "\n" + ns["PROMPT_B_EN"]).encode("utf-8")).hexdigest()

# verify every batch file == canonical template + facts + trailing newline
def verify_batches():
    src = open(os.path.join(INPUT_DIR, "build_english_corpus.py")).read()
    ns = {}
    for name in ("PROMPT_A_EN", "PROMPT_B_EN"):
        m = re.search(name + r'\s*=\s*("""|\'\'\')(.*?)\1', src, re.DOTALL)
        ns[name] = m.group(2)
    for bi in range(240 // BATCH):
        ids = list(range(bi * BATCH, (bi + 1) * BATCH))
        block = "\n".join(
            f"{i} | {FACTS[str(i)]['category']} | {FACTS[str(i)]['value']} | "
            f"{FACTS[str(i)]['claim_text']}" for i in ids)
        for tag, pname in (("dump", "PROMPT_A_EN"), ("teach", "PROMPT_B_EN")):
            expect = ns[pname].replace("{{FACTS}}", block) + "\n"
            actual = read_prompt(tag, bi)
            assert actual == expect, f"frozen batch drift: batch{bi:02d}_{tag}"
    return True

# ---- API ----
def api_call(prompt):
    payload = {"model": MODEL,
               "messages": [{"role": "user", "content": prompt}],
               "temperature": TEMPERATURE, "seed": SEED, "stream": False}
    rate_attempts = 0
    transient_attempts = 0
    while True:
        try:
            req = urllib.request.Request(
                BASE + "/chat/completions", data=json.dumps(payload).encode(), method="POST")
            req.add_header("Content-Type", "application/json")
            add_surrogate_to_request(req, "custom.unorouter",
                                     allowed_hosts=("api.unorouter.com", "unorouter.com"))
            with urllib.request.urlopen(req, timeout=300) as resp:
                body = read_json_response(resp)
            return body["choices"][0]["message"]["content"]
        except urllib.error.HTTPError as e:
            if e.code in (429, 503):
                rate_attempts += 1
                if rate_attempts > 21:
                    raise RuntimeError(f"rate-limited 21x in a row, aborting")
                print(f"  HTTP {e.code}: paced wait 90s "
                      f"(rate retry {rate_attempts}/21)", flush=True)
                time.sleep(90)
                continue
            raise
        except Exception as e:
            transient_attempts += 1
            if transient_attempts > 10:
                raise RuntimeError(f"api_call failed after 10 transient errors: {e}")
            print(f"  transient API error (attempt {transient_attempts}/10): "
                  f"{type(e).__name__}: {e}", flush=True)
            time.sleep(10 * transient_attempts)

# ---- parsing (mechanical; identical to Q2, accepts both layouts) ----
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
def run_artifact(tag, parse_fn):
    os.makedirs(RAW_DIR, exist_ok=True)
    merged, retries_log = {}, []
    for bi in range(240 // BATCH):
        ids = list(range(bi * BATCH, (bi + 1) * BATCH))
        prompt = read_prompt(tag, bi)
        raw_path = os.path.join(RAW_DIR, f"{tag}_batch{bi:02d}.txt")
        # resume: reuse raw output if it already parses
        done = False
        if os.path.exists(raw_path):
            with open(raw_path, encoding="utf-8") as f:
                raw = f.read()
            res, err = parse_fn(raw, ids)
            if err is None:
                merged.update(res)
                print(f"[{tag} batch {bi}] resumed from raw (parses)", flush=True)
                done = True
        attempt = 0
        while not done:
            raw = api_call(prompt)
            with open(raw_path, "w", encoding="utf-8") as f:
                f.write(raw)
            h = hashlib.sha256(raw.encode("utf-8")).hexdigest()
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
            if not done:
                time.sleep(5)   # polite pacing between model calls
        time.sleep(5)           # polite pacing between batches
    assert len(merged) == 240, f"{tag}: only {len(merged)}/240 facts"
    return merged, retries_log

def main():
    t0 = time.time()
    print("verifying frozen prompts...", flush=True)
    sha = canonical_sha()
    assert sha == EXPECTED_PROMPTS_SHA, f"canonical prompts sha drift: {sha}"
    verify_batches()
    print(f"frozen prompts OK (canonical sha256={sha[:16]}...; 40 batch files match)",
          flush=True)
    dump, log_a = run_artifact("dump", parse_dump)
    teach, log_b = run_artifact("teach", parse_teach)

    corpus = {
        "meta": {
            "model": MODEL, "temperature": TEMPERATURE, "seed": SEED,
            "batch": BATCH,
            "corpus_input": "championship-english/corpus-input (frozen 2026-09-21)",
            "prompts_sha256": EXPECTED_PROMPTS_SHA,
            "input_claim": "facts.json SUPPLIED values: trainer's intended English "
                           "records (228 world-true + 12 deliberately false)",
            "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "retries": log_a + log_b,
            "format_layout": dict(FORMAT_STATS),
            "procedure_note": "single-line block layout accepted mechanically "
                              "(same parser as q2-distillation-step37)",
            "english_box": "square (classes 1-4); categories alpha-pos/word-len/"
                           "pub-year/count-fact with boundaries 48/96/144",
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
    # LLM-error inventory (mechanical, vs facts.json SUPPLIED values)
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

    with open(os.path.join(CORPUS_DIR, "corpus.json"), "w", encoding="utf-8") as f:
        json.dump(corpus, f, indent=1, ensure_ascii=False)
        f.write("\n")
    with open(os.path.join(CORPUS_DIR, "corpus.json"), "rb") as f:
        sha = hashlib.sha256(f.read()).hexdigest()
    with open(os.path.join(CORPUS_DIR, "SHA256.txt"), "w") as f:
        f.write(sha + "\n")
    with open(os.path.join(RAW_DIR, "SHA256SUMS.txt"), "w") as f:
        for bi in range(240 // BATCH):
            for tag in ("dump", "teach"):
                p = os.path.join(RAW_DIR, f"{tag}_batch{bi:02d}.txt")
                with open(p, "rb") as rf:
                    f.write(hashlib.sha256(rf.read()).hexdigest() +
                            f"  {tag}_batch{bi:02d}.txt\n")
    print(f"corpus.json sha256={sha}", flush=True)
    print(f"error inventory: " +
          ", ".join(f"{k}={v['n']}" for k, v in corpus["error_inventory"].items()),
          flush=True)
    print(f"done in {time.time()-t0:.0f}s", flush=True)

if __name__ == "__main__":
    main()
