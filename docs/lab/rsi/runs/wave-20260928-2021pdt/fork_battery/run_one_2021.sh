#!/bin/sh
# run_one.sh <entry> <commit>  -- faithful rebuild of the frozen 2321pdt
# driver approach plus the 0821pdt orchestration layer (per wave-1121pdt
# procedure). Pure shell + git + sha256sum + the pinned znc + the rebuilt
# pure-Zag harness. No Python anywhere.
#
# Env expected: R (repo root), SCR (scratch root), HARNESS (rebuilt binary),
# ZNC_PIN, PROBE_PIN, B1_RUN_PIN, B2_BIN_PIN.
set -u

entry="$1"
commit="$2"
d="$SCR/E/$entry"
mkdir -p "$d" || exit 9
cd "$d" || exit 9

result() { # result k v
  printf '%s=%s\n' "$1" "$2"
}

# --- extract znc read-only ---
rm -f extract.err
git -C "$R" show "$commit:src/tools/toolchain/znc_linux_x86_64_abed8aa1" > znc.bin 2> extract.err
zx=$?
znc_sha=""
if [ "$zx" -eq 0 ]; then
  chmod +x znc.bin 2>/dev/null
  znc_sha=$(sha256sum znc.bin | cut -c1-64)
fi

RFILE="RESULT.txt"
{
  result entry "$entry"
  result ref "$commit"
  result commit "$commit"
} > "$RFILE"

if [ "$zx" -ne 0 ] || [ -z "$znc_sha" ]; then
  # extraction failure: UNTESTABLE per standing rule
  {
    result verdict UNTESTABLE
    result cause "pinned toolchain path absent in tree (git show exit $zx)"
  } >> "$RFILE"
  rm -f znc.bin
  exit 0
fi

{
  result znc_sha256 "$znc_sha"
} >> "$RFILE"

if [ "$znc_sha" != "$ZNC_PIN" ]; then
  { result verdict FAIL; result cause "znc sha mismatch (pin divergence)"; } >> "$RFILE"
  rm -f znc.bin
  exit 0
fi

# --- extract probe read-only ---
git -C "$R" show "$commit:src/tools/toolchain/znc_probe.zag" > tree_probe.zag 2>> extract.err
px=$?
probe_sha=""
if [ "$px" -eq 0 ]; then
  probe_sha=$(sha256sum tree_probe.zag | cut -c1-64)
fi
{
  result probe_sha256 "$probe_sha"
} >> "$RFILE"
if [ "$px" -ne 0 ] || [ "$probe_sha" != "$PROBE_PIN" ]; then
  { result verdict FAIL; result cause "probe sha mismatch or extraction failure"; } >> "$RFILE"
  rm -f znc.bin
  exit 0
fi

# --- znc.path + expected ---
printf '%s\n' "$d/znc.bin" > znc.path
printf 'FORKBATTERY-OK 42\n' > expected.out

# --- run the rebuilt pure-Zag harness, cwd = entry dir ---
"$HARNESS" > zag_harness.out 2> harness.err
harness_exit=$?
{
  result harness_exit "$harness_exit"
} >> "$RFILE"

# --- tokenize harness output on whitespace first (never split a packed line on '=') ---
b1_run_sha256=""
b2_bin_a_sha256=""
b1_tok=FAIL; b2_tok=FAIL; b3_tok=FAIL; b1_cmp_tok=FAIL
neg1_tok=FAIL; neg2_tok=FAIL; neg2diff_tok=FAIL
verdict_pass_count=0
for t in $(cat zag_harness.out); do
  case "$t" in
    b1_run_sha256=*) b1_run_sha256="${t#b1_run_sha256=}" ;;
    b2_bin_a_sha256=*) b2_bin_a_sha256="${t#b2_bin_a_sha256=}" ;;
    B1=PASS) b1_tok=PASS ;;
    B2=PASS) b2_tok=PASS ;;
    B3=PASS) b3_tok=PASS ;;
    b1_cmp=PASS) b1_cmp_tok=PASS ;;
    NEG1_fails_as_required=PASS) neg1_tok=PASS ;;
    NEG2_fails_as_required=PASS) neg2_tok=PASS ;;
    neg2_stdout_differs=PASS) neg2diff_tok=PASS ;;
    VERDICT=PASS) verdict_pass_count=$((verdict_pass_count + 1)) ;;
  esac
done
{
  result b2_bin_a_sha256 "$b2_bin_a_sha256"
  result b1_run_sha256 "$b1_run_sha256"
  result harness_verdict_pass_count "$verdict_pass_count"
  result b1 "$b1_tok"
  result b2 "$b2_tok"
  result b3 "$b3_tok"
  result b1_cmp "$b1_cmp_tok"
} >> "$RFILE"

