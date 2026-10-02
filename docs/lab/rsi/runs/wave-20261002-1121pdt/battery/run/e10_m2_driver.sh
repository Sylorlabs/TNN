#!/bin/bash
# e10_m2_driver.sh -- deterministic M2 world driver for battery E10.
# Implements PREREG_E10.md sections 6.4, 6.5, 6.6 (fixed, mechanical).
# Usage: e10_m2_driver.sh <w1|w2|w3> <run#> <reset:0|1>
# Sealed PIs from env: PI_W1 (0-5), PI_W2 (0-1), PI_W3A (0-1), PI_W3B (0-1).
# W2/W3 read W1's vocab file for the in-situ vocab-verify (correction 6).
# Deterministic: no timestamps, no PIDs, no randomness in any output.
# Any vocab-verify mismatch aborts nonzero (WORLD-INVALID, fail-closed).
set -e
export PATH="$HOME/safebin"
DIR=$HOME/workspace/tnn-rsi-work/wave-20261002-1121pdt/battery/docs/lab/rsi/runs/wave-20261002-1121pdt/battery/run
SHIM=~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/core_freeze_tnn2_shim/freeze_shim2_bin
W=$1; RUN=$2; RESET=$3
STATE=$DIR/m2_state_run${RUN}.bin
WORLD=$DIR/m2${W}_world_run${RUN}.txt
TRANS=$DIR/m2${W}_trans_run${RUN}.txt
LOG=$DIR/m2${W}_log_run${RUN}.txt
TRUTHS=$DIR/m2${W}_truths_run${RUN}.txt
VOCABF=$DIR/m2${W}_vocab_run${RUN}.txt

if [ "$RESET" = "1" ]; then rm -f "$STATE"; fi
cp /dev/null "$WORLD"
> "$TRANS"
> "$LOG"
> "$TRUTHS"

run_step() {
  printf "%s\n" "$1" >> "$WORLD"
  printf "%s\n" "$1" > /tmp/e10_m2_step.txt
  "$SHIM" /tmp/e10_m2_step.txt "$STATE" > /tmp/e10_m2_out.txt
  cat /tmp/e10_m2_out.txt >> "$TRANS"
}
get_choice() { grep "^CHOICE " /tmp/e10_m2_out.txt | tail -1 | awk '{print $2}'; }
get_answer() { grep "^ANSWER " /tmp/e10_m2_out.txt | tail -1 | awk '{print $4}'; }

# Sealed informant mappings (PIs embedded at generation; see PI_RECORD.txt).
inf_w1() {
  local c=$1
  case "$PI_W1" in
    0) case $c in 1) echo A;; 2) echo B;; 3) echo C;; *) echo NONE;; esac;;
    1) case $c in 1) echo A;; 2) echo C;; 3) echo B;; *) echo NONE;; esac;;
    2) case $c in 1) echo B;; 2) echo A;; 3) echo C;; *) echo NONE;; esac;;
    3) case $c in 1) echo B;; 2) echo C;; 3) echo A;; *) echo NONE;; esac;;
    4) case $c in 1) echo C;; 2) echo A;; 3) echo B;; *) echo NONE;; esac;;
    5) case $c in 1) echo C;; 2) echo B;; 3) echo A;; *) echo NONE;; esac;;
    *) echo NONE;;
  esac
}
inf_w2() {
  local c=$1
  case "$PI_W2" in
    0) case $c in 1) echo A;; 2) echo B;; *) echo NONE;; esac;;
    1) case $c in 1) echo B;; 2) echo A;; *) echo NONE;; esac;;
    *) echo NONE;;
  esac
}
inf_w3a() {
  local c=$1
  case "$PI_W3A" in
    0) case $c in 1) echo A;; 2) echo B;; *) echo NONE;; esac;;
    1) case $c in 1) echo B;; 2) echo A;; *) echo NONE;; esac;;
    *) echo NONE;;
  esac
}
inf_w3b() {
  local c=$1
  case "$PI_W3B" in
    0) case $c in 1) echo A;; 2) echo C;; *) echo NONE;; esac;;
    1) case $c in 1) echo C;; 2) echo A;; *) echo NONE;; esac;;
    *) echo NONE;;
  esac
}
inf_w3() {
  local k=$1; local c=$2
  case "$k" in
    64101|64102|64111|64112) inf_w3a "$c";;
    *) inf_w3b "$c";;
  esac
}

