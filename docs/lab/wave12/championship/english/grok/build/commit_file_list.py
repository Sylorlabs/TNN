#!/usr/bin/env python3
"""Build the file list for the grok English-box GitHub commit.

Walks ~/workspace/tnn-lab/wave12/championship-english/grok/ and emits the
absolute paths of files to commit, excluding:
  - compiled binaries (no extension ELF / named *_bin / grokt* etc.)
  - .zagd files, .zag-cache/ dirs
  - __pycache__/, *.pyc
  - build/gen_corpus_full.log (transient; the frozen corpus + manifest suffice)
  - the commit scripts themselves? (kept: they're part of the method)
Prints one path per line.
"""
import os
import sys

ROOT = os.path.expanduser(
    "~/workspace/tnn-lab/wave12/championship-english/grok")

EXCLUDE_DIRS = {".zag-cache", "__pycache__", ".git"}
EXCLUDE_EXT = {".zagd", ".pyc", ".o", ".a"}
EXCLUDE_NAMES = {"gen_corpus_full.log"}
# known binary outputs (no extension, ELF)
BINARIES = {"grokt", "groktA", "groktB", "groktC", "debate_bin"}


def main():
    out = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for fn in filenames:
            if fn in EXCLUDE_NAMES:
                continue
            if os.path.splitext(fn)[1] in EXCLUDE_EXT:
                continue
            if fn in BINARIES:
                continue
            p = os.path.join(dirpath, fn)
            # skip ELF binaries without extension
            if "." not in os.path.basename(fn):
                with open(p, "rb") as f:
                    if f.read(4) == b"\x7fELF":
                        continue
            out.append(p)
    out.sort()
    for p in out:
        print(p)
    print(f"# {len(out)} files", file=sys.stderr)


if __name__ == "__main__":
    main()