b2_bin_cmp=FAIL
if [ "$b2_bin_a_sha256" = "$B2_BIN_PIN" ] && [ -n "$b2_bin_a_sha256" ]; then
  b2_bin_cmp=PASS
fi
{
  result b2_bin_cmp "$b2_bin_cmp"
} >> "$RFILE"

# --- driver NEG1: must fail compile and check; fork's own znc reports E0002 ---
./znc.bin neg1.zag --no-zagd --no-analyze --no-foreground-cache -o neg1_dbin > neg1c.out 2> neg1c.err
driver_neg1_compile_exit=$?
./znc.bin check neg1.zag --strict --no-zagd > neg1k.out 2> neg1k.err
driver_neg1_check_exit=$?
neg1_e0002_hit=$(grep -c E0002 neg1c.err 2>/dev/null || true)
neg1_e0002_hit=${neg1_e0002_hit:-0}
neg1_ok=FAIL
if [ "$driver_neg1_compile_exit" -ne 0 ] && [ "$driver_neg1_check_exit" -ne 0 ] && [ "$neg1_e0002_hit" -ge 1 ]; then
  neg1_ok=PASS
fi
: compiles, passes check, runs, stdout differs at char 1 ---
./znc.bin neg2.zag --no-zagd --no-analyze --no-foreground-cache -o neg2_bin > /dev/null 2>&1
neg2_compile_exit=$?
./neg2_bin > neg2_run.out 2>/dev/null
neg2_run_exit=$?
neg2_run_stdout=$(head -c 64 neg2_run.out | tr -d '\n')
neg2_char1_expected=$(head -c1 expected.out)
neg2_char1_run=$(head -c1 neg2_run.out)
neg2_differs_at_char1=FAIL
if [ "$neg2_char1_expected" != "$neg2_char1_run" ]; then
  neg2_differs_at_char1=PASS
fi
neg2_ok=FAIL
if [ "$neg2_compile_exit" -eq 0 ] && [ "$neg2_run_exit" -eq 0 ] && [ "$neg2_differs_at_char1" = PASS ]; then
  neg2_ok=PASS
fi

# --- driver B3: strict check, frozen flag order ---
./znc.bin check forkbat_hello.zag --strict --no-zagd > /dev/null 2>&1
b3_check_exit=$?

# --- driver tree probe: compile with fork's own znc, expect R32_ZNC_PROBE_OK ---
./znc.bin tree_probe.zag --no-zagd --no-analyze --no-foreground-cache -o probe_bin > probe_build.log 2>&1
probe_build_exit=$?
./probe_bin > probe_run.out 2>/dev/null
probe_run_exit=$?
probe_run_stdout=$(tr -d '\n' < probe_run.out)

{
  result neg1_ok "$neg1_ok"
  result neg2_ok "$neg2_ok"
  result b3_check_exit "$b3_check_exit"
  result neg2_run_stdout "$neg2_run_stdout"
  result neg2_char1_expected "$neg2_char1_expected"
  result neg2_char1_run "$neg2_char1_run"
  result neg2_differs_at_char1 "$neg2_differs_at_char1"
  result neg1_e0002_hit "$neg1_e0002_hit"
  result driver_neg1_compile_exit "$driver_neg1_compile_exit"
  result driver_neg1_check_exit "$driver_neg1_check_exit"
  result probe_build_exit "$probe_build_exit"
  result probe_run_exit "$probe_run_exit"
  result probe_run_stdout "$probe_run_stdout"
} >> "$RFILE"

verdict=FAIL
if [ "$harness_exit" -eq 0 ] && [ "$verdict_pass_count" -eq 1 ] \
   && [ "$b1_tok" = PASS ] && [ "$b2_tok" = PASS ] && [ "$b3_tok" = PASS ] \
   && [ "$b1_cmp_tok" = PASS ] && [ "$b2_bin_cmp" = PASS ] \
   && [ "$neg1_ok" = PASS ] && [ "$neg2_ok" = PASS ] \
   && [ "$b3_check_exit" -eq 0 ] \
   && [ "$probe_build_exit" -eq 0 ] && [ "$probe_run_exit" -eq 0 ] \
   && [ "$probe_run_stdout" = "R32_ZNC_PROBE_OK" ]; then
  verdict=PASS
fi
{
  result verdict "$verdict"
} >> "$RFILE"

# --- delete per-entry znc copy (design: no znc.bin survives) ---
rm -f znc.bin neg1_dbin
exit 0
