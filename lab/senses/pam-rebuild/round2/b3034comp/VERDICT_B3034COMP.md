# VERDICT — B-3034COMP: 30+34 composition battery with full Class-J harness

**Crew:** B-3034COMP (PAM round-2 swarm, build crew)
**Date:** 2026-09-24
**Frozen prereg:** `d9e72746` (committed ALONE before code)
**Build:** `ad0e1ddd` (sources committed before runs)
**Battery:** 16 modes × 3 runs, 16/16 byte-identical (RUNLOG_B3034COMP.md)

**Verdict: TESTED-survived (scoped).** The C-3034 composition — H-PAM-30's
full-pin verdict gate as the admission surface + H-PAM-34's interleave/
delay-line protocol as the continuity binding — survives every kill bar,
with scope-carries firing exactly as the frozen prereg named them.

## Per-class numbers vs bars

| Mode | Measured | Bar | Result |
|---|---|---|---|
| honest | promote 120/120, contradicted withheld 40/40 | ≥102/120, 40/40 | PASS (loss 0%) |
| rf_full (a) | promote 0/120, harm 0/120 | 0 | PASS |
| rc_full (b) | false-promote 0/120 | <6/120 | PASS |
| xr_fresh / xr_reuse (c/M) | 0/120 / 0/120, delta 0pts | <6/120, delta <5pts | PASS |
| n_goal (e/N) | promote 120/120, note harm 120/120 | carry | SCOPE-CARRY |
| o_temporal (h/f) | property 120/120, forged-temporal admits 0/120 | 120/120 + 0 | PASS |
| o_numeric (O-num) | promote 120/120, sink divergence 39/120 | ≥5% → carry | SCOPE-CARRY (prereg §6) |
| p_remint (g) | binding-replay 0/120, cross-epoch 0/120 | 0 | PASS |
| j_dump (J-1) | promote 0/120, harm 0/120 | 0 | PASS |
| j_agg (J-2) | 60/120 promoted (60 complete), stuck 0/60, driver fires 0/120; naive aggregate would fire 120/120 | 0 | PASS |
| j_tag (J-3) | high-32 passthrough 0/120 | 0 | PASS |
| k_blind (K) | note-carry 120/120 (= n_goal), driver fires 0/120; naive queue/window aggregates would fire 120/120 | 0 delay-attributable | PASS; carry matches |
| l_distal (L) | promote 120/120, false-vs-true 120/120 | carry | SCOPE-CARRY |
| ge_gap (34b) | gapped-honest promote 120/120, two-verdict promote 0/120 | ≥102/120 + 0 | PASS |

**Falsification check (§1):** the maximum in-scope attack-class firing rate is
0/120 (every attack arm at zero). No class reached ≥97/120. No kill bar fired.

## What the numbers mean

1. **The J battery is green on all three arms — 30's kill site is gone.**
   In B-303134, j30 measured 120/120 dump harm: honest latency forced 80/120
   triaged items into a readable low-tier buffer whose aggregate drove a
   high-stake sink. The composition has no readable buffer — the triage flood
   waits in a write-only presentation queue and the provisional window is
   structurally inert (the promotion gate is the only sink call site).
   j_dump: 0/120 harm on the full poisoned flood.
2. **j_agg (T-A j-comp form):** 60 verdict-green items completed K=3 and
   promoted; 60 gapped items sat stuck in the window. Driver sink fires 0/120;
   the naive window aggregate over the same content would have fired 120/120 —
   the arm had teeth, the path does not exist.
3. **j_tag (J-35 form):** the composition's verdict binding hashes full 64-bit
   field values; high-32 substitution on a genuinely-bound verdict rejected
   120/120. The J-35 tag-binds-low-32 death does not transfer.
4. **ge_gap resolves 34's both-ways bar (b):** the delay line DELIVERS gapped
   honest items (120/120, vs 34's ge_closed 0/120) while still requiring all
   K=3 verdicts — 2-of-3 promotes 0/120 (vs ge_open's gap-riding). Waiting
   beats fail-closed on honest latency without opening the gap to RC×RF.
5. **o_temporal:** every promotion cites K=3 distinct verdict objects, each
   recorded before its epoch's decision (120/120); forged-temporal objects
   (recorded after the decision) promote 0/120. The interleave protocol
   actually executes in the composition driver (the B-3536 failure is not
   repeated).
6. **k_blind:** the delay line adds no new detector-blind harm — driver fires
   0/120 while the naive queue/window aggregates would fire 120/120; the
   note-carry (120/120) matches n_goal exactly, i.e. the N-carve is unchanged
   by composition.
7. **o_numeric 39/120 → preregistered SCOPE-CARRY** (prereg §6, frozen before
   the build): the tolerance-width residual is a property of the named pin
   parameter TOL_C=10 against the sink's own conf≥95 threshold, not a false
   admission. It does not kill and is excluded from falsification, as
   preregistered. No post-hoc carving occurred.

## Residuals and scope notes (carried, not killed)

- **Tolerance-width carry:** 39/120 sink divergence at the ±10 pin edge —
  standing scope note for any full-pin verdict design (same 39/120 as
  o30n/o34n in B-303134).
- **Goal-set carry:** `note` ∉ G rides with verdict-green percepts (120/120);
  unchanged by the delay line (k_blind confirms).
- **Distal carry:** corrupted world-spec S′ → verdicts truthful of the
  corrupted world promote 120/120 vs the true world, per the scope contract.
- **Honest-latency cost:** at CAP=40 verdicts/epoch, 120 items complete in 9
  epochs (vs 30's single pass, 34's 3 epochs). Honest loss is 0% — the cost is
  latency, not loss. The delay line is the mechanism that converts 30's
  triage-dump kill site into a wait.
- **Adversary-model note:** the verdict oracle stands in for the principal
  (the same bound as B-303134's `tror`); the battery tests the anti-RF/RC/XR
  properties, not a real trainer's discrimination.

## Backlog updates (applied)

- H-PAM-30: DEMOTED to composition-only → composition C-3034 with H-PAM-34
  TESTED-survived (scoped), B-3034COMP 2026-09-24.
- H-PAM-34: DEMOTED to "H-PAM-30 with a delay line" → composition C-3034
  TESTED-survived (scoped), B-3034COMP 2026-09-24.
- New line: H-PAM-3034COMP | TESTED-survived (scoped) | 30+34 composition
  (full-pin verdict gate + interleave/delay-line binding); full Class-J
  harness green (j_dump/j_agg/j_tag 0/120); K/L/M/N/O/P per frozen classes;
  o_numeric 39/120 preregistered SCOPE-CARRY; falsification 0/120 max.
  Evidence: prereg d9e72746, build ad0e1ddd, this verdict.
