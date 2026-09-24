#!/usr/bin/env python3
"""Verify the F5 fixture ledger SHA cited in the frozen prereg §7.
Downloads fixtures_ledger.txt from tnn-native-lab HEAD and compares SHA-256
to the prereg-cited 0c5e2c0db6576bd37ff53513fb1361cdf7936d4826274bdcc9742be2261233a0.
Also lists the round2/fixtures dir and the d1_debate probes dir (prior probe code
may be inspected for interface compatibility, but specs come only from frozen docs).
"""
import base64, json, subprocess, sys, os, hashlib

GH = os.path.expanduser("~/workspace/skills/github/bin/gh-api")
REPO = "sylorlabs/TNN"
CITED = "0c5e2c0db6576bd37ff53513fb1361cdf7936d4826274bdcc9742be2261233a0"

def gh(method, path):
    r = subprocess.run([GH, method, path, "--raw"], capture_output=True, text=True)
    if r.returncode != 0:
        print(f"GH API FAILED: {method} {path}\n{r.stderr}", file=sys.stderr)
        sys.exit(1)
    return json.loads(r.stdout)

def main():
    # 1. fixture dir listing at branch head
    listing = gh("GET", f"/repos/{REPO}/contents/docs/lab/senses/pam-rebuild/round2/fixtures?ref=tnn-native-lab")
    print("fixtures dir:")
    for e in listing:
        print(f"  {e['type']:5s} {e['name']}")
    # 2. fetch fixtures_ledger.txt and check sha256
    names = [e["name"] for e in listing]
    if "fixtures_ledger.txt" in names:
        blob = gh("GET", f"/repos/{REPO}/contents/docs/lab/senses/pam-rebuild/round2/fixtures/fixtures_ledger.txt?ref=tnn-native-lab")
        raw = base64.b64decode(blob["content"])
        sha = hashlib.sha256(raw).hexdigest()
        print(f"\nfixtures_ledger.txt sha256: {sha}")
        print(f"prereg-cited sha256:        {CITED}")
        print("MATCH" if sha == CITED else "MISMATCH — do not use as honest battery basis")
        with open(os.path.expanduser("~/workspace/pam_round2/d1_build/fixtures_ledger.txt"), "wb") as fh:
            fh.write(raw)
        print(f"saved local copy ({len(raw)} bytes)")

if __name__ == "__main__":
    sys.exit(main())
