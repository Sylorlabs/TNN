#!/usr/bin/env python3
"""B2 blind arc judging: frozen prompt, deterministic item order, two judges."""
import re, sys, subprocess, json

LAB = "/home/hatch/workspace/tnn-lab"
GOALB = LAB + "/GOALB_STORY"
CLI = "/home/hatch/workspace/skills/unorouter/bin/unorouter.py"

RUBRIC = """You are rating short stories for narrative arc. For each numbered story, give ONE integer ARC score 1-5:

5 = unmistakable setup, rising complication, distinct climax, and satisfying resolution, all connected
4 = all four arc elements present, minor weakness in one
3 = three of the four elements present; readable arc with a gap
2 = one or two elements; fragmentary, little sense of progression
1 = no discernible arc; disconnected sentences

Rules: judge the ARC only, not word choice, grammar, or style. Return EXACTLY one line per story in this format:
T01: 4
No explanations, no extra text, no markdown."""

POSCTRL = ("The detective had kept the lighthouse for twenty years. "
           "When the thunderstorm took the roof off the gallery, the key to the lamp room blew into the sea. "
           "The detective climbed the tower with only the accordion for company, playing through the night to stay awake. "
           "At dawn the tide returned the key to the rocks below. "
           "The detective wrote an apology to the town for the dark hours, and lit the lamp again.")

def load_items():
    items = []
    cur = None
    mode = None
    with open(GOALB + "/runs/rep1.log") as f:
        for line in f:
            line = line.rstrip("\n")
            m = re.match(r"### STORY (\S+) (POS|DEL)$", line)
            if m:
                cur = {"set": m.group(1), "var": m.group(2), "lines": []}
                mode = "story"
                items.append(cur)
                continue
            m = re.match(r"### PLAN (\S+) (POS|DEL)$", line)
            if m:
                mode = "plan"
                continue
            if line == "### END":
                mode = None
                continue
            if cur is not None and mode == "story" and line.strip():
                cur["lines"].append(line.strip())
    return items

def build_prompt(items):
    parts = [RUBRIC, ""]
    for i, it in enumerate(items):
        tid = f"T{i+1:02d}"
        parts.append(f"{tid}:")
        parts.extend(it["lines"])
        parts.append("")
    return "\n".join(parts)

def call_judge(model, prompt):
    sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
    from dynamic_credentials import add_surrogate_to_request, read_json_response
    import urllib.request, urllib.error, json, time
    payload = json.dumps({"model": model,
                          "messages": [{"role": "user", "content": prompt}],
                          "stream": False}).encode()
    last_err = None
    for attempt in (1, 2):
        req = urllib.request.Request("https://api.unorouter.com/v1/chat/completions",
                                     data=payload, method="POST")
        req.add_header("Content-Type", "application/json")
        add_surrogate_to_request(req, "custom.unorouter",
                                 allowed_hosts=("api.unorouter.com", "unorouter.com"))
        try:
            with urllib.request.urlopen(req, timeout=300) as resp:
                body = read_json_response(resp)
            ch = body.get("choices")
            if ch and ch[0].get("message", {}).get("content"):
                if attempt == 2:
                    print(f"NOTE: {model} needed a retry (first response had empty choices)")
                return ch[0]["message"]["content"]
            last_err = "empty choices in response"
        except urllib.error.HTTPError as e:
            last_err = f"HTTP {e.code}: {e.read()[:200]}"
        except Exception as e:
            last_err = repr(e)[:200]
        time.sleep(5)
    raise RuntimeError(f"judge {model} failed twice: {last_err}")

def parse_scores(text, n):
    scores = {}
    for line in text.splitlines():
        m = re.match(r"\s*(T\d{2})\s*[:=\-]\s*([1-5])\b", line)
        if m:
            scores[m.group(1)] = int(m.group(2))
    missing = [f"T{i+1:02d}" for i in range(n) if f"T{i+1:02d}" not in scores]
    return scores, missing

def main():
    trials = load_items()
    assert len(trials) == 16, f"expected 16, got {len(trials)}"
    # deterministic order: as emitted (S1 POS, S1 DEL, ... S8 DEL), control last
    items = trials + [{"set": "CTRL", "var": "POS", "lines": [POSCTRL]}]
    n = len(items)
    prompt = build_prompt(items)
    with open(GOALB + "/evidence/b2_prompt.txt", "w") as f:
        f.write(prompt)
    with open(GOALB + "/evidence/b2_item_key.txt", "w") as f:
        for i, it in enumerate(items):
            f.write(f"T{i+1:02d}: {it['set']} {it['var']}\n")
    judges = ["gpt-5.6-sol", "grok-4.6"]
    allscores = {}
    for j in judges:
        raw = call_judge(j, prompt)
        safe = j.replace(".", "_")
        with open(GOALB + f"/evidence/b2_raw_{safe}.txt", "w") as f:
            f.write(raw)
        scores, missing = parse_scores(raw, n)
        print(f"{j}: parsed {len(scores)}/{n}, missing={missing}")
        allscores[j] = scores
    # report
    header = ["TID", "SET", "VAR"] + judges + ["MEAN"]
    print("\t".join(header))
    per_variant = {"POS": [], "DEL": []}
    ctrl = []
    for i, it in enumerate(items):
        tid = f"T{i+1:02d}"
        row = [tid, it["set"], it["var"]]
        vals = []
        for j in judges:
            v = allscores[j].get(tid)
            row.append(str(v) if v else "?")
            if v:
                vals.append(v)
        mean = sum(vals)/len(vals) if vals else None
        row.append(f"{mean:.2f}" if mean else "?")
        print("\t".join(row))
        if it["set"] == "CTRL":
            if mean: ctrl.append(mean)
        elif mean:
            per_variant[it["var"]].append(mean)
    for var, ms in per_variant.items():
        ok = sum(1 for m in ms if m >= 3.5)
        print(f"B2-{var}: {ok}/8 >=3.5 (bar: >=6/8)")
    if ctrl:
        print(f"B2-CTRL mean={ctrl[0]:.2f} (bar: >=4.0 both judges)")

if __name__ == "__main__":
    main()
