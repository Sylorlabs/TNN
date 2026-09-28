#!/bin/bash
# WS2-B2 build: tocb binary (ToC + synonym bridge) with pinned znc.
# Regenerates src/syn_table.zag from SYN_TABLE_V1.txt and asserts the
# embedded bytes are byte-identical to the frozen table before compiling.
# @import is cwd-relative: copy sources + pinned substrate files into
# bdir_ws2b2/ first. (The build dir name must NOT equal this script's name:
# the script used to rm -rf its own path.)
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
cd "$HERE"
python3 gen_syn_table.py
# byte-identity assertion: embedded literal vs frozen table file
python3 - <<'EOF'
import re
src = open('src/syn_table.zag').read()
m = re.search(r'return "(.*)";', src, re.S)
assert m, 'literal not found'
embedded = m.group(1).replace('\\n', '\n')
tbl = open('SYN_TABLE_V1.txt').read()
want = ''.join(l + '\n' for l in tbl.split('\n') if l and not l.startswith('#'))
assert embedded == want, 'EMBEDDED TABLE DIFFERS FROM SYN_TABLE_V1.txt'
print('table byte-identity: OK (56 pairs)')
EOF
rm -rf "$HERE/bdir_ws2b2"
mkdir -p "$HERE/bdir_ws2b2"
cp "$HERE/src/toc_b2.zag" "$HERE/src/lib.zag" "$HERE/src/syn_table.zag" "$HERE/bdir_ws2b2/"
cp ~/workspace/tnn-lab/toolchain/R33_NATIVE_SHA256_V2.zag \
   ~/workspace/tnn-lab/toolchain/R33_NATIVE_IO_V1.zag "$HERE/bdir_ws2b2/"
cd "$HERE/bdir_ws2b2"
# NOTE: never pipe znc through `head` - closing the pipe early SIGPIPE-kills
# znc before it writes the binary. Log to a file and tail it instead.
"$ZNC" toc_b2.zag -o tocb > /tmp/znc_b2.log 2>&1 || { tail -30 /tmp/znc_b2.log; echo ZNC_FAILED; exit 1; }
grep -iE "^znc: error" /tmp/znc_b2.log | head -10 || true
tail -3 /tmp/znc_b2.log
ls -la tocb
echo BUILD_OK
