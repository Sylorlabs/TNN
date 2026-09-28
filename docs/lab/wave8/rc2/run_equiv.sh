#!/usr/bin/env bash
# RC2 equivalence proof (prereg amendment 2026-09-20 (2)).
# The 1/10 mini variant (12/12/4, IL budget ~= 80 <= 128) is compiled twice:
#   build A against the canonical 128-cap checker (wave4 il_core.zag)
#   build B against the leg-local 1024-cap checker (il_core_rc2.zag)
# The two builds' check verdicts must be byte-identical: the only behavioral
# difference between the caps is then unreachable in a valid run.
# Non-identity here STOPS the trial (amendment law).
set -u
BASE="$(cd "$(dirname "$0")" && pwd)"
ZNC="${1:-${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}}"
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
E="$BASE/EVIDENCE_EQUIV_$STAMP"
mkdir -p "$E"

# No-RNG check on both sources (fail-closed).
if sed 's|//.*||' "$BASE/rc2_mini.zag" "$BASE/il_core_rc2.zag" | grep -niE '\brng\b|\brand\b|srand|rand\(\)|random' >"$E/rng_grep.txt" 2>&1; then
  echo "RNG CHECK FAILED:"; cat "$E/rng_grep.txt"; exit 1
fi
echo "rng_check=clean"

run_build() {
  local tag="$1" checker="$2"
  cp "$checker" "$BASE/il_core_mini.zag"
  "$ZNC" "$BASE/rc2_mini.zag" --no-zagd --no-analyze --no-foreground-cache -o "$BASE/mini_${tag}_linux" \
    >"$E/compile_${tag}.stdout" 2>"$E/compile_${tag}.stderr" || { echo "COMPILE FAILED ($tag)"; tail -20 "$E/compile_${tag}.stderr"; exit 1; }
  "$BASE/mini_${tag}_linux" >"$E/mini_${tag}_run1.stdout" 2>"$E/mini_${tag}_run1.stderr" || { echo "RUN FAILED ($tag run1)"; exit 1; }
  "$BASE/mini_${tag}_linux" >"$E/mini_${tag}_run2.stdout" 2>"$E/mini_${tag}_run2.stderr" || { echo "RUN FAILED ($tag run2)"; exit 1; }
  h1=$(sha256sum "$E/mini_${tag}_run1.stdout" | cut -d' ' -f1)
  h2=$(sha256sum "$E/mini_${tag}_run2.stdout" | cut -d' ' -f1)
  if [ "$h1" != "$h2" ]; then echo "NONDETERMINISM within build $tag"; exit 1; fi
  echo "build_${tag}_self_identical=$h1"
  # the mini must also pass its own 40 checks (a valid trial, not just a diff fixture)
  bad=0; total=0
  while IFS=, read -r tag2 name actual expected; do
    total=$((total+1))
    if [ "$actual" != "$expected" ]; then echo "MISMATCH($tag): $name actual=$actual expected=$expected"; bad=$((bad+1)); fi
  done < <(grep '^CL_CHECK,' "$E/mini_${tag}_run1.stdout")
  echo "build_${tag}_checks_total=$total checks_bad=$bad"
  if [ "$total" -ne 40 ] || [ "$bad" -ne 0 ]; then echo "MINI TRIAL FAILED ($tag)"; exit 1; fi
}

run_build "cap128"  "$BASE/../../wave4/integrity-ledger/il_core.zag"
run_build "cap1024" "$BASE/il_core_rc2.zag"

if cmp -s "$E/mini_cap128_run1.stdout" "$E/mini_cap1024_run1.stdout"; then
  echo "EQUIVALENCE PROOF: PASS — byte-identical verdicts under IL_CAP=128 and IL_CAP=1024"
else
  echo "EQUIVALENCE PROOF: FAIL — outputs differ; trial STOPPED per amendment law"
  diff "$E/mini_cap128_run1.stdout" "$E/mini_cap1024_run1.stdout" | head -20
  exit 1
fi
rm -f "$BASE/il_core_mini.zag" "$BASE"/mini_*_linux
echo "equiv_evidence=$E"
