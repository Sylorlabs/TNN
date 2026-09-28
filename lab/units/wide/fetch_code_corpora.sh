#!/bin/bash
# EXPLORATORY — NOT EVIDENCE
# fetch_code_corpora.sh — EXPLORATORY fetcher for the TNN representation program.
# Downloads pinned upstream tarballs, extracts pinned source subtrees, and builds
# deterministic concatenated corpus files. Corpora are NEVER written under the repo.
# Default: DL_DIR=/tmp/code-corpora-dl OUT_DIR=/tmp/code-corpora
#
# Determinism: tarballs pinned by exact version URL; only the listed members are
# extracted; file list is LC_ALL=C sorted; each file is appended verbatim with
# at-least-one trailing "\n" enforced per file (so concatenation does not depend
# on upstream trailing newlines). MANIFEST records tarball URLs + sha256,
# corpus file counts, byte sizes, and sha256.
#
# Refuses to run if OUT_DIR resolves inside the tnn-lab repo.
set -u
OUT_DIR="${OUT_DIR:-/tmp/code-corpora}"
DL_DIR="${DL_DIR:-/tmp/code-corpora-dl}"

case "$OUT_DIR" in
  *tnn-lab*) echo "refusing: OUT_DIR inside repo: $OUT_DIR" >&2; exit 1;;
esac
mkdir -p "$OUT_DIR" "$DL_DIR"

fetch() { # filename url
  local name="$1"
  local url="$2"
  local dest="$DL_DIR/$name"
  if [ -f "$dest" ]; then
    echo "have $name"
  else
    echo "fetch $name"
    curl -sSL --retry 3 -o "$dest" "$url" || { echo "FAILED: $name" >&2; exit 1; }
  fi
  sha256sum "$dest" | awk '{print $1}' > "$dest.sha256"
}

fetch python-3.14.7.tar.xz  "https://www.python.org/ftp/python/3.14.7/Python-3.14.7.tar.xz"
fetch node-v26.9.0.tar.gz    "https://nodejs.org/dist/v26.9.0/node-v26.9.0.tar.gz"
fetch go1.27.1.src.tar.gz    "https://dl.google.com/go/go1.27.1.src.tar.gz"
fetch serde-1.0.229.crate    "https://static.crates.io/crates/serde/serde-1.0.229.crate"
fetch luvit-2.18.1.tar.gz    "https://github.com/luvit/luvit/archive/refs/tags/2.18.1.tar.gz"

# prep <name> <tarball> <member>... : extract ONLY the listed members.
prep() {
  local name="$1"
  local tb="$2"
  shift 2
  XTMP="$DL_DIR/x_$name"
  rm -rf "$XTMP"; mkdir -p "$XTMP"
  tar -xf "$DL_DIR/$tb" -C "$XTMP" "$@"
}

# build <out> <relroot> <find predicates...> : deterministic concat of the
# prepped tree. Requires XTMP set by prep.
build() {
  local out="$1"
  local root="$2"
  shift 2
  local list="$XTMP.files"
  ( cd "$XTMP/$root" && find . "$@" -type f | LC_ALL=C sort ) > "$list"
  local dest="$OUT_DIR/$out.txt"
  : > "$dest"
  while IFS= read -r f; do
    cat "$XTMP/$root/$f" >> "$dest"
    if [ -n "$(tail -c 1 "$dest")" ]; then printf '\n' >> "$dest"; fi
  done < "$list"
  sha256sum "$dest" | awk '{print $1}' > "$dest.sha256"
  echo "$out $(wc -l < "$list") files $(wc -c < "$dest") bytes sha256=$(cat "$dest.sha256")" \
    >> "$OUT_DIR/MANIFEST.txt"
}

: > "$OUT_DIR/MANIFEST.txt"
{
  echo "# code corpora manifest — built $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "# tarballs pinned by exact version URL; members listed per corpus below"
  for t in python-3.14.7.tar.xz node-v26.9.0.tar.gz go1.27.1.src.tar.gz \
           serde-1.0.229.crate luvit-2.18.1.tar.gz; do
    echo "tarball $t sha256=$(cat "$DL_DIR/$t.sha256")"
  done
} >> "$OUT_DIR/MANIFEST.txt"

# --- corpus definitions: pinned subtrees, test/example/bench suites excluded ---
prep python python-3.14.7.tar.xz Python-3.14.7/Lib
build python Python-3.14.7/Lib -name '*.py' -not -path './test/*'

prep javascript node-v26.9.0.tar.gz node-v26.9.0/lib
build javascript node-v26.9.0/lib \( -name '*.js' -o -name '*.mjs' \)

prep go go1.27.1.src.tar.gz go/src/encoding/json go/src/fmt go/src/strings
build go go/src -name '*.go' -not -name '*_test.go'

prep rust serde-1.0.229.crate serde-1.0.229/src
build rust serde-1.0.229/src -name '*.rs'

prep lua luvit-2.18.1.tar.gz luvit-2.18.1/deps luvit-2.18.1/init.lua \
  luvit-2.18.1/main.lua luvit-2.18.1/package.lua
build lua luvit-2.18.1 -name '*.lua'

echo "done. corpora in $OUT_DIR"
