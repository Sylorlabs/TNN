# BARS.md — Frozen K-bars with red-team compromise notes (Crew B)

Frozen source: `~/workspace/comp_b4/ref/PREREG.md` §7. All bars applied
exactly as frozen; the compromise notes are recorded alongside, not enacted.

## K1 — chance bar (frozen)

> "Combo accuracy is compared against two frozen chance arms, NULL and
> SINGLE-RULE (never anything else): chance = max(null_rate,
> single_rule_rate). If combo accuracy ≤ chance + 0.10, the composition
> claim is killed."

Measured: chance = max(13/600, 32/600) = 0.0533; kill line 0.1533;
learner combo accuracy 0/600 = 0.0000 ≤ 0.1533 → **composition claim KILLED**.

**Compromise note (A1, red team):** the frozen chance family {NULL,
SINGLE-RULE} is too narrow to kill every non-composing strategy. The pilot
showed wrong-order scoring 10/48 = 20.8% > the 14.2% frozen line. In this
battery wrong-order scores 62/600 = 10.3% < the 15.3% line (the frozen K1
would kill it here), but order-blind ascending/descending strategies score
35.7%/38.0% — still far above the frozen line. A1's proposed wrong-order
arm is necessary but not sufficient; the bar needs a broader non-composing
family. The kill recorded here (0%) is unaffected — it clears every floor.

## K2 — void-on-unmastered bar (frozen)

> "If >50% of P2 failures are class (a) — learner lacks at least one part
> — the battery is void: the parts were never learned, so nothing about
> composition was tested."

Measured: 600/600 = 100% (a) > 50% → **battery VOID**. (P0: 0/6 parts
mastered at the ≥7/8 bar; 48/48 probes "I don't know.")

**Compromise note (A2, red team):** the frozen 8-probe P0 gate is
launderable — a Caesar-shift memorizer passes 24/24 without learning any
rule, because the unsalted generator makes held-out tokens exact Caesar
shifts of training tokens. A future P0 pass under the frozen gate would not
prove mastery. This run's void is honest (the gate was not beaten), but any
rerun passing P0 under the frozen generator is suspect pending the salt
fix. New sharpening from this crew's audit: the generator's period is
exactly 52, so 66/600 P2 inputs are *byte-identical* to training inputs —
the memorization surface is larger than the red team's shift analysis
showed.

## K3 — retrieval-failure finding (frozen)

> "If >50% of P2 failures are class (b) — parts mastered but retrieval
> fails — the finding is 'retrieval failure', not 'composition failure'."

Measured: 0 (b) failures → not triggered.

## K4 — reflex defect bar (frozen)

> "Reflex probes (P3): if the learner applies rules to no-rule distractors
> at >20%, the reflex defect is confirmed."

Measured: 0/8 = 0% → no defect. The learner withholds on distractors.

## K5 — interference bar (frozen)

> "Per-pair interference: if any pair (i,j) shows the trained order
> succeeding while the reverse fails asymmetrically beyond the frozen
> criterion, the interference defect is confirmed."

Measured: no pair meets the asymmetry criterion (all pair scores 0) → no
defect.

## K6 — memorization audit (frozen)

> "K6 runs over all pairs: a composition success on an input sharing no
> bigram with any training string is clean; successes only on
> bigram-overlapping inputs are flagged as possible memorization."

Measured: 0 composition successes → **vacuous** (nothing for memorization
to explain).

**Compromise note (A4, red team):** K6 is inoperable on some pairs under
the frozen generator — the pilot found (1,0) and (3,1) had no bigram-clean
items. In this 6-rule battery, 5 of 30 pairs have zero bigram-clean inputs:
(0,4), (2,0), (3,1), (4,3), (5,4). On those pairs the frozen K6 cannot
distinguish clean composition from memorization even in principle.
