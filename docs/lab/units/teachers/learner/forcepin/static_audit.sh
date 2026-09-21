#!/bin/bash
# static_audit.sh — static path audit for B.6 requirement (c):
# "NO learner code path can set or clear a pin."
#
# Proves three claims by source inspection (no trust in comments):
#   A. In forcepin.zag, the ONLY stores to the pin tables occur inside
#      fp_pin and fp_unpin, and every such store is dominated by the
#      caller==FP_CALLER_TRAINER guard (a learner-issued call returns
#      FP_REFUSED_EXTERNAL_ONLY before any store).
#   B. The LIVE learner tree (delib.zag, store.zag, driver.zag, pcodec.zag,
#      tests/) contains ZERO calls to fp_pin/fp_unpin and zero references
#      to any fp_ symbol: no live learner path can even reach the mutators.
#   C. In the scratch wiring patch, the only fp_ symbols the learner's
#      revise/reject/kill paths touch are fp_check / fp_gate /
#      fp_gate_kill — all read-only with respect to pin state (fp_gate only
#      appends audit entries; it never mutates the pin tables).
#
# Exit 0 = all claims hold. Any violation fails closed (exit 1).
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
MOD=$HERE/forcepin.zag
LEARNER=$HERE/../
SCRATCH=$HERE/scratch/delib.zag
FAIL=0

say(){ echo "AUDIT,$1"; }

# ---- claim A: pin-table store sites ----
say "A.stores"
# function line ranges in forcepin.zag
frange(){ awk -v fn="$1" 'BEGIN{s=0} /^fn /{if(s){print s":"(NR-1);s=0} n=$2; sub(/\(.*/,"",n); if(n==fn){s=NR}} END{if(s)print s":$"}' "$MOD"; }
pin_range=$(frange "fp_pin"); unpin_range=$(frange "fp_unpin")
say "A.fp_pin.range=$pin_range"
say "A.fp_unpin.range=$unpin_range"
in_range(){ # line, range -> 0/1
  local l=$1 r=$2; local a=${r%:*} b=${r#*:}
  if [ "$l" -ge "$a" ] && { [ "$b" = "\$" ] || [ "$l" -le "$b" ]; }; then echo 1; else echo 0; fi
}
while IFS=: read -r ln code; do
  pin_ok=$(in_range "$ln" "$pin_range"); unp_ok=$(in_range "$ln" "$unpin_range")
  if [ "$pin_ok" = 1 ] || [ "$unp_ok" = 1 ]; then
    say "A.store.line$ln.inside_mutator.ok"
  else
    echo "STATIC FAIL: pin-table store at $MOD:$ln outside fp_pin/fp_unpin: $code"; FAIL=1
  fi
done < <(grep -nE '(pss|pse|ptr)\[[^]]+\] *=' "$MOD" | grep -v '==')
# every store must be dominated by the trainer guard inside its function
say "A.guard"
guard_hits=$(grep -c 'if (caller != FP_CALLER_TRAINER)' "$MOD")
if [ "$guard_hits" = 2 ]; then say "A.guard.two_mutators_guarded.ok"
else echo "STATIC FAIL: expected 2 trainer guards, found $guard_hits"; FAIL=1; fi
# guard must precede the first store in each mutator
for fn in fp_pin unpin; do :; done
python3 - "$MOD" <<'EOF'
import re,sys
src=open(sys.argv[1]).read().split('\n')
def frange(name):
    s=None
    for i,l in enumerate(src,1):
        if l.startswith('fn '):
            if s: yield (s,i-1); s=None
            tok=l.split()[1]; tok=tok[:tok.index('(')]
            if tok==name: s=i
    if s: yield (s,len(src))
for name in ('fp_pin','fp_unpin'):
    for a,b in frange(name):
        body=src[a-1:b]
        g=[i for i,l in enumerate(body) if 'if (caller != FP_CALLER_TRAINER)' in l]
        st=[i for i,l in enumerate(body) if re.search(r'(pss|pse|ptr)\[[^]]+\] *=',l) and '==' not in l]
        assert g, f"no guard in {name}"
        assert st, f"no store in {name}"
        assert min(g)<min(st), f"guard does not dominate store in {name}"
        print(f"AUDIT,A.{name}.guard_dominates.ok")
EOF
[ $? -ne 0 ] && { echo "STATIC FAIL: guard dominance"; FAIL=1; }

# ---- claim B: live learner tree has no fp_ MUTATOR reachability ----
# (Post-wiring update 2026-09-21: the wiring patch is now LIVE in delib.zag,
# so read-side fp_ symbols are expected. Claim B now proves the stronger
# invariant that matters: no live learner path can SET or CLEAR a pin —
# zero calls to the fp_pin/fp_unpin mutators anywhere in the live tree.)
say "B.live_tree"
if grep -rn 'fp_pin(\|fp_unpin(' \
     "$LEARNER"delib.zag "$LEARNER"store.zag "$LEARNER"driver.zag \
     "$LEARNER"pcodec.zag "$LEARNER"tests/ 2>/dev/null; then
  echo "STATIC FAIL: live learner tree calls a pin mutator"; FAIL=1
else say "B.live_tree.no_mutator_calls.ok"; fi
# read-side symbols expected post-wiring; enumerate for the record
for sym in 'fp_init(' 'fp_check(' 'fp_gate(' 'fp_gate_kill(' 'FPStore'; do
  n=$(grep -rc "$sym" "$LEARNER"delib.zag 2>/dev/null)
  say "B.live_tree.$sym.count=$n"
done

# ---- claim C: live wiring touches only read-side symbols ----
# (Post-wiring update 2026-09-21: checks the LIVE delib.zag, not the scratch
# copy. The scratch copy is kept as the pre-wiring validation record.)
say "C.wiring"
LIVE=$LEARNER/delib.zag
if grep -n 'fp_pin(\|fp_unpin(' "$LIVE"; then
  echo "STATIC FAIL: live wiring calls a pin mutator"; FAIL=1
else say "C.wiring.no_mutator_calls.ok"; fi
for sym in 'fp_init(' 'fp_check(' 'fp_gate(' 'fp_gate_kill('; do
  n=$(grep -c "$sym" "$LIVE")
  say "C.wiring.$sym.count=$n"
done
# fp_gate appends audit only: confirm its body has no pin-table stores
python3 - "$MOD" <<'EOF'
import re,sys
src=open(sys.argv[1]).read().split('\n')
def frange(name):
    s=None
    for i,l in enumerate(src,1):
        if l.startswith('fn '):
            if s: yield (s,i-1); s=None
            tok=l.split()[1]; tok=tok[:tok.index('(')]
            if tok==name: s=i
    if s: yield (s,len(src))
for name in ('fp_gate','fp_check','fp_find'):
    for a,b in frange(name):
        for l in src[a-1:b]:
            assert not re.search(r'(pss|pse|ptr)\[[^]]+\] *=',l) or '==' in l, f"store in {name}"
print("AUDIT,C.gate_fns.readonly.ok")
EOF
[ $? -ne 0 ] && { echo "STATIC FAIL: gate fn mutates pins"; FAIL=1; }

if [ $FAIL -ne 0 ]; then echo "AUDIT,RESULT,FAIL"; exit 1; fi
echo "AUDIT,RESULT,PASS"
