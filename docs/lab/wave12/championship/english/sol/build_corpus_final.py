#!/usr/bin/env python3
"""SOL ENGLISH BOX RECOVERY: build the final frozen corpus.json.

Completes the source team's capture (39/40 batches) under the parent's
procedural repair ruling (documented 2026-09-21; no bar changes, no frozen
prereg amendment):

- Retry budget exhausted for teach batch 18 (4 attempts, all mechanical
  DISTRACT_VALUE failures). The strict parser stands — no salvage parsing,
  no trainer judgment.
- Batch-18 teach rows are recovered per-id from the SURVIVING raw attempts:
  corpus/raw/teach_batch18.txt (attempt 3) and
  corpus/raw/teach_batch18_recovery.txt (attempt 4). An id parseable in at
  least one surviving raw is kept; per-id provenance is recorded in
  meta.batch18_provenance. An id unparseable in EVERY surviving raw becomes
  a WITHHELD fact: kept in corpus.json as a teach row with
  "withheld": true and "withheld_reason" (exact raw values), numeric lanes
  set to 0 (dead lanes — drivers skip withheld ids via muse_withheld_at).
- Teach batch 19 (ids 228-239) captured fresh by capture_batch19.py
  (frozen prompt, gpt-5.6-sol, temp=0, seed=42, same retry policy).

Result: 240 dump + 240 teach rows. withheld_ids lists corpus-level
withheld ids (empty on this run: batch 18 merged 12/12, batch 19 12/12).
"""
import hashlib
import json
import os
import re
import sys

SOL = os.path.dirname(os.path.abspath(__file__))
CHAMP = os.path.dirname(SOL)
INPUT_DIR = os.path.join(CHAMP, "corpus-input")
RAW_DIR = os.path.join(SOL, "corpus", "raw")

with open(os.path.join(INPUT_DIR, "facts.json")) as f:
    FACTS = json.load(f)
FALSE_IDS = sorted(int(x) for x in FACTS["false_ids"])
assert FALSE_IDS == [3, 29, 55, 71, 80, 103, 117, 139, 163, 178, 205, 231]

FIELDS = {"ID", "OBS_VALUE", "OBSERVATION", "DISTRACT_VALUE",
          "DISTRACTOR", "PROBE", "PROBE_VALUE"}
TEACH_SINGLE = re.compile(
    r"^ID:\s*(\d+)\s+OBS_VALUE:\s*(-?\d+)\s+OBSERVATION:\s*(.+?)"
    r"\s+DISTRACT_VALUE:\s*(-?\d+)\s+DISTRACTOR:\s*(.+?)"
    r"\s+PROBE:\s*(.+?)\s+PROBE_VALUE:\s*(-?\d+)\s*$")
SINGLE_FIELDS = ["ID", "OBS_VALUE", "OBSERVATION", "DISTRACT_VALUE",
                 "DISTRACTOR", "PROBE", "PROBE_VALUE"]
DUMP_SINGLE = re.compile(
    r"^ID:\s*(\d+)\s+VALUE:\s*(-?\d+)\s+SENTENCE:\s*(.+)$")


