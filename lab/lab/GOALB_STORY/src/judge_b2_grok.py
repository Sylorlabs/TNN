#!/usr/bin/env python3
"""B2 grok judge, batched (2x9) to avoid 524s. Appends to evidence/b2_raw_grok-4_6.txt as 'TID: score' lines."""
import sys, re, json, urllib.request, urllib.error, time
sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
from dynamic_credentials import add_surrogate_to_request, read_json_response

GOALB = "/home/hatch/workspace/tnn-lab/GOALB_STORY"
RUBRIC = open(GOALB + "/evidence/b2_prompt.txt").read().split("T01:")[0]

def load_items():
    items, cur, mode = [], None, None
    with open(GOALB + "/runs/rep1.log") as f:
        for line in f:
            line = line.rstrip("\n")
            m = re.match(r"### STORY (\S+) (POS|DEL)$", line)
            if m:
                cur = {"set": m.group(1), "var": m.group(2), "lines": []}
                mode = "story"; items.append(cur); continue
            if re.match(r"### PLAN (\S+) (POS|DEL)$", line):
                mode = "plan"; continue
            if line == "### END":
                mode = None; continue
            if cur is not None and mode == "story" and line.strip():
                cur["lines"].append(line.strip())
    return items

POSCTRL = ("The detective had kept the lighthouse for twenty years. "
           "When the thunderstorm took the roof off the gallery, the key to the lamp room blew into the sea. "
           "The detective climbed the tower with only the accordion for company, playing through the night to stay awake. "
           "At dawn the tide returned the key to the rocks below. "
           "The detective wrote an apology to the town for the dark hours, and lit the lamp again.")

def call(model, prompt):
    payload = json.dumps({"model": model, "messages": [{"role": "user", "content": prompt}], "stream": False}).encode()
    for attempt in (1, 2, 3):
        req = urllib.request.Request("https://api.unorouter.com/v1/chat/completions", data=payload, method="POST")
        req.add_header("Content-Type", "application/json")
        add_surrogate_to_request(req, "custom.unorouter", allowed_hosts=("api.unorouter.com", "unorouter.com"))
        try:
            with urllib.request.urlopen(req, timeout=240) as resp:
                body = read_json_response(resp)
            ch = body.get("choices")
            if ch and ch[0].get("message", {}).get("content"):
                return ch[0]["message"]["content"]
            print(f"  attempt {attempt}: empty choices", flush=True)
        except Exception as e:
            print(f"  attempt {attempt}: {repr(e)[:120]}", flush=True)
        time.sleep(10)
    raise RuntimeError("grok batch failed 3x")

def main():
    trials = load_items()
    items = trials + [{"set": "CTRL", "var": "POS", "lines": [POSCTRL]}]
    batches = [(0, 9), (9, 17)]
    allscores = {}
    for bi, (a, b) in enumerate(batches):
        parts = [RUBRIC, ""]
        for i in range(a, b):
            tid = f"T{i+1:02d}"
            parts.append(f"{tid}:")
            parts.extend(items[i]["lines"])
            parts.append("")
        prompt = "\n".join(parts)
        print(f"batch {bi+1} ({a+1}-{b}), prompt bytes={len(prompt)}", flush=True)
        text = call("grok-4.6", prompt)
        for line in text.splitlines():
            m = re.match(r"\s*(T\d{2})\s*[:=\-]\s*([1-5])\b", line)
            if m:
                allscores[m.group(1)] = int(m.group(2))
        print(f"batch {bi+1} got {len(allscores)} total so far", flush=True)
    missing = [f"T{i+1:02d}" for i in range(17) if f"T{i+1:02d}" not in allscores]
    if missing:
        raise RuntimeError(f"missing scores: {missing}")
    with open(GOALB + "/evidence/b2_raw_grok-4_6.txt", "w") as f:
        for i in range(17):
            f.write(f"T{i+1:02d}: {allscores[f'T{i+1:02d}']}\n")
    print("GROK-BATCHED-OK")

if __name__ == "__main__":
    main()
