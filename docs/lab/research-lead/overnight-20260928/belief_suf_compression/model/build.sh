#!/bin/sh
# build.sh -- BSC toy model build. Pure Zag; pinned znc; safebin PATH.
set -e
export PATH="$HOME/safebin"
HERE=$(dirname "$0")
cd "$HERE"
znc bsc.zag -o bsc 2>bsc_build.log || { echo "BSC BUILD FAILED"; grep -E "error" bsc_build.log | head -20; exit 1; }
echo "build ok"
sha256sum bsc | tee bin.sha256
cp bsc bsc1 && znc bsc.zag -o bsc2 2>/dev/null
cmp bsc1 bsc2 && echo "REBUILD IDENTICAL"
rm -f bsc1 bsc2
