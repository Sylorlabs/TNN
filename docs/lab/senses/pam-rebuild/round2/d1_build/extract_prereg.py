#!/usr/bin/env python3
"""Extract D1 frozen prereg BY SCRIPT from commit bfab522a (never from memory).
Fetches preregs/PREREG_D1_DRAFT.md at the frozen commit via GitHub API,
decodes base64 content, writes to the destination, and prints commit metadata.
"""
import base64, json, subprocess, sys, os

GH = os.path.expanduser("~/workspace/skills/github/bin/gh-api")
REPO = "sylorlabs/TNN"
COMMIT = "bfab522a"
PATH_IN_REPO = "docs/lab/senses/pam-rebuild/round2/preregs/PREREG_D1_DRAFT.md"
DEST = os.path.expanduser("~/workspace/pam_round2/d1_build/frozen_prereg_extracted.md")

def gh(method, path):
    r = subprocess.run([GH, method, path, "--raw"], capture_output=True, text=True)
    if r.returncode != 0:
        print(f"GH API FAILED: {method} {path}\n{r.stderr}", file=sys.stderr)
        sys.exit(1)
    return json.loads(r.stdout)

def main():
    # 1. Verify the frozen commit exists and is what we expect
    commit = gh("GET", f"/repos/{REPO}/commits/{COMMIT}")
    sha = commit["sha"]
    msg = commit["commit"]["message"].split("\n")[0]
    print(f"commit sha: {sha}")
    print(f"commit msg: {msg}")
    assert sha.startswith(COMMIT), f"commit prefix mismatch: {sha}"

    # 2. List files changed by the commit (frozen preregs must be committed ALONE)
    comp = gh("GET", f"/repos/{REPO}/commits/{COMMIT}")
    files = [f["filename"] for f in comp["files"]]
    print(f"commit file count: {len(files)}")
    for f in files:
        print(f"  - {f}")

    # 3. Fetch the frozen prereg content at that commit
    blob = gh("GET", f"/repos/{REPO}/contents/{PATH_IN_REPO}?ref={COMMIT}")
    if blob.get("encoding") != "base64":
        print(f"unexpected encoding: {blob.get('encoding')}", file=sys.stderr)
        sys.exit(1)
    content = base64.b64decode(blob["content"]).decode("utf-8")
    print(f"frozen blob sha: {blob['sha']}")
    print(f"content bytes: {len(content.encode('utf-8'))}")

    # 4. Write local copy (audit trail of extraction)
    os.makedirs(os.path.dirname(DEST), exist_ok=True)
    with open(DEST, "w") as fh:
        fh.write(content)
    print(f"wrote: {DEST}")
    # print header only for inspection
    print("--- first 12 lines ---")
    print("\n".join(content.splitlines()[:12]))

if __name__ == "__main__":
    main()
