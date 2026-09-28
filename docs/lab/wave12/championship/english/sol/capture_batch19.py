#!/usr/bin/env python3
"""SOL ENGLISH BOX RECOVERY: capture teach batch 19 (ids 228-239).

Same frozen prompt / model gpt-5.6-sol / temp=0 / seed=42 as the main run.
Retry policy (identical to gen_corpus_sol.py): mechanical parse failure only,
max 2 retries (3 attempts total). Each attempt's raw is preserved separately:
  corpus/raw/teach_batch19_attempt1.txt .. _attempt3.txt
On success the passing raw is copied to corpus/raw/teach_batch19.txt.
On 3 mechanical failures, exits 40 and leaves all attempt raws for the
withhold ruling (no 4th attempt, no salvage parse).

Long-polled by design: run in background.
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

SOL = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(os.path.dirname(SOL), "corpus-input")
RAW_DIR = os.path.join(SOL, "corpus", "raw")

BASE = "https://api.unorouter.com/v1"
MODEL = "gpt-5.6-sol"
TEMPERATURE = 0
SEED = 42
IDS = list(range(228, 240))

EXPECTED_PROMPTS_SHA = "ac5d7d3155f9a90dc60f4f3ec529a3c6125a0469ce5862c7193fb261441b8b7d"


def api_call(prompt):
    payload = {"model": MODEL,
               "messages": [{"role": "user", "content": prompt}],
               "temperature": TEMPERATURE, "seed": SEED, "stream": False}
    rate_attempts = 0
    transient_attempts = 0
    while True:
        try:
            req = urllib.request.Request(
                BASE + "/chat/completions", data=json.dumps(payload).encode(),
                method="POST")
            req.add_header("Content-Type", "application/json")
            add_surrogate_to_request(req, "custom.unorouter",
                                     allowed_hosts=("api.unorouter.com",
                                                    "unorouter.com"))
            with urllib.request.urlopen(req, timeout=300) as resp:
                body = read_json_response(resp)
            return body["choices"][0]["message"]["content"]
        except urllib.error.HTTPError as e:
            if e.code in (429, 503):
                rate_attempts += 1
                if rate_attempts > 21:
                    raise RuntimeError("rate-limited 21x in a row, aborting")
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


FIELDS = {"ID", "OBS_VALUE", "OBSERVATION", "DISTRACT_VALUE",
          "DISTRACTOR", "PROBE", "PROBE_VALUE"}
TEACH_SINGLE = re.compile(
    r"^ID:\s*(\d+)\s+OBS_VALUE:\s*(-?\d+)\s+OBSERVATION:\s*(.+?)"
    r"\s+DISTRACT_VALUE:\s*(-?\d+)\s+DISTRACTOR:\s*(.+?)"
    r"\s+PROBE:\s*(.+?)\s+PROBE_VALUE:\s*(-?\d+)\s*$")
SINGLE_FIELDS = ["ID", "OBS_VALUE", "OBSERVATION", "DISTRACT_VALUE",
                 "DISTRACTOR", "PROBE", "PROBE_VALUE"]


def parse_teach(text, ids):
    chunks = re.split(r"\n\s*\n", text.strip())
    blocks = []
    for ch in chunks:
        lines = ch.split("\n")
        if len(lines) == 1:
            line = lines[0].strip()
            keys_ok = all(line.count(f + ":") == 1 for f in SINGLE_FIELDS)
            m = TEACH_SINGLE.match(line) if keys_ok else None
            if m:
                blocks.append(dict(zip(SINGLE_FIELDS,
                                       (g.strip() for g in m.groups()))))
                continue
        d, cur = {}, None
        for line in lines:
            m = re.match(r"^([A-Z_]+):\s*(.*)$", line.strip())
            if m and m.group(1) in FIELDS:
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
            ov, dv, pv = (int(b["OBS_VALUE"]), int(b["DISTRACT_VALUE"]),
                          int(b["PROBE_VALUE"]))
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


def main():
    # frozen-prompt check (byte-exact vs main-run verifier)
    with open(os.path.join(INPUT_DIR, "batch19_teach.txt"),
              encoding="utf-8") as f:
        prompt = f.read()
    print("prompt sha256=" +
          hashlib.sha256(prompt.encode()).hexdigest()[:16], flush=True)
    retries = []
    for attempt in (1, 2, 3):
        raw = api_call(prompt)
        ap = os.path.join(RAW_DIR, f"teach_batch19_attempt{attempt}.txt")
        with open(ap, "w", encoding="utf-8") as f:
            f.write(raw)
        h = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        res, err = parse_teach(raw, IDS)
        if err is None:
            final = os.path.join(RAW_DIR, "teach_batch19.txt")
            with open(final, "w", encoding="utf-8") as f:
                f.write(raw)
            print(f"[teach batch 19] ok on attempt {attempt} "
                  f"sha256={h[:16]}", flush=True)
            with open(os.path.join(SOL, "batch19_retries.json"), "w") as f:
                json.dump(retries, f, indent=1)
            return 0
        retries.append({"attempt": attempt, "error": err, "raw_sha256": h})
        print(f"[teach batch 19] PARSE FAIL (attempt {attempt}): {err}",
              flush=True)
        if attempt < 3:
            time.sleep(5)
    with open(os.path.join(SOL, "batch19_retries.json"), "w") as f:
        json.dump(retries, f, indent=1)
    print("WITHHOLD-RULING: teach batch 19 unparseable after 2 retries; "
          "attempt raws preserved, no 4th attempt.", flush=True)
    return 40


if __name__ == "__main__":
    sys.exit(main())
