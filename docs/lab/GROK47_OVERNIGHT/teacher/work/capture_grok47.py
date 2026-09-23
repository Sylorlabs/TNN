#!/usr/bin/env python3
"""grok-4.7 English-box corpus capture (frozen protocol, experientiallabs gateway).

Follows wave12/championship/english/grok/build/gen_corpus.py semantics:
- frozen batch prompts read VERBATIM, fact-line drift assertions
- temperature=0, seed=42 requested (dropped+logged if gateway rejects)
- retries ONLY on mechanical parse failure (max 2) — never on wrong values
- 429/503: 90s pacing, STOP after ~2h cumulative
Every raw response byte captured + sha256'd.
Lane mode: --lane L --lanes K processes batches bi with bi % K == L.
Partials written to partial/<tag>_batchNN.json (resume-safe).
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
import dynamic_credentials as dc

MODEL = "grok-4.7"
HOST = "api.experientiallabs.ai"
BASE = f"https://{HOST}/v1"
CRED = "custom.experientiallabs"
TEMPERATURE = 0
SEED = 42

HERE = os.path.dirname(os.path.abspath(__file__))          # work/
REPORT = os.path.dirname(HERE)                             # teacher/
EV = os.path.join(REPORT, "evidence", "grok47_corpus")
RAW_DIR = os.path.join(EV, "raw")
PARTIAL_DIR = os.path.join(HERE, "partial")
INPUT = "/home/hatch/workspace/tnn-lab/wave12/championship-english/corpus-input"
FACTS_PATH = os.path.join(INPUT, "facts.json")
EXPECTED_FACTS_SHA = "4f1ba933a75a0f9e488ae170366afe7f514aec425f92432f5b0e0b49c4bfede5"
BATCH = 12
N_BATCHES = 20

_facts_raw = json.load(open(FACTS_PATH))
FALSE_IDS = set(_facts_raw["false_ids"])
FACTS = {int(k): v for k, v in _facts_raw.items() if k not in ("false_ids", "meta")}
assert set(FACTS) == set(range(240)), "facts.json id set drift"
assert sorted(FALSE_IDS) == [3,29,55,71,80,103,117,139,163,178,205,231], "false_ids drift"
with open(FACTS_PATH, "rb") as f:
    _h = hashlib.sha256(f.read()).hexdigest()
assert _h == EXPECTED_FACTS_SHA, f"facts.json sha mismatch: {_h}"

def t5_plant_claim(i):
    return FACTS[i]["value"]

def t5_cat(i):
    if i < 48: return "alpha-pos"
    if i < 96: return "word-len"
    if i < 144: return "pub-year"
    return "count-fact"

def batch_ids(bi):
    return list(range(bi * BATCH, (bi + 1) * BATCH))

def read_prompt(tag, bi):
    p = os.path.join(INPUT, f"batch{bi:02d}_{tag}.txt")
    with open(p) as f:
        prompt = f.read()
    fact_lines = [ln for ln in prompt.split("\n") if re.match(r"^\d+ \| ", ln)]
    ids = batch_ids(bi)
    assert len(fact_lines) == len(ids), f"{tag} batch {bi}: fact line count drift"
    for ln, i in zip(fact_lines, ids):
        want = f"{i} | {t5_cat(i)} | {t5_plant_claim(i)} | {FACTS[i]['claim_text']}"
        assert ln.strip() == want, f"{tag} batch {bi} fact line drift: {ln!r} != {want!r}"
    return prompt

_rate_limit_t0 = None

def api_call(prompt):
    """POST chat/completions; returns response text."""
    global _rate_limit_t0
    payload = {"model": MODEL,
               "messages": [{"role": "user", "content": prompt}],
               # NOTE 2026-09-21: experientiallabs gateway rejects "seed"
               # ("not supported by this gateway profile") — dropped per prereg.
               "temperature": TEMPERATURE,
               "max_tokens": 16384, "stream": False}
    body = json.dumps(payload).encode()
    last = None
    for attempt in range(1, 11):
        try:
            req = urllib.request.Request(BASE + "/chat/completions", data=body, method="POST")
            req.add_header("Content-Type", "application/json")
            dc.add_surrogate_to_request(req, CRED, allowed_hosts=(HOST,))
            with urllib.request.urlopen(req, timeout=240) as resp:
                data = dc.read_json_response(resp)
            return data["choices"][0]["message"]["content"]
        except urllib.error.HTTPError as e:
            last = e
            code = e.code
            if code in (429, 503):
                if _rate_limit_t0 is None:
                    _rate_limit_t0 = time.time()
                elapsed = time.time() - _rate_limit_t0
                if elapsed > 2 * 3600:
                    raise RuntimeError("STOP: 429/503 persists after ~2h — BLOCKED")
                print(f"  {code} rate-limit (paced wait 90s; elapsed {elapsed/60:.0f}m/120m)", flush=True)
                time.sleep(90)
                continue
            print(f"  HTTP error {code} (attempt {attempt}/10)", flush=True)
            time.sleep(10 * attempt)
        except Exception as e:
            last = e
            print(f"  transient API error (attempt {attempt}/10): {type(e).__name__}: {e}", flush=True)
            time.sleep(10 * attempt)
    raise RuntimeError(f"api_call failed after 10 attempts: {last}")

# ---- parsing (byte-identical semantics to frozen gen_corpus.py) ----
DUMP_SINGLE = re.compile(r"^ID:\s*(\d+)\s+VALUE:\s*(-?\d+)\s+SENTENCE:\s*(.+)$")
TEACH_SINGLE = re.compile(
    r"^ID:\s*(\d+)\s+OBS_VALUE:\s*(-?\d+)\s+OBSERVATION:\s*(.+?)"
    r"\s+DISTRACT_VALUE:\s*(-?\d+)\s+DISTRACTOR:\s*(.+?)"
    r"\s+PROBE:\s*(.+?)\s+PROBE_VALUE:\s*(-?\d+)\s*$")

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
                out.append(dict(zip(single_fields, (g.strip() for g in m.groups()))))
                continue
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
    blocks = parse_blocks(text, {"ID", "VALUE", "SENTENCE"}, DUMP_SINGLE, ["ID", "VALUE", "SENTENCE"])
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
    blocks = parse_blocks(text, {"ID", "OBS_VALUE", "OBSERVATION", "DISTRACT_VALUE",
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

def transport_ok(tag, raw):
    """Truncation guard (FALLBACK ALERT 2026-09-21: grok-4.7 truncating).
    Frozen grok-4.6 raws: all 20 dump raws end with '.'; all 20 teach raws
    end with 'PROBE_VALUE: <int>'. A response failing this is a TRANSPORT
    truncation, not a model error: void the batch and recapture (own budget).
    """
    s = raw.strip()
    if tag == "dump":
        return s.endswith(".")
    return re.search(r"PROBE_VALUE:\s*-?\d+\s*$", s) is not None

PARSERS = {"dump": parse_dump, "teach": parse_teach}

def process_batch(tag, bi):
    ids = batch_ids(bi)
    prompt = read_prompt(tag, bi)
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(PARTIAL_DIR, exist_ok=True)
    raw_path = os.path.join(RAW_DIR, f"{tag}_batch{bi:02d}.txt")
    part_path = os.path.join(PARTIAL_DIR, f"{tag}_batch{bi:02d}.json")
    if os.path.exists(part_path) and os.path.exists(raw_path):
        res, err = PARSERS[tag](open(raw_path).read(), ids)
        if err is None:
            print(f"[{tag} batch {bi}] resumed (partial+raw parse)", flush=True)
            return res, []
    retries = []
    trunc_retries = []
    attempt = 0
    while True:
        raw = api_call(prompt)
        with open(raw_path, "w") as f:
            f.write(raw)
        h = hashlib.sha256(raw.encode()).hexdigest()
        if not transport_ok(tag, raw):
            trunc_retries.append({"tag": tag, "batch": bi, "raw_sha256": h,
                                  "note": "TRANSPORT TRUNCATION — batch voided, recapturing"})
            print(f"[{tag} batch {bi}] TRUNCATED RESPONSE (voided, recapture "
                  f"#{len(trunc_retries)}): sha256={h[:16]}", flush=True)
            if len(trunc_retries) > 3:
                raise SystemExit(f"FATAL: {tag} batch {bi} truncated 4x — gateway degraded, STOP")
            continue
        res, err = PARSERS[tag](raw, ids)
        if err is None:
            with open(part_path, "w") as f:
                json.dump({"tag": tag, "batch": bi, "raw_sha256": h, "facts": res,
                           "retries": retries, "truncations": trunc_retries}, f, ensure_ascii=False)
            print(f"[{tag} batch {bi}] ok sha256={h[:16]}", flush=True)
            return res, retries
        attempt += 1
        retries.append({"tag": tag, "batch": bi, "attempt": attempt, "error": err, "raw_sha256": h})
        print(f"[{tag} batch {bi}] PARSE FAIL (attempt {attempt}): {err}", flush=True)
        if attempt > 2:
            raise SystemExit(f"FATAL: {tag} batch {bi} unparseable after 2 retries: {err}")

def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", required=True, choices=("dump", "teach"))
    ap.add_argument("--lane", type=int, default=0)
    ap.add_argument("--lanes", type=int, default=1)
    ap.add_argument("--only-batch", type=int, default=None)
    a = ap.parse_args()
    if a.only_batch is not None:
        res, _ = process_batch(a.tag, a.only_batch)
        print(f"smoke {a.tag} batch {a.only_batch}: ok ({len(res)} facts)", flush=True)
        return
    t0 = time.time()
    for bi in range(N_BATCHES):
        if bi % a.lanes != a.lane:
            continue
        process_batch(a.tag, bi)
    print(f"lane {a.lane}/{a.lanes} tag {a.tag} done in {time.time()-t0:.0f}s", flush=True)

if __name__ == "__main__":
    main()
