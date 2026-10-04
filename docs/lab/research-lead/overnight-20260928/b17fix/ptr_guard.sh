#!/bin/bash
# PTR_GUARD (TNN research program)
#
# PURPOSE
#   `[]u8 as *u8` is a REAL COMPILER DEFECT (B17 / C500), not a style rule.
#   The cast yields an address that is not the slice's data pointer. Reads
#   through it return unrelated memory (a literal 7 read back as 8) and writes
#   through it damage the ORIGINAL arena (7 -> 0, which is neither the old nor
#   the new value, so no aliasing semantics explains it). Verified 9/9, 5/5.
#
#   This guard makes the invariant MECHANICAL and FAILS CLOSED.
#
# INVARIANT ENFORCED
#   P1 NO-CORRUPT-CAST  no .zag source may cast a slice to *u8 and then
#                       dereference the result. The only sound `*u8` sources
#                       are `_zag_malloc(n) as *u8` and `null as *u8`; an
#                       existing slice's address comes from _zag_slice_ptr(b).
#
#   Shell's role is ENUMERATION AND ORCHESTRATION ONLY (charter section 4).
#   Every classification decision is made by the pure-Zag binary ptr_guard.
#
# WHY A SHELL WRAPPER AT ALL
#   Zag has no directory-listing builtin. The corpus is enumerated by `find`
#   and handed to the Zag scanner as a manifest. This keeps the *analysis*
#   pure Zag while still covering the whole tree.
#
# USAGE
#   ptr_guard.sh                     scan the whole corpus, fail on CORRUPT
#   ptr_guard.sh --selftest          prove the guard rejects known-bad sources
#   ptr_guard.sh --allowlist PATH    pins for reviewed non-canonical casts
#   ptr_guard.sh --root PATH         scan a different tree (default: repo root)
#
# EXIT CODES
#   0 = PASS
#   1 = REFUSED (a CORRUPT slice-as-pointer cast is present)
#   2 = usage / infrastructure error
#
# EXTENDS the guard family installed by lane/restores (mint_guard_v2.sh, the
# >1000-path-deletion tripwire): same shape -- a bash driver, an explicit
# invariant list, fail-closed exit, and a --selftest that demonstrates the
# guard actually fires.

set -u

HERE="$(cd "$(dirname "$0")" && pwd)"
ZNC="${TNN_ROOT:-/Users/Shared/micah/Documents/TNN}/.bin/znc"
SCANNER="$HERE/ptr_guard"
SRC="$HERE/ptr_guard.zag"
DEFAULT_ALLOW="$HERE/ptr_guard.allow"
ROOT="$(cd "$HERE/../../../../.." && pwd)"
ALLOW=""
SELFTEST=0

usage() { sed -n '2,45p' "$0"; exit 2; }
fail()  { echo "PTR_GUARD: REFUSED ($1)" >&2; exit 1; }
infra() { echo "PTR_GUARD: INFRA-FAIL: $1" >&2; exit 2; }

while [ $# -gt 0 ]; do
  case "$1" in
    --selftest) SELFTEST=1; shift ;;
    --allowlist) ALLOW="${2:-}"; shift 2 ;;
    --root) ROOT="${2:-}"; shift 2 ;;
    -h|--help) usage ;;
    *) echo "ptr_guard: unknown arg '$1'" >&2; exit 2 ;;
  esac
done

[ -f "$SRC" ] || infra "scanner source missing: $SRC"

build_scanner() {
  OUT=$("$ZNC" --target macos-arm64 --no-zagd --no-analyze \
        --no-foreground-cache "$SRC" 2>&1); RC=$?
  if [ $RC -ne 0 ]; then
    echo "$OUT" | sed 's/^/[znc] /'
    infra "ptr_guard.zag failed to compile (rc=$RC)"
  fi
  [ -x "$SCANNER" ] || chmod +x "$SCANNER" 2>/dev/null
  [ -x "$SCANNER" ] || infra "no scanner binary at $SCANNER"
}

# ------------------------------------------------------------------ selftest
# Proves the guard FIRES. A guard whose selftest passes on known-bad input is
# not a guard. Each fixture below is a minimal .zag source containing one cast
# of the given class; the expected verdict is asserted.
if [ "$SELFTEST" = "1" ]; then
  TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
  build_scanner
  W="${TNN_ROOT:-/Users/Shared/micah/Documents/TNN}/TNN/tools/tnnwatch.sh"
  mkdir -p "$TMP/fx"

  # fixture generators ------------------------------------------------------
  # FIXTURE 1: slice cast, then dereferenced. MUST be refused.
  cat > "$TMP/fx/bad_corrupt.zag" <<'ZAG'
fn main()i32 {
  let p:*u8=_zag_malloc(64) as *u8;
  let b:[]u8=p[0..64];
  b[0]=7;
  let cp:*u8=b as *u8;
  let viaCast:[]u8=cp[0..64];
  _zag_print("x"); _zag_println(_zag_i64_to_str(viaCast[0] as i64));
  return 0;
}
ZAG

  # FIXTURE 2: a PROHIBITION COMMENT. MUST NOT be flagged. This is the fixture
  # that the naive-grep guard fails; it is why comment stripping is load-bearing.
  cat > "$TMP/fx/good_comment.zag" <<'ZAG'
// Alloc pattern: _zag_malloc as *u8 then [0..n] (the sound pattern;
// never `as *i32` + slice, never `[]u8 as *u8`).
fn main()i32 { _zag_println("OK"); return 0; }
ZAG

  # FIXTURE 3: the two canonical SAFE forms. MUST NOT be flagged.
  cat > "$TMP/fx/good_canonical.zag" <<'ZAG'
