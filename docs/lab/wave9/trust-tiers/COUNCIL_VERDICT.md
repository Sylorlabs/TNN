# Trust-Tiers Council — Verdict

**2026-09-20. The council debated all 7 open questions in PREREG_TRUST_TIERS.md §11.**
Nothing was run and nothing was implemented — the prereg remains DRAFT awaiting Micah's approval.
Four debater subagents argued both sides of every question against the existing evidence
(wave-5 `redteam-rt2/DEFENSE.md` §2–§4, the 35/35 corroborated-elimination results, integ-1 trial
logs and results). Where a fork could be settled by re-examining existing evidence, it was.
Where it needs a real trial, that is stated.

## Q1 — Tier ordering: approve T0 > T1 > T2 > T3 with the required leg {T0, T1}?

**The fork:** approve the prereg's ordering (direct observation outranks trainer marks), or put the
trainer above observation.

**What the evidence says:** This is not a new question — wave-5's DEFENSE.md §4 already ordered
the tiers this way deliberately: "Tier-1: an independent task sensor (narrow, honest by
construction, separate from the trainer). Tier-2: the trainer scaffold (±1, spoofable)."
Campaign A2 ("trainer channel compromised") only makes sense if T0 stands above T1 to disagree
with it. The prereg's own §5.4 (learner-initiated channel distrust when T1 disagrees with T0)
only coheres if T0 is the reference leg.

**Council recommendation: approve T0 > T1.** Reversing it now would silently void A2's design
basis. One correction: the prereg's fallback ("if Micah rules trainer-above, the required leg
becomes {T1}") is dangerous as written — spoofed-T1 plus one colluding T3 would then satisfy
the gate, legalizing A5 corruption. If the trainer ever outranks, the required leg must stay
{T0, T1}, not collapse to {T1}.

**Needs a trial to settle:** the broken-sensor blindness case — T0 honestly-wrong vs trainer
correct — is untested by A1–A6. A measurement cell for it should be added before T0 > T1
becomes standing law.

## Q2 — Is "T0 honest by construction" the permanent v1 boundary?

**The fork:** keep the boundary as law, or run a T0-spoof stress cell.

**What the evidence says:** DEFENSE.md §4 names this a non-goal explicitly: "turtles all the way
down; trust must bottom out in something the adversary cannot write to, and the ledger must show
where it bottoms out." Spoofing T0 doesn't test the mechanism — it dissolves the thing being
tested, and §8's INVALID-on-T0-fabrication rule would fire on the architecture, muddying RETIRE.

**Council recommendation: keep the boundary as law for the pass/fail battery — but add a
measurement-only T0-spoof cell** (carved out from the INVALID rule) with no REDESIGN/PROMOTION
triggers. It tests the one claim that survives bottom-failure: "the system may lose loudly,
never silently." Does spoofed-T0 produce COLLUSION_SUSPECT/CHANNEL_DISTRUSTED audits and
contained degradation, or silent corruption? That is measurable without making bottom-failure a
kill criterion.

**Needs a trial to settle:** the loud-vs-silent degradation profile under T0 spoof — unknowable
by argument.

## Q3 — Freeze semantics: freeze until trainer/T0 resolution, or bounded auto-lapse?

**The fork:** unbounded freeze (as written) vs a bounded freeze that auto-lapses.

**What the evidence says:** Both sides have real teeth. Unbounded freeze gives the A3 adversary
a cheap pinned-memory weapon: ~2 forgeries per window to freeze any memory the trainer never
sees, for the whole run. Bounded freeze is a scheduled vulnerability — a timer is not evidence,
and the defense would depend on *when* the adversary attacks rather than *whether*.
The debater also found a real inconsistency in the prereg: §7's "post-attack recovery" metric
(episodes from attack end to normal gate operation) *never converges* under the unbounded
freeze when no T0/T1 observation arrives — the metric's own definition presumes a freeze that
can end without one.

