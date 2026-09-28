#!/bin/bash
# Ruling 3 runner: T1-T3 (r3_implants) + T4 (JI cells per scheme x arm x variant).
# Builds ONE binary per implant scheme from the frozen sources: the only
# difference between builds is the R3_SCHEME const in r3_scheme.zag
# (1=SHIFT, 2=1-INDEXED, 3=DROP-5). Committed trial/ keeps the template
# (R3_SCHEME=1); each build dir gets its frozen const.
# Every binary runs twice; outputs must be byte-identical (diffed).
set -u
R=~/workspace/tnn-lab/wave12/strength-rulings/r3
T=$R/trial
OUT=$R/evidence
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
mkdir -p "$OUT"
LOG="$OUT/runner.log"
: > "$LOG"
note(){ echo "$1" | tee -a "$LOG"; }
fail(){ note "RUNNER_FAIL,$1"; exit 1; }
pass=0; fail_n=0

note "== static checks =="
cd "$T" || exit 1
if grep -rniE 'rand\(|srand|getrandom|/dev/urandom|rdtsc' \
    strength_core.zag strength_learner.zag strength_trial.zag strength_checker.zag \
    r3_scheme.zag >/dev/null 2>&1; then fail "RNG token found"; fi
for f in strength_learner.zag strength_trial.zag strength_checker.zag; do
  if grep -q '^@import' "$f"; then :; else fail "$f import not bare"; fi
done
# strength writes only in core (legal set + none new here)
if grep -nE 'st_write_strength|st_clear_strength' strength_learner.zag \
    strength_trial.zag strength_checker.zag >/dev/null 2>&1; then
  fail "strength write outside core"
fi
note "STATIC_OK"; pass=$((pass+1))

note "== T1-T3: r3_implants =="
"$ZNC" "$R/r3_implants.zag" --no-zagd --no-analyze --no-foreground-cache \
  -o "$R/r3_implants_bin" || fail "compile r3_implants"
for run in 1 2; do
  "$R/r3_implants_bin" > "$OUT/t123_r$run.log" 2>&1 || fail "t123 run$run"
done
if cmp -s "$OUT/t123_r1.log" "$OUT/t123_r2.log"; then
  note "PASS t123_deterministic"
else fail "t123_deterministic"; fi
pass=$((pass+1))

note "== T2d: 1-indexing qualifier-site audit (static) =="
# Every site in the learner whose meaning changes if episodes are
# renumbered 1..H: episode-number closed forms, (m>0)-style qualifiers,
# absolute episode indices, revelation offsets.
{
  echo "--- closed forms evaluated at episode numbers ---"
  grep -n "lr_imp(\|lr_wrong(\|lr_vj(\|lr_designated(" strength_learner.zag
  echo "--- qualifiers / absolute indices ---"
  grep -n "t>0\|t==99\|t==401\|m==0\|t==0" strength_learner.zag
  echo "--- revelation / contradiction offsets (relative: scheme-invariant) ---"
  grep -n "LR_D\|t-25\|t-50\|m+12\|+12" strength_learner.zag | head -12
} > "$OUT/r3_t2d_sites.txt" 2>&1
note "T2D_SITES_WRITTEN lines=$(wc -l < "$OUT/r3_t2d_sites.txt")"

note "== T4: JI cells per scheme =="
for scheme in 1 2 3; do
  B="$R/build_s$scheme"
  rm -rf "$B"; mkdir -p "$B"
  cp -r "$T"/* "$B"/
  sed -i "s/const R3_SCHEME:i32=1;/const R3_SCHEME:i32=$scheme;/" "$B/r3_scheme.zag"
  grep -q "const R3_SCHEME:i32=$scheme;" "$B/r3_scheme.zag" || fail "scheme const s$scheme"
  ( cd "$B" && "$ZNC" strength_trial.zag --no-zagd --no-analyze \
      --no-foreground-cache -o "r3_bin_s$scheme" ) || fail "compile s$scheme"
  BIN="$B/r3_bin_s$scheme"
  for arm in B C; do
    for var in 0 1 2; do
      for run in 1 2; do
        "$BIN" "$arm" JI "$var" S1 > "$OUT/cell_s${scheme}_${arm}_JI_${var}_r${run}.log" 2>&1
        ec=$?
        if [ $ec -ne 0 ]; then note "FAIL cell s${scheme} $arm JI $var r$run exit=$ec"; fail_n=$((fail_n+1)); fi
      done
      if cmp -s "$OUT/cell_s${scheme}_${arm}_JI_${var}_r1.log" "$OUT/cell_s${scheme}_${arm}_JI_${var}_r2.log"; then
        : # deterministic
      else note "FAIL deterministic s${scheme} $arm JI $var"; fail_n=$((fail_n+1)); fi
      if grep -q "^ST_INVALID 1$" "$OUT/cell_s${scheme}_${arm}_JI_${var}_r1.log"; then
        note "FAIL invalid s${scheme} $arm JI $var"; fail_n=$((fail_n+1)); fi
      if ! grep -q "^ST_DONE$" "$OUT/cell_s${scheme}_${arm}_JI_${var}_r1.log"; then
        note "FAIL nodone s${scheme} $arm JI $var"; fail_n=$((fail_n+1)); fi
      if grep -q "^CL_CHECK," "$OUT/cell_s${scheme}_${arm}_JI_${var}_r1.log"; then
        # CL_CHECK lines print actual,expected; count mismatches via analysis
        :
      fi
    done
  done
  note "SCHEME_${scheme}_CELLS_DONE"
done

note "== T5: episode-0 edge audit (static) =="
{
  echo "--- m==0 / t==0 special cases in learner ---"
  grep -n "==0\|>=0\|>0" strength_learner.zag | grep -v ">=0;" | head -20
  echo "--- implant-at-0 admission path (scheme 1 T4 log, arm B var0) ---"
  grep -h "ST_METRIC 3" "$OUT"/cell_s1_B_JI_*_r1.log
} > "$OUT/r3_t5_edge.txt" 2>&1
note "T5_EDGE_WRITTEN"

note "== done =="
note "pass=$pass fail_n=$fail_n"
if [ "$fail_n" = 0 ]; then echo "R3_COMPLETE" > "$OUT/VERDICT.txt"; else echo "R3_FAILED" > "$OUT/VERDICT.txt"; fi
