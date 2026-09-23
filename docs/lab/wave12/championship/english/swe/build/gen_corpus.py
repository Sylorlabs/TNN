#!/usr/bin/env python3
"""SWE-ENGLISH championship corpus generation (source: swe-1-6-slow:free ONLY).

Real-English championship box ("square", classes 3+4): replaces the toy
Zharovia facts with real English data. Frozen input:
  ../corpus-input/batchNN_{dump,teach}.txt  (40 frozen batch prompts)
  ../corpus-input/facts.json                (240 facts, supplied values)
  prompts sha256 ac5d7d3155f9a90dc60f4f3ec529a3c6125a0469ce5862c7193fb261441b8b7d
  (verified before run; batch files = template + facts + trailing newline,
  verified byte-for-byte for all 40).

Adapted from wave12/q2-distillation-swe/build/gen_corpus.py:
- Prompts are READ VERBATIM from the 40 frozen batch files (no extraction,
  no {{FACTS}} substitution — the facts are already in the files).
- Claim reference = facts.json SUPPLIED values (trainer's intended records:
  228 true + 12 deliberately false; same 12 ids as Q2 for comparability).
- Model: swe-1-6-slow:free, temperature=0, seed=42 requested; the UnoRouter
  proxy 400-rejects the seed param for this model (toy-run evidence
  2026-09-21, request id 202609211914357796387028268d9d6KOC4olqi). This run
  probes once at startup and records the outcome in seed_behavior.json.
- Batches retried ONLY on mechanical parse failure (max 2, logged) — NEVER
  retried because values were "wrong" (wrong values are the experiment).
- 1 request/min pacing (free tier); 429 despite pacing -> 90s wait, single
  mechanical retry, then hard stop. Do not hammer.
- Every raw response byte captured + sha256'd; corpus.json is the frozen
  artifact.
"""
import hashlib
import json
import os
import re
import sys
import argparse
import time
import urllib.request

P = argparse.ArgumentParser()
P.add_argument("--pace", type=float, default=65.0,
               help="min seconds between API calls (free tier: use 65)")
ARGS = P.parse_args()
_LAST_CALL = [0.0]

sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
from dynamic_credentials import add_surrogate_to_request, read_json_response

HERE = os.path.dirname(os.path.abspath(__file__))       # swe/build
SWE = os.path.dirname(HERE)                             # swe
INPUT = "/home/hatch/workspace/tnn-lab/wave12/championship-english/corpus-input"
CORPUS_DIR = os.path.join(SWE, "corpus")
RAW_DIR = os.path.join(CORPUS_DIR, "raw")
FACTS_PATH = os.path.join(INPUT, "facts.json")
INPUT_SUMS = os.path.join(INPUT, "SHA256SUMS.txt")

BASE = "https://api.unorouter.com/v1"
MODEL = "swe-1-6-slow:free"
TEMPERATURE = 0
SEED = 42
BATCH = 12
PROMPTS_SHA_FROZEN = "ac5d7d3155f9a90dc60f4f3ec529a3c6125a0469ce5862c7193fb261441b8b7d"

SEED_BEHAVIOR = {"model": MODEL, "seed_requested": SEED, "seed_sent": None,
                 "probe": {}, "calls": []}

# ---- frozen input verification ----
facts = json.load(open(FACTS_PATH))
_fact_keys = [k for k in facts if k.isdigit()]
assert len(_fact_keys) == 240, "facts.json must have 240 fact entries"
FALSE_IDS = set(facts["false_ids"])
assert FALSE_IDS == {3, 29, 55, 71, 80, 103, 117, 139, 163, 178, 205, 231}, \
    "false ids drift — aborting"
SUPPLIED = {i: facts[str(i)]["value"] for i in range(240)}
CATEGORY = {i: facts[str(i)]["category"] for i in range(240)}
CLAIMTXT = {i: facts[str(i)]["claim_text"] for i in range(240)}
assert facts["meta"]["prompts_sha256"] == PROMPTS_SHA_FROZEN, \
    "facts.json prompts_sha256 drift — aborting"


def t5_plant_claim(i):
    return SUPPLIED[i]


# verify every frozen batch file: name, sha256 (from frozen SHA256SUMS.txt),
# and that its facts rows match facts.json supplied values exactly.
_sums = {}
for line in open(INPUT_SUMS):
    line = line.strip()
    if line:
        h, n = line.split()
        _sums[n] = h
PROMPTS = {}
for bi in range(20):
    for tag in ("dump", "teach"):
        name = f"batch{bi:02d}_{tag}.txt"
        raw = open(os.path.join(INPUT, name), "rb").read()
        assert hashlib.sha256(raw).hexdigest() == _sums[name], \
            f"frozen prompt {name} sha256 mismatch — aborting"
        text = raw.decode("utf-8")
        PROMPTS[(tag, bi)] = text
        rows = re.findall(r"^(\d+) \| ([a-z-]+) \| (-?\d+) \| (.+)$", text,
                          re.MULTILINE)
        assert len(rows) == 12, f"{name}: {len(rows)} fact rows != 12"
        for rid, rcat, rval, rclaim in rows:
            i = int(rid)
            assert rcat == CATEGORY[i], f"{name} id {i}: category drift"
            assert int(rval) == SUPPLIED[i], f"{name} id {i}: value drift"
            assert rclaim == CLAIMTXT[i], f"{name} id {i}: claim drift"
        ids = [int(r[0]) for r in rows]
        assert ids == list(range(bi * 12, (bi + 1) * 12)), \
            f"{name}: id order drift"