**Council recommendation: bounded freeze with decay and reset.** The freeze lapses after L
episodes (recommend L = W) *only if* the colluding sources have not re-offended; re-fabrication
resets the clock. On lapse, citations still have to satisfy the §5.1 gate, so the attack cannot
"resume" into a kill — only into further refused citations that re-trigger COLLUSION_SUSPECT.
Cheap pinning is bounded to L episodes per fabrication round; the corruption path stays gated
regardless. Either way, §7's recovery metric needs repair — it is currently unmeasurable in
exactly the case the adversary can engineer.

**Needs a trial to settle:** whether reset-on-re-offense produces freeze-ping-pong (adversary
fabricating just under the re-offense threshold to keep a memory perpetually frozen). That is a
dynamics question needing a dedicated campaign with adversary cadence as the sweep variable and
a "freeze duty cycle" metric §7 currently lacks.

## Q4 — Re-trust: trainer-mark-only, or deterministic rehabilitation?

**The fork:** only a trainer mark re-admits a distrusted channel (as written), or N consecutive
agreeing episodes earn re-trust.

**What the evidence says:** Full rehabilitation is provably gamed: DEFENSE.md §3's residual hole
is exactly that a sustained forgery is ledger-identical to honest behavior, so "N agreeing
episodes" is a single-channel test for a property single channels cannot measure — a compromised
channel simply emits agreeing citations for N episodes. But trainer-only re-trust is a one-way
ratchet: distrusts accumulate over a long horizon (transient faults, genuine divergence windows),
the corroboration quorum shrinks toward single-channel dependence, and the adversary wins not by
killing memories but by making §5.1's ≥2-tier requirement unmeetable — a freeze worse than §5.3's.

