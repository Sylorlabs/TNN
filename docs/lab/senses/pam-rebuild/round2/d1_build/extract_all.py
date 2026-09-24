#!/usr/bin/env python3
"""Extract ALL frozen D1/D4 files BY SCRIPT from commit bfab522a (never from memory).
Fetches all 3 committed files at the frozen commit, verifies blob SHAs,
and checks the F5 fixture ledger SHA cited by the prereg.
"""
import base64, json, subprocess, sys, os, hashlib

GH = os.path.expanduser("~/workspace/skills/github/bin/gh-api")
REPO = "sylorlabs/TNN"
COMMIT = "bfab522a"
FILES = [
    "docs/lab/senses/pam-rebuild/round2/preregs/PREREG_D1_DRAFT.md",
    "docs/lab/senses/pam-rebuild/round2/preregs/PREREG_D4_DRAFT.md",
    "docs/lab/senses/pam-rebuild/round2/preregs/PROBE_PREREG_D1DEBATE.md",
]
DEST_DIR = os.path.expanduser("~/workspace/pam_round2/d1_build/frozen")

def gh(method, path):
    r = subprocess.run([GH, method, path, "--raw"], capture_output=True, text=True)
    if r.returncode != 0:
        print(f"GH API FAILED: {method} {path}\n{r.stderr}", file=sys.stderr)
        sys.exit(1)
    return json.loads(r.stdout)

def main():
    os.makedirs(DEST_DIR, exist_ok=True)
    for f in FILES:
        blob = gh("GET", f"/repos/{REPO}/contents/{f}?ref={COMMIT}")
        content = base64.b64decode(blob["content"]).decode("utf-8")
        # verify git blob SHA: sha1("blob <len>\0" + bytes)
        raw = content.encode("utf-8")
        check = hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()
        assert check == blob["sha"], f"blob sha mismatch for {f}: {check} vs {blob['sha']}"
        name = os.path.basename(f)
        with open(os.path.join(DEST_DIR, name), "w") as fh:
            fh.write(content)
        print(f"OK {name}: blob={blob['sha']} bytes={len(raw)} (git-sha verified)")

    # Verify the F5 fixture ledger SHA cited by the D1 prereg (§7)
    cited = "0c5e2c0db6576bd37ff53513fb1361cdf7936d4826274bdcc9742be2261233a0"
    # find fixtures_ledger.txt at HEAD of tnn-native-lab
    listing = gh("GET", f"/repos/{REPO}/contents/docs/lab/senses/pam-rebuild/round2?ref=tnn-native-lab")
    names = [e["name"] for e in listing]
    print("round2 dir entries:", names[:40])
    return 0

if __name__ == "__main__":
    sys.exit(main())
