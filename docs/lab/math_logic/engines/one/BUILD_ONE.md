# ONE ENGINE — Build Report

## Source files (committed)
- `engines/common/cx_str.zag` — byte/string helpers, FNV-1a-64.
- `engines/common/cx_claim.zag` — canonical claim parser/tree/printer. Node =
  7xi32 in a []u8 arena (ZNC-007-safe). Kinds: CONST/APP/VAR/NOT/IMP/AND/OR/
  FORALL/FALSE. start/len = full source span; aux = head (CONST/APP), binder
  (FORALL), varnum (VAR).
- `engines/common/cx_match.zag` — match-and-bind (CXB), substitution, UI
  universe walk, `cx_match_bvar` (named-CONST-as-variable for backward UI).
- `engines/common/cx_store.zag` — claim store (canonical bytes + audit +
  depth + kind), structural contradiction (adding F while not(F) present
  derives `false` via CONTRA).
- `engines/common/cx_schemas.zag` — committed schema bytes/hashes, startup
  assertion (exit 6 on mismatch).
- `engines/common/cx_io.zag` — sealed-path guard (exit 3), .form parser,
  structured store parser.
- `engines/common/cx_fwd.zag` — shared forward core: ONEP patterns,
  one_mp/one_ui/one_pbc_direct, one_bfs, one_pbc_for.
- `engines/one/one.zag` — ONE main: one_emit, one_run, main (3x determinism).

## Design (per frozen prereg §3)
- One core operation: match-and-bind.
- Deterministic BFS by depth (bound 8; bound 16 only for B6).
- Stop on target derived, fixpoint, or bound.
- Referee: derive target (forward + PBC subproof); derive not(target)
  (forward + PBC subproof). WITHHELD unless exactly one derived.
- Confidence: 1 iff derived/refuted, 0 iff WITHHELD. No numeric evidence.
- Full audit: every claim cites schema + premise/binding chain.

## Build
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- CWD must be `engines/one` (imports resolve relative to CWD).
- Command: `znc_linux_x86_64_abed8aa1 one.zag --no-zagd --no-analyze --no-foreground-cache -o one_bin`
- Pure Zag, zero RNG. 3x in-process reruns, byte-identical asserted (exit 5
  on divergence).

## CEREMONY DEFECT #1 (reported, not silently edited)
`COMMIT_SCHEMAS.md` lists S_PBC's hash as the 17-char string
`0369efe53016bbe1a` (spurious leading zero; not valid 64-bit hex). The true
FNV-1a-64 of the committed canonical bytes is `369efe53016bbe1a` (16 chars).
The engine asserts the true value; canonical bytes are unaffected and verified
correct. The committed document is preserved as-is per ceremony terms.

## Smoke results (2026-09-25)
- P01-FORMAL (≤3-step MP): DERIVED, conf=1.
- SMOKE01 (MP): DERIVED. SMOKE02 (open): WITHHELD. SMOKE03 (refutation):
  REFUTED. SMOKE04 (PBC subproof): DERIVED.
- Sealed guard: exit 3 on `sealed` path.