print(f"frozen input verified: 40 batch prompts (sha256 ok), "
      f"240 facts, prompts_sha256={PROMPTS_SHA_FROZEN}", flush=True)

# ---- API ----
def _post(payload):
    req = urllib.request.Request(
        BASE + "/chat/completions", data=json.dumps(payload).encode(),
        method="POST")
    req.add_header("Content-Type", "application/json")
    add_surrogate_to_request(req, "custom.unorouter",
                             allowed_hosts=("api.unorouter.com", "unorouter.com"))
    with urllib.request.urlopen(req, timeout=240) as resp:
        body = read_json_response(resp)
    return body


def seed_probe():
    """One paced probe call WITH seed=42 to test provider support."""
    payload = {"model": MODEL,
               "messages": [{"role": "user",
                             "content": "Reply with the single word: ok"}],
               "temperature": TEMPERATURE, "seed": SEED, "stream": False}
    try:
        body = _post(payload)
        SEED_BEHAVIOR["probe"] = {
            "seed_param": "accepted",
            "response_keys": sorted(body.keys()),
            "system_fingerprint": body.get("system_fingerprint"),
            "seed_echo": body.get("seed"),
            "content": body["choices"][0]["message"]["content"][:80],
        }
        return True
    except Exception as e:
        SEED_BEHAVIOR["probe"] = {
            "seed_param": "rejected",
            "error": f"{type(e).__name__}: {e}",
        }
        return False


def api_call(prompt, use_seed):
    if ARGS.pace > 0:
        dt = time.time() - _LAST_CALL[0]
        if dt < ARGS.pace:
            time.sleep(ARGS.pace - dt)
    _LAST_CALL[0] = time.time()
    payload = {"model": MODEL,
               "messages": [{"role": "user", "content": prompt}],
               "temperature": TEMPERATURE, "stream": False}
    if use_seed:
        payload["seed"] = SEED
    last = None
    retried_429 = False
    attempt = 0
    while True:
        attempt += 1
        try:
            body = _post(payload)
            SEED_BEHAVIOR["calls"].append({
                "response_keys": sorted(body.keys()),
                "system_fingerprint": body.get("system_fingerprint"),
                "seed_echo": body.get("seed"),
                "usage": body.get("usage"),
            })
            return body["choices"][0]["message"]["content"]
        except Exception as e:
            code = getattr(e, "code", None)
            if code == 429:
                if not retried_429:
                    print("  HTTP 429 despite pacing: waiting 90s, "
                          "single mechanical retry (logged)", flush=True)
                    time.sleep(90)
                    retried_429 = True
                    attempt = 0
                    continue
                raise RuntimeError(
                    "HTTP 429 again after 90s wait + retry: throttle "
                    "impassable; BLOCKED") from e
            last = e
            if attempt >= 10:
                raise RuntimeError(
                    f"api_call failed after 10 transient attempts: {last}")
            print(f"  transient API error (attempt {attempt}/10): "
                  f"{type(e).__name__}: {e}", flush=True)
            time.sleep(10 * attempt)

# ---- parsing (mechanical) ----
# Accepts both the prompt's one-field-per-line layout and the whole-block
# single-line layout (step-3.7-flash:free emitted single-line at temp=0 in
# the Q2 run; swe-1-6-slow:free layout is recorded per batch in
# meta["format_layout"]). Layout acceptance is content-neutral: block count,
# id set, field presence, int parsing, and the value inventory are
# unchanged. Per-batch layout is recorded in meta["format_layout"].
DUMP_SINGLE = re.compile(
    r"^ID:\s*(\d+)\s+VALUE:\s*(-?\d+)\s+SENTENCE:\s*(.+)$")
TEACH_SINGLE = re.compile(
    r"^ID:\s*(\d+)\s+OBS_VALUE:\s*(-?\d+)\s+OBSERVATION:\s*(.+?)"
    r"\s+DISTRACT_VALUE:\s*(-?\d+)\s+DISTRACTOR:\s*(.+?)"
    r"\s+PROBE:\s*(.+?)\s+PROBE_VALUE:\s*(-?\d+)\s*$")
FORMAT_STATS = {"single_line": 0, "multi_line": 0, "unparsed": 0}


