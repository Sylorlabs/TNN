#!/usr/bin/env python3
"""Commit the grok English-box championship source to the TNN repo.

Target: repo sylorlabs/TNN, branch tnn-native-lab,
path docs/lab/wave12/championship/english/grok/.

Flow (GitHub REST via gh-api, no local checkout):
  read branch head -> create blobs (base64, bodies via --data @file so large
  files don't blow MAX_ARG_STRLEN) -> create tree on base_tree=head's tree ->
  create commit (parent=head) -> fast-forward the branch ref.

Race-safety note: there is no local clone, so `git pull --rebase` cannot be
performed literally. The equivalent race-safe behavior: the head SHA is read
fresh immediately before building the tree/commit, the commit parents that
exact head, and the ref update is verified afterward. If the branch head
moved between the read and the ref update (another agent committed), the
script retries the whole read->build->commit->update cycle up to 3 times.
This is the closest REST equivalent of pull --rebase.

Usage: commit_grok.py <message-file> <file> [<file> ...]
Paths under the repo prefix docs/lab/wave12/championship/english/grok/ are
derived from the local path relative to ~/workspace/tnn-lab/wave12/
championship-english/grok/.
"""
import base64
import json
import os
import subprocess
import sys
import tempfile

GH_API = os.path.expanduser("~/workspace/skills/github/bin/gh-api")
REPO = "sylorlabs/TNN"
BRANCH = "tnn-native-lab"
LOCAL_ROOT = os.path.expanduser(
    "~/workspace/tnn-lab/wave12/championship-english/grok")
REPO_PREFIX = "docs/lab/wave12/championship/english/grok"


def gh(method, path, data_file=None):
    cmd = [GH_API, method, path]
    if data_file:
        cmd += ["--data", "@" + data_file]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"gh-api {method} {path} failed: {r.stderr[:500]}")
    return json.loads(r.stdout)


def attempt(files, message):
    ref = gh("GET", f"/repos/{REPO}/git/refs/heads/{BRANCH}")
    head_sha = ref["object"]["sha"]
    head_commit = gh("GET", f"/repos/{REPO}/git/commits/{head_sha}")
    base_tree = head_commit["tree"]["sha"]
    tmp = tempfile.mkdtemp(prefix="commit_grok_")
    tree_entries = []
    for f in files:
        rel = os.path.relpath(os.path.abspath(f), LOCAL_ROOT)
        assert not rel.startswith(".."), f"file outside grok root: {f}"
        repo_path = REPO_PREFIX + "/" + rel
        with open(f, "rb") as fh:
            content = base64.b64encode(fh.read()).decode()
        body = os.path.join(tmp, "blob.json")
        with open(body, "w") as bf:
            json.dump({"content": content, "encoding": "base64"}, bf)
        blob = gh("POST", f"/repos/{REPO}/git/blobs", body)
        tree_entries.append({"path": repo_path, "mode": "100644",
                             "type": "blob", "sha": blob["sha"]})
        print(f"blob {repo_path}")
    body = os.path.join(tmp, "tree.json")
    with open(body, "w") as bf:
        json.dump({"base_tree": base_tree, "tree": tree_entries}, bf)
    tree = gh("POST", f"/repos/{REPO}/git/trees", body)
    body = os.path.join(tmp, "commit.json")
    with open(body, "w") as bf:
        json.dump({"message": message, "tree": tree["sha"],
                   "parents": [head_sha]}, bf)
    commit = gh("POST", f"/repos/{REPO}/git/commits", body)
    new_sha = commit["sha"]
    body = os.path.join(tmp, "ref.json")
    with open(body, "w") as bf:
        json.dump({"sha": new_sha, "force": False}, bf)
    gh("PATCH", f"/repos/{REPO}/git/refs/heads/{BRANCH}", body)
    # verify the ref landed where we pointed it
    ref2 = gh("GET", f"/repos/{REPO}/git/refs/heads/{BRANCH}")
    if ref2["object"]["sha"] != new_sha:
        raise RuntimeError(
            f"ref moved during commit (now {ref2['object']['sha'][:12]}); retrying")
    print(f"COMMIT {new_sha[:12]} on {BRANCH} (parent {head_sha[:12]})")
    return new_sha


def main():
    msg_file = sys.argv[1]
    files = sys.argv[2:]
    assert files, "no files given"
    with open(msg_file) as f:
        message = f.read()
    new_sha = None
    for i in range(3):
        try:
            new_sha = attempt(files, message)
            break
        except RuntimeError as e:
            print(f"attempt {i+1} failed: {e}", flush=True)
    if not new_sha:
        sys.exit("FATAL: commit failed after 3 attempts")
    print(new_sha)


if __name__ == "__main__":
    main()