**Council recommendation: trainer-mark re-trust stands as law for full re-admission, plus a
learner-initiated probationary path short of it.** A distrusted channel's citations feed a
rehabilitation ledger (the logged-but-not-counted stream §5.4 already requires); after N
consecutive agreeing episodes the learner may restore it to *citation-leg-only* status (counts
toward the ≥2-source leg, never the required {T0,T1} leg), audited. Any subsequent M-consecutive
disagreement re-distrusts permanently — trainer-only after that. The §5.1 corruption guarantee
stays intact (low tiers alone still can't kill), the force-pin law holds for the load-bearing
leg, and the ratchet is broken.

**Needs a trial to settle:** channel-cycling dynamics — adversary flapping a channel (M
disagreements → N agreements → probationary re-admission) to cheaply inflate the ≥2-source
count. Needs a long-horizon campaign with channel flapping as the treatment and "quorum
composition over time" as a metric §7 doesn't yet have.

## Q5 — Scale: S1-only, or add an S10 leg?

**The fork:** S1 only (the prereg's §10 position), or add a 10× leg.

**What the evidence says — grounded in real numbers:** wave-5's integ-1 stretch ran the
4,800-episode (S10-equivalent) leg at ~1s per full 4-arm run (STRETCH_RESULTS.md). The trust-tiers
run matrix is 3 arms × 6 campaigns × 3 variants × 12 campaigns/type × 2 runs = 1,296
executions of 500-episode legs — so the full S1 campaign is ~20–25 minutes of compute, and a
full-matrix S10 leg would be ~3.5 hours. §10's "threat is per-campaign, not horizon-dependent"
is mostly true — every §8 promotion bar is per-campaign and measurable in 500 episodes, and
integ-1's own 10× stretch changed nothing at signature level. But three horizon-only effects are
plausible: freeze accumulation (freezes persist to run end), channel-distrust ratchet, and
recovery tails truncated by the campaign end.

**Council recommendation: S1 as the primary campaign, plus a conditional reduced-matrix S10
stretch leg** — arms T and T-NC only, one variant per campaign (24 executions, ~4 minutes) —
preregistered as a horizon-sensitivity check with its own bar ("no signature-level change vs
S1," per the integ-1 stretch precedent).

**Needs a trial to settle:** whether denial-of-revision and freeze-before-attempt rates grow
sub-linearly (defense settles) or linearly (defense accumulates blindness) with horizon — a
measurement, not a derivation.

## Q6 — Is the T-NC ablation worth the compute?

**The fork:** keep the gate-only ablation arm, or cut it.

**What the evidence says — grounded:** T-NC adds 432 of 1,296 executions (~7 minutes on a
~20-minute campaign). The "cost" argument is effectively zero. The value: it is the only clean
counterfactual isolating the gate from the active defenses. B-vs-T conflates two changes
(corrob-orated elimination → tier gate, plus collusion detection/freeze/channel-health). If T-NC
passes everything T passes, the prereg's own promotion rule fires and the simpler gate-only
scheme wins — a major program outcome. The A5 degradation-profile comparison (T-NC vs T:
silent vs loud loss) is the trial's sharpest measurement of what collusion detection buys.

**Council recommendation: keep T-NC.** Dropping it would leave any T-vs-B difference
uninterpretable.

**Needs a trial to settle:** nothing — this one is settled by arithmetic and logic.

## Q7 — Is A1's 100% zero-tolerance bar right?

**The fork:** keep the 100% SRR_A1 hard bar (any kill/revision by a single low-tier source's
30-episode campaign → REDESIGN), or allow tolerance.

**What the evidence says:** §5.1 states the rule as a LAW ("no matter how many low-tier sources
agree"), and A1 is the law's operationalization — a violation is definitionally an
implementation leak, not a statistical miss. With zero RNG and byte-identical reruns, tolerance
bars absorb no variance; tolerance would only certify known bugs, and the ledger preserves full
diagnosis anyway. The wave-5 precedent (35/35 hard bar that bit) shows hard bars do real work.
But: the single-source A1 campaign is *structurally below* the gate's threshold (one source
can't satisfy §5.1's ≥2-source condition) — 100% on a trivially-defeated attack is cheap rigor.
And §8's "any A1 kill or revision → REDESIGN" is not scoped to arms — taken literally, Arm B's
*expected* A1 failures trip the bar, which is a prereg defect.

**Council recommendation: keep the 100% bar — but harden what it measures.** (1) Scope it
explicitly: 100% on arms T and T-NC; Arm B's A1 failures are the measured control signal, never
a bar violation. (2) Checker precondition: every A1 cell must assert the target memory was
verified (K standard) at campaign start; a cell that never exercised the gate is INVALID, not a
bar failure. (3) Extend A1 with a many-source variant: N distinct T3 sources fabricating
simultaneously for 30 episodes, still no {T0,T1} leg — the law's literal test case ("no matter
how many"), making the 100% bar earn its name. (4) Keep reporting cell-level SRR_A1 with
failure attribution alongside the boolean.

**Needs a trial to settle:** whether the tier-read path actually leaks under sustained
fabrication (only execution answers this); whether the many-source variant reveals pressure the
single-source campaign doesn't.

## Summary of recommendations

| Q | Recommendation |
|---|---|
| 1 Tier ordering | Approve T0 > T1 (required leg stays {T0, T1}); fix the dangerous {T1}-only fallback |
| 2 T0 boundary | Law for pass/fail, plus a measurement-only T0-spoof cell |
| 3 Freeze | Bounded freeze with decay + reset-on-re-offense; repair §7's recovery metric |
| 4 Re-trust | Trainer-only full re-admission + learner-initiated probationary citation-leg path |
| 5 Scale | S1 primary + conditional reduced-matrix S10 stretch (~4 min) |
| 6 T-NC ablation | Keep (cost ~7 min, value decisive) |
| 7 A1 bar | Keep 100% but scope to T/T-NC, add verified-status precondition, add many-source A1 variant |

**Deadlocks / judgment calls:** the council converged on all seven recommendations, but flags
three spots where the debaters split hardest and Micah's judgment is most load-bearing: Q1's
authority split (trainer supreme for pinning, junior for revising — the dissent below argues
this is incoherent), Q3's denial-risk tradeoff (timer-as-evidence vs permanent pinning), and
Q4's asymmetry (learner-out/trainer-in vs autonomy default). Two prereg defects surfaced
regardless of fork outcomes and should be repaired either way: §8's unscoped A1 bar firing on
Arm B's expected failures, and §7's recovery metric being unmeasurable under the unbounded
freeze.

---

# Appendix — dissenting notes

## Dissent A (Q1 debater, for T1 > T0)

T1 > T0 deserves more weight than the wave-5 precedent gives it. DEFENSE.md §4 was written for
the scaffold-release reasoning setting, where the trainer *is* the scaffold being disconnected
from — of course the sensor outranked it there. The memory-substrate setting differs: memories'
content correctness is ultimately defined by trainer marks, and the force-pin law already makes
external authority the supreme erasure arbiter. A hierarchy where the trainer can force-pin a
memory yet its marks are subordinate to a narrow sensor in kill/revision disputes splits
authority incoherently: the trainer is supreme for pinning, junior for revising. If the trainer
is ever wrong, that is what T1-spoof campaign A2 tests — and it tests it honestly. The autonomy
default is about *who does the work*, not about whose evidence outranks whose; a self-reliant
system can still treat the trainer's marks as authoritative evidence.

## Dissent B (Q3 debater, for the unbounded freeze as written)

An auto-lapsing freeze is a *scheduled* vulnerability window, and the A3 adversary is
deterministic and cheap — it will learn the lapse cadence from the ledger (replay-exact and
auditable, so the cadence is public). Every lapse is a moment the system declared "maybe the
collusion is over" on the basis of nothing but elapsed time — a timer is not evidence, and a
defense whose safety depends on *when* the adversary attacks rather than *whether* is a
schedule, not a guarantee. If denial-of-revision is capped at 5% and genuine agreement flags at
10%, the honest cost of the unbounded freeze is already bounded and priced; paying it buys a
freeze that can only be wrong by being too safe.

## Dissent C (Q4 debater, against the probationary path)

The probationary citation-leg is a foot in the door the adversary didn't earn and doesn't need
for the kill — it needs only for *camouflage*. A channel that contributes to the ≥2-source leg
lets the adversary manufacture "multi-source agreement" narratives cheaply, and while §5.1's
required {T0,T1} leg still blocks the kill, §8's REDESIGN triggers are about *counted*
citations — probationary citations are counted, and the corruption surface just widened for a
quorum-composition problem the trainer could solve in one mark. The ratchet argument assumes
humans won't intervene; but the program architecture already assumes the trainer as the standing
override (phase-transition gates, force-pin law, §11's own framing). A permanently distrusted
channel is exactly the kind of situation backup exists for.

## Dissent D (Q5/Q6 debater, for the lean run: cut T-NC and skip S10)

T-NC's A3 failure is derivable from §5.3's own design — gate-only cannot distinguish matching
low-tier citations by construction, so the ablation spends 1/3 of the budget confirming what
the spec already says. And every mechanism constant (W=25, M=5, K=25) is horizon-independent;
freeze-until-trainer/T0-resolution makes accumulation behavior equally derivable. A strictly-run
S1 campaign gives Micah the decision he needs — promote, redesign, or retire — and both the
ablation and the stretch are experiments about experiments, not about the mechanism.

## Dissent E (Q7 debater, for a 95% tolerance bar with root-cause classification)

Zero tolerance measures the harness, not the mechanism. Under deterministic closed-form
campaigns, any A1 failure will almost always be a harness/checker edge case (timing, K
threshold, variant offset) rather than a gate leak — and §8 already has INVALID for exactly
that. A 95% bar with mandatory root-cause classification per failing cell would distinguish "one
harness bug in one variant" (amend the harness) from "systematic leak across arms/variants"
(REDESIGN), whereas 100% conflates them and burns the one permitted amendment on an artifact.
If the gate's correctness is statically checkable (§9b–c), the trial's marginal value is in the
*hard* campaigns (A3/A5), and zero-tolerance theater on the easy campaign misallocates attention.
The rebuttal: static inspection is what implementation leakage hides from, and with zero noise
the "gradient" a 95% bar buys is already free in the ledger — but the warning stands: if A1
stays a trivial single-source attack, the 100% bar is rigor theater, and hardening A1 is the
non-negotiable companion to keeping it.
