#!/bin/bash
# cf_probe.sh -- TEST WHETHER "PLAN ORDER" IS NONDETERMINISTIC (mission item 3).
#
# Q1. From BYTE-IDENTICAL source (the 6-file corefreeze concatenation, hashed
#     once), build N times and compare binary sha256 + porder fields.
# Q2. From LOGICALLY IDENTICAL but BYTE-DIFFERENT source (same 6 files,
#     concatenated in a different order), build and compare. This is the
#     "logically identical source" phrasing in the corefreeze report; if plan
#     order moves HERE and not in Q1, the observation is a source-state
#     difference, not build instability.
# Q3. Byte-offset trap audit: does the harness call get32/set32 with a CELL
#     index instead of a byte offset? (B16 closed as an API trap.)
# Q4. []u8 as *u8 audit (B17). If present, run-to-run nondeterminism would be
#     B17 and not build instability.
#
# Every binary execution goes through tnnwatch.sh reg.

set -u
BD=/Users/Shared/micah/Documents/TNN/.worktrees/buildstab/docs/lab/research-lead/overnight-20260928/buildstab
ZNC=/Users/Shared/micah/Documents/TNN/.bin/znc
W=/Users/Shared/micah/Documents/TNN/TNN/tools/tnnwatch.sh
CP="$BD/cfprobe"
R=/Users/Shared/micah/Documents/TNN/.bt/cfprobe
rm -rf "$R"; mkdir -p "$R"
. /Users/Shared/micah/Documents/TNN/.env/pure-zag.sh

FLAGS="--no-zagd --no-analyze --no-foreground-cache"
N=5

# ---------------------------------------------------------------- Q3 / Q4 ----
echo "== Q3 get32/set32 definition (byte offsets?) =="
grep -n -A3 "^fn get32" "$CP/cf_full.zag" | head -8
echo "== Q4 []u8 as *u8 occurrences in harness =="
if grep -n "\[\]u8 as \*u8" "$CP/cf_full.zag"; then echo "  B17 FORM PRESENT"; else echo "  NONE -- B17 does NOT apply to this harness"; fi
echo "== every 'as *u8' operand in harness =="
grep -o "[A-Za-z_0-9]* as \*u8" "$CP/cf_full.zag" | sort | uniq -c

# ---------------------------------------------------------------- Q1 ---------
echo "== Q1 N=$N builds from BYTE-IDENTICAL source =="
SRC_SHA=$(shasum -a 256 "$CP/cf_full.zag" | cut -d' ' -f1)
echo "  src_sha=$SRC_SHA"
D1=""; NDISTINCT=0; declare -a SEEN=()
for i in $(seq 1 $N); do
  rm -f "$R/cf"; rm -rf "$R/.zag-cache"
  "$ZNC" --target macos-arm64 $FLAGS "$CP/cf_full.zag" -o "$R/cf" > "$R/cf.compile.$i.txt" 2>&1
  rc=$?
  B=$(shasum -a 256 "$R/cf" | cut -d' ' -f1)
  "$W" reg "cf_b${i}_r1" 600 "$R/cf" > "$R/cf.run.$i.1.txt" 2>/dev/null
  O=$(shasum -a 256 "$R/cf.run.$i.1.txt" | cut -d' ' -f1)
  OB=$(wc -c < "$R/cf.run.$i.1.txt" | tr -d ' ')
  # porder multiset, extracted by grep
  P=$(grep -o "porder=[0-9:,]*" "$R/cf.run.$i.1.txt" | shasum -a 256 | cut -d' ' -f1)
  PORDERS=$(grep -o "porder=[0-9:,]*" "$R/cf.run.$i.1.txt" | sort -u | tr '\n' ' ')
  echo "  b$i rc=$rc bin_sha=${B:0:16} out_sha=${O:0:16} out_bytes=$OB porder_lines_sha=${P:0:12}"
  [ -z "$D1" ] && D1=$B
  [ "$B" = "$D1" ] || echo "  *** BUILD-TO-BUILD BINARY DIFFERENCE at build $i"
  hit=0; for s in "${SEEN[@]:-}"; do [ "$s" = "$B" ] && hit=1; done
  if [ "$hit" = "0" ]; then NDISTINCT=$((NDISTINCT+1)); SEEN+=("$B"); fi
  echo "  b$i porder_set: $PORDERS"
  # 3 runs of this binary
  for r in 2 3; do "$W" reg "cf_b${i}_r${r}" 600 "$R/cf" > "$R/cf.run.$i.$r.txt" 2>/dev/null; done
  cmp -s "$R/cf.run.$i.1.txt" "$R/cf.run.$i.2.txt" && cmp -s "$R/cf.run.$i.1.txt" "$R/cf.run.$i.3.txt" \
    && echo "  b$i run 3/3 byte-identical" || echo "  *** RUN-TO-RUN DIFFERENCE at build $i"