fn main()i32 {
  let p:*u8=_zag_malloc(64) as *u8;
  if(p==null as *u8){ _zag_println("null"); return 0; }
  let b:[]u8=p[0..64];
  let sp:*u8=_zag_slice_ptr(b);
  let q:[]u8=sp[0..64];
  _zag_print("y"); _zag_println(_zag_i64_to_str(q[0] as i64));
  return 0;
}
ZAG

  # FIXTURE 4: slice cast bound but never dereferenced -> SUSPECT, not CORRUPT.
  cat > "$TMP/fx/suspect_noderef.zag" <<'ZAG'
fn main()i32 {
  let p:*u8=_zag_malloc(64) as *u8;
  let b:[]u8=p[0..64];
  let cp:*u8=b as *u8;
  if(cp==null as *u8){ _zag_println("null"); }
  return 0;
}
ZAG

  : > "$TMP/empty.allow"

  run_case() {
    # $1 label  $2 fixture  $3 expected rc  $4 expected substring
    #           $5 expected CORRUPT count (default any)  $6 expected SUSPECT
    echo "--- selftest: $1"
    printf '%s\n' "$2" > "$TMP/man.txt"
    if [ -n "$W" ] && [ -x "$W" ]; then
      "$W" reg ptrself 300 "$SCANNER" "$TMP/man.txt" "$TMP/empty.allow" \
        > "$TMP/out.txt" 2>&1
    else
      "$SCANNER" "$TMP/man.txt" "$TMP/empty.allow" > "$TMP/out.txt" 2>&1
    fi
    RC=$?
    echo "    rc=$RC (expected $3)"
    sed 's/^/    | /' "$TMP/out.txt"
    if [ "$RC" != "$3" ]; then
      echo "PTR_GUARD SELFTEST: FAILED ($1: rc $RC, expected $3)" >&2
      exit 1
    fi
    if ! grep -q "$4" "$TMP/out.txt"; then
      echo "PTR_GUARD SELFTEST: FAILED ($1: output missing '$4')" >&2
      exit 1
    fi
    # Counting matters as much as the exit code: a guard that flags EVERYTHING
    # also returns 0 on clean input. Assert the exact tallies.
    if [ -n "${5:-}" ]; then
      GC=$(grep '^  CORRUPT' "$TMP/out.txt" | tr -s ' ' | cut -d' ' -f3)
      if [ "$GC" != "$5" ]; then
        echo "PTR_GUARD SELFTEST: FAILED ($1: CORRUPT=$GC, expected $5)" >&2
        exit 1
      fi
    fi
    if [ -n "${6:-}" ]; then
      GS=$(grep '^  SUSPECT' "$TMP/out.txt" | tr -s ' ' | cut -d' ' -f3)
      if [ "$GS" != "$6" ]; then
        echo "PTR_GUARD SELFTEST: FAILED ($1: SUSPECT=$GS, expected $6)" >&2
        exit 1
      fi
    fi
  }

  echo "PTR_GUARD SELFTEST"
  run_case "CORRUPT slice cast + deref is REFUSED" \
           "$TMP/fx/bad_corrupt.zag" 1 "CORRUPT" 1 0
  run_case "prohibition COMMENT is not flagged" \
           "$TMP/fx/good_comment.zag" 0 "PASS" 0 0
  run_case "canonical malloc/null/slice_ptr are SAFE" \
           "$TMP/fx/good_canonical.zag" 0 "PASS" 0 0
  run_case "slice cast without deref is SUSPECT not CORRUPT" \
           "$TMP/fx/suspect_noderef.zag" 0 "SUSPECT" 0 1

  # Aggregate case: the good fixtures and the bad fixture together must fail.
  echo "--- selftest: mixed corpus is REFUSED (proves it is not per-file luck)"
  printf '%s\n%s\n%s\n' "$TMP/fx/good_comment.zag" "$TMP/fx/good_canonical.zag" \
      "$TMP/fx/bad_corrupt.zag" > "$TMP/man2.txt"
  "$SCANNER" "$TMP/man2.txt" "$TMP/empty.allow" > "$TMP/out2.txt" 2>&1
  RC=$?
  sed 's/^/    | /' "$TMP/out2.txt"
  if [ "$RC" != "1" ]; then
    echo "PTR_GUARD SELFTEST: FAILED (mixed corpus rc=$RC, expected 1)" >&2
    exit 1
  fi

  echo "PTR_GUARD SELFTEST: PASS (5/5 cases behaved as preregistered)"
  exit 0
fi

# ----------------------------------------------------------------- main scan
[ -n "$ROOT" ] || infra "no root"
[ -d "$ROOT" ] || infra "root is not a directory: $ROOT"
[ -n "$ALLOW" ] || ALLOW="$DEFAULT_ALLOW"

build_scanner

MAN="$(mktemp)"; trap 'rm -f "$MAN"' EXIT
find "$ROOT/docs/lab/research-lead" -name '*.zag' -type f 2>/dev/null \
  | sort > "$MAN"
NFILES=$(wc -l < "$MAN" | tr -d ' ')
[ "$NFILES" -gt 0 ] || infra "no .zag files found under $ROOT/docs/lab/research-lead"

echo "PTR_GUARD: scanning $NFILES .zag files under $ROOT"
echo "PTR_GUARD: allowlist $ALLOW"

ALLOWARG=""
if [ -f "$ALLOW" ]; then
  ALLOWARG="$ALLOW"
  echo "PTR_GUARD: allowlist has $(grep -c . "$ALLOW" 2>/dev/null || echo 0) pin(s)"
fi

if [ -n "$ALLOWARG" ]; then
  "$SCANNER" "$MAN" "$ALLOWARG"
else
  "$SCANNER" "$MAN"
fi
RC=$?
exit $RC
