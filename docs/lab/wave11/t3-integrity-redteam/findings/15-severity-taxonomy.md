# Slice 15 — Red-team severity taxonomy and kill criteria (Track 3, Arm C)

## Slice
Red-team leadership, slice 15: the meta-slice defining severity levels, aggregation rules,
deliverable format, and disagreement rules for all 15 Track 3 red-team findings on Arm C.

## Falsifiable claim
The taxonomy below is complete and correctly calibrated: every red-team finding against the
Arm C build maps to exactly one severity level, the aggregation rule derives the correct
track-level verdict (KILL vs REPAIR-AND-RETRIAL vs GO) from the finding set, and no later
Arm C trial event that compromises a MUST-NOT-vary observable (verdict, memory decision,
integrity refusal, ledger bytes) is ever classified below S1. Kill: a single compromised
MUST-NOT-vary observable classified ≤S2, or any attack class in the build trial that the
taxonomy cannot classify, kills this taxonomy (not the program — the taxonomy).

## Design
Four severity levels, judged against the brief's hard invariant — what MUST NOT vary:
verdicts, memory decisions (kill/pin/promote), integrity refusals, ledger contents.

- **S0 — concept-kill.** Exact criteria: the finding demonstrates that the *design*, not one
  build, cannot hold the invariant — i.e., (a) verdict divergence across expression variants
  of identical (input, state) is reachable by design, not just by one buggy firewall
  (e.g., the two coincident barriers of slices 12/20 are provably defeatable via
  phase-seam timing); (b) memory-op divergence under variation-state perturbation that no
  spec-conforming repair prevents (K4-class); (c) ledger-byte divergence or integrity-trap
  flip attributable to expression-state leakage (K2-class); (d) a self-change weakening
  integrity that passes post-change verification by design (RC precedent class).
  One S0 kills the Arm C *concept*: retire Arm C, report as-is per kill-criteria law.
- **S1 — implementation-kill.** Exact criteria: a working exploit defeats one *build* while
  the prereg'd design survives — the spec is sound, the implementation misapplied it
  (e.g., slice 09's no-RNG auditor catches 20/20 planted sources but misses a deterministic
  unlogged constant the spec's enumeration requires; slice 15's ledger canonicalization
  in 15 drops a VARIATION_CHOICE field). One dated repair + full re-trial allowed; a
  second S1 in the same mechanism → escalated to S0 review.
- **S2 — bruise.** Exact criteria, ALL must hold: (i) attacker influence is confined to
  expression-only observables (phrasing/path/order/depth); (ii) influence is fully logged
  (variant_id + selector_hash in ledger); (iii) influence is detectable by an existing
  auditor (arbitrariness detector 11 or calibration band 21) firing on the trial corpus;
  (iv) zero impact on MUST-NOT-vary observables; (v) no unlogged state created.
  Example: adversarial state shaping (slice 22's class) pushes the phrasing variant
  function to a maximally verbose but lawful register — boring, logged, detected.
  An S2 that evades its designated auditor escalates to S1 immediately.
- **S3 — note.** Exact criteria: plausible attack mechanism argued in writing, but no
  working exploit after a good-faith build attempt within the trial window
  (e.g., "a sufficiently exotic lawful mapping could false-positive the arbitrariness
  detector" — slice 11's blind spot — with no concrete mapping exhibited). Kept on the
  watchlist; two S3s in one mechanism across consecutive trials → review for S2.

**Aggregation rule.** Severities do not sum linearly; they escalate by family and by
auditor-evasion. (1) Three confirmed S2s in the *same mechanism* within one trial epoch
→ aggregate to one S1 (systematic weakness, one repair window). (2) S2s across different
mechanisms stay S2 — do not combine. (3) Any S1 whose repair fails re-trial → S0 review
of that mechanism's design. (4) S3s never aggregate. (5) A single S0 on any
MUST-NOT-vary observable kills the Arm C concept, not just the attacked slice — the
firewalls and sealing are design-level claims, so a design-level defeat is program-arm
level. It does NOT kill committed evidence (RC3, wave5/6, debate) or arms A/B unless
the same finding reproduces against them; the blast radius is Arm C unless the
finding's mechanism is shared, in which case the shared mechanism is quarantined
pending its own trial.

**Disagreement rule.** Severity is proposed by the attacking slice, cross-checked by a
second slice. Disputes settle by reproduction, not argument: the exploit replays
byte-identically on a clean build → the higher severity stands. If still split, escalate
to the coordinator with the full evidence bundle; the tie-break defaults to the higher
severity (red-team errs toward severity). A slice may not downgrade its own finding
after a repair without a passing re-trial.

## Kill bar
This taxonomy is dead (revert to ad-hoc judgment, flag for Micah) if ANY fires: (K1) a
MUST-NOT-vary compromise in the Arm C build trial was classified ≤S2 before the fact;
(K2) an attack class appears in the trial that the four levels cannot classify;
(K3) more than one unresolved severity disagreement per trial epoch survives the
reproduction rule. Repair of the taxonomy needs Micah's re-approval (prereg rule change).

## Honesty notes
Weakest point: the S0/S1 boundary rests on "the spec is sound" — but spec soundness is
exactly what red team is testing, so the boundary can be gamed by writing a permissive
spec; I mitigate by requiring the S0/S1 call to cite the specific prereg clause that
fails. The "3 S2s → S1" threshold is a judgment call, not derived — benchmark it
(no-free-lunch): if it over-escalates noise, loosen to 5; if it misses patterns, tighten
to 2. I am NOT claiming this taxonomy transfers to arms A or B (different invariants),
nor that S3 watchlist items are safe — they are the likeliest source of a future S0.
The honest limit: a taxonomy cannot see an attack class nobody theorized; coverage is
bounded by the 15 slices' imagination.

## Next build step
Before the Arm C build trial starts, run a calibration drill: each of the 15 red-team
slices submits one synthetic finding (drawn from historical wave5/6 and RC rollback
cases with known severity) and the taxonomy must classify all 15 correctly with zero
disagreements surviving the reproduction rule — this tests the taxonomy itself, per K1–K3.
