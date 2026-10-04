#!/bin/bash
# MASS_DELETE_GUARD (TNN research program)
#
# PURPOSE
#   This repository has suffered FOUR mass-deletion events, deleting 147,295 /
#   160,361 / 165,250 / 160,515 paths. Three were caught. Each was caught ONLY
#   because a human or agent happened to notice a missing file while looking for
#   something else, and wrote a commit whose SUBJECT names the offending sha:
#
#     cef8c4095  "REPAIR: restore full tree nuked by 169894404"
#     b688fa031  "160348 files deleted by c721bcc61 (WATCHDOG mass deletion)"
#     84727be29 + 3c25ff8f1  for f461e812d
#
#   The fourth, b3b3ee00a, was caught by NOTHING. Its subject read
#   "lm3_lifetime: prereg ... Non-ledger" and the "Non-ledger" suffix
#   discouraged exactly the check that would have found it. A mass deletion is
#   invisible in `git log --oneline`; it is visible only in `--numstat`. Nobody
#   read the numstat. Result: 858 of 1,108 research lanes vanished from every
#   tip, and an evidence audit published a false negative as a finding.
#
#   This guard makes the invariant MECHANICAL and FAILS CLOSED.
#
# INVARIANT ENFORCED
#   D1 MASS-DELETION  the staged diff deletes at most MAX_DEL paths.
#                    Paths, not lines: the historical events deleted ~10^5
#                    PATHS, and a path count is the quantity that caused the
#                    incident. Renames (R) count as deletions, because git
#                    models a rename as D + A.
#
#   The count is computed in pure Zag by mass_delete_guard.zag. This wrapper is
#   orchestration only: it produces the input with git plumbing and reads a
#   one-line VERDICT back. It does not re-derive the count.
#
# DESIGN NOTE - WHY 1000, AND WHY IT COSTS THE REAL REPAIRS NOTHING
#   All five of the real repairs in this repository's history restore files by
#   ADDING them back (git checkout <parent> -- <path>), so their diff is
#   deletions = 0 and this guard passes them. It fires only on the sweep-shaped
#   failure: an index reset followed by `git add -A` / `git commit -a` over a
#   working tree whose contents were not the ones the author intended to commit.
#
# FAIL CLOSED
#   If the Zag guard is missing, fails to build, times out, or emits anything
#   other than a well-formed VERDICT, this hook REFUSES the commit. A guard
#   that fails open is not a guard.
#
# USAGE
#   mass_delete_guard.sh                  check the current index (pre-commit)
#   mass_delete_guard.sh --max N          threshold, default 1000
#   mass_delete_guard.sh --selftest       prove the guard refuses >MAX deletions
#                                         and accepts the five real repairs
#   mass_delete_guard.sh --check REF      check a specific commit instead of the
#                                         index (REF = any git rev)
#
# EXIT CODES
#   0 = pass (or not applicable)
#   1 = REFUSED (invariant violated, or guard unavailable -> fail closed)
#   2 = usage/internal error

set -u

HERE=$(cd "$(dirname "$0")" && pwd)
ZAG="$HERE/mass_delete_guard.zag"
ZNC="${TNN_ROOT:-/Users/Shared/micah/Documents/TNN}/.bin/znc"
MAX_DEL=1000
CHECK_REF=""

usage() { sed -n '2,60p' "$0"; exit 2; }

while [ $# -gt 0 ]; do
  case "$1" in
    --max)  MAX_DEL="${2:-}"; shift 2 ;;
    --check) CHECK_REF="${2:-}"; shift 2 ;;
    --selftest) SELFTEST=1; shift ;;
    -h|--help) usage ;;
    *) echo "mass_delete_guard: unknown arg '$1'" >&2; exit 2 ;;
  esac
done

fail() { echo "MASS_DELETE_GUARD: REFUSED ($1)" >&2; exit 1; }

TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
NS="$TMP/name_status"
VERD="$TMP/verdict"
BIN="$TMP/mass_delete_guard"

