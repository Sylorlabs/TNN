#!/usr/bin/env python3
"""SWE-leg Phase 1 — frozen LLM corpus generation (source: swe-1-6-slow:free ONLY).

Adapted from q2-distillation/build/gen_corpus.py: MODEL changed; pacing
support (--pace SECONDS, default 0) added because the free tier allows
1 request/min on this model (429 body 2026-09-21: "nothing is used up,
retry in 8s"); seed-behavior logging added (records whether the API
echoes seed / returns system_fingerprint).

Governed by prereg/PREREG_Q2_DISTILLATION.md (FROZEN 2026-09-21).
- Prompts are extracted PROGRAMMATICALLY from the frozen prereg (single source of truth).
- Model: swe-1-6-slow:free, temperature=0, seed=42 (UnoRouter chat/completions).
- Batches retried ONLY on mechanical parse failure (max 2, logged) — NEVER
  retried because values were wrong (wrong values are the experiment, §7/C1).
- Every raw response byte captured + sha256'd; corpus.json is the frozen artifact.
"""
import hashlib
import json
import os
import re
import struct
import sys
import argparse
import time
import urllib.request

P = argparse.ArgumentParser()
P.add_argument("--pace", type=float, default=0.0,
               help="min seconds between API calls (free tier: use 65)")
ARGS = P.parse_args()
_LAST_CALL = [0.0]

sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
from dynamic_credentials import add_surrogate_to_request, read_json_response

HERE = os.path.dirname(os.path.abspath(__file__))  # q2-distillation/build
ROOT = os.path.dirname(HERE)                        # q2-distillation
PREREG = os.path.join(ROOT, "prereg", "PREREG_Q2_DISTILLATION.md")
CORPUS_DIR = os.path.join(ROOT, "corpus")
RAW_DIR = os.path.join(CORPUS_DIR, "raw")

BASE = "https://api.unorouter.com/v1"
MODEL = "swe-1-6-slow:free"
TEMPERATURE = 0
SEED = 42
BATCH = 12
SEED_BEHAVIOR = {"model": MODEL, "seed_requested": SEED, "seed_sent": False,
                 "seed_status": "UNSUPPORTED: UnoRouter proxy returned HTTP 400 "
                                "'Unsupported sampling parameter(s): seed. The "
                                "upstream backend ignores these, so this proxy "
                                "rejects them rather than silently dropping them. "
                                "Remove them, or set penalties to 0.' "
                                "(request id 202609211914357796387028268d9d6KOC4olqi). "
                                "Seed param REMOVED from payload 2026-09-21; "
                                "temperature=0 is the only determinism lever. "
                                "The API does NOT honor seed=42. Calls below "
                                "carry no seed.",
                 "calls": []}

CATS = ["province-code", "council-rank", "chronicle-year",
        "founding-year", "harbor-index", "ruler-index"]

# ---- Zharovia domain (mechanical port of t5_core.zag; hash-verified) ----
def t5_cat(i):
    if i < 48: return 0
    if i < 72: return 1
    if i < 108: return 2
    if i < 156: return 3
    if i < 192: return 4
    return 5

def t5_truth(i):
    c = t5_cat(i)
    x = [i, i-48, i-72, i-108, i-156, i-192][c]
    m = [12, 8, 100, 200, 48, 36][c]
    r = [(x*7+3) % m, (x*5+1) % m, (x*11+7) % m,
         (x*13+2) % m, (x*9+5) % m, (x*17+4) % m][c]
    return [0, 0, 1800, 1700, 0, 0][c] + r

FALSE_IDS = {3, 29, 55, 71, 80, 103, 117, 139, 163, 178, 205, 231}

def t5_plant_claim(i):
    if i in FALSE_IDS:
        c = t5_cat(i)
        m = [12, 8, 100, 200, 48, 36][c]
        b = [0, 0, 1800, 1700, 0, 0][c]
        return b + ((t5_truth(i) - b + 1) % m)
    return t5_truth(i)

# sanity: domain hash must match the frozen expectation
_buf = b"".join(struct.pack("<i", t5_truth(i)) for i in range(240))
assert hashlib.sha256(_buf).hexdigest() == \
    "7cd0baf80a62acc338e1c9bdec5b33c0e3427af18d78b98b7cbda153a3f92ee8", \
    "domain port drift — aborting"

# ---- prompt extraction from the frozen prereg ----
def extract_prompt(name):
    with open(PREREG) as f:
        text = f.read()
    m = re.search(r"### " + name + r".*?```\n(.*?)```", text, re.DOTALL)
    assert m, f"prompt {name} not found in frozen prereg"
    tmpl = m.group(1)
    assert "{{FACTS}}" in tmpl, f"prompt {name} missing {{{{FACTS}}}} placeholder"
    return tmpl

