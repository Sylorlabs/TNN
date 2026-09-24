#!/usr/bin/env python3
"""Extract H-PAM-35/36 prereg drafts BY SCRIPT from the frozen Round-C commits.

Used by PAM round-2 probe crew P-C (2026-09-24) to satisfy the task requirement
that prereg text be extracted programmatically from the frozen commits, never
transcribed from memory (cf. AGENTS.md lesson on dispatching from frozen docs).

Sources:
  - prereg-alone commit 0db769f2 -> round_c/PREREG_ROUNDC_PROBES.md
    (verified: covers H-PAM-29..34 only; 35/36 probe preregs not there)
  - evidence commit 64daa8b6 -> round_c/preregs/PREREG_HPAM35.md (DRAFT)
                                round_c/preregs/PREREG_HPAM36.md (DRAFT)
                                round_c/grok_objections_roundc.md
                                round_c/HYPOTHESES_ROUND_C.md (parent sections)
Drills the git-tree API by subtree SHA (full recursive tree is truncated).
"""
import base64
import json
import subprocess

GH = "/home/hatch/workspace/skills/github/bin/gh-api"
REPO = "sylorlabs/TNN"

def gh(path):
    r = subprocess.run([GH, "GET", f"/repos/{REPO}{path}"],
                       capture_output=True, text=True, cwd="/home/hatch/workspace")
    r.raise_for_status()
    return json.loads(r.stdout)

def tree(sha):
    return gh(f"/git/trees/{sha}")["tree"]

def descend(root_sha, parts):
    cur = root_sha
    for p in parts:
        hits = [e for e in tree(cur) if e["path"] == p]
        assert hits, f"missing {p} under {cur}"
        e = hits[0]
        print(f"{p} {e['type']} {e['sha']}")
        cur = e["sha"]
    return cur

def get_blob_text(sha):
    d = gh(f"/git/blobs/{sha}")
    return base64.b64decode(d["content"]).decode()

if __name__ == "__main__":
    for commit in ("0db769f2", "64daa8b6"):
        c = gh(f"/commits/{commit}")
        print("commit", commit, "->", c["sha"][:12], "|", c["commit"]["message"].splitlines()[0])
        root = c["commit"]["tree"]["sha"]
        rc = descend(root, ["docs", "lab", "senses", "pam-rebuild", "round2", "round_c"])
        for e in tree(rc):
            print("   ", e["path"], e["type"], e["sha"])
