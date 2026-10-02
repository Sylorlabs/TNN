#!/usr/bin/env python3
"""hy3 ENGLISH-box corpus capture (SOURCE team, opportunistic leg).

Captures the 40 FROZEN English batch prompts (corpus-input/batchNN_{dump,teach}.txt)
via UnoRouter model hy3:free (temperature=0, seed=42), then freezes
corpus/corpus.json in the Q2 structure, plus corpus/SHA256.txt,
corpus/raw/{dump,teach}_batchNN.txt, corpus/SHA256SUMS.txt.

Prompt integrity: the 40 batch files are verified against the frozen
corpus-input/SHA256SUMS.txt before any API call (abort on mismatch).

Claim reference = facts.json SUPPLIED values (authoritative for the model;
228 real-world-true + 12 deliberately false).

Retry policy:
- Transient API errors (HTTP 503 "all providers busy", timeouts, ...) are
  retried with 90s pacing, up to API_ATTEMPTS_MAX per batch. These are
  mechanical transport failures, not content judgments.
- A batch whose response PARSES is never re-called (resume-safe).
- PARSE failures: retry ONLY on mechanical parse failure (max 2 per batch),
  logged in meta["retries"]. NEVER retried because values were "wrong"
  (wrong values are the experiment, §7/C1).
- After 2 failed parse retries the run aborts (FATAL) so a human can inspect.
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

HERE = os.path.dirname(os.path.abspath(__file__))          # hy3/
INPUT = os.path.abspath(os.path.join(HERE, "..", "corpus-input"))
FACTS_JSON = os.path.join(INPUT, "facts.json")
FROZEN_SUMS = os.path.join(INPUT, "SHA256SUMS.txt")
CORPUS_DIR = os.path.join(HERE, "corpus")
RAW_DIR = os.path.join(CORPUS_DIR, "raw")
LOG = os.path.join(HERE, "capture.log")

BASE = "https://api.unorouter.com/v1"
MODEL = "hy3:free"
TEMPERATURE = 0
SEED = 42
BATCH = 12
NBATCH = 20
PARSE_RETRIES_MAX = 2
API_ATTEMPTS_MAX = 60      # per batch; 60 x 90s = ~90 min cap
API_WAIT_S = 90
REQ_TIMEOUT_S = 240


def log(msg):
    line = f"{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())} {msg}"
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")


# ---- frozen prompt verification ----
def verify_prompts():
    sums = {}
    with open(FROZEN_SUMS) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            h, name = line.split(None, 1)
            sums[name] = h
    for bi in range(NBATCH):
        for tag in ("dump", "teach"):
            name = f"batch{bi:02d}_{tag}.txt"
            p = os.path.join(INPUT, name)
            with open(p, "rb") as f:
                got = hashlib.sha256(f.read()).hexdigest()
            exp = sums.get(name)
            if exp is None or got != exp:
                sys.exit(f"FATAL: frozen prompt {name} sha256 mismatch: "
                         f"got {got} want {exp}")
    log("all 40 frozen prompts verified against SHA256SUMS.txt")


# ---- claim reference (facts.json supplied values) ----
def load_claims():
    d = json.load(open(FACTS_JSON))
    supplied, is_false = {}, {}
    for k, v in d.items():
        if k in ("false_ids", "meta"):
            continue
        i = int(k)
        supplied[i] = int(v["value"])
        is_false[i] = bool(v["false"])
    assert len(supplied) == 240, f"facts.json has {len(supplied)} facts"
    false_ids = sorted(int(x) for x in d["false_ids"])
    assert false_ids == [3, 29, 55, 71, 80, 103, 117, 139, 163, 178, 205, 231], \
        f"unexpected false_ids {false_ids}"
    for i in false_ids:
        assert is_false[i], f"false id {i} not flagged in facts.json"
    log(f"claims loaded: 240 supplied values, 12 false ids {false_ids}")
    return supplied, false_ids


# ---- API ----
def api_call(prompt):
    payload = {"model": MODEL,
               "messages": [{"role": "user", "content": prompt}],
               "temperature": TEMPERATURE, "seed": SEED, "stream": False}
    last = None
    for attempt in range(1, API_ATTEMPTS_MAX + 1):
        try:
            req = urllib.request.Request(
                BASE + "/chat/completions", data=json.dumps(payload).encode(),
                method="POST")
            req.add_header("Content-Type", "application/json")
            add_surrogate_to_request(req, "custom.unorouter",
                                     allowed_hosts=("api.unorouter.com",
                                                    "unorouter.com"))
            with urllib.request.urlopen(req, timeout=REQ_TIMEOUT_S) as resp:
                body = read_json_response(resp)
            return body["choices"][0]["message"]["content"]
        except urllib.error.HTTPError as e:
            last = e
            try:
                eb = e.read().decode("utf-8", "replace")[:160]
            except Exception:
                eb = ""
            log(f"  transient API error (attempt {attempt}/{API_ATTEMPTS_MAX}): "
                f"HTTPError {e.code}: {eb}")
            if e.code in (400, 404):
                sys.exit(f"FATAL: HTTP {e.code} on {MODEL}: {eb}")
        except Exception as e:
            last = e
            log(f"  transient API error (attempt {attempt}/{API_ATTEMPTS_MAX}): "
                f"{type(e).__name__}: {str(e)[:160]}")
        time.sleep(API_WAIT_S)
    sys.exit(f"FATAL: api_call failed after {API_ATTEMPTS_MAX} attempts: {last}")


# ---- parsing (mechanical; mirrors q2-distillation-step37 build) ----
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
            ov = int(b["OBS_VALUE"])
            dv = int(b["DISTRACT_VALUE"])
            pv = int(b["PROBE_VALUE"])
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
    for bi in range(NBATCH):
        ids = list(range(bi * BATCH, (bi + 1) * BATCH))
        with open(os.path.join(INPUT, f"batch{bi:02d}_{tag}.txt")) as f:
            prompt = f.read()
        raw_path = os.path.join(RAW_DIR, f"{tag}_batch{bi:02d}.txt")
        done = False
        if os.path.exists(raw_path):
            with open(raw_path) as f:
                raw = f.read()
            res, err = parse_fn(raw, ids)
            if err is None:
                merged.update(res)
                log(f"[{tag} batch {bi}] resumed from raw (parses)")
                done = True
        attempt = 0
        while not done:
            raw = api_call(prompt)
            with open(raw_path, "wb") as f:
                f.write(raw.encode("utf-8"))
            h = hashlib.sha256(raw.encode("utf-8")).hexdigest()
            res, err = parse_fn(raw, ids)
            if err is None:
                merged.update(res)
                log(f"[{tag} batch {bi}] ok sha256={h[:16]}")
                done = True
            else:
                attempt += 1
                retries_log.append({"tag": tag, "batch": bi,
                                    "attempt": attempt, "error": err,
                                    "raw_sha256": h})
                log(f"[{tag} batch {bi}] PARSE FAIL (attempt {attempt}): {err}")
                if attempt > PARSE_RETRIES_MAX:
                    sys.exit(f"FATAL: {tag} batch {bi} unparseable after "
                             f"{PARSE_RETRIES_MAX} retries: {err}")
    assert len(merged) == 240, f"{tag}: only {len(merged)}/240 facts"
    return merged, retries_log


def main():
    t0 = time.time()
    verify_prompts()
    supplied, false_ids = load_claims()
    dump, log_a = run_artifact("dump", parse_dump)
    teach, log_b = run_artifact("teach", parse_teach)

    corpus = {
        "meta": {
            "model": MODEL, "temperature": TEMPERATURE, "seed": SEED,
            "batch": BATCH,
            "prompts": "corpus-input/batchNN_{dump,teach}.txt (frozen; "
                       "sha256 ac5d7d3155f9a90dc60f4f3ec529a3c6125a0469ce58"
                       "62c7193fb261441b8b7d)",
            "input_claim": "facts.json SUPPLIED values (authoritative): "
                           "228 real-world-true + 12 deliberately false "
                           "(ids 3,29,55,71,80,103,117,139,163,178,205,231)",
            "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ",
                                           time.gmtime()),
            "retries": log_a + log_b,
            "format_layout": dict(FORMAT_STATS),
            "procedure_note": "single-line block layout accepted mechanically "
                              "(mirrors q2-distillation-step37 build); batch "
                              "prompts read verbatim from the frozen 40 files",
        },
        "input_claims": {str(i): supplied[i] for i in range(240)},
        "false_ids": false_ids,
        "dump": [{"id": i, "value": dump[i]["value"],
                  "sentence": dump[i]["sentence"]} for i in range(240)],
        "teach": [{"id": i, "obs_value": teach[i]["obs_value"],
                   "observation": teach[i]["observation"],
                   "distract_value": teach[i]["distract_value"],
                   "distractor": teach[i]["distractor"],
                   "probe": teach[i]["probe"],
                   "probe_value": teach[i]["probe_value"]}
                  for i in range(240)],
    }
    # LLM-error inventory (mechanical, §7)
    inv = {"E_dump": [], "E_obs": [], "E_prb": [],
           "inconsistent": [], "sentence_missing_value": []}
    for i in range(240):
        want = supplied[i]
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
    corpus["error_inventory"] = {k: {"n": len(v), "ids": v}
                                 for k, v in inv.items()}

    with open(os.path.join(CORPUS_DIR, "corpus.json"), "w") as f:
        json.dump(corpus, f, indent=1, ensure_ascii=False)
        f.write("\n")
    with open(os.path.join(CORPUS_DIR, "corpus.json"), "rb") as f:
        sha = hashlib.sha256(f.read()).hexdigest()
    with open(os.path.join(CORPUS_DIR, "SHA256.txt"), "w") as f:
        f.write(sha + "\n")
    with open(os.path.join(RAW_DIR, "SHA256SUMS.txt"), "w") as f:
        for bi in range(NBATCH):
            for tag in ("dump", "teach"):
                p = os.path.join(RAW_DIR, f"{tag}_batch{bi:02d}.txt")
                with open(p, "rb") as rf:
                    f.write(hashlib.sha256(rf.read()).hexdigest() +
                            f"  {tag}_batch{bi:02d}.txt\n")
    log(f"corpus.json sha256={sha}")
    log("error inventory: " +
        ", ".join(f"{k}={v['n']}" for k, v in corpus["error_inventory"].items()))
    log(f"done in {time.time()-t0:.0f}s")
    print(f"corpus.json sha256={sha}")


if __name__ == "__main__":
    main()
