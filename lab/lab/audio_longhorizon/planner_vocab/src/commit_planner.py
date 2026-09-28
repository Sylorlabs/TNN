#!/usr/bin/env python3
"""commit_planner.py — commit B-F1 planner/vocabulary evidence to tnn-native-lab.
Explicit repo paths (docs/lab/audio_longhorizon/planner_vocab/...), base_tree =
branch's own tree + delta entries only (never another branch's tree).
Blob bodies via gh-api --data @file (large-file safe).
Usage: commit_planner.py <msg_file> <local_path> [<local_path> ...]
Each local path must be under ~/workspace/audio_longhorizon/planner_vocab/.
"""
import base64, json, os, subprocess, sys, tempfile

GH_API = os.path.expanduser("~/workspace/skills/github/bin/gh-api")
REPO = "sylorlabs/TNN"
BRANCH = "tnn-native-lab"
PV = os.path.expanduser("~/workspace/audio_longhorizon/planner_vocab")
REPO_PREFIX = "docs/lab/audio_longhorizon/planner_vocab/"

def gh(method, path, data_file=None):
    cmd = [GH_API, method, path]
    if data_file:
        cmd += ["--data", "@" + data_file]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError("gh-api %s %s failed: %s" % (method, path, r.stderr[:500]))
    return json.loads(r.stdout)

def main():
    msg_file = sys.argv[1]
    files = sys.argv[2:]
    message = open(msg_file).read()
    ref = gh("GET", "/repos/%s/git/refs/heads/%s" % (REPO, BRANCH))
    head_sha = ref["object"]["sha"]
    head_commit = gh("GET", "/repos/%s/git/commits/%s" % (REPO, head_sha))
    base_tree = head_commit["tree"]["sha"]
    print("base:", head_sha[:12], "tree:", base_tree[:12])
    tmp = tempfile.mkdtemp(prefix="commit_planner_")
    entries = []
    for f in files:
        f = os.path.abspath(os.path.expanduser(f))
        assert f.startswith(PV + "/"), "not under planner_vocab: " + f
        if os.path.isdir(f):
            raise SystemExit("directories not supported, list files: " + f)
        repo_path = REPO_PREFIX + os.path.relpath(f, PV)
        # skip build artifacts / caches / wavs by policy
        rel = os.path.relpath(f, PV)
        if rel.startswith("build/") or ".zag-cache" in rel or rel.endswith(".zagd") \
           or rel.endswith(".wav") or "/runs/" in rel and rel.endswith(".wav"):
            print("SKIP (derived):", rel)
            continue
        body = os.path.join(tmp, "blob.json")
        with open(f, "rb") as fh:
            content = base64.b64encode(fh.read()).decode()
        with open(body, "w") as bf:
            json.dump({"content": content, "encoding": "base64"}, bf)
        blob = gh("POST", "/repos/%s/git/blobs" % REPO, body)
        entries.append({"path": repo_path, "mode": "100644", "type": "blob",
                        "sha": blob["sha"]})
        print("blob", repo_path)
    body = os.path.join(tmp, "tree.json")
    with open(body, "w") as bf:
        json.dump({"base_tree": base_tree, "tree": entries}, bf)
    tree = gh("POST", "/repos/%s/git/trees" % REPO, body)
    body = os.path.join(tmp, "commit.json")
    with open(body, "w") as bf:
        json.dump({"message": message, "tree": tree["sha"], "parents": [head_sha]}, bf)
    commit = gh("POST", "/repos/%s/git/commits" % REPO, body)
    new_sha = commit["sha"]
    body = os.path.join(tmp, "ref.json")
    with open(body, "w") as bf:
        json.dump({"sha": new_sha}, bf)
    gh("PATCH", "/repos/%s/git/refs/heads/%s" % (REPO, BRANCH), body)
    print("COMMITTED", new_sha)
    return new_sha

if __name__ == "__main__":
    main()