done
echo "Q1_RESULT byte_identical_source_N=$N DISTINCT_BIN_SHA=$NDISTINCT ref=$D1"

# ---------------------------------------------------------------- Q2 ---------
echo "== Q2 LOGICALLY IDENTICAL, BYTE-DIFFERENT source (swapped concatenation order) =="
CF=/Users/Shared/micah/Documents/TNN/.worktrees/corefreeze/docs/lab/research-lead/overnight-20260928/corefreeze
RR=/Users/Shared/micah/Documents/TNN/TNN/docs/lab/research-lead/overnight-20260928
cat "$CF/cf_base.zag" "$CF/cf_engine.zag" "$CF/cf_data.zag" \
    "$RR/hook_phase1/hq_module.zag" "$RR/cogops_learnosc2/c8_learn.zag" > "$CP/cf_perm.zag"
echo "  perm_src_sha=$(shasum -a 256 "$CP/cf_perm.zag" | cut -d' ' -f1)"
echo "  base_src_sha=$SRC_SHA"
rm -f "$R/cfp"; rm -rf "$R/.zag-cache"
"$ZNC" --target macos-arm64 $FLAGS "$CP/cf_perm.zag" -o "$R/cfp" > "$R/cfp.compile.txt" 2>&1
echo "  perm compile rc=$? msg=$(head -2 "$R/cfp.compile.txt" | tr '\n' ' ')"
if [ -x "$R/cfp" ]; then
  echo "  perm_bin_sha=$(shasum -a 256 "$R/cfp" | cut -d' ' -f1)"
  "$W" reg cf_perm 600 "$R/cfp" > "$R/cfp.run.txt" 2>/dev/null
  echo "  perm_out_sha=$(shasum -a 256 "$R/cfp.run.txt" | cut -d' ' -f1) bytes=$(wc -c < "$R/cfp.run.txt" | tr -d ' ')"
fi

echo "== Q2b same 6 files, whitespace-only difference (trailing newline appended) =="
cp "$CP/cf_full.zag" "$CP/cf_nl.zag"; printf '\n' >> "$CP/cf_nl.zag"
echo "  nl_src_sha=$(shasum -a 256 "$CP/cf_nl.zag" | cut -d' ' -f1)"
rm -f "$R/cfn"; rm -rf "$R/.zag-cache"
"$ZNC" --target macos-arm64 $FLAGS "$CP/cf_nl.zag" -o "$R/cfn" > "$R/cfn.compile.txt" 2>&1
echo "  nl_compile rc=$?"
if [ -x "$R/cfn" ]; then
  echo "  nl_bin_sha=$(shasum -a 256 "$R/cfn" | cut -d' ' -f1)"
  "$W" reg cf_nl 600 "$R/cfn" > "$R/cfn.run.txt" 2>/dev/null
  echo "  nl_out_sha=$(shasum -a 256 "$R/cfn.run.txt" | cut -d' ' -f1) bytes=$(wc -c < "$R/cfn.run.txt" | tr -d ' ')"
fi
echo "CF_PROBE_DONE"