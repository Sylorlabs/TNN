#!/bin/bash
# ds_build.sh -- SPEC-DRIFTRATE-SWEEP: build + run + verify.
# Usage: ./ds_build.sh  (run from this directory)
# safebin PATH is mandatory; the pinned znc builds ds_bin; the binary
# runs 3x; sha256/cmp equality across the three runs is checked; the
# frozen kill bars from PREREG.md are adjudicated.
export PATH="$HOME/safebin"
set -u
D="$(cd "$(dirname "$0")" && pwd)"
DA="$D/../disagreement_attribution"
RB="$D/../spec_relationblind"
ET="$D/../spec_epochtag"
RR="$D/../spec_refusal_recovery"
ZNC="$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
cd "$D" || exit 1

# K2 toolchain guard record
echo "PATH=$PATH"
echo "python3: $(which python3 || echo MISSING)"
echo "python:  $(which python  || echo MISSING)"
which znc

fail() { echo "BUILD-FAIL: $1"; exit 1; }

[ -f "$ZNC" ] || fail "pinned znc missing at $ZNC"
for f in "$DA/da_base.zag" "$DA/da_module.zag" "$DA/da_learn.zag" \
         "$RB/rb_world.zag" "$RB/rb_fix.zag" \
         "$ET/et_world.zag" "$ET/et_spec.zag" \
         "$RR/rr_spec.zag"; do
  [ -f "$f" ] || fail "missing reused source: $f"
done
# K11 (part): reused sources byte-unmodified (no unstaged diff vs HEAD)
for f in "$DA/da_learn.zag" "$RR/rr_spec.zag" "$ET/et_spec.zag" "$ET/et_world.zag"; do
  /usr/bin/git diff --quiet -- "$f" || fail "K11: reused source modified: $f"
done

# assemble: real da_base + relationblind world + epochtag epoch machinery +
# real da_module + real da_learn (NOT modified) + relationblind fix variants
# + epochtag epoch specs + refusal-recovery wrappers (all unmodified) +
# lane sweep steps + lane harness main.
cat "$DA/da_base.zag" "$RB/rb_world.zag" "$ET/et_world.zag" "$DA/da_module.zag" \
    "$DA/da_learn.zag" "$RB/rb_fix.zag" "$ET/et_spec.zag" "$RR/rr_spec.zag" \
    ds_spec.zag ds_main.zag > ds_full.zag
[ "$(grep -c '^fn main(' ds_full.zag)" = "1" ] || fail "expected exactly one fn main in ds_full.zag"
grep -q "901\|902" ds_spec.zag && fail "ds_spec.zag contains world literals"
grep -q "901\|902" ds_main.zag && fail "ds_main.zag contains world literals"

"$ZNC" build ds_full.zag -o ds_bin > ds_compile.txt 2>&1 || fail "znc build of ds_full.zag failed"
grep -q ": error" ds_compile.txt && fail "compiler reported an error (see ds_compile.txt)"

# run 3x
for i in 1 2 3; do
  ./ds_bin > "ds_run$i.txt" 2> "ds_run$i.err"; echo "ds_bin run$i exit=$?"
done

# determinism: byte-identical across the 3 runs
cmp ds_run1.txt ds_run2.txt || fail "ds_run1/ds_run2 differ"
cmp ds_run1.txt ds_run3.txt || fail "ds_run1/ds_run3 differ"

# K3 stderr must be empty (exits printed above must be 0)
for f in ds_run1.err ds_run2.err ds_run3.err; do
  [ -s "$f" ] && fail "K3: non-empty stderr: $f"
done

echo "--- output ---"
cat ds_run1.txt
echo "--- kill bars ---"

cell_field() { # $1=M $2=N $3=P $4=field -> numeric value
  grep "^CELL M=$1 N=$2 P=$3 " ds_run1.txt | grep -o "$4=[0-9]*" | head -1 | cut -d= -f2
}

# K10 (part): exactly 75 CELL lines
[ "$(grep -c '^CELL ' ds_run1.txt)" = "75" ] || fail "K10: expected 75 CELL lines"

