#!/usr/bin/env python3
"""Write per-cell MANIFEST.sha256 files and the top-level SHASUMS.

Run from the corpora/ directory. Uses only stdlib.
"""
import hashlib
import os

CORP = os.path.dirname(os.path.abspath(__file__)) + "/.."
CORP = os.path.normpath(CORP)

CELLS = {
    "world": ["store.jsonl", "gaps.jsonl"],
    "cell-a": ["CELL_A.md", "r2p_manifest.sha256"],
    "cell-c1": ["c1_drafts.jsonl", "README.md"],
    "cell-c2": ["c2_tasks.jsonl", "README.md"],
    "cell-c3": ["c3_items.jsonl", "README.md"],
    "cell-w": ["w_claims.jsonl", "README.md"],
    "cell-p": ["p_drafts.jsonl", "README.md", "WARRANT_VOCAB.md"],
    "cell-d": ["d_dialogues.jsonl", "README.md"],
    "cell-s": ["REUSE.md"],
}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    all_lines = []
    for cell, files in sorted(CELLS.items()):
        lines = []
        for fn in files:
            p = os.path.join(CORP, cell, fn)
            digest = sha256(p)
            lines.append("%s  %s" % (digest, fn))
            all_lines.append("%s  corpora/%s/%s" % (digest, cell, fn))
        man = os.path.join(CORP, cell, "MANIFEST.sha256")
        with open(man, "w") as f:
            f.write("\n".join(lines) + "\n")
        print("wrote %s (%d files)" % (man, len(lines)))
    # generators get their own manifest too (archived generators are sealed)
    gen_files = sorted(f for f in os.listdir(os.path.join(CORP, "generators"))
                       if f.endswith(".py"))
    glines = []
    for fn in gen_files:
        p = os.path.join(CORP, "generators", fn)
        d = sha256(p)
        glines.append("%s  %s" % (d, fn))
        all_lines.append("%s  corpora/generators/%s" % (d, fn))
    with open(os.path.join(CORP, "generators", "MANIFEST.sha256"), "w") as f:
        f.write("\n".join(glines) + "\n")
    print("wrote generators/MANIFEST.sha256 (%d files)" % len(glines))
    # top-level README + SHASUMS
    all_lines.append("%s  corpora/README.md" % sha256(os.path.join(CORP, "README.md")))
    with open(os.path.join(CORP, "SHASUMS"), "w") as f:
        f.write("\n".join(sorted(all_lines)) + "\n")
    print("wrote SHASUMS (%d entries)" % len(all_lines))
    print("NOTE: redteam/ keeps its own sealed MANIFEST.sha256 (sibling crew).")


if __name__ == "__main__":
    main()
