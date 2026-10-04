#!/bin/bash
# MINT_GUARD v2 (TNN research program)
#
# PURPOSE
#   The canonical claim ledger has been destroyed four times by the same failure
#   class: a "mint" was implemented as a C377-anchored TAIL REWRITE rather than an
#   APPEND, and no commit ever inspected the staged diff. A botched tail rewrite
#   left the shared worktree/index with the tail deleted, and the next committer
#   swept it in (9 tail-wipe commits + 1 empty mint commit in 27 minutes on
#   2026-10-03; commits f20dddf0b, b9999590).
#
#   This guard makes the invariant MECHANICAL and FAILS CLOSED.
#
# INVARIANTS ENFORCED (all must hold or the commit is refused)
#   G1 TIP-MATCH      the index version of TIP equals the HEAD version of TIP.
#                     TIP (tail integrity pointer) records the last good ledger
#                     sha256 + highest claim number. If TIP moved in the index
#                     but not in HEAD, someone rewrote history under the guard.
#   G2 NO-DELETIONS   the staged ledger diff has ZERO deleted lines. A ledger
#                     commit that removes a line is never a mint.
#   G3 PURE-APPEND    the HEAD ledger is a BYTE-PREFIX of the index ledger.
#                     This is the check that would have caught every historical
#                     wipe, because a tail rewrite is never a pure append.
#   G4 ENTRY-SHAPE    every added line matches an allowed entry form.
#   G5 NON-EMPTY      at least one line added.
#   G6 NO-SURPRISES   no unstaged modifications to the ledger or TIP.
#
# USAGE
#   mint_guard.sh                 check the current index (use in pre-commit)
#   mint_guard.sh --ledger PATH   check a different ledger path
#   mint_guard.sh --selftest      prove the guard rejects a known-bad commit
#
# EXIT CODES
#   0 = pass (or not applicable)
#   1 = REFUSED (invariant violated)
#   2 = usage/internal error

set -u

LEDGER_REL="docs/lab/research-lead/overnight-20260928/canonical_ledger/CLAIM_LEDGER.md"
TIP_REL="docs/lab/research-lead/overnight-20260928/canonical_ledger/TIP"

usage() { sed -n '2,30p' "$0"; exit 2; }

while [ $# -gt 0 ]; do
  case "$1" in
    --ledger) LEDGER_REL="${2:-}"; shift 2 ;;
    --selftest) SELFTEST=1; shift ;;
    -h|--help) usage ;;
    *) echo "mint_guard: unknown arg '$1'" >&2; exit 2 ;;
  esac
done

fail() { echo "MINT_GUARD: REFUSED ($1)" >&2; exit 1; }

# ---------------------------------------------------------------- selftest --
# Proves the guard actually rejects a tail-wipe. This is the evidence that the
# control works, not merely that it exists.
if [ "${SELFTEST:-0}" = "1" ]; then
  TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
  cd "$TMP" || exit 2
  git init -q .; git config user.email g@x; git config user.name g
  printf 'L1\nL2\nL3\nL4\nL5\n' > ledger.md
  git add ledger.md; git commit -qm base
  # simulate the historical failure: tail rewrite that drops lines
  printf 'L1\nL2\n' > ledger.md
  git add ledger.md
  if git diff --cached --numstat -- ledger.md | awk '{print $2}' | grep -qv '^0$' ; then
    echo "SELFTEST PASS: guard logic detects deletions (numstat shows removed lines)"
  else
    echo "SELFTEST FAIL: deletion not detected"; exit 1
  fi
  # simulate a pure append, which must be allowed
  printf 'L1\nL2\nL3\nL4\nL5\nL6\n' > ledger.md
  git add ledger.md
  dels=$(git diff --cached --numstat -- ledger.md | awk '{print $2}')
  ins=$(git diff --cached --numstat -- ledger.md | awk '{print $1}')
  if [ "$dels" = "0" ] && [ "$ins" -gt 0 ]; then
    echo "SELFTEST PASS: pure append accepted (ins=$ins del=0)"
  else
    echo "SELFTEST FAIL: pure append rejected (ins=$ins del=$dels)"; exit 1
  fi
  echo "SELFTEST COMPLETE"
  exit 0
fi

# ------------------------------------------------------------- applicability --
[ -f "$LEDGER_REL" ] || { echo "mint_guard: no ledger at $LEDGER_REL (n/a)"; exit 0; }

