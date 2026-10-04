#!/usr/bin/env bash
# R0 ARMS M8 smoke: byte-identical reruns (N=5) + adversarial perturbations,
# round-trip tiling check, per arm x input. Pure bash + python3 for checks.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
BIN="$HERE/arms_bin"
ZNC="${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}"
# NOTE: scratch lives under the arms dir (not /tmp) — /tmp is a 512M tmpfs
# shared with other crews and filled mid-run once (ENOSPC truncated outputs).
OUT="$HERE/smoke_out"; mkdir -p "$OUT"
fail=0
log="$OUT/SMOKE_M8.log"; : > "$log"

note(){ echo "$*" | tee -a "$log"; }
die(){ note "FAIL: $*"; fail=$((fail+1)); }

# ---- rebuild from source (freshness: binary must match current .zag) ----
"$ZNC" "$HERE/arms.zag" --no-zagd --no-analyze --no-foreground-cache -o "$BIN" >>"$log" 2>&1 \
  || { die "compile failed"; tail -5 "$log"; exit 1; }
note "compile: OK"

# ---- test vectors (deterministic, fixed) ----
printf '' > "$OUT/t0.bin"
printf 'Q' > "$OUT/t1b.bin"
printf 'the quick brown fox jumps over the lazy dog. the quick brown fox jumps! 0123456789 abcabcabc' > "$OUT/t2.bin"
python3 -c "open('$OUT/t3.bin','wb').write(b'ab'*200 + b'xy'*50 + b'ab'*200)"
python3 -c "
d=b'int main(){int x=0;for(int i=0;i<10;i++){x+=i;}return x;}'
open('$OUT/t4.bin','wb').write(d*40 + b'// comment '*30)"
python3 -c "
import hashlib
h=int(hashlib.sha256(b'seed-r0-smoke').hexdigest(),16)
out=bytearray()
for i in range(65536):
    h=(h*6364136223846793005+1442695040888963407)%(2**64)
    out.append((h>>33)%256)
open('$OUT/t5.bin','wb').write(bytes(out))"
# t6: highly repetitive -> exercises inventory/motif paths hard
python3 -c "open('$OUT/t6.bin','wb').write((b'the cat sat on the mat. '*500 + b'0123456789'*200))"

ARMS="predictive_surprise fixed_window_4 fixed_window_8 fixed_window_16 fixed_window_64 adaptive_mdl grounded_adaptive_mdl hierarchical_mdl raw_micro random_chunks"
INPUTS="t0 t1b t2 t3 t4 t5 t6"

# ---- round-trip + determinism ----
for a in $ARMS; do
  for t in $INPUTS; do
    f="$OUT/$t.bin"; n=$(stat -c%s "$f")
    # N=5 plain runs + 3 perturbation modes
    for run in 1 2 3 4 5; do "$BIN" "$a" < "$f" > "$OUT/o_${a}_${t}_r$run.txt" 2>"$OUT/e_${a}_${t}_r$run.txt" || die "$a/$t run$run exit=$?"; done
    for p in perturb1 perturb2 perturb3; do "$BIN" "$a" "$p" < "$f" > "$OUT/o_${a}_${t}_$p.txt" 2>"$OUT/e_${a}_${t}_$p.txt" || die "$a/$t $p exit=$?"; done
    base=$(sha256sum "$OUT/o_${a}_${t}_r1.txt" | cut -d' ' -f1)
    for run in 2 3 4 5; do
      h=$(sha256sum "$OUT/o_${a}_${t}_r$run.txt" | cut -d' ' -f1)
      [ "$h" = "$base" ] || die "$a/$t run$run differs (M8 N=5)"
    done
    for p in perturb1 perturb2 perturb3; do
      h=$(sha256sum "$OUT/o_${a}_${t}_$p.txt" | cut -d' ' -f1)
      [ "$h" = "$base" ] || die "$a/$t $p differs (M8 perturbation)"
    done
    # stderr must be empty on success (no nondeterministic chatter)
    for run in 1 2 3 4 5 perturb1 perturb2 perturb3; do
      [ -s "$OUT/e_${a}_${t}_$run.txt" ] && die "$a/$t $run stderr non-empty: $(head -c200 "$OUT/e_${a}_${t}_$run.txt")"
    done
    # round-trip tiling check
    python3 - "$OUT/o_${a}_${t}_r1.txt" "$n" "$a" "$t" <<'EOF'
import sys
path, n, arm, t = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
hdr=None; segs=[]; end=None; meta=0
for line in open(path):
    line=line.rstrip("\n")
    if line.startswith("ARMS "): hdr=line
    elif line.startswith("META "): meta+=1
    elif line.startswith("SEG "):
        _, s, l, i, k = line.split(" "); segs.append((int(s),int(l),int(i),k))
    elif line.startswith("END "): end=line
    else: print(f"BADLINE {arm}/{t}: {line}"); sys.exit(1)
assert hdr==f"ARMS v=1 arm={arm} n={n}", f"header mismatch {arm}/{t}: {hdr}"
exp=0
for (s,l,i,k) in segs:
    assert s==exp, f"gap/overlap {arm}/{t}: seg at {s}, expected {exp}"
    assert l>=1, f"empty seg {arm}/{t}"
    exp+=l
assert exp==n, f"coverage {arm}/{t}: {exp} != {n}"
assert end==f"END chunks={len(segs)}", f"trailer mismatch {arm}/{t}: {end}"
if arm=="random_chunks": assert meta==1, f"missing META analog label {t}"
print(f"OK {arm}/{t}: {len(segs)} segs, {n} bytes")
EOF
    [ $? -eq 0 ] || die "$a/$t round-trip check failed"
  done
done

# ---- ASLR-equivalent: setarch -R run must match ----
if command -v setarch >/dev/null 2>&1; then
  for a in predictive_surprise adaptive_mdl hierarchical_mdl raw_micro random_chunks fixed_window_4; do
    "$BIN" "$a" < "$OUT/t6.bin" > "$OUT/o_aslr_base.txt" 2>/dev/null
    setarch "$(uname -m)" -R "$BIN" "$a" < "$OUT/t6.bin" > "$OUT/o_aslr_nor.txt" 2>/dev/null
    cmp -s "$OUT/o_aslr_base.txt" "$OUT/o_aslr_nor.txt" || die "$a ASLR-disabled run differs"
  done
  note "aslr-check: OK (setarch -R identical)"
else
  note "aslr-check: SKIPPED (no setarch)"
fi

# ---- no clock/entropy/syscall reads in source (canary audit) ----
if grep -nE "_zag_raw_syscall\((39|98|107|318|355)|getpid|clock_gettime|getrandom|/dev/urandom|_zag_time|_zag_rand" "$HERE/arms.zag" | grep -v "^.*://" >/dev/null; then
  die "canary: source references clock/entropy/pid"
else
  note "canary-check: OK (no clock/entropy/pid references in arms.zag)"
fi

# ---- summary table ----
note ""
note "=== per-arm segment counts on t6 (19.7KB repetitive; informational) ==="
for a in $ARMS; do
  c=$(grep -c "^SEG " "$OUT/o_${a}_t6_r1.txt")
  kinds=$(grep "^SEG " "$OUT/o_${a}_t6_r1.txt" | awk '{print $5}' | sort | uniq -c | tr '\n' ' ')
  note "$a: chunks=$c kinds: $kinds"
done

if [ $fail -eq 0 ]; then note ""; note "M8-SMOKE: PASS (all arms x inputs byte-identical across N=5 + 3 perturbations; round-trip tiling holds)"; else note ""; note "M8-SMOKE: FAIL ($fail failures)"; fi
exit $fail