# ---------------- W1: informant selection v2 ----------------
w1() {
  run_step "ACT";                       C1=$(get_choice)
  run_step "QUERY 62901 62900 62911"
  run_step "ACT";                       C2=$(get_choice)
  printf "NULL %s\nINQ %s\n" "$C1" "$C2" > "$VOCABF"
  run_step "OBSERVE 62991 62990 62991
OBSERVE 62992 62990 62992
OBSERVE 62993 62990 62993
OBSERVE 62994 62990 62994
OBSERVE 62091 62500 62999
OBSERVE 62092 62500 62999"
  local prev=62999 k truth C INF ans
  for k in 62101 62102 62103 62104 62105; do
    truth=$((k - 62101 + 62201))
    run_step "QUERY $k 62500 $truth"
    run_step "ACT";                     C=$(get_choice)
    INF=$(inf_w1 "$C")
    printf "ACT CAL %s %s %s\n" "$k" "$C" "$INF" >> "$LOG"
    if [ "$INF" != "NONE" ]; then
      ans=$truth
      if [ "$INF" = "B" ]; then ans=$((truth + 1)); fi
      if [ "$INF" = "C" ]; then ans=$prev; fi
      run_step "OBSERVE $k 62500 $ans"
    fi
    run_step "OBSERVE $k 62500 $truth"
    run_step "QUERY $k 62500 $truth"
    prev=$truth
  done
  prev=62205
  for k in 62111 62112 62113; do
    truth=$((k - 62111 + 62211))
    printf "%s %s\n" "$k" "$truth" >> "$TRUTHS"
    run_step "QUERY $k 62500 $truth"
    for a in 1 2; do
      run_step "ACT";                   C=$(get_choice)
      INF=$(inf_w1 "$C")
      printf "ACT HID %s %s %s\n" "$k" "$C" "$INF" >> "$LOG"
      if [ "$INF" != "NONE" ]; then
        ans=$truth
        if [ "$INF" = "B" ]; then ans=$((truth + 1)); fi
        if [ "$INF" = "C" ]; then ans=$prev; fi
        run_step "OBSERVE $k 62500 $ans"
      fi
    done
    run_step "QUERY $k 62500 $truth"
    prev=$truth
  done
}

# ---------------- W2: inquiry budget ----------------
w2() {
  run_step "OBSERVE 63991 63990 63991
OBSERVE 63992 63990 63992
OBSERVE 63993 63990 63993
OBSERVE 63994 63990 63994"
  local NULLV INQV C0 C1 ok
  NULLV=$(awk '/^NULL/{print $2}' "$DIR/m2w1_vocab_run${RUN}.txt")
  INQV=$(awk '/^INQ/{print $2}' "$DIR/m2w1_vocab_run${RUN}.txt")
  run_step "ACT";                       C0=$(get_choice)
  run_step "QUERY 63901 63900 63911"
  run_step "ACT";                       C1=$(get_choice)
  ok=0
  if [ "$C0" = "$NULLV" ] && [ "$C1" = "$INQV" ]; then ok=1; fi
  printf "NULL %s\nINQ %s\n" "$C0" "$C1" > "$VOCABF"
  printf "VOCAB null=%s inq=%s ok=%s\n" "$NULLV" "$INQV" "$ok" >> "$LOG"
  if [ "$ok" != "1" ]; then echo "W2 vocab-verify failed" >&2; exit 3; fi
  local k truth C INF ans Cc nacts early a
  for k in 63101 63102 63103; do
    truth=$((k - 63101 + 63201))
    run_step "QUERY $k 63500 $truth"
    nacts=0; C="NONE"
    for a in 1 2; do
      run_step "ACT";                   Cc=$(get_choice)
      printf "ACT CAL %s %s %s\n" "$k" "$Cc" "$(inf_w2 "$Cc")" >> "$LOG"
      nacts=$((nacts + 1))
      if [ "$Cc" = "$NULLV" ]; then break; fi
      C=$Cc
    done
    early=0; if [ "$nacts" -lt 2 ]; then early=1; fi
    printf "KEYDONE CAL %s %s %s\n" "$k" "$nacts" "$early" >> "$LOG"
    INF=$(inf_w2 "$C")
    if [ "$INF" != "NONE" ]; then
      ans=$truth
      if [ "$INF" = "B" ]; then ans=$((truth + 1)); fi
      run_step "OBSERVE $k 63500 $ans"
    fi
    run_step "OBSERVE $k 63500 $truth"
    run_step "QUERY $k 63500 $truth"
  done
  for k in 63111 63112 63113 63114; do
    truth=$((k - 63111 + 63211))
    printf "%s %s\n" "$k" "$truth" >> "$TRUTHS"
    run_step "QUERY $k 63500 $truth"
    nacts=0; C="NONE"
    for a in 1 2 3; do
      run_step "ACT";                   Cc=$(get_choice)
      printf "ACT HID %s %s %s\n" "$k" "$Cc" "$(inf_w2 "$Cc")" >> "$LOG"
      nacts=$((nacts + 1))
      if [ "$Cc" = "$NULLV" ]; then break; fi
      C=$Cc
    done
    early=0; if [ "$nacts" -lt 3 ]; then early=1; fi
    printf "KEYDONE HID %s %s %s\n" "$k" "$nacts" "$early" >> "$LOG"
    INF=$(inf_w2 "$C")
    if [ "$INF" != "NONE" ]; then
      ans=$truth
      if [ "$INF" = "B" ]; then ans=$((truth + 1)); fi
      run_step "OBSERVE $k 63500 $ans"
    fi
    run_step "QUERY $k 63500 $truth"
  done
  collateral
}

