#!/bin/bash
# run_verify.sh — W6 §C tripwire verification runner.
# 1. static no-RNG / no-wallclock scan (comments stripped first)
# 2. compiles tw_verify.zag to a temp binary
# 3. runs it 5x; outputs must be byte-identical (no-RNG law)
# 4. every CL_CHECK must have actual==expected
# 5. TWV_FAILURES,0 and exit code 0
# 6. writes canonical output + sha256 into the evidence dir
# Exits nonzero on any failure.
set -u
DIR="$(cd "$(dirname "$0")" && pwd)"
ZNC="$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1"
BIN="$(mktemp /tmp/tw_verify_bin.XXXXXX)"
OUTS=""
fail=0
say(){ echo "TWV: $*"; }
die(){ say "FAIL: $*"; fail=1; }

# ---- 1. static scans ----
say "static no-RNG / no-wallclock scan"
hits="$(for f in "$DIR"/tw_verify.zag "$DIR"/../tb_tripwire.zag; do sed 's|//.*||' "$f"; done | grep -inE 'rand|srand|random|_zag_time|wallclock|gettime|clock_gettime|rdtsc|/dev/urandom|[^a-z_]seed[^a-z_]' || true)"
if [ -n "$hits" ]; then die "forbidden token found: $hits"; else say "clean"; fi

# ---- 2. compile ----
say "compiling"
if ! "$ZNC" "$DIR/tw_verify.zag" --no-zagd --no-analyze --no-foreground-cache -o "$BIN" > /tmp/tw_verify_compile.log 2>&1; then
  die "compile failed"; cat /tmp/tw_verify_compile.log; rm -f "$BIN"; exit 1
fi
say "compiled ok"

# ---- 3. run 5x, byte-identical ----
say "running 5x"
prev=""
for r in 1 2 3 4 5; do
  o="$(mktemp /tmp/tw_verify_out.XXXXXX)"
  "$BIN" > "$o" 2>&1; c=$?
  [ "$c" = 0 ] || die "run$r exit=$c"
  OUTS="$OUTS $o"
  if [ -n "$prev" ]; then cmp -s "$prev" "$o" || die "run$r differs from run1"; fi
  prev="$o"
done
say "byte-identical across 5 runs"

# ---- 4. CL_CHECK actual==expected ----
first="$(echo "$OUTS" | awk '{print $1}')"
bad="$(awk -F, '/^CL_CHECK/{if($3!=$4) print}' "$first" || true)"
nchk="$(grep -c '^CL_CHECK' "$first")"
if [ -n "$bad" ]; then die "CL_CHECK mismatches: $bad"; else say "CL_CHECK $nchk/$nchk actual==expected"; fi

# ---- 5. TWV_FAILURES,0 ----
if ! grep -qxF "TWV_FAILURES,0" "$first"; then die "TWV_FAILURES nonzero"; else say "TWV_FAILURES,0"; fi

# ---- 6. canonical evidence ----
cp "$first" "$DIR/tw_verify.out"
sha256sum "$first" | awk '{print $1}' > "$DIR/tw_verify.out.sha256"
say "canonical output: $DIR/tw_verify.out sha256=$(cat "$DIR/tw_verify.out.sha256")"
grep '^TWV,' "$first" > "$DIR/tw_verify_twv.csv"

rm -f "$BIN" $OUTS
if [ "$fail" = 0 ]; then say "TRIPWIRE VERIFICATION PASS"; else say "TRIPWIRE VERIFICATION FAIL"; fi
exit "$fail"
