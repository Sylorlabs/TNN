#!/bin/bash
# DECLINE INVESTIGATION runner: ordering x bar x front-end cells, 3 reps each.
cd ~/workspace/tnn-lab/prose-learning/epistemic_wave/speechact_exp || exit 1
EV=scored_evidence
fail=0

run_cell() {
  # $1=binary $2=workdir $3=name $4=rung $5=items $6=mode
  local bin="$1" wd="$2" name="$3" rung="$4" items="$5" mode="$6"
  local outs=()
  for r in 1 2 3; do
    local f="$EV/dec_${name}_rep${r}.txt"
    "./$bin" "$wd" "$rung" "$items" "$mode" > "$f" 2>/dev/null
    outs+=("$f")
    ( cd "$EV" && sha256sum "$(basename "$f")" > "$(basename "$f" .txt).sha256" )
  done
  if cmp -s "${outs[0]}" "${outs[1]}" && cmp -s "${outs[1]}" "${outs[2]}"; then
    echo "OK   $name  $(tail -1 "${outs[0]}")"
  else
    echo "FAIL $name  reps differ!"
    fail=1
  fi
}

RUNGS="0 1 2 4 8 16 32"

if [ "$1" = "orders" ] || [ -z "$1" ]; then
  for ord in diverse redundant proto outlier; do
    for rg in $RUNGS; do
      run_cell delib_vol_bin "$PWD/ord_$ord" "ord_${ord}_r${rg}" "$rg" c70.txt all
    done
  done
fi

if [ "$1" = "bars" ] || [ -z "$1" ]; then
  for v in cnt b2 b3; do
    for rg in $RUNGS; do
      run_cell "delib_${v}_bin" . "bar_${v}_r${rg}" "$rg" c70.txt all
    done
    # control legs at r2 and r32
    run_cell "delib_${v}_bin" . "bar_${v}_r2_b12f" 2 b12_false.txt all
    run_cell "delib_${v}_bin" . "bar_${v}_r32_b12f" 32 b12_false.txt all
    run_cell "delib_${v}_bin" . "bar_${v}_r2_b12t" 2 b12_true.txt all
    run_cell "delib_${v}_bin" . "bar_${v}_r32_b12t" 32 b12_true.txt all
  done
fi

if [ "$1" = "frontends" ] || [ -z "$1" ]; then
  for v in f2 f3; do
    for rg in $RUNGS; do
      run_cell "delib_${v}_bin" . "fe_${v}_r${rg}" "$rg" c70.txt all
    done
    run_cell "delib_${v}_bin" . "fe_${v}_r2_b12f" 2 b12_false.txt all
    run_cell "delib_${v}_bin" . "fe_${v}_r32_b12f" 32 b12_false.txt all
    run_cell "delib_${v}_bin" . "fe_${v}_r2_b12t" 2 b12_true.txt all
    run_cell "delib_${v}_bin" . "fe_${v}_r32_b12t" 32 b12_true.txt all
  done
fi

# combined corrected candidate: diverse ordering + count rule
if [ "$1" = "cntdiv" ] || [ -z "$1" ]; then
  for rg in $RUNGS; do
    run_cell delib_cnt_bin "$PWD/ord_diverse" "cntdiv_r${rg}" "$rg" c70.txt all
  done
  run_cell delib_cnt_bin "$PWD/ord_diverse" "cntdiv_r2_b12f" 2 b12_false.txt all
  run_cell delib_cnt_bin "$PWD/ord_diverse" "cntdiv_r32_b12f" 32 b12_false.txt all
  run_cell delib_cnt_bin "$PWD/ord_diverse" "cntdiv_r2_b12t" 2 b12_true.txt all
  run_cell delib_cnt_bin "$PWD/ord_diverse" "cntdiv_r32_b12t" 32 b12_true.txt all
fi

# baseline control legs (original engine) at r2/r32 for comparison
if [ "$1" = "controls" ] || [ -z "$1" ]; then
  for rg in 2 32; do
    run_cell delib_vol_bin . "base_r${rg}_b12f" "$rg" b12_false.txt all
    run_cell delib_vol_bin . "base_r${rg}_b12t" "$rg" b12_true.txt all
  done
fi

echo "fail=$fail"
exit $fail
