#!/bin/bash
# BUILD_G0.sh: G0 diagnostic build and run script.
# Pure Zag + shell only. No Python.
# Run from the repo root: bash docs/lab/research-lead/overnight-20260928/beam_g0/BUILD_G0.sh
set -u
cd "$(dirname "$0")/../../../../.." || exit 1
ZNC=src/tools/toolchain/znc_linux_x86_64_abed8aa1
G0D=docs/lab/research-lead/overnight-20260928/beam_g0
CLD=docs/lab/research-lead/overnight-20260928/beam_unified_clean
EXPECT_MD5=6a8568a7232de691606e09712df0f17d

echo "=== step 1: control (unmodified r3u.zag) ==="
"$ZNC" "$CLD/r3u.zag" -o "$G0D/g0ctl_bin" || exit 1
"$G0D/g0ctl_bin" > "$G0D/G0Q_CTL.txt" 2> "$G0D/G0Q_CTL.err" || exit 1
CTL_MD5=$(md5sum "$G0D/G0Q_CTL.txt" | cut -d' ' -f1)
echo "control md5: $CTL_MD5"
if [ "$CTL_MD5" != "$EXPECT_MD5" ]; then
  echo "CONTROL-FAIL: baseline moved. Halting."
  exit 1
fi
if [ -s "$G0D/G0Q_CTL.err" ]; then
  echo "CONTROL-FAIL: stderr non-empty."
  exit 1
fi
echo "CONTROL-OK: reproduces committed raw."

echo "=== step 2: instrumented build ==="
"$ZNC" "$G0D/r3u_g0.zag" -o "$G0D/r3u_g0_bin" || exit 1

echo "=== step 3: three instrumented runs ==="
R=1
while [ $R -le 3 ]; do
  "$G0D/r3u_g0_bin" > "$G0D/G0Q_RAW_$R.txt" 2> "$G0D/G0Q_RAW_$R.err" || exit 1
  M=$(md5sum "$G0D/G0Q_RAW_$R.txt" | cut -d' ' -f1)
  echo "run $R stdout md5: $M"
  if [ "$M" != "$EXPECT_MD5" ]; then
    echo "F-NOPERTURB-FAIL on run $R. Halting before reading any log."
    exit 1
  fi
  if [ -s "$G0D/G0Q_RAW_$R.err" ]; then
    echo "STDERR-NONEMPTY on run $R. Halting."
    exit 1
  fi
  cp "$G0D/g0q.log" "$G0D/g0q_run$R.log" || exit 1
  R=$((R+1))
done

echo "=== step 4: determinism checks ==="
md5sum "$G0D/G0Q_RAW_1.txt" "$G0D/G0Q_RAW_2.txt" "$G0D/G0Q_RAW_3.txt"
md5sum "$G0D/g0q_run1.log" "$G0D/g0q_run2.log" "$G0D/g0q_run3.log"
cmp "$G0D/g0q_run1.log" "$G0D/g0q_run2.log" || exit 1
cmp "$G0D/g0q_run2.log" "$G0D/g0q_run3.log" || exit 1
wc -l "$G0D/g0q_run1.log"
echo "G0Q-BUILD-RUN-OK"
