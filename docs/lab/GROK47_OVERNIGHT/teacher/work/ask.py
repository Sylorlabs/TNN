#!/usr/bin/env python3
"""ask.py — grok-4.7 hypothesis/attack engine client (experientiallabs gateway).

Usage: ask.py "<prompt>" [--max-tokens N] [--temp T]
chat.py hardcodes max_tokens=16 (one line); hypotheses need full responses.
Same gateway, same model, same credential; temperature default 0.
"""
import json
import sys
import urllib.request
import urllib.error

sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
import dynamic_credentials as dc

HOST = "api.experientiallabs.ai"
BASE = f"https://{HOST}/v1"
CRED = "custom.experientiallabs"
MODEL = "grok-4.7"

def ask(prompt, max_tokens=4096, temperature=0):
    payload = {"model": MODEL,
               "messages": [{"role": "user", "content": prompt}],
               "temperature": temperature, "max_tokens": max_tokens, "stream": False}
    for attempt in range(1, 6):
        try:
            req = urllib.request.Request(BASE + "/chat/completions",
                                         data=json.dumps(payload).encode(), method="POST")
            req.add_header("Content-Type", "application/json")
            dc.add_surrogate_to_request(req, CRED, allowed_hosts=(HOST,))
            with urllib.request.urlopen(req, timeout=300) as resp:
                data = dc.read_json_response(resp)
            return data["choices"][0]["message"]["content"]
        except urllib.error.HTTPError as e:
            print(f"HTTP {e.code}: {e.read().decode('utf-8','replace')[:300]}", file=sys.stderr)
            if e.code in (429, 503):
                import time; time.sleep(60); continue
            sys.exit(1)
        except Exception as e:
            print(f"transient {type(e).__name__}: {e} (attempt {attempt}/5)", file=sys.stderr)
            import time; time.sleep(10 * attempt)
    sys.exit("ask failed after 5 attempts")

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("prompt")
    ap.add_argument("--max-tokens", type=int, default=4096)
    ap.add_argument("--temp", type=float, default=0)
    a = ap.parse_args()
    print(ask(a.prompt, a.max_tokens, a.temp))
