#!/usr/bin/env python3
"""Verify local deliberation_depth files against frozen GitHub commits."""
import hashlib, json, os, subprocess, sys

GH = os.path.expanduser("~/workspace/skills/github/bin/gh-api")
LOCAL = os.path.expanduser("~/workspace/tnn-lab/deliberation_depth")

# artifact commit -> repo/local subpath(s) within deliberation_depth
ARTIFACTS = {
    "248392f20ac52f9b4d51841a8da450ae8b4919ea": ["DEPTH_DEF.md"],
    "e45b5f536d9d7c31798d856bbd7ef277057d4f6a": ["harness"],
    "f57760b3267c73df9d14989be6f87feaed42d2b7": ["harness"],
    "50a62d38c8353eff2169e5a676c45b046f81729f": ["batteries"],
    "ba05b096f12ee7dd7404838c95845330d2a7da5a": ["redteam"],
    "c317d36082d6d6f6b9828d71d96c38c95df81087": ["PREREG_H5.md"],
}

def gh(path):
    p = subprocess.run([GH, "GET", path], capture_output=True, text=True)
    if p.returncode != 0:
        print(f"GH ERROR {path}: {p.stderr[:300]}", file=sys.stderr)
        return None
    return json.loads(p.stdout)

def blob_sha(path):
    with open(path, "rb") as f:
        data = f.read()
    h = hashlib.sha1()
    h.update(("blob %d\0" % len(data)).encode() + data)
    return h.hexdigest()

def local_files(sub):
    base = os.path.join(LOCAL, sub)
    out = {}
    if os.path.isfile(base):
        out[sub] = blob_sha(base)
    else:
        for root, dirs, files in os.walk(base):
            dirs[:] = sorted(d for d in dirs if not d.startswith("."))
            for fn in sorted(files):
                if fn.startswith(".") or fn.endswith(".zagd"):
                    continue
                full = os.path.join(root, fn)
                rel = os.path.relpath(full, LOCAL)
                out[rel] = blob_sha(full)
    return out

def tree_blobs(commit, sub):
    c = gh("/repos/sylorlabs/TNN/commits/%s" % commit)
    if not c: return None
    tsha = c["commit"]["tree"]["sha"]
    t = gh("/repos/sylorlabs/TNN/git/trees/%s?recursive=1" % tsha)
    if not t: return None
    prefix = "docs/lab/deliberation_depth/%s" % sub
    out = {}
    for e in t["tree"]:
        if e["type"] == "blob" and (e["path"] == prefix or e["path"].startswith(prefix + "/")):
            rel = e["path"][len("docs/lab/deliberation_depth/"):]
            out[rel] = e["sha"]
    return out

fails = 0
for commit, subs in ARTIFACTS.items():
    for sub in subs:
        remote = tree_blobs(commit, sub)
        local = local_files(sub)
        if remote is None:
            print("[%s] %s: TREE FETCH FAILED" % (commit[:8], sub)); fails += 1; continue
        only_remote = sorted(set(remote) - set(local))
        only_local = sorted(set(local) - set(remote))
        mism = sorted(k for k in set(remote) & set(local) if remote[k] != local[k])
        ok = not only_remote and not only_local and not mism
        print("[%s] %s: %s (remote=%d local=%d mism=%d)" % (commit[:8], sub, "MATCH" if ok else "DIFF", len(remote), len(local), len(mism)))
        for k in mism[:10]: print("   MISMATCH %s: remote=%s local=%s" % (k, remote[k][:8], local[k][:8]))
        for k in only_remote[:10]: print("   ONLY-REMOTE %s" % k)
        for k in only_local[:10]: print("   ONLY-LOCAL %s" % k)
        if not ok: fails += 1
print("FAILURES:", fails)
