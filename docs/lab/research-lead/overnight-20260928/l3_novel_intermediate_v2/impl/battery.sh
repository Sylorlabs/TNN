#!/bin/sh
# battery.sh -- L3-NIV2 battery supervisor (dev fixtures).
# Shell only: FIFO plumbing, process orchestration, log collection,
# sha256 digests. All research computation is pure Zag in the two
# binaries. Uses /usr/bin/mkfifo explicitly (not in safebin; shell
# plumbing, not research computation).
set -u
export PATH="$HOME/safebin"
D="$HOME/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/l3_novel_intermediate_v2/impl"
cd "$HOME/workspace/tnn-rsi"
MKFIFO=/usr/bin/mkfifo
SEED=42

build() {
  cat "$D/prelude.zag" "$D/isa.zag" "$D/lm_prot.zag" "$D/lm_cons.zag" \
      "$D/lm_cons2.zag" "$D/lm_arms.zag" "$D/lm_main.zag" > "$D/learner_full.zag"
  cat "$D/prelude.zag" "$D/isa.zag" "$D/world.zag" > "$D/world_full.zag"
  znc "$D/learner_full.zag" -o "$D/learner_bin" 2>"$D/learner_compile.txt" || return 1
  znc "$D/world_full.zag" -o "$D/world_bin" 2>"$D/world_compile.txt" || return 1
  echo "build ok"
}

# run_one <name> <key> <learner args...>
# Single arm, single world key, no pauses.
run_one() {
  name=$1; key=$2; shift 2
  L2W=/tmp/niv2_$name.l2w; W2L=/tmp/niv2_$name.w2l
  rm -f $L2W $W2L; $MKFIFO $L2W $W2L
  exec 3<>$L2W; exec 4<>$W2L
  "$D/world_bin" "$key" <$L2W >$W2L 2>"$D/run_$name.world.log" &
  WPID=$!
  timeout 900 "$D/learner_bin" "$SEED" "$@" >$L2W <$W2L 2>"$D/run_$name.log"
  LRC=$?
  kill $WPID 2>/dev/null; wait $WPID 2>/dev/null
  exec 3>&-; exec 4>&-
  rm -f $L2W $W2L
  echo "$name learner_rc=$LRC"
}

# run_t1t4 <name> : T1 T2 PAUSE T3 PAUSE T4 with key swaps on PHASE-DONE.
run_t1t4() {
  name=$1
  L2W=/tmp/niv2_$name.l2w; W2L=/tmp/niv2_$name.w2l
  rm -f $L2W $W2L; $MKFIFO $L2W $W2L
  exec 3<>$L2W; exec 4<>$W2L
  start_world() {
    "$D/world_bin" "$1" <$L2W >$W2L 2>>"$D/run_$name.world.log" &
    WPID=$!
  }
  start_world "$D/dev/DEV-S1.key"
  timeout 1200 "$D/learner_bin" "$SEED" T1 T2 PAUSE T3 PAUSE T4 >$L2W <$W2L 2>"$D/run_$name.log" &
  LPID=$!
  swaps=0
  start_s=$(date +%s)
  while kill -0 $LPID 2>/dev/null; do
    n=$(grep -c "PHASE-DONE" "$D/run_$name.log" 2>/dev/null || true)
    if [ -z "$n" ]; then n=0; fi
    if [ "$n" -gt "$swaps" ]; then
      swaps=$n
      if [ "$n" -eq 1 ]; then start_world "$D/dev/DEV-S2.key"; echo "swapped to DEV-S2"; fi
      if [ "$n" -eq 2 ]; then start_world "$D/dev/DEV-S3.key"; echo "swapped to DEV-S3"; fi
    fi
    now_s=$(date +%s)
    if [ $((now_s - start_s)) -gt 1150 ]; then echo "TIMEOUT"; break; fi
    sleep 1
  done
  wait $LPID; LRC=$?
  kill $WPID 2>/dev/null; wait $WPID 2>/dev/null
  exec 3>&-; exec 4>&-
  rm -f $L2W $W2L
  echo "$name learner_rc=$LRC swaps=$swaps"
}

# c3 needs T1's committed program hex: extract from the T1-T4 log.
c3hex() {
  grep "^TR .* COMMIT 0 " "$D/run_$1.log" | head -1 | sed 's/.*COMMIT 0 [0-9]* [0-9]* [0-9]* //'
}

case "${1:-all}" in
  build) build ;;
  t1t4) run_t1t4 "t1t4_$2" ;;
  one) shift; run_one "$@" ;;
  all)
    build || exit 1
    run_t1t4 "t1t4_r$2"
    run_one "t5a_r$2" "$D/dev/DEV-S4a.key" T5A
    run_one "t5b_r$2" "$D/dev/DEV-S4b.key" T5B
    run_one "c0_r$2" "$D/dev/DEV-S1.key" C0
    run_one "c1_r$2" "$D/dev/DEV-S1.key" C1
    run_one "c2_r$2" "$D/dev/DEV-S1.key" C2
    HX=$(c3hex "t1t4_r$2")
    echo "c3 hex: $HX"
    run_one "c3_r$2" "$D/dev/DEV-S3.key" C3 "$HX"
    run_one "c4_r$2" "$D/dev/DEV-S1.key" C4
    run_one "c5_r$2" "$D/dev/DEV-S3.key" C5
    ;;
esac
echo "battery-done"
