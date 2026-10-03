#!/bin/bash
# ld_build.sh -- SPEC-LAZY-DEFAULT: build + run + verify.
# Usage: ./ld_build.sh  (run from this directory)
# safebin PATH is mandatory; the pinned znc builds ld_bin; the binary
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
# lane policy layer + lane harness main.
cat "$DA/da_base.zag" "$RB/rb_world.zag" "$ET/et_world.zag" "$DA/da_module.zag" \
    "$DA/da_learn.zag" "$RB/rb_fix.zag" "$ET/et_spec.zag" "$RR/rr_spec.zag" \
    ld_spec.zag ld_main.zag > ld_full.zag
[ "$(grep -c '^fn main(' ld_full.zag)" = "1" ] || fail "expected exactly one fn main in ld_full.zag"
grep -q "901\|902" ld_spec.zag && fail "ld_spec.zag contains world literals"
grep -q "901\|902" ld_main.zag && fail "ld_main.zag contains world literals"

"$ZNC" build ld_full.zag -o ld_bin > ld_compile.txt 2>&1 || fail "znc build of ld_full.zag failed"
grep -q ": error" ld_compile.txt && fail "compiler reported an error (see ld_compile.txt)"

# run 3x
for i in 1 2 3; do
  ./ld_bin > "ld_run$i.txt" 2> "ld_run$i.err"; echo "ld_bin run$i exit=$?"
done

# determinism: byte-identical across the 3 runs
cmp ld_run1.txt ld_run2.txt || fail "ld_run1/ld_run2 differ"
cmp ld_run1.txt ld_run3.txt || fail "ld_run1/ld_run3 differ"
sha256sum ld_run1.txt

# K3 stderr must be empty (exits printed above must be 0)
for f in ld_run1.err ld_run2.err ld_run3.err; do
  [ -s "$f" ] && fail "K3: non-empty stderr: $f"
done

echo "--- output ---"
cat ld_run1.txt
echo "--- kill bars ---"

cell_field() { # $1=M $2=N $3=P $4=field -> numeric value
  grep "^CELL M=$1 N=$2 P=$3 " ld_run1.txt | grep -o "$4=[0-9]*" | head -1 | cut -d= -f2
}

# K10 (part): exactly 75 CELL lines
[ "$(grep -c '^CELL ' ld_run1.txt)" = "75" ] || fail "K10: expected 75 CELL lines"

for M in 1 2 4 8 16; do
  for N in 1 2 4 8 16; do
    # per-arm values, distinct names per arm (no cross-arm reuse)
    dd=$(cell_field $M $N default D);       qd=$(cell_field $M $N default Q)
    rd=$(cell_field $M $N default rebuilds); ad=$(cell_field $M $N default answered)
    fd=$(cell_field $M $N default refusals); kd=$(cell_field $M $N default kb)
    de=$(cell_field $M $N eager D);          qe=$(cell_field $M $N eager Q)
    re=$(cell_field $M $N eager rebuilds);  ae=$(cell_field $M $N eager answered)
    fe=$(cell_field $M $N eager refusals);   ke=$(cell_field $M $N eager kb)
    je=$(cell_field $M $N eager just)
    r0=$(cell_field $M $N eager0 rebuilds);  a0=$(cell_field $M $N eager0 answered)
    f0=$(cell_field $M $N eager0 refusals);  fb0=$(cell_field $M $N eager0 fb)
    j0=$(cell_field $M $N eager0 just)
    if [ "$dd" -lt "$qd" ]; then m=$dd; else m=$qd; fi
    # K4: default correctness (answered=Q, refusals=rebuilds, kb=2Q)
    { [ "$ad" = "$qd" ] && [ "$fd" = "$rd" ] && [ "$kd" = "$(( qd * 2 ))" ]; } \
      || fail "K4: M=$M N=$N default: answered=$ad refusals=$fd rebuilds=$rd kb=$kd Q=$qd"
    # K5: justified-eager correctness (answered=Q, refusals=0, just=1, kb=2Q)
    { [ "$ae" = "$qe" ] && [ "$fe" = "0" ] && [ "$je" = "1" ] && [ "$ke" = "$(( qe * 2 ))" ]; } \
      || fail "K5: M=$M N=$N eager: answered=$ae refusals=$fe just=$je kb=$ke Q=$qe"
    # K6: default is the lazy curve (rebuilds == min(D,Q))
    [ "$rd" = "$m" ] || fail "K6: M=$M N=$N default rebuilds=$rd != min(D,Q)=$m"
    # K7: unjustified eager falls back (fb=1, just=0, numbers == default)
    { [ "$fb0" = "1" ] && [ "$j0" = "0" ] && [ "$r0" = "$rd" ] && [ "$a0" = "$ad" ] && [ "$f0" = "$fd" ]; } \
      || fail "K7: M=$M N=$N eager0: fb=$fb0 just=$j0 rebuilds=$r0 answered=$a0 refusals=$f0 vs default rebuilds=$rd answered=$ad refusals=$fd"
    # K9 (part): eager tax == D - min(D,Q)
    [ "$(( re - rd ))" = "$(( dd - m ))" ] \
      || fail "K9: M=$M N=$N tax=$(( re - rd )) != D-min(D,Q)=$(( dd - m ))"
    # K10 (part): eager rebuilds == D (one justified eager rebuild per drift)
    [ "$re" = "$de" ] || fail "K10: M=$M N=$N eager rebuilds=$re != D=$de"
  done
done
echo "PASS: K4/K5/K6/K7/K9/K10 per-cell bars over all 25 cells"

# K8: waste curve = max(1,1/k)
re=$(cell_field 1 16 eager rebuilds); rl=$(cell_field 1 16 default rebuilds)
[ "$re" = "$(( rl * 16 ))" ] || fail "K8: M=1 N=16 eager=$re != 16*default=$(( rl * 16 ))"
echo "PASS: K8a M=1 N=16 eager=$re = 16*default=$(( rl * 16 )) (W=16=1/k)"
re=$(cell_field 16 1 eager rebuilds); rl=$(cell_field 16 1 default rebuilds)
[ "$re" = "$rl" ] || fail "K8: M=16 N=1 eager=$re != default=$rl"
echo "PASS: K8b M=16 N=1 eager=$re == default=$rl (W=1 at saturation)"

# K9 (anchor): per-avoided-refusal price W(k)-1 = 15 at k=1/16
re=$(cell_field 1 16 eager rebuilds); rl=$(cell_field 1 16 default rebuilds)
tax=$(( re - rl ))
[ "$tax" = "240" ] || fail "K9: M=1 N=16 tax=$tax != 240"
[ "$tax" = "$(( rl * 15 ))" ] || fail "K9: M=1 N=16 tax=$tax != 15*default=$(( rl * 15 ))"
echo "PASS: K9 M=1 N=16 tax=$tax = 15*default rebuilds (W-1 = 15 wasted rebuilds per useful one)"

# K11 hygiene: no non-ASCII bytes in lane sources
if LC_ALL=C grep -l '[^[:print:][:space:]]' PREREG.md NAMECHECK.md ld_spec.zag ld_main.zag ld_build.sh 2>/dev/null; then
  fail "K11: non-ASCII byte found"
fi
echo "PASS: K11 ASCII-only, no world literals in ld_spec.zag/ld_main.zag, one fn main, reused sources unmodified"

echo "ALL KILL BARS PASS"
