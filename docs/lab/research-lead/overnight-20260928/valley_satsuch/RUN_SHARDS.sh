#!/bin/bash
# RUN_SHARDS.sh: build and run each shard 3x with byte-identical logs.
# Pure shell. Frozen oracle sha-verified per shard.
set -e
D="$(cd "$(dirname "$0")" && pwd)"
cd "$D"
REPO="$HOME/workspace/tnn-rsi"
ZNC="$REPO/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
V2GEN_SHA="a93f9cd624294b7e1e2c475b392024e300f1a8be05173438979b8c6fc37604a9"
V2INST_SHA="2b9b8bca05ffb88bd39fad1cff2dd1fed922833573e9d516c7486bf09b54e5a4"

# shards: "name:base:count"
SHARDS="s1:1:12 s2:13:12 s3:25:9 s4:34:12 s5:46:12 s6:58:14"

echo "[0] verifying frozen oracle"
echo "$V2GEN_SHA  v2gen_frozen.zag" | sha256sum -c -
echo "$V2INST_SHA  v2inst_frozen.zag" | sha256sum -c -

for spec in $SHARDS; do
  name=$(echo "$spec" | cut -d: -f1)
  base=$(echo "$spec" | cut -d: -f2)
  count=$(echo "$spec" | cut -d: -f3)
  echo "=== shard $name (oids $base..$((base+count-1))) ==="
  # generate shard table
  sed -e "s/fn s3_base()i32 { return 1; }/fn s3_base()i32 { return $base; }/" \
      -e "s/fn s3_count()i32 { return 12; }/fn s3_count()i32 { return $count; }/" \
      table_shard.zag > "table_$name.zag"
  # assemble
  sed -n '1,67p' v2inst_frozen.zag > "myinst_$name.zag"
  cat "table_$name.zag" >> "myinst_$name.zag"
  sed -n '187,204p' v2inst_frozen.zag >> "myinst_$name.zag"
  cat "myinst_$name.zag" v2gen_frozen.zag > "satsuch_$name.zag"
  # verify v2gen section byte-identical
  MLEN=$(wc -l < "myinst_$name.zag")
  tail -n +$((MLEN+1)) "satsuch_$name.zag" | diff - v2gen_frozen.zag
  # compile
  "$ZNC" "satsuch_$name.zag" -o "satsuch_${name}_bin" 2>/dev/null
  # run 3x
  "./satsuch_${name}_bin" > "RUN_${name}_1.txt" 2> "RUN_${name}_1.err"
  "./satsuch_${name}_bin" > "RUN_${name}_2.txt" 2> "RUN_${name}_2.err"
  "./satsuch_${name}_bin" > "RUN_${name}_3.txt" 2> "RUN_${name}_3.err"
  sha256sum "RUN_${name}_1.txt" "RUN_${name}_2.txt" "RUN_${name}_3.txt"
  cmp "RUN_${name}_1.txt" "RUN_${name}_2.txt"
  cmp "RUN_${name}_2.txt" "RUN_${name}_3.txt"
  echo "shard $name: 3/3 byte-identical"
done
echo "ALL SHARDS OK"
