#!/usr/bin/env python3
"""Minimal chat completion against the ExperientialLabs gateway.

Usage: chat.py <model-slug> [prompt]
"""
import sys
import json
import urllib.request
import urllib.error

sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
import dynamic_credentials as dc

HOST = "api.experientiallabs.ai"
BASE = f"https://{HOST}/v1"
CRED = "custom.experientiallabs"


def main() -> None:
    model = sys.argv[1]
    prompt = sys.argv[2] if len(sys.argv) > 2 else "Reply with exactly: ok"
    body = json.dumps(
        {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 4000,
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        BASE + "/chat/completions",
        data=body,
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    dc.add_surrogate_to_request(req, CRED, allowed_hosts=[HOST])
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            data = dc.read_json_response(resp)
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:600]}")
        sys.exit(1)
    print(data["choices"][0]["message"]["content"])


if __name__ == "__main__":
    main()
