#!/usr/bin/env bash
# mint_guard.sh -- pre-commit gate for WATCHDOG claim-ledger mints.
#
# DESIGN ARTIFACT. Not wired into any live procedure. Claim minting is
# paused per f40fbeb11 ("WATCHDOG: ledger C463"); see MINT_GUARD.md.
#
# Placement in the mint procedure: run AFTER `git add` and BEFORE `git commit`,
# from the repo root (~/workspace/tnn-rsi). Exit 0 = the commit may proceed.
# Any non-zero exit = DO NOT COMMIT. Re-run the guard after any fix.
#
# Mint mode (default):  ./mint_guard.sh --claim 411
# Restore mode:         ./mint_guard.sh --restore --expect-sha <sha256>
# Advance TIP:          ./mint_guard.sh --advance-tip   (after a guarded commit)
#
# Toolchain: bash, git (/usr/bin/git; the $HOME/safebin/git symlink has known
# EPERM write failures), sha256sum, grep, awk, cmp, head, tail, mktemp.
# No forbidden executables.

set -u -o pipefail

LEDGER="docs/lab/research-lead/overnight-20260928/canonical_ledger/CLAIM_LEDGER.md"
LANE="docs/lab/research-lead/overnight-20260928/mint_guard"
TIP_FILE="$LANE/TIP"
GIT="/usr/bin/git"

die() { echo "MINT-GUARD FAIL: $1" >&2; exit 1; }
ok()  { echo "MINT-GUARD PASS: $1"; }

MODE="mint"; CLAIM=""; EXPECT_SHA=""; ADVANCE_TIP=0
while [ $# -gt 0 ]; do
  case "$1" in
    --claim)       CLAIM="$2"; shift 2 ;;
    --restore)     MODE="restore"; shift ;;
    --expect-sha)  EXPECT_SHA="$2"; shift 2 ;;
    --advance-tip) ADVANCE_TIP=1; shift ;;
    *) die "unknown argument: $1" ;;
  esac
done

[ -f "$LEDGER" ]   || die "ledger file not found: $LEDGER"
[ -f "$TIP_FILE" ] || die "TIP file not found: $TIP_FILE"
[ -x "$GIT" ]      || die "git binary not found: $GIT"

if [ "$ADVANCE_TIP" -eq 1 ]; then
  new_sha="$($GIT show "HEAD:$LEDGER" | sha256sum | cut -d' ' -f1)"
  new_max="$($GIT show "HEAD:$LEDGER" | grep -oE '^- C[0-9]+ ' | grep -oE '[0-9]+' | sort -n | tail -1)"
  [ -n "$new_max" ] || die "could not determine max claim id at HEAD"
  tmp_tip="$(mktemp)"
  grep -E '^[[:space:]]*(#|$)' "$TIP_FILE" > "$tmp_tip" || true
  printf '%s %s\n' "$new_sha" "$new_max" >> "$tmp_tip"
  mv "$tmp_tip" "$TIP_FILE"
  ok "TIP advanced to sha=$new_sha max_claim=C$new_max"
  exit 0
fi

# TIP data line: last non-comment, non-blank line of the TIP file.
tip_line="$(grep -vE '^[[:space:]]*(#|$)' "$TIP_FILE" | tail -1)"
tip_sha="$(printf '%s' "$tip_line" | cut -d' ' -f1)"
tip_max="$(printf '%s' "$tip_line" | cut -d' ' -f2)"
[ -n "$tip_sha" ] || die "TIP file has no data line; see MINT_GUARD.md section 4.4"
[ "$tip_sha" != "UNINITIALIZED" ] || die "TIP not initialized; see MINT_GUARD.md section 4.4"

# ---------------------------------------------------------------- restore --
if [ "$MODE" = "restore" ]; then
  [ -n "$EXPECT_SHA" ] || die "--restore requires --expect-sha <sha256>"
  # Restores replace the working-tree file, then stage it. Verify content first.
  actual="$(sha256sum "$LEDGER" | cut -d' ' -f1)"
  [ "$actual" = "$EXPECT_SHA" ] \
    || die "working-tree ledger SHA $actual != expected $EXPECT_SHA; not a verified restore source"
  stat_line="$($GIT diff --cached --numstat -- "$LEDGER")"
  [ -n "$stat_line" ] || die "restore not staged; run: $GIT add -- $LEDGER"
  added="$(printf '%s' "$stat_line" | cut -f1)"
  deleted="$(printf '%s' "$stat_line" | cut -f2)"
  [ "$added" -gt 0 ]  || die "restore stages 0 insertions"
  [ "$deleted" -eq 0 ] || die "restore must not delete lines (deleted=$deleted)"
  staged_sha="$($GIT show ":$LEDGER" | sha256sum | cut -d' ' -f1)"
  [ "$staged_sha" = "$EXPECT_SHA" ] \
    || die "staged ledger SHA $staged_sha != expected $EXPECT_SHA"
  ok "restore verified (sha=$EXPECT_SHA). Commit with subject starting 'WATCHDOG: restore', then run --advance-tip."
  exit 0