PROMPT_A = extract_prompt("PROMPT-A")
PROMPT_B = extract_prompt("PROMPT-B")
PROMPTS_SHA = hashlib.sha256((PROMPT_A + "\n" + PROMPT_B).encode()).hexdigest()
print(f"extracted frozen prompts from prereg; sha256={PROMPTS_SHA}", flush=True)

# ---- API ----
def api_call(prompt):
    if ARGS.pace > 0:
        dt = time.time() - _LAST_CALL[0]
        if dt < ARGS.pace:
            time.sleep(ARGS.pace - dt)
    _LAST_CALL[0] = time.time()
    payload = {"model": MODEL,
               "messages": [{"role": "user", "content": prompt}],
               "temperature": TEMPERATURE, "stream": False}
    # NOTE 2026-09-21: "seed" removed. UnoRouter proxy returns HTTP 400
    # "Unsupported sampling parameter(s): seed. The upstream backend
    # ignores these, so this proxy rejects them rather than silently
    # dropping them" — the API cannot honor seed=42 at all (recorded in
    # seed_behavior.json as evidence, step 2). Source identity unchanged
    # (same model id); temperature=0 is the only determinism lever.
    # PREREG intent (deterministic call params) is best-effort under
    # provider constraints; recorded, not bent.
    last = None
    retried_429 = False
    attempt = 0
    while True:
        attempt += 1
        try:
            req = urllib.request.Request(
                BASE + "/chat/completions", data=json.dumps(payload).encode(), method="POST")
            req.add_header("Content-Type", "application/json")
            add_surrogate_to_request(req, "custom.unorouter",
                                     allowed_hosts=("api.unorouter.com", "unorouter.com"))
            with urllib.request.urlopen(req, timeout=240) as resp:
                body = read_json_response(resp)
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
                # pacing miss: wait 90s, single mechanical retry, then hard stop
                if not retried_429:
                    print("  HTTP 429 despite pacing: waiting 90s, "
                          "single mechanical retry (logged)", flush=True)
                    time.sleep(90)
                    retried_429 = True
                    attempt = 0  # give the retry a fresh transient-error budget
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
def parse_blocks(text, fields):
    """Split response into blocks on blank lines; each block is a dict of
    FIELD -> text (multi-line values joined)."""
    chunks = re.split(r"\n\s*\n", text.strip())
    out = []
    for ch in chunks:
        d, cur = {}, None
        for line in ch.split("\n"):
            m = re.match(r"^([A-Z_]+):\s*(.*)$", line.strip())
            if m and m.group(1) in fields:
                cur = m.group(1)
                d[cur] = m.group(2).strip()
            elif cur is not None:
                d[cur] = (d[cur] + " " + line.strip()).strip()
        out.append(d)
    return out

def parse_dump(text, ids):
    blocks = parse_blocks(text, {"ID", "VALUE", "SENTENCE"})
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
               "DISTRACTOR", "PROBE", "PROBE_VALUE"})
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
def run_artifact(tag, prompt_tmpl, parse_fn):
    os.makedirs(RAW_DIR, exist_ok=True)
    merged, retries_log = {}, []
    for bi in range(240 // BATCH):
        ids = list(range(bi * BATCH, (bi + 1) * BATCH))
        facts = "\n".join(f"{i} | {CATS[t5_cat(i)]} | {t5_plant_claim(i)}" for i in ids)
        prompt = prompt_tmpl.replace("{{FACTS}}", facts)
        raw_path = os.path.join(RAW_DIR, f"{tag}_batch{bi:02d}.txt")
        # resume: reuse raw output if it already parses
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
    dump, log_a = run_artifact("dump", PROMPT_A, parse_dump)
    teach, log_b = run_artifact("teach", PROMPT_B, parse_teach)

    corpus = {
        "meta": {
            "model": MODEL, "temperature": TEMPERATURE,
            "seed_requested": SEED, "seed_sent": False,
            "seed_note": "provider 400-rejects seed; see seed_behavior.json",
            "batch": BATCH, "prereg": "prereg/PREREG_Q2_DISTILLATION.md",
            "prompts_sha256": PROMPTS_SHA,
            "input_claim": "t5_plant_claim(id): trainer's intended Zharovia records "
                           "(228 world-true + 12 deliberately false)",
            "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "retries": log_a + log_b,
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
    # LLM-error inventory (mechanical, §7)
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
    # raw batch hashes
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
    print(f"seed behavior: {n_calls} calls, fingerprints={sorted(x for x in fps if x)}, "
          f"seed_echo_values={sorted(set(str(e) for e in echoes))}", flush=True)
    print(f"corpus.json sha256={sha}", flush=True)
    print(f"error inventory: " +
          ", ".join(f"{k}={v['n']}" for k, v in corpus["error_inventory"].items()),
          flush=True)
    print(f"done in {time.time()-t0:.0f}s", flush=True)

if __name__ == "__main__":
    main()
