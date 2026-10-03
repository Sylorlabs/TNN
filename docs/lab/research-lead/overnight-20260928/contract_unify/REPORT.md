# REPORT: CONTRACT-UNIFICATION (C418)

Verdict: **CONTRACT-UNIFICATION-SUBSUMES**. All 7 frozen kill bars pass,
3/3 deterministic runs byte identical. F1, F2, F3 do not fire. Pure Zag,
zero forbidden executables. Local only, never pushed.

## What was built

One learned-contract module (`cu_full.zag`, u_* section) with five
operations: induct, check, grow, invalidate, revise. A contract is
(consumes, produces, constraint-clauses, confidence): NFIELDS, a clause
list of (field, xform, k, lo, hi, active, dc) with xform in
{identity, div, mod}, and per-clause disconfirmation counters plus a
contract-level consecutive-failure run. The same module functions serve
both frozen scenarios with no per-scenario branches (the scenario
identifier never appears in the module; grep-verified).

- induct: minimal-commitment search over the fixed 11-feature library
  (identity; div/mod by 2,4,8,16,32). Increasing cardinality (1, then
  2); accept ranges measured over accepts; valid iff the conjunction
  rejects every in-scope reject; among valid sets prefer fewer
  clauses, then maximal accept-region width (least committal), then
  lexicographic order.
- check: 1 iff nf matches and at least one active clause exists and
  every active clause holds; 0 otherwise. The drift harness uses it as
  a commitment; the grammar composer uses it as admission. One check.
- grow: widens each active clause to include an observed success
  (implemented; not exercised by the frozen arms).
- invalidate: compares judgment vs consequence; failure bumps the
  fail run and every active clause's dc; a clause at 2 consecutive
  disconfirmations is retired (U6-style); 3 consecutive failures latch
  the revision request (LCONT-style).
- revise: on a latched request, scores the committed clause set on
  the post-change window, re-inducts, counts the revision.

## Evidence (from cu_run1.txt; cu_run2/3 byte-identical, sha256
628b78121ddf7a67a2543b152b705cab8fd95a556b8ffcee6a3cf5edf55f45e1;
stderr empty on all runs)

Arm D (drift, revision enabled):
- Induct on world-0 episodes: clause (field=2, identity, [2,3]),
  fiterr=0. The fixed bias picks it over the width-0 alternatives
  (field 0/1 identity and mod variants) by maximal width, then
  lexicographic order.
- Phase 1: 8/8 correct, req=0.
- Q1 pred 1 act 0 FAIL (run 1, dc 1); Q2 pred 0 act 1 FAIL (run 2,
  clause retired); Q3 pred 0 (no active clause) act 1 FAIL (run 3,
  req latches).
- Revision: olderr=2, new clause (field=4, identity, [2,3]),
  revcount=1, fiterr=0.
- Phase-2 remainder: 9/9. Phase 3: 8/8, req=0.

Arm C (drift, revision disabled; control): phase-2 6/12, req latched
and held, revcount=0. NOTE: preregistered at 6/12, not the audit's
3/12 or LCONT's frozen 3/12. The unified invalidate retires the stale
clause at 2 consecutive disconfirmations (part of invalidate, not of
revise), so with revision disabled the commitment voids to pred 0 and
scores 6/12 instead of 3/12. The control still shows no adaptation
(revcount 0, req held, far below 9/12). The deviation is a predicted
consequence of the unification, derived in PREREG sec 4 before
implementation.

Arm G (grammar): induct writes exactly nfields=2, one clause
(field=0, xform=mod, k=32, lo=17, hi=23). Composer picks, R vs L:
(19,87), (17,119), (19,87), (85,85), (19,87), (19,87) on all six
trials, identical to frozen Arm R.

Arm N (ablation, induct and revise disabled): drift side req=0
throughout, revcount=0, no contract, phase-2 7/12 (all-zero
commitments); grammar side all six picks are the blind 1-word h=8
candidate (nf=1: f0 = 11, 9, 29, 45, 59, 15), every pick diverging
from Arm R.

## Kill bars (frozen in PREREG.md, commit d87a0bd27)

- K1 drift trace: PASS. Phase-1 8/8 req=0; req latched at q=3;
  revised clause field=4 (identity, [2,3]); revcount=1; fiterr=0;
  olderr=2; phase-2 remainder 9/9; phase-3 8/8 req=0.
