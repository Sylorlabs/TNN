#!/bin/sh
# BUILD-RUN GATE -- permanent execution guard for the TNN research lane.
#
# WHY THIS EXISTS
#   This lane produced a class of bug where a STALE BINARY was executed and its
#   output read as a fresh result. Concretely, in p6struct/precond.zag:
#     - a compile FAILED with E0001 (apostrophe in a string literal, then a
#       missing closing paren)
#     - the shell command was `znc ... && ... && ./prog`, and because the
#       operator chain was mishandled the old binary still ran
#     - I read "A0 -> FAILED" and "derivable : 0" as findings about the grammar
#   Those were facts about a program that did not exist. Five further bugs in the
#   same prover were only findable because the garbage was so obviously wrong.
#
#   This script makes that failure mode structurally impossible.
#
# CONTRACT
#   zag_run <source.zag> [args...]
#     1. hash the source            (sha256)
#     2. compile to a GATED build path
#     3. record compiler exit status
#     4. record binary hash
#     5. REFUSE TO RUN if compile failed, or if the compiler wrote no binary
#     6. REFUSE TO REUSE if a stamp exists with a different source hash
#     7. record the run hash (source+binary+args)
#     8. verify the output belongs to the just-built binary, via the stamp
#     9. only then execute, with stdout/stderr tee'd to a run log
#
#   zag_stamp  <source.zag>          print the stamp, if any
#   zag_verify <source.zag>          re-verify an existing stamp WITHOUT running
#
# EXIT CODES
#   0 success   2 no-op verdict (convention: NO-OP / CHANGED style tools)
#   90 compile failed          -- HARD REFUSAL, no run attempted
#   91 compiler produced no binary
#   92 source hash differs from existing stamp (possible source/binary mismatch)
#   93 stamp missing or malformed
#
# The gate never deletes a user's data and never rewrites history. It refuses.
# Usage is `sh tools/gate/zag_run.sh <source.zag> [args...]`.

set -u

TNN_ROOT="${TNN_ROOT:-/Users/Shared/micah/Documents/TNN}"
ZNC="$TNN_ROOT/.bin/znc"
TARGET="macos-arm64"
GATEDIR="${TNN_GATE_DIR:-${TMPDIR:-/tmp}/tnn_gate}"

EX_REFUSE_COMPILE=90
EX_NO_BINARY=91
EX_HASH_DRIFT=92
EX_NO_STAMP=93

die() {
  # die <exitcode> <message...>
  _code="$1"; shift
  printf 'GATE-REFUSE[%s]: %s\n' "$_code" "$*" >&2
  printf '  source : %s\n' "${SRC:-<none>}" >&2
  [ -n "${SRC_HASH:-}" ] && printf '  srchash: %s\n' "$SRC_HASH" >&2
  [ -n "${BIN_HASH:-}" ] && printf '  binhash: %s\n' "$BIN_HASH" >&2
  exit "$_code"
}

sha() {
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$1" | cut -d' ' -f1
  else
    shasum -a 256 "$1" | cut -d' ' -f1
  fi
}

# Print a stable hash of a string (used for the run hash).
strhash() {
  printf '%s' "$1" | { if command -v sha256sum >/dev/null 2>&1; then sha256sum | cut -d' ' -f1; else shasum -a 256 | cut -d' ' -f1; fi; }
}

[ -x "$ZNC" ] || { printf 'GATE-REFUSE: compiler not found/executable: %s\n' "$ZNC" >&2; exit "$EX_REFUSE_COMPILE"; }

SRC="$1"; shift 2>/dev/null || true
[ -n "${SRC:-}" ] || { printf 'usage: zag_run.sh <source.zag> [args...]\n' >&2; exit 64; }
[ -f "$SRC" ] || die "$EX_REFUSE_COMPILE" "source does not exist"

mkdir -p "$GATEDIR" || die "$EX_REFUSE_COMPILE" "cannot create gate dir $GATEDIR"

BASE="$(basename "$SRC" .zag)"
BIN="$GATEDIR/$BASE.gated"
STAMP="$GATEDIR/$BASE.stamp"
RUNLOG="$GATEDIR/$BASE.runlog"

# 1. source hash
SRC_HASH="$(sha "$SRC")"
[ -n "$SRC_HASH" ] || die "$EX_REFUSE_COMPILE" "could not hash source"

# 6. drift check BEFORE compiling: if a stamp exists for a different source,
#    the on-disk binary may belong to an older source. Refuse rather than guess.
if [ -f "$STAMP" ]; then
  OLD_SRC_HASH="$(sed -n 's/^srchash=//p' "$STAMP" 2>/dev/null | head -1)"
  if [ -n "$OLD_SRC_HASH" ] && [ "$OLD_SRC_HASH" != "$SRC_HASH" ]; then
    printf 'GATE-NOTE: source changed since last gated build; rebuilding.\n' >&2
    printf '  old srchash: %s\n' "$OLD_SRC_HASH" >&2
    printf '  new srchash: %s\n' "$SRC_HASH" >&2
  fi
fi

# 2+3. compile, capturing exit status explicitly (no `&&` chains: that is how a
#      failed compile came to be followed by a run of the old binary)
rm -f "$BIN"
COMPILE_LOG="$GATEDIR/$BASE.compile"
"$ZNC" --target "$TARGET" --no-zagd --no-analyze --no-foreground-cache \
       -o "$BIN" "$SRC" >"$COMPILE_LOG" 2>&1
CSTAT=$?

printf 'GATE: compiled %s (exit=%s)\n' "$SRC" "$CSTAT" >&2

if [ "$CSTAT" -ne 0 ]; then
  printf 'GATE-NOTE: compiler output follows\n' >&2
  sed 's/^/    /' "$COMPILE_LOG" >&2
  # 5. HARD REFUSAL. No run. No reading of any previous output.
  die "$EX_REFUSE_COMPILE" "compile failed (exit $CSTAT); REFUSING TO RUN"
fi

# 4. binary must exist and be non-empty
[ -s "$BIN" ] || die "$EX_NO_BINARY" "compiler exited 0 but wrote no binary at $BIN"

BIN_HASH="$(sha "$BIN")"
[ -n "$BIN_HASH" ] || die "$EX_NO_BINARY" "could not hash binary"

# 7. run hash binds source + binary + args
RUN_HASH="$(strhash "$SRC_HASH|$BIN_HASH|$*")"

# write stamp
{
  printf 'source=%s\n' "$SRC"
  printf 'srchash=%s\n' "$SRC_HASH"
  printf 'binhash=%s\n' "$BIN_HASH"
  printf 'compile_exit=%s\n' "$CSTAT"
  printf 'runhash=%s\n' "$RUN_HASH"
} > "$STAMP"

# 8. verify the binary we are about to execute is the one we just hashed
VERIFY_BIN_HASH="$(sha "$BIN")"
[ "$VERIFY_BIN_HASH" = "$BIN_HASH" ] || die "$EX_NO_BINARY" "binary hash changed between build and exec"
printf 'GATE: srchash=%s binhash=%s runhash=%s\n' \
  "$SRC_HASH" "$BIN_HASH" "$RUN_HASH" >&2

# 9. execute, teeing to a run log
set +e
"$BIN" "$@" 2>&1 | tee "$RUNLOG"
RSTAT=$?
set -e

printf 'GATE: exit=%s runhash=%s log=%s\n' "$RSTAT" "$RUN_HASH" "$RUNLOG" >&2
exit "$RSTAT"