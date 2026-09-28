#!/usr/bin/env python3
"""Goal-B B2 second judge: grok-4.7 via ExperientialLabs wrapper path.
Reads the FROZEN prompt (evidence/b2_prompt.txt) — does not regenerate it.
Writes evidence/b2_raw_grok-4_7.txt, parses T01..T17 scores."""
import sys, re, json, urllib.request, urllib.error, time

sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
import dynamic_credentials as dc

GOALB = "/home/hatch/workspace/tnn-lab/GOALB_STORY"
HOST = "api.experientiallabs.ai"
PROMPT = open(GOALB + "/evidence/b2_prompt.txt").read()
assert "T17:" in PROMPT and "T01:" in PROMPT, "frozen prompt missing story blocks"
print(f"prompt bytes={len(PROMPT)}", flush=True)

def call(model, prompt, max_tokens=1500):
    body = json.dumps({"model": model,
                       "messages": [{"role": "user", "content": prompt}],
                       "max_tokens": max_tokens}).encode("utf-8")
    for attempt in (1, 2, 3):
        req = urllib.request.Request(f"https://{HOST}/v1/chat/completions",
                                     data=body, method="POST",
                                     headers={"Content-Type": "application/json"})
        dc.add_surrogate_to_request(req, "custom.experientiallabs", allowed_hosts=[HOST])
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                data = dc.read_json_response(resp)
            ch = data.get("choices")
            if ch and ch[0].get("message", {}).get("content"):
                return ch[0]["message"]["content"]
            print(f"  attempt {attempt}: empty choices", flush=True)
        except urllib.error.HTTPError as e:
            print(f"  attempt {attempt}: HTTP {e.code}: {e.read().decode('utf-8','replace')[:200]}", flush=True)
            if e.code == 429:
                break  # credits out: hard stop, do not burn
        except Exception as e:
            print(f"  attempt {attempt}: {repr(e)[:150]}", flush=True)
        time.sleep(10)
    raise RuntimeError("grok-4.7 judge call failed")

def parse(text):
    scores = {}
    for line in text.splitlines():
        m = re.match(r"\s*(T\d{2})\s*[:=\-]\s*([1-5])\b", line)
        if m:
            scores[m.group(1)] = int(m.group(2))
    return scores

raw = call("grok-4.7", PROMPT)
print(f"raw response bytes={len(raw)}", flush=True)
scores = parse(raw)
missing = [f"T{i+1:02d}" for i in range(17) if f"T{i+1:02d}" not in scores]
print(f"parsed {len(scores)}/17, missing={missing}", flush=True)
if missing:
    print("RAW:\n" + raw[:1500])
    raise RuntimeError(f"missing scores: {missing}")

with open(GOALB + "/evidence/b2_raw_grok-4_7.txt", "w") as f:
    f.write(raw if raw.endswith("\n") else raw + "\n")
print("GROK47-JUDGE-OK")
for i in range(17):
    tid = f"T{i+1:02d}"
    print(f"{tid}: {scores[tid]}")
