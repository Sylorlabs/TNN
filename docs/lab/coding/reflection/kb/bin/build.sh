#!/bin/bash
# build.sh — compile the KB installer and recall learner with the pinned toolchain.
# Deterministic plumbing: no decisions, just znc invocations.
set -e
KB="$(cd "$(dirname "$0")/.." && pwd)"
ZNC="$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1"
mkdir -p "$KB/bin"
"$ZNC" "$KB/src/kb_install.zag" -o "$KB/bin/kb_install" --no-analyze
"$ZNC" "$KB/src/kb_main.zag" -o "$KB/bin/kb_main" --no-analyze
echo "built: $KB/bin/kb_install $KB/bin/kb_main"