# ---------------- W3: selection under population change ----------------
w3() {
  run_step "OBSERVE 64991 64990 64991
OBSERVE 64992 64990 64992
OBSERVE 64993 64990 64993
OBSERVE 64994 64990 64994"
  local NULLV INQV C0 C1 ok
  NULLV=$(awk '/^NULL/{print $2}' "$DIR/m2w1_vocab_run${RUN}.txt")
  INQV=$(awk '/^INQ/{print $2}' "$DIR/m2w1_vocab_run${RUN}.txt")
  run_step "ACT";                       C0=$(get_choice)
  run_step "QUERY 64901 64900 64911"
  run_step "ACT";                       C1=$(get_choice)
  ok=0
  if [ "$C0" = "$NULLV" ] && [ "$C1" = "$INQV" ]; then ok=1; fi
  printf "NULL %s\nINQ %s\n" "$C0" "$C1" > "$VOCABF"
  printf "VOCAB null=%s inq=%s ok=%s\n" "$NULLV" "$INQV" "$ok" >> "$LOG"
  if [ "$ok" != "1" ]; then echo "W3 vocab-verify failed" >&2; exit 3; fi
  local k truth C INF ans
  for k in 64101 64102 64103 64104; do
    truth=$((k - 64101 + 64201))
    run_step "QUERY $k 64500 $truth"
    run_step "ACT";                     C=$(get_choice)
    INF=$(inf_w3 "$k" "$C")
    printf "ACT CAL %s %s %s\n" "$k" "$C" "$INF" >> "$LOG"
    if [ "$INF" != "NONE" ]; then
      ans=$truth
      if [ "$INF" = "B" ]; then ans=$((truth + 1)); fi
      if [ "$INF" = "C" ]; then ans=64999; fi
      run_step "OBSERVE $k 64500 $ans"
    fi
    run_step "OBSERVE $k 64500 $truth"
    run_step "QUERY $k 64500 $truth"
  done
  for k in 64111 64112 64113 64114; do
    truth=$((k - 64111 + 64211))
    printf "%s %s\n" "$k" "$truth" >> "$TRUTHS"
    run_step "QUERY $k 64500 $truth"
    run_step "ACT";                     C=$(get_choice)
    INF=$(inf_w3 "$k" "$C")
    printf "ACT HID %s %s %s\n" "$k" "$C" "$INF" >> "$LOG"
    if [ "$INF" != "NONE" ]; then
      ans=$truth
      if [ "$INF" = "B" ]; then ans=$((truth + 1)); fi
      if [ "$INF" = "C" ]; then ans=64999; fi
      run_step "OBSERVE $k 64500 $ans"
    fi
    run_step "QUERY $k 64500 $truth"
  done
  collateral
}

collateral() {
  local s r exp got
  for spec in "62091 62500 62999" "62092 62500 62999"; do
    s=$(echo "$spec" | awk '{print $1}')
    r=$(echo "$spec" | awk '{print $2}')
    exp=$(echo "$spec" | awk '{print $3}')
    run_step "QUERY $s $r $exp"
    got=$(get_answer)
    printf "COLLATERAL %s %s %s %s\n" "$s" "$r" "$got" "$exp" >> "$LOG"
  done
}

case "$W" in
  w1) w1;;
  w2) w2;;
  w3) w3;;
  *) echo "usage: e10_m2_driver.sh <w1|w2|w3> <run#> <reset:0|1>" >&2; exit 2;;
esac