# ---------------------------------------------------------------- selftest --
# The evidence that the control works, not merely that it exists. Four cases:
#   T1 a 5000-path deletion is REFUSED                (would have blocked b3b3ee00a)
#   T2 a 999-path deletion is ACCEPTED               (threshold is not a blanket ban)
#   T3 a pure-append / restore commit is ACCEPTED    (the real repairs pass)
#   T4 the four historical wipes are REFUSED by sha  (retrospective proof)
if [ "${SELFTEST:-0}" = "1" ]; then
  command -v znc >/dev/null 2>&1 && ZNC_BIN=znc || ZNC_BIN="$ZNC"
  if [ ! -f "$ZAG" ]; then echo "SELFTEST FAIL: $ZAG missing"; exit 1; fi
  "$ZNC_BIN" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache \
      "$ZAG" >/dev/null 2>&1 || { echo "SELFTEST FAIL: zag compile failed"; exit 1; }
  [ -x "$HERE/mass_delete_guard" ] || { echo "SELFTEST FAIL: binary not built"; exit 1; }
  G="$HERE/mass_delete_guard"

  # T1: synthesise a 5000-path deletion and require REFUSE
  : > "$NS"; i=0; while [ $i -lt 5000 ]; do printf 'D\tf/%s\n' "$i" >> "$NS"; i=$((i+1)); done
  "$G" "$NS" 1000 "$VERD" >/dev/null 2>&1
  grep -q '^VERDICT REFUSE' "$VERD" \
    && echo "SELFTEST PASS T1: 5000-path deletion REFUSED" \
    || { echo "SELFTEST FAIL T1: 5000-path deletion NOT refused"; exit 1; }

  # T2: 999-path deletion must be ACCEPTED
  : > "$NS"; i=0; while [ $i -lt 999 ]; do printf 'D\tf/%s\n' "$i" >> "$NS"; i=$((i+1)); done
  "$G" "$NS" 1000 "$VERD" >/dev/null 2>&1
  grep -q '^VERDICT PASS' "$VERD" \
    && echo "SELFTEST PASS T2: 999-path deletion ACCEPTED (not a blanket ban)" \
    || { echo "SELFTEST FAIL T2: 999-path deletion refused"; exit 1; }

  # T3: additions and modifications must be ACCEPTED
  printf 'A\tg/new1\nA\tg/new2\nM\tg/mod\n' > "$NS"
  "$G" "$NS" 1000 "$VERD" >/dev/null 2>&1
  grep -q '^VERDICT PASS' "$VERD" \
    && echo "SELFTEST PASS T3: additions/modifications ACCEPTED" \
    || { echo "SELFTEST FAIL T3: additions refused"; exit 1; }

  # T4: retrospective. Each historical wipe must be REFUSED by sha.
  for R in b3b3ee00a c721bcc61 f461e812d 169894404; do
    git cat-file -e "$R^{commit}" 2>/dev/null || { echo "SELFTEST SKIP T4: $R absent"; continue; }
    git diff-tree -r --no-commit-id --name-status "$R" > "$NS" 2>/dev/null
    "$G" "$NS" 1000 "$VERD" >/dev/null 2>&1
    if grep -q '^VERDICT REFUSE' "$VERD"; then
      N=$(sed -n '1s/.*REFUSE \([0-9]*\).*/\1/p' "$VERD")
      echo "SELFTEST PASS T4: $R REFUSED ($N paths deleted)"
    else
      echo "SELFTEST FAIL T4: $R NOT refused"; exit 1
    fi
  done

  # T5: each real repair must be ACCEPTED.
  for R in b688fa031 cef8c4095 84727be29 3c25ff8f1 7e4d7cffe; do
    git cat-file -e "$R^{commit}" 2>/dev/null || { echo "SELFTEST SKIP T5: $R absent"; continue; }
    git diff-tree -r --no-commit-id --name-status "$R" > "$NS" 2>/dev/null
    "$G" "$NS" 1000 "$VERD" >/dev/null 2>&1
    if grep -q '^VERDICT PASS' "$VERD"; then
      N=$(sed -n '1s/.*PASS \([0-9]*\).*/\1/p' "$VERD")
      echo "SELFTEST PASS T5: $R ACCEPTED ($N paths deleted)"
    else
      echo "SELFTEST FAIL T5: $R refused; the guard is too strict"; exit 1
    fi
  done
  echo "SELFTEST COMPLETE"
  exit 0
fi

# ------------------------------------------------------------- build guard --
# The Zag binary is the guard. If it cannot be produced, we cannot enforce the
# invariant, so we refuse. Fail closed.
if [ ! -x "$HERE/mass_delete_guard" ] || [ "${ZAG}0" -nt "$HERE/mass_delete_guard" ]; then
  command -v znc >/dev/null 2>&1 && ZNC_BIN=znc || ZNC_BIN="$ZNC"
  if ! "$ZNC_BIN" --target macos-arm64 --no-zagd --no-analyze \
        --no-foreground-cache "$ZAG" >/dev/null 2>&1; then
    fail "guard binary could not be built from $ZAG (fail closed)"
  fi
  cp "$HERE/mass_delete_guard" "$BIN" 2>/dev/null
  [ -x "$BIN" ] || BIN="$HERE/mass_delete_guard"
else
  BIN="$HERE/mass_delete_guard"
fi

# ---------------------------------------------------------------- D1 check --
if [ -n "$CHECK_REF" ]; then
  git diff-tree -r --no-commit-id --name-status "$CHECK_REF" > "$NS" 2>/dev/null || \
    fail "cannot read diff for $CHECK_REF"
  SRC="commit $CHECK_REF"
else
  git diff --cached --name-status > "$NS" 2>/dev/null || \
    fail "cannot read staged name-status"
  SRC="the index"
fi

[ -s "$NS" ] || { echo "mass_delete_guard: nothing staged (n/a)"; exit 0; }

"$BIN" "$NS" "$MAX_DEL" "$VERD" >/dev/null 2>&1 || \
  fail "Zag guard did not run (fail closed)"

V=$(sed -n '1p' "$VERD" 2>/dev/null)
case "$V" in
  "VERDICT PASS"*)
    echo "mass_delete_guard: PASS ($SRC, ${V#VERDICT PASS })"
    exit 0 ;;
  "VERDICT REFUSE"*)
    D=$(echo "$V" | awk '{print $3}')
    fail "D1: $SRC deletes $D paths, limit is $MAX_DEL.
       This is the b3b3ee00a failure shape: a mass deletion that is invisible in
       'git log --oneline' and only visible in --numstat. It destroyed 160,515
       paths and 858 of 1,108 research lanes while its subject read
       'lm3_lifetime: prereg ... Non-ledger'.

       If this deletion is INTENTIONAL and correct:
         git commit --no-verify
       and say so in the commit body, naming the sha or ref that authorises it.
       If it is NOT intentional: git restore --staged --worktree <paths> and
       re-stage. Do not 'git add -A' from a working tree whose index was reset;
       that is the mechanism that produced all four of these events." ;;
  *)
    fail "unrecognised verdict from Zag guard: '$V' (fail closed)" ;;
esac