def parse_blocks(text, fields, single_pat=None, single_fields=None):
    """Split response into blocks on blank lines; each block is a dict of
    FIELD -> text (multi-line values joined). Also accepts whole-block
    single-line layout via single_pat (full-line match, each keyword must
    appear exactly once in the line)."""
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
def run_artifact(tag, parse_fn, use_seed):
    os.makedirs(RAW_DIR, exist_ok=True)
    merged, retries_log = {}, []
    for bi in range(240 // BATCH):
        ids = list(range(bi * BATCH, (bi + 1) * BATCH))
        prompt = PROMPTS[(tag, bi)]
        raw_path = os.path.join(RAW_DIR, f"{tag}_batch{bi:02d}.txt")
        done = False
        if os.path.exists(raw_path):
            with open(raw_path) as f:
                raw = f.read()
            res, err = parse_fn(raw, ids)
            if err is None:
                merged.update(res)
                print(f"[{tag} batch {bi}] resumed from raw (parses)",
                      flush=True)
                done = True
        attempt = 0
        while not done:
            raw = api_call(prompt, use_seed)
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
                retries_log.append({"tag": tag, "batch": bi,
                                    "attempt": attempt, "error": err,
                                    "raw_sha256": h})
                print(f"[{tag} batch {bi}] PARSE FAIL (attempt {attempt}): "
                      f"{err}", flush=True)
                if attempt > 2:
                    raise SystemExit(
                        f"FATAL: {tag} batch {bi} unparseable after "
                        f"2 retries: {err}")
    assert len(merged) == 240, f"{tag}: only {len(merged)}/240 facts"
    return merged, retries_log

def main():
    t0 = time.time()
    print("seed probe: sending one call WITH seed=42 ...", flush=True)
    use_seed = seed_probe()
    SEED_BEHAVIOR["seed_sent"] = bool(use_seed)
    if use_seed:
        print("seed probe: ACCEPTED — main run will send seed=42",
              flush=True)
    else:
        print("seed probe: REJECTED — main run omits seed (recorded); "
              "temperature=0 is the only determinism lever", flush=True)
    _LAST_CALL[0] = time.time()  # pace the first corpus call after the probe

    dump, log_a = run_artifact("dump", parse_dump, use_seed)
    teach, log_b = run_artifact("teach", parse_teach, use_seed)

    corpus = {
        "meta": {
            "model": MODEL, "temperature": TEMPERATURE,
            "seed_requested": SEED, "seed_sent": bool(use_seed),
            "seed_note": ("provider honored seed=42" if use_seed else
                          "provider 400-rejects seed; see seed_behavior.json"),
            "batch": BATCH,
            "corpus": "english-championship-v1",
            "prompt_source": "corpus-input/batchNN_{dump,teach}.txt "
                             "(frozen, read verbatim)",
            "prompts_sha256": PROMPTS_SHA_FROZEN,
            "input_claim": "facts.json supplied values: trainer's intended "
                           "English records (228 true + 12 deliberately "
                           "false; same 12 ids as Q2 for comparability)",
            "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ",
                                            time.gmtime()),
            "retries": log_a + log_b,
            "format_layout": dict(FORMAT_STATS),
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
                   "probe_value": teach[i]["probe_value"]}
                  for i in range(240)],
    }
    # LLM-error inventory (mechanical, vs trainer-SUPPLIED claims).
    # Transcription-failure taxonomy (§2, two directions):
    #   FOOLED   = model reports the SUPPLIED value for a false id
    #              (faithful transcription; prompt-obedient)
    #   CORRECTED = model reports the TRUE value for a false id despite the
    #              instruction to state the given value (prior-knowledge
    #              override; transcription failure in the other direction)
    inv = {"E_dump": [], "E_obs": [], "E_prb": [],
           "inconsistent": [], "sentence_missing_value": [],
           "distractor_eq_obs": []}
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
        if teach[i]["distract_value"] == teach[i]["obs_value"]:
            inv["distractor_eq_obs"].append(i)
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
        for bi in range(240 // BATCH):
            for tag in ("dump", "teach"):
                p = os.path.join(RAW_DIR, f"{tag}_batch{bi:02d}.txt")
                with open(p, "rb") as rf:
                    f.write(hashlib.sha256(rf.read()).hexdigest() +
                            f"  {tag}_batch{bi:02d}.txt\n")
    with open(os.path.join(CORPUS_DIR, "seed_behavior.json"), "w") as f:
        json.dump(SEED_BEHAVIOR, f, indent=1)
        f.write("\n")
    n_calls = len(SEED_BEHAVIOR["calls"])
    fps = {c["system_fingerprint"] for c in SEED_BEHAVIOR["calls"]}
    echoes = [c["seed_echo"] for c in SEED_BEHAVIOR["calls"]]
    print(f"seed behavior: probe={SEED_BEHAVIOR['probe'].get('seed_param')}, "
          f"{n_calls} calls, "
          f"fingerprints={sorted(x for x in fps if x)}, "
          f"seed_echo_values={sorted(set(str(e) for e in echoes))}",
          flush=True)
    print(f"corpus.json sha256={sha}", flush=True)
    print(f"error inventory: " +
          ", ".join(f"{k}={v['n']}"
                    for k, v in corpus["error_inventory"].items()),
          flush=True)
    print(f"done in {time.time()-t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
