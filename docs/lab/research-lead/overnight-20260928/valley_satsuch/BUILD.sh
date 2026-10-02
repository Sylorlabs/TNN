#!/bin/bash
# BUILD.sh: assemble and run the valley satisfiability search.
# Pure Zag + shell. No Python. The frozen v2gen.zag oracle is used
# byte-identically (sha256-verified). Aborts on any mismatch.
set -e
D="$(cd "$(dirname "$0")" && pwd)"
cd "$D"
REPO="$HOME/workspace/tnn-rsi"
ZNC="$REPO/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
V2GEN_SHA="a93f9cd624294b7e1e2c475b392024e300f1a8be05173438979b8c6fc37604a9"
V2INST_SHA="2b9b8bca05ffb88bd39fad1cff2dd1fed922833573e9d516c7486bf09b54e5a4"
V2INST="docs/lab/research-lead/overnight-20260928/valley_redesign2/v2inst.zag"
V2GEN="docs/lab/research-lead/overnight-20260928/valley_redesign2/v2gen.zag"

echo "[1] extracting frozen oracle blobs"
git -C "$REPO" show "ea920137b:$V2GEN" > v2gen_frozen.zag
git -C "$REPO" show "ea920137b:$V2INST" > v2inst_frozen.zag
echo "$V2GEN_SHA  v2gen_frozen.zag" | sha256sum -c -
echo "$V2INST_SHA  v2inst_frozen.zag" | sha256sum -c -

echo "[2] assembling myinst.zag (frozen helpers + new table + frozen score/s0)"
sed -n '1,67p' v2inst_frozen.zag > myinst.zag
cat table.zag >> myinst.zag
sed -n '187,204p' v2inst_frozen.zag >> myinst.zag
# byte-identity proof of the frozen generic parts
head -n 67 v2inst_frozen.zag > /tmp/h1.zag
head -n 67 myinst.zag > /tmp/h2.zag
diff /tmp/h1.zag /tmp/h2.zag
tail -n +187 v2inst_frozen.zag > /tmp/t1.zag
TOT=$(wc -l < myinst.zag); START=$((TOT-17))
tail -n +$START myinst.zag > /tmp/t2.zag
diff /tmp/t1.zag /tmp/t2.zag
echo "[2] frozen generic parts byte-identical"

echo "[3] concatenating satsuch.zag = myinst.zag + v2gen_frozen.zag"
cat myinst.zag v2gen_frozen.zag > satsuch.zag
MLEN=$(wc -l < myinst.zag)
tail -n +$((MLEN+1)) satsuch.zag > /tmp/g1.zag
diff /tmp/g1.zag v2gen_frozen.zag
echo "[3] v2gen section byte-identical"

echo "[4] compiling with pinned znc"
"$ZNC" satsuch.zag -o satsuch_bin

echo "[5] running 3x"
./satsuch_bin > RUN1.txt 2> RUN1.err
./satsuch_bin > RUN2.txt 2> RUN2.err
./satsuch_bin > RUN3.txt 2> RUN3.err
sha256sum RUN1.txt RUN2.txt RUN3.txt
cmp RUN1.txt RUN2.txt && cmp RUN2.txt RUN3.txt
echo "[5] 3/3 runs byte-identical"
echo "BUILD OK"
