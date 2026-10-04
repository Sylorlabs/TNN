# RESULT: LEARNER-INTEGRATION-PASS

Date: 2026-09-30 PDT. Worker: Continuing-Learner Integration Worker.
Prereg: PREREG_INTEGRATION.md (c6288274d), frozen before implementation.
Implementation: integrate_learn.zag (1095 lines, pure Zag, u8-backed cells).
Raw output: INTEGRATION_RAW_OUTPUT.txt (sha256
55bc37380a752b3a8659208d8c5ed75567c6979a91e3fe9956cd091bcbcf6e59).

## Verdict: LEARNER-INTEGRATION-PASS (bounded L2)

One learner binary, one persistent state (single 32768-byte W; stress
store in W[0..8192], DDES ledger as the slice W[16384..32768]), one
process, one main(), no resets. It runs the frozen 8-phase stress
lifetime, then encounters causal ambiguity (P9), resolves it by adaptive
intervention, persists the outcome as learner state, and reuses it after
a third pressure wave (P10) under the recency-guarded earning discipline.

## Kill bars

K1 (prereg strictly precedes implementation): PASS. Prereg committed
alone as c6288274d; implementation committed after; verified by
`git merge-base --is-ancestor c6288274d <impl>`.

K2 (no regression + new capability): PASS.
- Regression: P1-P8 output byte-identical to the committed baseline
  STRESS_RAW_OUTPUT.txt at daa9bf2fc (verified by cmp). This entails
  P1_RECALL 8/8, P4_CORR 5/5 and 5/5, P4_COLL 0/12, P5_CORR 4/4,
  P5_RECALL 8/8, P6_TWOHOP 5/5, P8_RECALL 8/8, P8_CORR 2/2,
  FOUND_EVICT 0, and P1-P8 STATEHASH ticks 16,64,108,153,201,211,231,241.
- C1: P9_RESOLVED winner=2 rounds=2 status=1. ADAPT chained two
  genuinely different interventions (round 1 TARGET V*=1 PLAN
  [S,W,O(1)] eliminated h0; round 2 TARGET V*=2 PLAN [S,W,W,O(2)]
  eliminated h1; winner h2).
- C2: P10_CAUSAL 3/3. The three persisted causal facts (winner,
  rounds, round-1 elimination) retrieved correctly after P10's
  20-item pressure wave. Delayed reuse of intervention-derived
  knowledge through pressure.
- C3: P10_FOUNDATION 8/8 and P10_CORR 2/2. No regression from the
  causal episode or the third wave.
- C4: EARN_SKIPPED 519. The recency guard is active in the composed
  learner: earn_guarded skipped the highest-subj survivor (the most
  recent arrival). Efficacy (9/10 across 3 episodes) cited from the
  closed retention lane RECENCY-GUARD-CONTAINED, not re-proven.

K3 (pure Zag, determinism, hygiene): PASS. Zero Python at every step
(pinned znc build; shell/grep/awk/cmp/sha256sum analysis). 3/3
byte-identical runs (sha256 above), exit 0, zero stderr. No em or en
dashes (shell-only check_no_dash.sh). STATEHASH P1-P10 ticks strictly
increasing (16..292). u8-backed cells only; no `as *i32` slices.

## With/without comparison

| Measure | Pre-DDES baseline (daa9bf2fc) | Composed learner |
|---|---|---|
| P1_RECALL | 8/8 | 8/8 (byte-identical) |
| P4 corrections | 5/5, 5/5; coll 0/12 | identical |
| P5 corrections/recall | 4/4, 8/8 | identical |
| P6 two-hop | 5/5 | identical |
| P8 recall/corr | 8/8, 2/2; evict 0 | identical |
| Causal ambiguity | N/A (withheld only) | resolved by intervention, winner=h2, 2 rounds |
| Delayed causal reuse | N/A | 3/3 after pressure |
| Post-P8 foundation/corr | N/A | 8/8, 2/2 |

No regression on any frozen bar; the composition adds the causal
intervention loop and its persistence, which neither part had alone.

## New compositional capability

The learner encounters the frozen M1 ambiguous causal case DURING the
continuing lifetime (after 8 phases of vocabulary, corrections,
interference, and pressure), detects AMBIGUOUS from passive evidence,
constructs and executes two adaptive interventions conditioned on real
outcomes, resolves to h2, writes the outcome into its own rule store
as three earned facts, and retrieves all three after a further
20-item pressure wave. Neither the stress learner (no intervention)
nor the DDES planners (no lifetime, no pressure, no persistence) did
this.

## Implementation notes (honest)

- During the first build, P10_CAUSAL was 0/3: 20 evictions reached the
  importance-11 tier where minimally-earned causal facts sat tied with
  older items at lower indices. Fixed by earning each causal fact 3x
  in P9 (importance 31), matching the battery's own P2 earning
  discipline. The prereg froze the outcome (3/3) and the mechanism
  (earn immediately); the query count was an implementation detail.
- The DDES `query` was renamed `dquery`; the revert `i64s` (newline
  stripping) was renamed `i64s_ddes` to preserve DDES emit behavior
  while keeping the stress `i64s` for store hashes. All other
  functions verbatim from the frozen sources.
- Scope: bounded L2. Candidate graphs are researcher-supplied; the
  learner authors the chaining, targets, and persistence, not the
  hypothesis space. Pipeline steps 4-11 not run on the composition;
  no SURVIVES claim, no L3 claim.

## Recommended next integration target

Port the C1 law-revert fix into this same learner: P9 currently covers
the M1 ambiguity family, but the composed learner has no defense
against the C1-pathology (monotonic retirement across changing laws)
demonstrated by REVERT-ADAPT-PASS's STATIC mode. The concrete step is
a P11 episode using the frozen R1 change-then-revert case (true phases
G0,G1,G0) inside the lifetime, with the bar that ADAPT re-derives h0
post-revert (1 round) while a STATIC control inside the same binary
shows the pathology. Rationale: the "one continuing learner" mandate
requires surviving law change, not just resolving static ambiguity,
and the R1 case plus both modes are already frozen and validated, so
this is pure composition with no new mechanism risk.