fi

# ------------------------------------------------------------------- mint --
[ -n "$CLAIM" ] || die "mint mode requires --claim <number>, e.g. --claim 411"

# Check 1: TIP. HEAD's ledger version must be the last known-good state.
# A mint built on a damaged or unguarded-moved HEAD is blocked here.
head_sha="$($GIT show "HEAD:$LEDGER" | sha256sum | cut -d' ' -f1)"
[ "$head_sha" = "$tip_sha" ] \
  || die "HEAD ledger SHA $head_sha != TIP $tip_sha (max C$tip_max). Ledger moved outside the guarded procedure; restore/reconcile before minting."

# Check 2: staged numstat. A mint must add lines and delete none.
# Threshold: insertions > 0, deletions == 0. No legitimate mint deletes.
stat_line="$($GIT diff --cached --numstat -- "$LEDGER")"
[ -n "$stat_line" ] || die "no staged change for $LEDGER; stage the mint first (explicit pathspec), then re-run the guard"
added="$(printf '%s' "$stat_line" | cut -f1)"
deleted="$(printf '%s' "$stat_line" | cut -f2)"
[ "$added" -gt 0 ]  || die "staged insertions = 0 (catches empty mints like 9bb51ff39)"
[ "$deleted" -eq 0 ] || die "staged deletions = $deleted (threshold 0; catches the C377-tail wipe family)"

# Check 3: byte-prefix. The staged file must be exactly HEAD ++ appended block.
# This retires the tail-rewrite semantics: silent repairs are forbidden here.
tmp_old="$(mktemp)"; tmp_new="$(mktemp)"; tmp_block="$(mktemp)"
trap 'rm -f "$tmp_old" "$tmp_new" "$tmp_block"' EXIT
$GIT show "HEAD:$LEDGER" > "$tmp_old"
$GIT show ":$LEDGER"      > "$tmp_new"
old_bytes="$(wc -c < "$tmp_old")"
head -c "$old_bytes" "$tmp_new" | cmp -s - "$tmp_old" \
  || die "staged ledger is not a pure append of HEAD (tail rewrite detected)"

# Check 4: entry shape. Exactly one new 4-line claim block at EOF.
[ "$added" -eq 4 ] || die "expected exactly 4 added lines (one claim block), got $added"
tail -n 4 "$tmp_new" > "$tmp_block"
l1="$(sed -n '1p' "$tmp_block")"
l2="$(sed -n '2p' "$tmp_block")"
l3="$(sed -n '3p' "$tmp_block")"
l4="$(sed -n '4p' "$tmp_block")"
[ -z "$l1" ] || die "appended block line 1 is not blank"
printf '%s' "$l2" | grep -qE '^- C[0-9]+ \(' || die "appended block line 2 is not a claim header: $l2"
[ -z "$l3" ] || die "appended block line 3 is not blank"
[ "$l4" = "No em dashes were used in this entry (verified)." ] \
  || die "appended block line 4 is not the standard trailer"
new_id="$(printf '%s' "$l2" | sed -E 's/^- C([0-9]+) .*/\1/')"
[ "$new_id" = "$CLAIM" ] || die "appended entry is C$new_id, expected C$CLAIM"
[ "$new_id" -eq "$((tip_max + 1))" ] \
  || die "appended entry C$new_id != TIP max C$tip_max + 1"
[ "$(grep -c -- "^- C${new_id} " "$tmp_new")" -eq 1 ] \
  || die "claim id C$new_id does not appear exactly once in the staged ledger"

# Check 5: dash hygiene. WARNING ONLY (not blocking): existing entries
# routinely contain em dashes despite the trailer, so blocking would halt
# all minting under current practice. Flagged for parent review.
emdash_n="$(LC_ALL=C grep -cP '\xe2\x80\x94' "$tmp_block" || true)"
[ "$emdash_n" -eq 0 ] \
  || echo "MINT-GUARD WARN: $emdash_n em-dash byte(s) in appended block; trailer claim is false" >&2

# Check 6: no unstaged surprises from a concurrent worker in the shared worktree.
$GIT diff --quiet -- "$LEDGER" \
  || die "unstaged changes present for $LEDGER; stage, re-run guard, then commit"

ok "mint C$new_id may proceed. Commit with an explicit pathspec, then run --advance-tip."
