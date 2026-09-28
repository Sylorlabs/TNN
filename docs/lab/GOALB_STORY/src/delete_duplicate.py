#!/usr/bin/env python3
"""Delete the accidental docs/lab/docs/lab/GOALB_STORY/ duplicate from tnn-native-lab."""
import json, subprocess, sys, os

GH_API = os.path.expanduser("~/workspace/skills/github/bin/gh-api")
REPO = "sylorlabs/TNN"
BRANCH = "tnn-native-lab"
DUPS = [
    "docs/lab/docs/lab/GOALB_STORY/FALLBACK_LOG.md",
    "docs/lab/docs/lab/GOALB_STORY/PREREG.md",
    "docs/lab/docs/lab/GOALB_STORY/PREREG_AMENDMENT_A1.md",
]

def gh(method, path, data=None):
    cmd = [GH_API, method, path]
    if data is not None:
        cmd += ["--data", json.dumps(data)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"gh-api {method} {path} failed: {r.stderr[:500]}")
    return json.loads(r.stdout)

ref = gh("GET", f"/repos/{REPO}/git/refs/heads/{BRANCH}")
head_sha = ref["object"]["sha"]
head_commit = gh("GET", f"/repos/{REPO}/git/commits/{head_sha}")
base_tree = head_commit["tree"]["sha"]

tree_entries = [{"path": p, "mode": "100644", "type": "blob", "sha": None} for p in DUPS]
tree = gh("POST", f"/repos/{REPO}/git/trees",
          {"base_tree": base_tree, "tree": tree_entries})
commit = gh("POST", f"/repos/{REPO}/git/commits",
            {"message": "GOAL-B: remove accidental docs/lab/docs/lab/GOALB_STORY/ duplicate paths (canonical files live at docs/lab/GOALB_STORY/)",
             "tree": tree["sha"], "parents": [head_sha]})
gh("PATCH", f"/repos/{REPO}/git/refs/heads/{BRANCH}",
   {"sha": commit["sha"], "force": False})
print("deleted duplicate, commit", commit["sha"])
