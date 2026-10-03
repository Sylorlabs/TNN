#!/bin/bash
# cs_posthoc.sh -- SPEC-COLD-START post-hoc analysis (NOT a bar
# re-adjudication). cs_build.sh already rendered the frozen verdict:
# BUILD-FAIL (K5 as written: sel=1 clause contradicted by the
# preregistered K7a flip on CS1). This script, run on the same frozen
# 3/3-byte-identical cs_run1.txt, (1) confirms the K5 quirk-core
# fields (commit-time; sel excluded), (2) evaluates K6/K7/K8 as
# "holds" checks, and (3) prints the finding tables for REPORT.md.
# It must not and does not move any frozen bar.
export PATH="$HOME/safebin"
set -u
D="$(cd "$(dirname "$0")" && pwd)"
cd "$D" || exit 1

field() {
  grep "^CELL R=$1 " cs_run1.txt | grep " P=$2 " | grep " L=$3 " \
    | grep -o " $4=[0-9-]*" | head -1 | cut -d= -f2
}
adapt_field() { field "$1" "adapt" "$2" "$3"; }
guard_field() { field "$1" "guard" "$2" "$3"; }
j_val() {
  rb=$(field "$1" "$2" "$3" rebuilds); rf=$(field "$1" "$2" "$3" refusals)
  echo $(( rb + rf * $3 ))
}
line_nop() {
  grep "^CELL R=$1 " cs_run1.txt | grep " P=$2 " | grep " L=$3 " | sed 's/ P=[a-z]*//'
}

echo "=== K5 quirk-core (commit-time fields; sel reported, not barred) ==="
for R in 21 60 82; do
  for L in 1 3 7; do
    tc=$(adapt_field $R $L tc); cm=$(adapt_field $R $L cm)
    sel=$(adapt_field $R $L sel); Dc=$(adapt_field $R $L Dc)
    Qc=$(adapt_field $R $L Qc)
    dh=$(adapt_field $R $L dh); dlo=$(adapt_field $R $L dlo)
    dhi=$(adapt_field $R $L dhi); pnum=$(adapt_field $R $L pnum)
    phin=$(adapt_field $R $L phin); phid=$(adapt_field $R $L phid)
    fl=$(adapt_field $R $L flips); tf1=$(adapt_field $R $L tf1)
    fdir=$(adapt_field $R $L fdir); rs=$(adapt_field $R $L rs)
    echo "adapt R=$R L=$L: tc=$tc cm=$cm sel=$sel Dc=$Dc Qc=$Qc dh=$dh dlo=$dlo dhi=$dhi pnum=$pnum phin=$phin phid=$phid flips=$fl tf1=$tf1 fdir=$fdir rs=$rs"
  done
done
echo "=== K5 L=0 clause (sel=0, cm!=2) ==="
for R in 21 60 82 120; do
  s0=$(adapt_field $R 0 sel); c0=$(adapt_field $R 0 cm); t0=$(adapt_field $R 0 tc)
  echo "adapt R=$R L=0: sel=$s0 cm=$c0 tc=$t0"
done

echo "=== K6a guard lines (tc/cm/sel/Dc) ==="
for R in 21 60 82; do
  for L in 1 3 7; do
    cm=$(guard_field $R $L cm); tc=$(guard_field $R $L tc)
    Dc=$(guard_field $R $L Dc); sel=$(guard_field $R $L sel)
    fl=$(guard_field $R $L flips)
    echo "guard R=$R L=$L: tc=$tc cm=$cm sel=$sel Dc=$Dc flips=$fl"
  done
done
echo "=== K6b L=0 identity ==="
for R in 21 60 82 120; do
  if [ "$(line_nop $R adapt 0)" = "$(line_nop $R guard 0)" ]; then echo "R=$R L=0: IDENTICAL"; else echo "R=$R L=0: DIFFER"; fi
done
echo "=== K6c CS3 identity ==="
for L in 0 1 3 7; do
  if [ "$(line_nop 120 adapt $L)" = "$(line_nop 120 guard $L)" ]; then echo "R=120 L=$L: IDENTICAL"; else echo "R=120 L=$L: DIFFER"; fi
done

echo "=== K7 economics: J=rb+rf*L per arm ==="
printf "%-8s %-4s %10s %10s %10s %10s\n" "cell" "L" "J_lazy" "J_eager" "J_adapt" "J_guard"
for R in 21 60 82 120; do
  for L in 0 1 3 7; do
    jl=$(j_val $R lazy -1); je=$(j_val $R eager -1)
    ja=$(j_val $R adapt $L); jg=$(j_val $R guard $L)
    printf "R=%-5s %-4s %10s %10s %10s %10s\n" "$R" "$L" "$jl" "$je" "$ja" "$jg"
  done
done

echo "=== K7a CS1 adapt flips ==="
for L in 0 1 3 7; do
  fl=$(adapt_field 60 $L flips); sel=$(adapt_field 60 $L sel)
  tf1=$(adapt_field 60 $L tf1); fdir=$(adapt_field 60 $L fdir); tf2=$(adapt_field 60 $L tf2)
  echo "adapt R=60 L=$L: flips=$fl sel=$sel tf1=$tf1 fdir=$fdir tf2=$tf2"
done
echo "=== CS1 guard flips (did the guard need rescue?) ==="
for L in 0 1 3 7; do
  fl=$(guard_field 60 $L flips); sel=$(guard_field 60 $L sel); cm=$(guard_field 60 $L cm)
  echo "guard R=60 L=$L: flips=$fl sel=$sel cm=$cm"
done
echo "=== CS2/CS0 adapt flips ==="
for R in 82 21; do
  for L in 1 3 7; do
    fl=$(adapt_field $R $L flips); sel=$(adapt_field $R $L sel); cm=$(adapt_field $R $L cm)
    echo "adapt R=$R L=$L: flips=$fl sel=$sel cm=$cm"
  done
done
echo "=== K8 ASCII check ==="
if LC_ALL=C grep -l '[^[:print:][:space:]]' PREREG.md NAMECHECK.md cs_spec.zag cs_main.zag cs_build.sh cs_posthoc.sh probe.zag 2>/dev/null; then
  echo "non-ASCII found"
else
  echo "ASCII clean"
fi
echo "=== no 901/902 in new sources ==="
grep -l "901\|902" cs_spec.zag cs_main.zag probe.zag 2>/dev/null || echo "clean"
echo "=== one fn main in cs_full.zag ==="
grep -c '^fn main(' cs_full.zag
echo "=== reused sources unmodified ==="
for f in ../disagreement_attribution/da_base.zag ../disagreement_attribution/da_module.zag ../disagreement_attribution/da_learn.zag ../spec_relationblind/rb_world.zag ../spec_relationblind/rb_fix.zag ../spec_epochtag/et_world.zag ../spec_epochtag/et_spec.zag ../spec_refusal_recovery/rr_spec.zag ../spec_lazy_default/ld_spec.zag ../spec_abstention_trap/at_spec.zag; do
  /usr/bin/git diff --quiet -- "$f" && echo "OK $f" || echo "MODIFIED $f"
done