def parse_rows(text, ids, single_pat, single_fields, numeric, required_text):
    chunks = re.split(r"\n\s*\n", text.strip())
    blocks = []
    for ch in chunks:
        lines = ch.split("\n")
        if len(lines) == 1:
            line = lines[0].strip()
            keys_ok = all(line.count(f + ":") == 1 for f in single_fields)
            m = single_pat.match(line) if keys_ok else None
            if m:
                blocks.append(dict(zip(single_fields,
                                       (g.strip() for g in m.groups()))))
                continue
        d, cur = {}, None
        for line in lines:
            m = re.match(r"^([A-Z_]+):\s*(.*)$", line.strip())
            if m and m.group(1) in FIELDS | {"ID", "VALUE", "SENTENCE"}:
                cur = m.group(1)
                d[cur] = m.group(2).strip()
            elif cur is not None:
                d[cur] = (d[cur] + " " + line.strip()).strip()
        blocks.append(d)
    if len(blocks) != len(ids):
        return None, f"block count {len(blocks)} != {len(ids)}"
    res = {}
    for b in blocks:
        try:
            i = int(b["ID"])
            nums = {k: int(b[k]) for k in numeric}
        except (KeyError, ValueError) as e:
            return None, f"bad numeric field: {e} in {b}"
        for f in required_text:
            if f not in b or not b[f]:
                return None, f"missing {f} for id {i}"
        if i in res:
            return None, f"duplicate id {i}"
        res[i] = {"id": i, **nums,
                  **{k.lower(): b[k] for k in required_text}}
    if set(res) != set(ids):
        return None, f"id set mismatch: got {sorted(res)} want {sorted(ids)}"
    return res, None


def parse_dump(text, ids):
    r, e = parse_rows(text, ids, DUMP_SINGLE, ["ID", "VALUE", "SENTENCE"],
                      ["VALUE"], ["SENTENCE"])
    if r is None:
        return None, e
    return {i: {"value": r[i]["VALUE"], "sentence": r[i]["sentence"]}
            for i in r}, None


def parse_teach(text, ids):
    r, e = parse_rows(text, ids, TEACH_SINGLE, SINGLE_FIELDS,
                      ["OBS_VALUE", "DISTRACT_VALUE", "PROBE_VALUE"],
                      ["OBSERVATION", "DISTRACTOR", "PROBE"])
    if r is None:
        return None, e
    return {i: {"obs_value": r[i]["OBS_VALUE"],
                "observation": r[i]["observation"],
                "distract_value": r[i]["DISTRACT_VALUE"],
                "distractor": r[i]["distractor"],
                "probe": r[i]["probe"],
                "probe_value": r[i]["PROBE_VALUE"]} for i in r}, None


