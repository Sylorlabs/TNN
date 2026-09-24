#!/usr/bin/env python3
"""CELL-A corpus pinning: fetch the R2-3 crew's sealed R2P manifest from the
branch and verify it. This is a PIN (reference), not a generation: the
1,200 pair files themselves live at
docs/lab/senses/pam-rebuild/round2/fixtures/r2p/ on branch tnn-native-lab.

Requires: ~/workspace/skills/github/bin/gh-api with the stored credential.
Output: cell-a/r2p_manifest.sha256 (byte-identical copy of the sealed
upstream MANIFEST.r2p.sha256).

Upstream manifest git blob: 33b5fc5d9787011bbf1161c64350ce3ee5e9cddb
Expected: 1200 entries, sha256
cdda12c19557c7e773f144e6a2d0c014b58ec3f853df13fd23ad4742f39217b6
"""
import base64
import hashlib
import json
import os
import subprocess
import sys

GH_API = os.path.expanduser("~/workspace/skills/github/bin/gh-api")
REPO = "sylorlabs/TNN"
BRANCH = "tnn-native-lab"
BLOB = "33b5fc5d9787011bbf1161c64350ce3ee5e9cddb"
EXPECT_SHA = "cdda12c19557c7e773f144e6a2d0c014b58ec3f853df13fd23ad4742f39217b6"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "cell-a", "r2p_manifest.sha256")


def main():
    r = subprocess.run(
        [GH_API, "GET", "/repos/%s/git/blobs/%s" % (REPO, BLOB), "--raw"],
        capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("gh-api failed: %s" % r.stderr[:200])
    body = base64.b64decode(json.loads(r.stdout)["content"])
    digest = hashlib.sha256(body).hexdigest()
    assert digest == EXPECT_SHA, "manifest sha mismatch: %s" % digest
    lines = [l for l in body.decode().split("\n") if l.strip()]
    assert len(lines) == 1200, "expected 1200 pair entries, got %d" % len(lines)
    with open(OUT, "wb") as f:
        f.write(body)
    print("pinned %d pair entries -> %s" % (len(lines), OUT))


if __name__ == "__main__":
    main()