for M in 1 2 4 8 16; do
  for N in 1 2 4 8 16; do
    # K4: refuse-only arm sanity
    r=$(cell_field $M $N refuse rebuilds); a=$(cell_field $M $N refuse answered)
    f=$(cell_field $M $N refuse refusals);  k=$(cell_field $M $N refuse kb)
    q=$(cell_field $M $N refuse Q)
    { [ "$r" = "0" ] && [ "$a" = "0" ] && [ "$f" = "$q" ] && [ "$k" = "0" ]; } \
      || fail "K4: M=$M N=$N refuse: rebuilds=$r answered=$a refusals=$f kb=$k Q=$q"
    # K5: eager correctness at all rates
    a=$(cell_field $M $N eager answered); f=$(cell_field $M $N eager refusals)
    q=$(cell_field $M $N eager Q)
    { [ "$a" = "$q" ] && [ "$f" = "0" ]; } \
      || fail "K5: M=$M N=$N eager: answered=$a refusals=$f Q=$q"
    # K6: lazy correctness + single-refusal mechanism
    a=$(cell_field $M $N lazy answered); f=$(cell_field $M $N lazy refusals)
    r=$(cell_field $M $N lazy rebuilds);  q=$(cell_field $M $N lazy Q)
    { [ "$a" = "$q" ] && [ "$f" = "$r" ]; } \
      || fail "K6: M=$M N=$N lazy: answered=$a refusals=$f rebuilds=$r Q=$q"
    # K7: lazy never rebuilds more than eager
    rl=$(cell_field $M $N lazy rebuilds); re=$(cell_field $M $N eager rebuilds)
    [ "$rl" -le "$re" ] || fail "K7: M=$M N=$N lazy=$rl > eager=$re"
    # K10 (part): eager rebuilds == D (exactly one rebuild per drift)
    d=$(cell_field $M $N eager D)
    [ "$re" = "$d" ] || fail "K10: M=$M N=$N eager rebuilds=$re != D=$d"
  done
done
echo "PASS: K4/K5/K6/K7/K10 per-cell bars over all 25 cells"

# K8: unit-economics crossover bracketed (k=1/16 vs k=16)
r=$(cell_field 1 16 eager rebuilds); a=$(cell_field 1 16 eager answered)
[ "$r" -gt "$a" ] || fail "K8: M=1 N=16 eager rebuilds=$r not > answered=$a"
echo "PASS: K8a M=1 N=16 eager rebuilds=$r > answered=$a (k=1/16, >1 rebuild per answer)"
r=$(cell_field 16 1 eager rebuilds); a=$(cell_field 16 1 eager answered)
[ "$r" -lt "$a" ] || fail "K8: M=16 N=1 eager rebuilds=$r not < answered=$a"
echo "PASS: K8b M=16 N=1 eager rebuilds=$r < answered=$a (k=16)"

# K9: eager-vs-lazy waste crossover
re=$(cell_field 1 16 eager rebuilds); rl=$(cell_field 1 16 lazy rebuilds)
[ "$re" -ge "$(( rl * 2 ))" ] || fail "K9: M=1 N=16 eager=$re < 2*lazy=$(( rl * 2 ))"
echo "PASS: K9a M=1 N=16 eager=$re >= 2*lazy=$(( rl * 2 )) (high-churn waste)"
re=$(cell_field 16 1 eager rebuilds); rl=$(cell_field 16 1 lazy rebuilds)
[ "$re" = "$rl" ] || fail "K9: M=16 N=1 eager=$re != lazy=$rl"
echo "PASS: K9b M=16 N=1 eager=$re == lazy=$rl (no waste at saturation)"

# K11 hygiene: no non-ASCII bytes in lane sources
if LC_ALL=C grep -l '[^[:print:][:space:]]' PREREG.md NAMECHECK.md ds_spec.zag ds_main.zag ds_build.sh 2>/dev/null; then
  fail "K11: non-ASCII byte found"
fi
echo "PASS: K11 ASCII-only, no world literals in ds_spec.zag/ds_main.zag, one fn main, reused sources unmodified"

echo "ALL KILL BARS PASS"
