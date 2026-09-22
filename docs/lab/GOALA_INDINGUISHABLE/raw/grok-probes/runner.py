#!/usr/bin/env python3
"""Robust unorouter chat runner. Usage: runner.py <promptfile> <outfile>"""
import json, sys, time, urllib.request

sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
from dynamic_credentials import add_surrogate_to_request, read_json_response

BASE = "https://api.unorouter.com/v1"
prompt = open(sys.argv[1]).read()
payload = json.dumps({"model": "gpt-5.6-sol",
                      "messages": [{"role": "user", "content": prompt}],
                      "stream": False}).encode()

for attempt in range(5):
    try:
        req = urllib.request.Request(BASE + "/chat/completions", data=payload,
                                     method="POST",
                                     headers={"Content-Type": "application/json"})
        add_surrogate_to_request(req, "custom.unorouter",
                                 allowed_hosts=("api.unorouter.com", "unorouter.com"))
        with urllib.request.urlopen(req, timeout=180) as r:
            body = read_json_response(r)
        ch = (body.get("choices") or [None])[0]
        content = ch and ch.get("message", {}).get("content")
        if content:
            open(sys.argv[2], "w").write(content)
            print(f"OK attempt={attempt} chars={len(content)}")
            sys.exit(0)
        print(f"attempt {attempt}: empty content, body keys={list(body.keys())}", flush=True)
    except Exception as e:
        print(f"attempt {attempt} failed: {e}", flush=True)
    time.sleep(20)
sys.exit(1)