def load(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


# ---- dump: 20/20 clean (source team) ----
dump = {}
for bi in range(20):
    ids = list(range(bi * 12, (bi + 1) * 12))
    res, err = parse_dump(load(os.path.join(RAW_DIR, f"dump_batch{bi:02d}.txt")),
                          ids)
    assert err is None, f"dump batch {bi}: {err}"
    dump.update(res)
assert len(dump) == 240

# ---- teach batches 0-17: clean (source team) ----
teach = {}
for bi in range(18):
    ids = list(range(bi * 12, (bi + 1) * 12))
    res, err = parse_teach(
        load(os.path.join(RAW_DIR, f"teach_batch{bi:02d}.txt")), ids)
    assert err is None, f"teach batch {bi}: {err}"
    teach.update(res)

# ---- teach batch 18: per-id union of the two surviving raws ----
# Lenient per-block parse: an id is recovered if ANY surviving raw has a
# parseable block for it. Blocks that fail keep failing only for their id.
B18_IDS = list(range(216, 228))
B18_RAWS = [("corpus/raw/teach_batch18.txt",            # attempt 3
             load(os.path.join(RAW_DIR, "teach_batch18.txt"))),
            ("corpus/raw/teach_batch18_recovery.txt",   # attempt 4
             load(os.path.join(RAW_DIR, "teach_batch18_recovery.txt")))]


def parse_block_lenient(block):
    """Parse one text block; return (id, row) or (None, raw)."""
    lines = block.split("\n")
    if len(lines) == 1:
        line = lines[0].strip()
        keys_ok = all(line.count(f + ":") == 1 for f in SINGLE_FIELDS)
        m = TEACH_SINGLE.match(line) if keys_ok else None
        if m:
            d = dict(zip(SINGLE_FIELDS, (g.strip() for g in m.groups())))
        else:
            return None, block.strip()
    else:
        d, cur = {}, None
        for line in lines:
            m = re.match(r"^([A-Z_]+):\s*(.*)$", line.strip())
            if m and m.group(1) in FIELDS:
                cur = m.group(1)
                d[cur] = m.group(2).strip()
            elif cur is not None:
                d[cur] = (d[cur] + " " + line.strip()).strip()
    try:
        i = int(d["ID"])
        row = {"obs_value": int(d["OBS_VALUE"]),
               "observation": d["OBSERVATION"],
               "distract_value": int(d["DISTRACT_VALUE"]),
               "distractor": d["DISTRACTOR"],
               "probe": d["PROBE"],
               "probe_value": int(d["PROBE_VALUE"])}
    except (KeyError, ValueError):
        return None, block.strip()
    for f in ("OBSERVATION", "DISTRACTOR", "PROBE"):
        if not d.get(f):
            return None, block.strip()
    return i, row


b18_rows = {}
b18_prov = {}
b18_bad = {}  # id -> list of exact raw blocks that failed
withheld = {}  # id -> reason
for path, raw in B18_RAWS:
    sha = hashlib.sha256(raw.encode()).hexdigest()
    for block in re.split(r"\n\s*\n", raw.strip()):
        if not block.strip():
            continue
        i, row = parse_block_lenient(block)
        if row is not None:
            if i in B18_IDS and i not in b18_rows:
                b18_rows[i] = row
                b18_prov[str(i)] = {"source": path, "source_sha256": sha}
        else:
            m = re.match(r"^ID:\s*(\d+)", block.strip())
            if m and int(m.group(1)) in B18_IDS:
                b18_bad.setdefault(int(m.group(1)), []).append(
                    f"{path}: {block.strip().replace(chr(10), ' ')}")
for i in B18_IDS:
    if i not in b18_rows:
        raws = " | ".join(b18_bad.get(i, ["<block not found>"]))
        withheld[i] = ("unparseable DISTRACT_VALUE after 4 attempts: " + raws)
teach.update(b18_rows)
print(f"batch 18: {len(b18_rows)}/12 parsed, "
      f"{len([i for i in B18_IDS if i in withheld])}/12 withheld",
      flush=True)

# ---- teach batch 19: fresh capture ----
B19_IDS = list(range(228, 240))
b19_raw = load(os.path.join(RAW_DIR, "teach_batch19.txt"))
res, err = parse_teach(b19_raw, B19_IDS)
if err is None:
    teach.update(res)
    print("batch 19: 12/12 parsed, 0/12 withheld", flush=True)
else:
    # withhold ruling: keep the row, mark withheld, exact raw values
    for i in B19_IDS:
        m = re.search(rf"^ID:\s*{i}\b(.*?)(?=^ID:\s*\d|\Z)",
                      b19_raw, re.M | re.S)
        raw = m.group(0).strip().replace("\n", " ") if m else "<not found>"
        withheld[i] = (f"unparseable DISTRACT_VALUE after 2 retries: {raw}")
    print(f"batch 19 WITHHELD: {err}", flush=True)

assert len(teach) + len(withheld) == 240

# retries record (source team log + batch 18 failures + batch 19)
retries = []
for line in open(os.path.join(SOL, "corpus_gen.log"),
                 encoding="utf-8", errors="replace"):
    if "PARSE FAIL" in line:
        retries.append(line.strip())
retries.append(
    "teach batch 18 attempt 4 (recovery): PARSE FAIL: bad numeric field: "
    "invalid literal for int() with base 10: 'kl' (id 226)")
b19r = os.path.join(SOL, "batch19_retries.json")
if os.path.exists(b19r):
    retries.extend("batch19: " + json.dumps(r)
                   for r in json.load(open(b19r)))

corpus = {
    "meta": {
        "model": "gpt-5.6-sol", "temperature": 0, "seed": 42, "batch": 12,
        "corpus_input": "championship-english/corpus-input (frozen 2026-09-21)",
        "prompts_sha256": "ac5d7d3155f9a90dc60f4f3ec529a3c6125a0469ce5862c7193fb261441b8b7d",
        "input_claim": "facts.json SUPPLIED values: trainer's intended English "
                       "records (228 world-true + 12 deliberately false)",
        "generated_utc": __import__("time").strftime("%Y-%m-%dT%H:%M:%SZ",
                                                     __import__("time").gmtime()),
        "retries": retries,
        "format_layout": "single/multi-line block layout (same parser as "
                         "q2-distillation-step37)",
        "english_box": "square (classes 1-4); categories alpha-pos/word-len/"
                       "pub-year/count-fact with boundaries 48/96/144",
        "withhold_ruling": (
            "parent ruling 2026-09-21 (procedural repair, no bar changes): "
            "batch-18 retry budget exhausted after 4 mechanical failures; no "
            "5th attempt, no salvage parsing. Unparseable rows become WITHHELD "
            "facts: kept as teach rows with withheld=true, numeric lanes 0 "
            "(dead lanes — teaching drivers skip withheld ids via "
            "muse_withheld_at, the existing withheld counter path), exact raw "
            "values in withheld_reason. Batch-19 same policy if needed."),
        "batch18_provenance": b18_prov,
        "batch19_capture": "capture_batch19.py, frozen prompt, attempt 1 ok, "
                           "sha256=6a6825e8b0b71ea4",
    },
    "input_claims": {str(i): int(FACTS[str(i)]["value"]) for i in range(240)},
    "false_ids": FALSE_IDS,
    "withheld_ids": sorted(withheld),
    "dump": [{"id": i, "value": dump[i]["value"],
              "sentence": dump[i]["sentence"]} for i in range(240)],
    "teach": [],
}
for i in range(240):
    if i in withheld:
        corpus["teach"].append(
            {"id": i, "obs_value": 0, "observation": "",
             "distract_value": 0, "distractor": "", "probe": "",
             "probe_value": 0, "withheld": True,
             "withheld_reason": withheld[i]})
    else:
        corpus["teach"].append({"id": i, **teach[i]})

# LLM-error inventory (mechanical, vs facts.json SUPPLIED values;
# withheld rows excluded — they carry no values)
inv = {"E_dump": [], "E_obs": [], "E_prb": [], "E_format": [],
       "inconsistent": [], "sentence_missing_value": []}
for i in range(240):
    want = int(FACTS[str(i)]["value"])
    if dump[i]["value"] != want:
        inv["E_dump"].append(i)
    t = next(e for e in corpus["teach"] if e["id"] == i)
    if t.get("withheld"):
        inv["E_format"].append(i)
        continue
    if t["obs_value"] != want:
        inv["E_obs"].append(i)
    if t["probe_value"] != want:
        inv["E_prb"].append(i)
    if t["obs_value"] != t["probe_value"]:
        inv["inconsistent"].append(i)
    if str(dump[i]["value"]) not in dump[i]["sentence"]:
        inv["sentence_missing_value"].append(i)
corpus["error_inventory"] = {k: {"n": len(v), "ids": v} for k, v in inv.items()}

out = os.path.join(SOL, "corpus", "corpus.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(corpus, f, indent=1, ensure_ascii=False)
    f.write("\n")
with open(out, "rb") as f:
    sha = hashlib.sha256(f.read()).hexdigest()
with open(os.path.join(SOL, "corpus", "SHA256.txt"), "w") as f:
    f.write(sha + "\n")
wsh = os.path.join(SOL, "corpus", "withheld_ids.json")
with open(wsh, "w") as f:
    json.dump({"withheld_ids": sorted(withheld),
               "reasons": {str(i): withheld[i] for i in sorted(withheld)}},
              f, indent=1)
    f.write("\n")
print(f"corpus.json sha256={sha}", flush=True)
print("teach rows: %d, withheld: %s" % (len(corpus["teach"]),
                                        sorted(withheld) or "none"), flush=True)
print("error inventory: " + ", ".join(f"{k}={v['n']}"
      for k, v in corpus["error_inventory"].items()), flush=True)
