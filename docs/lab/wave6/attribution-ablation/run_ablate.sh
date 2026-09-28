#!/bin/bash
# run_ablate.sh — Wave-6 Investigation 1 (attribution-ablation) runner.
# Preregistered nine-arm ablation sweep over the real scaffold-release
# learner (PREREG_ABLATION.md, frozen before this script ran).
# Native on this Linux VM. Fails closed on any gate. Usage: ./run_ablate.sh
set -u
cd "$(dirname "$0")"
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
SRC=ablate.zag
BIN=ablate.bin
LOGDIR=logs
mkdir -p "$LOGDIR"

fail(){ echo "GATE_FAIL: $1" | tee -a "$LOGDIR/run.log"; exit 1; }
pass(){ echo "GATE_PASS: $1" | tee -a "$LOGDIR/run.log"; }
: > "$LOGDIR/run.log"

# --- Gate 0: toolchain present ---
[ -x "$ZNC" ] || fail "compiler missing: $ZNC"
"$ZNC" --version >> "$LOGDIR/run.log" 2>&1 || true

# --- Gate 1: substrates unmodified (prereg §12 hashes) ---
SR=~/workspace/tnn-lab/wave4/scaffold-release/sr.zag
IL=~/workspace/tnn-lab/wave4/integrity-ledger/il_core.zag
SRH=$(sha256sum "$SR" | cut -d' ' -f1)
ILH=$(sha256sum "$IL" | cut -d' ' -f1)
[ "$SRH" = "24a61ed672dd2b47a21543729d634306d33fc877302855ec127d29372bbd1e5d" ] \
  || fail "sr.zag modified: $SRH"
[ "$ILH" = "4b723b65a4808bc3896b6afe5f9b903648a4c1564301092ca0462d62f440b325" ] \
  || fail "il_core.zag modified: $ILH"
pass "imported substrates match prereg hashes"
# ablation source hash (authored in this study, recorded for reproducibility)
NOHSH=$(sha256sum sr_nohs.zag | cut -d' ' -f1)
echo "sr_nohs.zag sha256: $NOHSH" | tee -a "$LOGDIR/run.log"
ABLATESH=$(sha256sum "$SRC" | cut -d' ' -f1)
echo "ablate.zag sha256: $ABLATESH" | tee -a "$LOGDIR/run.log"

# --- Gate 2: no RNG tokens anywhere in AI decision paths (comments stripped) ---
for F in "$SRC" sr_nohs.zag; do
  sed 's|//.*||' "$F" | grep -nEi 'rand|srand|random|entropy|/dev/urandom|getrandom|rdtsc|time\(|clock\(' \
    && fail "RNG token found in $F" || true
done
pass "no RNG tokens in $SRC / sr_nohs.zag"

# --- Gate 3: claims-channel isolation — clmk/prefa/mon never referenced
# --- inside the learner region (the learner must not see claims); and the
# --- ablated learner module must not reference them at all ---
python3 - "$SRC" <<'EOF'
import sys
src = open(sys.argv[1]).read()
b = src.index('// ABL-LEARNER-BEGIN')
e = src.index('// ABL-LEARNER-END')
region = '\n'.join(l.split('//')[0] for l in src[b:e].split('\n'))
bad = [t for t in ('clmk', 'prefa', 'mon', 'claims_arena', 'claim_kind') if t in region]
if bad:
    print('CLAIMS LEAK INTO LEARNER REGION:', bad); sys.exit(1)
print('claims channel isolated from learner region')
EOF
[ $? -eq 0 ] || fail "claims channel leaks into learner region"
pass "claims channel isolated from learner region"
python3 - sr_nohs.zag <<'EOF'
src = open('sr_nohs.zag').read()
code = '\n'.join(l.split('//')[0] for l in src.split('\n'))
bad = [t for t in ('clmk', 'prefa', 'mon', 'claim_kind') if t in code]
if bad:
    print('CLAIMS LEAK INTO sr_nohs.zag:', bad); raise SystemExit(1)
print('sr_nohs.zag references no claims channel')
EOF
[ $? -eq 0 ] || fail "claims channel leaks into sr_nohs.zag"
pass "sr_nohs.zag references no claims channel"

# --- Gate 4: compile (native, same flags as the wave-4 substrates) ---
"$ZNC" "$SRC" -O3 -o "$BIN" > "$LOGDIR/compile.log" 2>&1 \
  || { tail -40 "$LOGDIR/compile.log"; fail "compile failed"; }
pass "compiled: $BIN"
[ -x "$BIN" ] || fail "binary not executable"

# --- Gate 5: two runs, byte-identical output ---
"./$BIN" > "$LOGDIR/run1.log" 2>&1; R1=$?
"./$BIN" > "$LOGDIR/run2.log" 2>&1; R2=$?
[ $R1 -eq 0 ] || fail "run 1 exited $R1"
[ $R2 -eq 0 ] || fail "run 2 exited $R2"
H1=$(sha256sum "$LOGDIR/run1.log" | cut -d' ' -f1)
H2=$(sha256sum "$LOGDIR/run2.log" | cut -d' ' -f1)
[ "$H1" = "$H2" ] || fail "runs differ: $H1 vs $H2"
pass "byte-identical reruns: sha256 $H1"

# --- Gate 6: every ABL_CHECK line actual==expected; ABL_FAILURES,0 ---
python3 - "$LOGDIR/run1.log" <<'EOF'
import sys, re
n = 0; bad = []
fails = None
for line in open(sys.argv[1]):
    m = re.match(r'ABL_CHECK,([^,]+),(-?\d+),(-?\d+)\s*$', line)
    if m:
        n += 1
        name, actual, expected = m.group(1), int(m.group(2)), int(m.group(3))
        if actual != expected:
            bad.append((name, actual, expected))
    m2 = re.match(r'ABL_FAILURES,(-?\d+)\s*$', line)
    if m2:
        fails = int(m2.group(1))
print('checks parsed:', n)
for name, a, e in bad:
    print('CHECK_FAIL:', name, 'actual', a, 'expected', e)
if fails is None:
    print('MISSING ABL_FAILURES'); sys.exit(1)
print('ABL_FAILURES =', fails)
if bad or fails != 0:
    sys.exit(1)
print('all', n, 'checks hold')
EOF
[ $? -eq 0 ] || fail "check validation failed (see above)"
pass "all ABL_CHECK lines hold, ABL_FAILURES,0"

# --- summary excerpts for the report ---
echo "--- judge verdicts ---" | tee -a "$LOGDIR/run.log"
grep '^ABL_JUDGE' "$LOGDIR/run1.log" | tee -a "$LOGDIR/run.log"
echo "--- IL gate verdicts ---" | tee -a "$LOGDIR/run.log"
grep '^ABL_IL' "$LOGDIR/run1.log" | tee -a "$LOGDIR/run.log"
echo "--- branch decisions ---" | tee -a "$LOGDIR/run.log"
grep '^ABL_BRANCH' "$LOGDIR/run1.log" | tee -a "$LOGDIR/run.log"
echo "ALL GATES PASSED" | tee -a "$LOGDIR/run.log"