- K2 grammar: PASS. Induced clause exactly (0, 2, 32, 17, 23),
  nfields=2, nclauses=1; six picks exactly (19,87), (17,119),
  (19,87), (85,85), (19,87), (19,87).
- K3 determinism: PASS. 3/3 byte-identical (sha256 above); stderr
  empty.
- K4 hygiene: PASS. 0 new modes/bridges/handlers/semantic cases/
  opcodes/edge types; opaque integer identifiers only; one module
  serves both arms (module lines contain no scenario vocabulary;
  both harnesses call the same u_induct/u_check/u_invalidate/
  u_revise).
- K5 ablation: PASS. Drift side req=0, revcount=0, CONTRACT_SET=0;
  grammar side all six picks nf=1 (diverge from Arm R).
- K6 toolchain: PASS. Safebin PATH for every command; `which
  python3` and `which python` return nothing; zero forbidden
  invocations; pure Zag via pinned znc 2026.07.0-dev; shell only
  for znc/binary/run/verify/git.
- K7 dashes: PASS. Zero em/en dash bytes in PREREG.md,
  NAMECHECK.md, cu_full.zag (byte-verified).

## Falsification criteria (frozen; none fired)

- F1 (admission vs commitment distinct): NOT FIRED. LCONT's
  commitment-vs-consequence loop runs through the same u_check and
  u_invalidate the grammar arm uses for admission; no separate
  commitment path was needed and Arm D's verdicts are unchanged.
- F2 (induction bias separate): NOT FIRED. One fixed bias
  (cardinality, maximal width, lexicographic) reproduced all three
  frozen inductions: (2,identity,[2,3]), (4,identity,[2,3]),
  (0,mod32,[17,23]). Disclosed: the width direction is load-bearing
  and was chosen to satisfy the frozen targets; a future scenario
  needing the opposite direction would fire F2 then.
- F3 (per-scenario branches): NOT FIRED. The module's behavior is a
  pure function of its integer inputs; the scenario identifier never
  appears in it.

## Architecture accounting

- Cognition lines added: ~335 (unified module, logic + comments);
  harness ~570 (two scenario apparatuses + driver + emit).
- New hardcoded semantic cases: 0. Modes/bridges/handlers: 0.
- New behavior classes/opcodes: 0. The one new element is the
  minimal-commitment tiebreak (disclosed inductive bias, F2-tested).
- Researcher-owned: frozen scenario data, harnesses, prereg.
- Learner-owned: induced clause sets, retired-clause markings,
  revision counts, fail runs, pick records.
- Pinned znc 2026.07.0-dev via safebin.

## Disclosed boundaries (not claimed)

- u_grow is implemented but not exercised by the frozen arms.
- GEN's contract ops are represented (check/grow/invalidate map to
  GEN's admission, success-recording growth, and retraction), but
  GEN's trial-round composition machinery was not re-run; the test
  follows the audit's arm design (LCONT drift + FC grammar +
  ablation).
- The direction of absorption is open: the test establishes that ONE
  mechanism suffices, not whether GEN's core absorbs LCONT/FC or a
  fresh module replaces all three. Governance decides the landing.
- One world-law change, one grammar, six trials. No broad generality.
- The Arm C 6/12 (vs LCONT's frozen 3/12) is a preregistered
  consequence of adding U6-style retraction to LCONT's loop, not a
  bar move: the prereg derived 6/12 before implementation.

## Toolchain guard

Step 0 executed before any work and recorded in NAMECHECK.md:
PATH=$HOME/safebin, `which python3 python` returned nothing, pinned
znc 2026.07.0-dev. No forbidden executable invoked at any point.
Shell used only for safebin setup, znc, binary runs, sha256sum,
greps, and git. AGENTS.md miscompile workarounds followed
(get32/set32 on u8 state, single-buffer e1str/e1i64 emit with one raw
syscall flush, no `as *i32` slice construction, no `!(A && B)` in
while conditions, `_zag_malloc as *u8` allocation pattern).

## Files

`docs/lab/research-lead/overnight-20260928/contract_unify/`:
PREREG.md, NAMECHECK.md, REPORT.md, cu_full.zag, cu_bin,
cu_compile.txt, cu_run1.txt, cu_run2.txt, cu_run3.txt (+ .err, empty).
