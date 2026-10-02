# Preregistration: TNN-1 ACT 24/24 Remediation Port

Date: 2026-09-30. Status: FROZEN (design only, no implementation in this commit).

## 1. Background and mandate

The integration prereg (`7fc7148ac`), P-INT2, requires:

> the integrated binary passes ACT's 24/24 tests (P-ACT1 planning,
> P-ACT2 inquiry, P-ACT3 null policy, P-ACT4 ablation, P-ACT5
> generality, P-ACT6 memory prerequisite), all in one process, with
> the directional bid. No test changes from the aligned ACT.

K4 references P-INT2 as (24/24).

The TNN-1 build (`0323b97d5`) shipped a compact 6-test ACT battery
(t_a1..t_a6, tnn1.zag lines 865-912) instead of the 24/24. The ACT
coverage assessment (`4b36f0c1e`) maps the compact battery against the
standalone suite: 3 of 16 unique checks fully covered, 1 partial,
1 weak, 11 not covered. The uncovered checks include the planning
claim (P-ACT1 state-varying emission and D1 derivation), the no-bleed
claim (P-ACT2 decoy/other), the honesty claims (P-ACT4 no-goal and
fact-alive), and the retention negative half (P-ACT6A eviction under
pressure).

As it stands, K4's P-INT2 (24/24) line is not literally satisfied.
This remediation fulfills the existing frozen P-INT2 requirement. It
does not modify the integration prereg.

## 2. Scope of the port

The remediation ports the full standalone ACT suite
(`act_build/act.zag`, 614 lines, aligned ACT after the bid fix) into
the TNN-1 integrated binary:

- All 23 `ptest` checks, with identical names and identical expected
  values: P-ACT3 null-root (1), P-ACT1 (5: s1->10, s2->11, s3->10,
  3 guides, D1 derivation), P-ACT2 (3: uncert->20, decoy->21,
  other->0), P-ACT4 (4: pre s1->10, no-guides->0, no-goal->0,
  fact-alive), P-ACT5 (generality: identical act_event handler serves
  both classes), P-ACT6A (2: pre s1->10, post->0), P-ACT6B (1:
  post s1->10).
- The ALL-PASS banner, so the run emits 24 lines containing "PASS".
- The standalone scaffolding mapped onto TNN-1 conventions:
  `mk_fact`, `mk_goal`, `mk_guide`, `mk_uncert`, `derive_d1`,
  `evict_to_cap` become TNN-1 workspace operations on the shared
  `W:[]u8`; `act_event` becomes `ev_act`; edge types are TNN-1's
  (ET_DEP=1, ET_SUP=2, ET_CON=3, ET_USE=6, ET_CFM=7, ET_MEM=10).

"No test changes" means: no change to what the tests assert (names,
expected values, properties under test). The eviction invoked by the
ported P-ACT6A/P-ACT6B is TNN-1's real 3-step directional routine,
not the standalone's test stand-in; the standalone RESULTS.md
documents the stand-in explicitly, and the integrated binary is the
mechanism under test. The port is strictly more informative than the
original for the retention claim.

The six existing compact tests (t_a1..t_a6) are retained; the port
adds the missing checks alongside them. The integrated binary then
carries the full 24/24 plus the compact extras.

## 3. Frozen predictions

- R-ACT1: the remediated binary passes all 24/24 ACT checks in one
  process with the directional bid, byte-identical output across
  3 runs.
- R-ACT2: the ported P-ACT6A exercises TNN-1's real 3-step eviction
  (unevidenced guides evicted under pressure); P-ACT6B confirms
  evidenced guides survive the same pressure.
- R-ACT3: no new core operations, modes, bridges, handlers, or
  semantic cases are introduced by the port. The port is test
  scaffolding plus calls into the existing `ev_act` machinery.
- R-ACT4: the final integrated source line count is reported
  against the frozen 1200-line F-INT1 ceiling.

## 4. Kill bars

- K1 (ordering): this prereg commit strictly precedes any
  remediation implementation commit. An implementation commit whose
  ancestry does not include this prereg fails review.
- K2 (purity): pure Zag plus shell orchestration only. Zero Python
  or other implementation languages at every step. The Worker
  Toolchain Guard applies literally: any forbidden invocation is
  wave-level PROCESS-FAIL.
- K3 (fidelity): every ported ptest keeps its standalone name and
  expected value. Any renamed, re-valued, or dropped check fails
  the remediation.
- K4 (determinism): 3 runs byte-identical (sha256 recorded).
- K5 (ceiling interaction): the final line count is measured and
  reported. If the remediated binary exceeds the frozen 1200-line
  F-INT1 ceiling, the remediation reports the overage as a finding
  against F-INT1; the ceiling is not waived and not retroactively
  altered.

## 5. Falsifiers

- F-RACT1: any of the 24 checks fails on the integrated binary
  while passing standalone. The failure is reported with the exact
  check name and observed vs expected values; the port does not
  paper over it by adjusting the test.
- F-RACT2: the port requires a new mode, bridge, handler, or
  semantic case to pass. The requirement is reported and the
  remediation stops; One-System Rule violation.
- F-RACT3: the ported P-ACT6A passes only by reintroducing the
  stand-in eviction instead of TNN-1's real routine. The retention
  claim must be tested against the integrated mechanism.

## 6. Controls

- C1: the standalone `act_bin all` 24/24 result is re-run as the
  reference; the ported checks must agree check-by-check.
- C2: the existing 6-test compact battery still passes unchanged
  after the port (no regression in the shipped tests).

## 7. What this prereg does NOT authorize

- No implementation in this commit. The implementation worker builds
  only after review.
- No modification of the integration prereg (`7fc7148ac`). P-INT2
  and K4 stand as written; this remediation fulfills them.
- No new core execution operations, even if the port proves
  awkward. Awkwardness is reported; F-RACT2 decides.
- No changes to the ACT standalone source. The standalone is the
  reference; it is read-only for this wave.
- No sealed FW1-FW9 access at any step.

## Verdict: ACT-REMED-PREREG-FROZEN (design only).