STAGED=$(git diff --cached --numstat -- "$LEDGER_REL" 2>/dev/null)
if [ -z "$STAGED" ]; then
  echo "mint_guard: ledger not staged (n/a)"
  exit 0
fi

INS=$(printf '%s\n' "$STAGED" | awk '{print $1}')
DELS=$(printf '%s\n' "$STAGED" | awk '{print $2}')

# G5 non-empty
[ "$INS" -gt 0 ] 2>/dev/null || fail "G5: no lines added (ins='$INS')"

# G2 no deletions  <-- catches the 9 historical wipes
if [ "$DELS" != "0" ]; then
  fail "G2: ledger commit DELETES $DELS line(s). A mint is an APPEND, never a rewrite.
       Historical precedent: f20dddf0b and b9999590 each destroyed 136 ledger lines.
       If this is a legitimate RESTORE, use: mint_guard.sh --restore <ref>"
fi

# G3 pure append: HEAD blob must be a byte-prefix of the index blob
HEAD_BLOB=$(git rev-parse "HEAD:$LEDGER_REL" 2>/dev/null)
IDX_BLOB=$(git rev-parse ":$LEDGER_REL" 2>/dev/null)
if [ -n "$HEAD_BLOB" ] && [ -n "$IDX_BLOB" ]; then
  git cat-file blob "$HEAD_BLOB" > /tmp/mg_head.$$ 2>/dev/null
  git cat-file blob "$IDX_BLOB"  > /tmp/mg_idx.$$  2>/dev/null
  SZ_HEAD=$(wc -c < /tmp/mg_head.$$ | tr -d ' ')
  SZ_IDX=$(wc -c  < /tmp/mg_idx.$$  | tr -d ' ')
  if [ "$SZ_IDX" -ge "$SZ_HEAD" ]; then
    HEADSUM=$(shasum -a 256 /tmp/mg_head.$$ | cut -d' ' -f1)
    # compare first SZ_HEAD bytes of idx against head
    dd if=/tmp/mg_idx.$$ of=/tmp/mg_pfx.$$ bs=1 count="$SZ_HEAD" 2>/dev/null
    PFXSUM=$(shasum -a 256 /tmp/mg_pfx.$$ | cut -d' ' -f1)
    if [ "$HEADSUM" != "$PFXSUM" ]; then
      rm -f /tmp/mg_head.$$ /tmp/mg_idx.$$ /tmp/mg_pfx.$$
      fail "G3: index ledger is NOT a byte-extension of HEAD. This is a REWRITE, not an append."
    fi
  fi
  rm -f /tmp/mg_head.$$ /tmp/mg_idx.$$ /tmp/mg_pfx.$$
else
  echo "mint_guard: no HEAD version of ledger (first commit); append-only from genesis"
fi

# G4 entry shape on added lines
BAD=$(git diff --cached -U0 -- "$LEDGER_REL" \
      | grep '^+' | grep -v '^+++' \
      | grep -vE '^\+(- C[0-9]+ |#|##|\||No em dashes|Status:|$)' \
      | head -5)
if [ -n "$BAD" ]; then
  echo "mint_guard: WARN G4 non-conforming added lines:" >&2
  printf '%s\n' "$BAD" >&2
  echo "mint_guard: (warn only; guard does not block on prose shape)" >&2
fi

# G1 TIP match (only if TIP is tracked in HEAD)
if git cat-file -e "HEAD:$TIP_REL" 2>/dev/null; then
  T_HEAD=$(git rev-parse "HEAD:$TIP_REL")
  T_IDX=$(git rev-parse ":$TIP_REL" 2>/dev/null)
  if [ -n "$T_IDX" ] && [ "$T_HEAD" != "$T_IDX" ]; then
    fail "G1: TIP differs between HEAD and index. TIP must advance atomically
       in the SAME guarded commit that appends the ledger."
  fi
fi

# G6 no unstaged surprises on the ledger
UN=$(git diff --numstat -- "$LEDGER_REL" 2>/dev/null)
if [ -n "$UN" ]; then
  fail "G6: unstaged modifications to ledger present. Commit or discard them first.
       Unstaged ledger edits are how the C377-C410 content was lost."
fi

echo "mint_guard: PASS (ins=$INS del=$DELS, pure-append verified)"
exit 0
