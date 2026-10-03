# H5R2 Implementation Record: trial-loop provenance gate

Lane TNN3H5R, wave-20261001-2321pdt. Implements the frozen prereg
PREREG_H5R2.md (commit dc7df4aba1db84e71e3e0b61c84adbf77244e590,
coordinator rulings Q1-Q5 all CONFIRM) section 4 exactly. Pure Zag,
safebin toolchain, no forbidden executables (KB-P1 clean).

## Ordering and base verification (NC-7R2)

- Prereg freeze commit: dc7df4aba1db84e71e3e0b61c84adbf77244e590
  (2026-10-02 06:30:12 UTC), committed alone. Implementation files in
  this lane were created after: tnn3_h5r2.zag (base copy 06:3x UTC,
  edits after), tnn3_h5r2.bin built after the edits. No implementation
  artifact predates the prereg freeze.
- Base: docs/lab/rsi/runs/wave-20261001-2021pdt/TNN3H5R/tnn3_h5r.zag at
  commit 830f95ab7. Worktree copy byte-identical to the git blob,
  SHA-256 d98d08f0746cab4fef88fb062933a314c12492f78ee98b496e8d8912cd7fd384
  (matches the frozen record in PREREG_H5R.md section 3 and
  SEALED_H5R.md).
- Working file tnn3_h5r2.zag created by byte-copy; copy SHA-256 verified
  identical to the base before any edit.

## Changes (prereg section 4, exact)

Hunk 1: added t2_prov_ok before t2_try_verify (9 non-blank non-comment
lines). The gate returns 0 if any licensing fact is not live, not
tag-1, or superseded; 1 otherwise. Uses only existing field reads
(ng/get32) and the existing is_superseded predicate.

Hunk 2: the four t2_trial promote sites gated in place (modified lines,
no lines added):
- chain path: `&& t2_prov_ok(W,f,k)==1`
- sum path: `&& t2_prov_ok(W,ff,c)==1`
- count path: `&& t2_prov_ok(W,f,len-1)==1`
- single-hop path: `&& t2_prov_ok(W,f,1)==1`

Nothing else changed: activate, promote_graph, ev_teach_in, ev_teach,
ev_observe, ev_query, ev_act, miss_inquire, mp_run, t2_try_verify,
t2_gather, t2_gather_sum, t2_chain, bid, ref_prot, is_superseded,
supersede, resolve_uncertainty, revise_on_contradict, the 4-op ISA and
execute are byte-identical to the base.

## Build (pinned znc src/tools/toolchain/znc_linux_x86_64_abed8aa1)

- tnn3_h5r2.bin SHA-256:
  19dcf2e4436079a4ab6f9cf48b2b6a556f743d0ed1d9d16102249cd5ac970287
- 3/3 byte-identical builds (same SHA-256 across three znc
  invocations). Only compiler warnings (A0102 ignored-return-value,
  pre-existing style), no errors.
- Built-in battery: 46/46 PASS (identical to the H5R base battery).
- Binary stdout 3/3 byte-identical across runs.
- Grep of the incremental diff for time/clock/random/rand/seed/PID:
  none.

## KB-S1 self-check (substrate gate)

The working diff against the verified base contains the H5R activate
hunk and the H5R promote_graph hunk (inherited in the base, byte
verified), plus the new t2_prov_ok helper and the gate at all four
t2_trial promote sites (5 occurrences of t2_prov_ok: 1 definition + 4
call sites). KB-S1 SATISFIED on the working tree. The evaluator
re-verifies on the committed diff before assembling any sealed world.

## KB-G1R self-check (architecture accounting)

- Added cognition lines (non-blank, non-comment): 9 (the t2_prov_ok
  helper; the four gate sites are modified in place). Budget <= 15.
  PASS. Removed lines: 0.
- New modes: 0. New bridges: 0. New routers: 0. New handlers: 0. The
  gate is a candidate-admission predicate over existing node state.
- Core-ISA additions: 0. Only existing field reads, COMPARE, and the
  existing is_superseded predicate.
- Forbidden protected semantic operations (FIND_POLYNOMIAL_ORDER,
  DETECT_NEGATION, BUILD_CAUSAL_RULE, LEARN_PROCEDURE, FIND_THRESHOLD,
  MAKE_CONDITIONAL): none present in the diff.
- Cumulative vs the TNN-2 base: reported in the sealed eval.
- KB-G1R: PASS.

## Unsealed smoke worlds (NOT sealed; keys 9xxx, disjoint from any
sealed battery)

Driver /tmp/h5r2_smoke.zag (scratch, not a deliverable): byte-copy of
tnn3_h5r2.zag with a smoke main exercising the provenance fix.

- Revert probe: teach (9010,9101,9020), (9020,9102,90301); query MAP key
  (9010,9201) with expected 90301 (promote, t1live=0); OBSERVE
  (9020,9102,90302); query expects 90302; OBSERVE (9020,9102,90301);
  query expects 90301. All correct.
- White-box: exactly 1 live MAP on the key, exactly 2 superseded MAPs,
  all DEP edges of the live MAP target live tag-1 non-superseded facts
  (dep->2 sup=0, dep->36 sup=0). The stale-provenance failure mode from
  the killed battery does not occur.
- Chained probe: teach; query c0; OBSERVE c1; query c1; OBSERVE c2;
  query c2; OBSERVE c0 (revert); query c0. All correct. White-box:
  exactly 1 live MAP, exactly 3 superseded MAPs, all DEP edges target
  live facts (dep->2 sup=0, dep->66 sup=0).
- SMOKE PASS. 3/3 byte-identical stdout across runs
  (529e4e4ed038974d23f0046f711f8753ec9f8bc04ec9031442de1ad947b4d48c).

## Deviations from the prereg

None.

## Process (KB-P1)

PATH was $HOME/safebin for every command. `which python3` printed
nothing (exit 1) at lane startup (recorded in NAMECHECK.md Step 0).
Shell invoked only: the pinned znc, built binaries, git read-only ops
(log/show/status/diff), and file copies. Zero forbidden-executable
invocations. No push. No files written outside the lane directory and
/tmp scratch. The sealed world files were not assembled or run; the
driver template was written pre-freeze and hashed in the prereg
(f2d60568f55aef62d27d260a7ca3966933738b864b645e6c1e5e1cbfa1ea20af);
no world output was used to tune the substrate.

## Readiness

READY FOR SEALED EVALUATION. The provenance gate is implemented exactly
as pinned in prereg section 4; the base is verified byte-for-byte
against the frozen H5R record; the binary is frozen at SHA-256
19dcf2e4436079a4ab6f9cf48b2b6a556f743d0ed1d9d16102249cd5ac970287 with
3/3 byte-identical builds; KB-S1 and KB-G1R self-checks pass; the
unsealed smoke demonstrates the fix (revert and chained reverts anchor
DEP edges to live facts; zero tag-1 facts on the MAP key at every
step).
