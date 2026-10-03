#!/usr/bin/env python3
"""Championship ENGLISH corpus generation (source: step-3.7-flash:free).

English box, "square": real English data replaces the toy Zharovia facts.

Frozen inputs (read-only, verified before run):
- 40 batch prompt files in championship-english/corpus-input/
  (sha256 verified OK against SHA256SUMS.txt)
- facts.json: 240 facts with trainer-SUPPLIED values (12 deliberately false)
- Prompt template sha256 ac5d7d31... (recorded in facts.json meta)

- Prompts are read DIRECTLY from the frozen batch files (no extraction,
  no construction). The script asserts every facts line (id|category|value)
  in each prompt matches facts.json.
- Model: step-3.7-flash:free, temperature=0, seed=42 (UnoRouter chat/completions).
- Batches retried ONLY on mechanical parse failure (max 2, logged) — NEVER
  retried because values were wrong (wrong values are the experiment).
- 429/503: paced 90s waits; no hammering.
- Every raw response byte captured + sha256'd; corpus.json is the frozen artifact.
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

HERE = os.path.dirname(os.path.abspath(__file__))  # step/build
ROOT = os.path.dirname(HERE)                        # step
CORPUS_IN = "/home/hatch/workspace/tnn-lab/wave12/championship-english/corpus-input"
CORPUS_DIR = os.path.join(ROOT, "corpus")
RAW_DIR = os.path.join(CORPUS_DIR, "raw")

BASE = "https://api.unorouter.com/v1"
MODEL = "step-3.7-flash:free"
TEMPERATURE = 0
SEED = 42
BATCH = 12
N_BATCH = 20

FROZEN_PROMPTS_SHA = "ac5d7d3155f9a90dc60f4f3ec529a3c6125a0469ce5862c7193fb261441b8b7d"

# ---- claim reference: facts.json trainer-supplied values ----
_fj = json.load(open(os.path.join(CORPUS_IN, "facts.json")))
SUPPLIED, CAT, CLAIM, IS_FALSE = {}, {}, {}, {}
for k, v in _fj.items():
    if k in ("false_ids", "meta"):
        continue
    i = int(k)
    SUPPLIED[i] = v["value"]
    CAT[i] = v["category"]
    CLAIM[i] = v["claim_text"]
    IS_FALSE[i] = v["false"]
FALSE_IDS = sorted(_fj["false_ids"])
assert sorted(SUPPLIED) == list(range(240)), "facts.json must have ids 0..239"
assert FALSE_IDS == [3, 29, 55, 71, 80, 103, 117, 139, 163, 178, 205, 231]
assert _fj["meta"]["prompts_sha256"] == FROZEN_PROMPTS_SHA, "prompts sha drift"
# true values: supplied for all but the 12 false ids (mechanical categories
# cross-checked; pub-year/count-fact from ground_truth_notes.md).
_TRUE_CORRECTIONS = {3: 4, 29: 4, 55: 8, 71: 20, 80: 9, 103: 1678,
                     117: 1850, 139: 1895, 163: 3, 178: 9, 205: 37, 231: 8}
for _i in range(48):  # alpha-pos mechanical
    assert (SUPPLIED[_i] == ord(CLAIM[_i]) - 64) != IS_FALSE[_i], f"alpha-pos assert id {_i}"
for _i in range(48, 96):  # word-len mechanical
    assert (SUPPLIED[_i] == len(CLAIM[_i])) != IS_FALSE[_i], f"word-len assert id {_i}"
TRUE = {i: _TRUE_CORRECTIONS.get(i, SUPPLIED[i]) for i in range(240)}
print(f"claim reference loaded: 240 facts, {len(FALSE_IDS)} false ids, prompts_sha OK",
      flush=True)

# ---- frozen prompt files: verify sha + assert facts lines match facts.json ----
_PROMPT_FILES = {}   # (tag, batch_idx) -> prompt text
_PROMPT_SHAS = {}
_sumfile = {parts[1]: parts[0] for line in open(os.path.join(CORPUS_IN, "SHA256SUMS.txt"))
            for parts in (line.split(),) if len(parts) == 2}
for _bi in range(N_BATCH):
    for _tag in ("dump", "teach"):
        _name = f"batch{_bi:02d}_{_tag}.txt"
        _path = os.path.join(CORPUS_IN, _name)
        _data = open(_path, "rb").read()
        _h = hashlib.sha256(_data).hexdigest()
        assert _h == _sumfile[_name], f"frozen prompt {_name} sha mismatch — aborting"
        text = _data.decode("utf-8")
        _lines = [l for l in text.splitlines() if re.match(r"^\d+ \|", l)]
        assert len(_lines) == BATCH, f"{_name}: {_lines} fact lines"
        for _l in _lines:
            _id, _cat, _val, _claim = [p.strip() for p in _l.split("|", 3)]
            _id = int(_id)
            assert _cat == CAT[_id] and int(_val) == SUPPLIED[_id] and _claim == CLAIM[_id], \
                f"{_name}: facts line drift: {_l}"
        _PROMPT_FILES[(_tag, _bi)] = text
        _PROMPT_SHAS[_name] = _h
print(f"frozen prompts verified: 40/40 sha OK, facts lines match facts.json", flush=True)

# ---- API ----
def api_call(prompt):
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
            with urllib.request.urlopen(req, timeout=300) as resp:
                body = read_json_response(resp)
            return body["choices"][0]["message"]["content"]
        except urllib.error.HTTPError as e:
            last = e
            if e.code in (429, 503):
                print(f"  rate-limited/server busy ({e.code}); paced 90s wait", flush=True)
                time.sleep(90)
            else:
                print(f"  HTTP error {e.code} (attempt {attempt}/10): {e}", flush=True)
                time.sleep(10 * attempt)
        except Exception as e:
            last = e
            print(f"  transient API error (attempt {attempt}/10): "
                  f"{type(e).__name__}: {e}", flush=True)
            time.sleep(10 * attempt)
    raise RuntimeError(f"api_call failed after 10 attempts: {last}")

# ---- parsing (mechanical; ported from the proven q2 sibling) ----
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
    for bi in range(N_BATCH):
        ids = list(range(bi * BATCH, (bi + 1) * BATCH))
        prompt = _PROMPT_FILES[(tag, bi)]
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
    assert len(merged) == 240, f"{tag}: only {len(merged)}/240 facts"
    return merged, retries_log

def main():
    t0 = time.time()
    dump, log_a = run_artifact("dump", parse_dump)
    teach, log_b = run_artifact("teach", parse_teach)

    corpus = {
        "meta": {
            "model": MODEL, "temperature": TEMPERATURE, "seed": SEED,
            "batch": BATCH,
            "prompt_source": "championship-english/corpus-input/batchNN_{dump,teach}.txt "
                             "(frozen; 40/40 sha256 verified against SHA256SUMS.txt)",
            "prompts_sha256": FROZEN_PROMPTS_SHA,
            "prompt_files_sha256": {n: _PROMPT_SHAS[n] for n in sorted(_PROMPT_SHAS)},
            "facts_ref": "facts.json supplied values (228 world-true + 12 deliberately false)",
            "categories": ["alpha-pos", "word-len", "pub-year", "count-fact"],
            "cat_bounds": [48, 96, 144],
            "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "retries": log_a + log_b,
            "format_layout": dict(FORMAT_STATS),
        },
        "input_claims": {str(i): SUPPLIED[i] for i in range(240)},
        "false_ids": FALSE_IDS,
        "fact_meta": {str(i): {"category": CAT[i], "claim_text": CLAIM[i],
                               "supplied": SUPPLIED[i], "true": TRUE[i],
                               "false_plant": IS_FALSE[i]} for i in range(240)},
        "dump": [{"id": i, "value": dump[i]["value"],
                  "sentence": dump[i]["sentence"]} for i in range(240)],
        "teach": [{"id": i, "obs_value": teach[i]["obs_value"],
                   "observation": teach[i]["observation"],
                   "distract_value": teach[i]["distract_value"],
                   "distractor": teach[i]["distractor"],
                   "probe": teach[i]["probe"],
                   "probe_value": teach[i]["probe_value"]} for i in range(240)],
    }
    # LLM-error inventory (mechanical, vs facts.json supplied claims)
    inv = {"E_dump": [], "E_obs": [], "E_prb": [],
           "inconsistent": [], "sentence_missing_value": []}
    for i in range(240):
        want = SUPPLIED[i]
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
        for bi in range(N_BATCH):
            for tag in ("dump", "teach"):
                p = os.path.join(RAW_DIR, f"{tag}_batch{bi:02d}.txt")
                with open(p, "rb") as rf:
                    f.write(hashlib.sha256(rf.read()).hexdigest() +
                            f"  {tag}_batch{bi:02d}.txt\n")
    print(f"corpus.json sha256={sha}", flush=True)
    print(f"error inventory: " +
          ", ".join(f"{k}={v['n']}" for k, v in corpus["error_inventory"].items()),
          flush=True)
    print(f"format_layout: {dict(FORMAT_STATS)}", flush=True)
    print(f"done in {time.time()-t0:.0f}s", flush=True)

if __name__ == "__main__":
    main()
