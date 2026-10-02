#!/usr/bin/env python3
"""Championship SEPARATE-class corpus generation (source: step-3.7-flash:free).

Governed by prereg/PREREG_Q2_DISTILLATION.md (FROZEN 2026-09-21,
commit ac564a133cc1; prompt sha256 eff5f91f0... verified before run).
- Prompts are extracted PROGRAMMATICALLY from the frozen prereg (single source of truth).
- Model: step-3.7-flash:free, temperature=0, seed=42 (UnoRouter chat/completions).
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
import time
import urllib.request

sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
from dynamic_credentials import add_surrogate_to_request, read_json_response

HERE = os.path.dirname(os.path.abspath(__file__))  # q2-distillation-step37/build
ROOT = os.path.dirname(HERE)                        # q2-distillation-step37
# Frozen prereg — the corpus prompt source of truth (commit ac564a133cc1;
# prompt sha256 eff5f91f0... verified before run).
PREREG = "/home/hatch/workspace/tnn-lab/wave12/q2-distillation/prereg/PREREG_Q2_DISTILLATION.md"
CORPUS_DIR = os.path.join(ROOT, "corpus")
RAW_DIR = os.path.join(CORPUS_DIR, "raw")

BASE = "https://api.unorouter.com/v1"
MODEL = "step-3.7-flash:free"
TEMPERATURE = 0
SEED = 42
BATCH = 12

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
        except Exception as e:
            last = e
            print(f"  transient API error (attempt {attempt}/10): "
                  f"{type(e).__name__}: {e}", flush=True)
            time.sleep(10 * attempt)
    raise RuntimeError(f"api_call failed after 10 attempts: {last}")

# ---- parsing (mechanical) ----
# PROCEDURE NOTE (step37 team, 2026-09-21): step-3.7-flash:free emits each
# block on ONE line ("ID: 0 VALUE: 3 SENTENCE: ...") instead of the prompt's
# one-field-per-line layout, deterministically at temp=0/seed=42 (attempts 1
# and 2 byte-identical in format). The frozen corpus-construction rules
# (C1..C4) constrain content per fact, not intra-block whitespace, so the
# parser accepts both layouts mechanically. Every other check (block count,
# id set, field presence, int parsing, value inventory) is unchanged and
# content-neutral. Per-batch layout is recorded in meta["format_layout"].
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
            # each field keyword must occur exactly once -> unambiguous split
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
            "model": MODEL, "temperature": TEMPERATURE, "seed": SEED,
            "batch": BATCH, "prereg": "prereg/PREREG_Q2_DISTILLATION.md",
            "prompts_sha256": PROMPTS_SHA,
            "input_claim": "t5_plant_claim(id): trainer's intended Zharovia records "
                           "(228 world-true + 12 deliberately false)",
            "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "retries": log_a + log_b,
            "format_layout": dict(FORMAT_STATS),
            "procedure_note": "single-line block layout accepted mechanically "
                              "(see PROCEDURE NOTE at top of build/gen_corpus.py)",
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
    print(f"corpus.json sha256={sha}", flush=True)
    print(f"error inventory: " +
          ", ".join(f"{k}={v['n']}" for k, v in corpus["error_inventory"].items()),
          flush=True)
    print(f"done in {time.time()-t0:.0f}s", flush=True)

if __name__ == "__main__":
    main()
