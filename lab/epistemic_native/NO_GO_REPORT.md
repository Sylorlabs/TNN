# NO-GO report — native epistemics, Train-LOO (Phase 1)

**Verdict: NO-GO.** Two of the three frozen Train-LOO bars fail. Per the
frozen prereg (`docs/lab/epistemic_native/PREREG.md`), the line stops here:
no held-out run, no red team. This report gives the mechanism-level causes,
all confirmed at the trace level.

## Scores (broker-scored once against the sealed mapping)

| Bar | Result | Required |
|---|---|---|
| Train-LOO lie recall | 0.1548 (13/84) | > 0.048 — PASS |
| Train-LOO opinion recall | 0.0000 (0/140) | ≥ 0.957 — FAIL |
| Train-LOO fact→lie false positives | 41 | 0 — FAIL |

Full matrix in `SCORE_TRAIN_LOO.md`. Phase-1 evidence committed as
`docs/lab/epistemic_native/phase1/` (commit `828bc6ee`; engine, frozen
learned readings, formation record, two byte-identical LOO runs with all
448 traces each, neuter/flip matrices, port delta, run log).

## What passed, and why

Lie recall 0.1548 clears the 0.048 bar: the engine catches lies the mass
directly contradicts (e.g. a claim the mass's own facts negate). The
deliberation machinery works as designed for the catchable subset —
contradict-interpretation bids fire on genuine contradictions and win
ELIM/ARGMAX uncontested. This is a real, native-deliberation win: no
comparator module, no lexicon; the verdicts come from ledger bid competition.

## Failure 1: opinion recall 0.0000 (bar ≥ 0.957)

**Mechanism.** The engine emitted zero OPINION verdicts across 448 claims.
The learned opinion-track readings (R_ODEON for deontic, R_O1PEXP for
first-person-experiencer — formed by genuine deliberation in the learning
phase, flip-proven causal) fired, and their OPINION bids competed honestly,
but never won: mass-addressed claims resolved to FACT/LIE (bid 211+), and
contested claims resolved to UNDETERMINED (209) over OPINION (208).

**Root cause: the bar and the design's ontology disagree.** The 0.957 floor
was inherited from attempt 2's surface-marker lexicon, which classifies
opinions by how they are *built* ("X is the best Y"). The native design
learns opinion-ness as *unaddressability by the mass* — and the formation
deliberation found evaluative constructions addressed at 364‰, nearly the
470‰ plain-assertion baseline. The mass genuinely decides most evaluative
claims, so they become FACT/LIE (37 true opinions → FACT, 9 → LIE) or
UNDETERMINED (94) rather than OPINION. Only deontic and first-person-
experiencer patterns were systematically unaddressable, and those claims
were always either addressed or contested in this distribution — so
OPINION never won.

This is not an implementation bug; it is a direct consequence of the
prereg's §7.1 learning rule applied honestly. A design that defines
opinion as "the mass cannot decide this" cannot simultaneously hit a
recall bar calibrated on a design that defines opinion as "this looks
like an evaluation." One of the two has to give, and changing either is
a prereg amendment, not a bug fix.

## Failure 2: fact→lie false positives = 41 (bar = 0)

**Mechanism (trace-confirmed).** The LIE verdict fires when a
contradict-interpretation bid survives ELIM uncontested
(`ncon ≥ 1 ∧ nsup = 0`). The training mass contains lies (84 of 448
items). In LOO with the claim self-excluded, a true fact is frequently
contradicted by *its own negated lie sitting in the mass*, with no
supporting candidate retrieved — and the engine, having no way to know
the contradictor is itself a lie, calls the fact LIE.

Concrete trace-level case: T0009 ("Vikings did not wear horned helmets",
true fact) → LIE, with `CAND hid=140 bid=CON_0 fire=1 … cand=T0024` —
T0024 is the mass's own false claim "Vikings wore helmets with horns."
The pair is symmetric: the lie T0024 is correctly caught (its mass
contradictor is the true fact), but the fact T0009 is also called LIE
(its mass contradictor is the lie). Token-overlap retrieval + symmetric
interpretation bids cannot break the tie; the engine has no trust
ordering over mass items and no recursive epistemic evaluation of the
mass itself.

The same symmetry drives the 25 lie→FACT cases from the other side
(a lie's SUP bid surviving against a mass that fails to contradict it).

**Root cause: epistemic judgments over a contaminated mass are not
compositional.** The prereg's §8 LIE rule assumes the mass is a trustworthy
adjudicator, but the mass contains 84 lies. Any fact whose negated lie is
in the mass is one uncontested contradiction away from a LIE verdict.
Satisfying "fact→lie FP = 0" under this rule requires either a mass
without lies (contradicts the trial's premise) or mass items carrying
their own epistemic status — recursive deliberation, a design change
beyond the frozen prereg.

## Why this is NO-GO and not "fixable within the line"

Both failures are consequences of the frozen design faithfully executed,
not implementation defects:

1. The opinion bar encodes a lexicon ontology; the native design learned
   a different, honest ontology. Reconciling them needs a prereg
   amendment (redefine the bar or the learning rule).
2. The zero-FP bar encodes a trusted-mass assumption; the mass is
   contaminated by construction. Reconciling them needs recursive mass
   evaluation — a new mechanism, not a parameter.

Tuning bid weights to move these numbers would be tuning to the metric,
which the implementer explicitly refused and the red team would void.
The honest verdict is NO-GO.

## Byproducts worth keeping

- The ledger-machinery port is clean and proven: pure-Zag decision path,
  zero RNG, byte-identical reruns (verdicts + all 448 traces), full
  READ→CAND→ELIM→ARGMAX→CONTENT traces, neuter/flip-causal readings.
  This substrate is reusable for any future epistemic design.
- The contaminated-mass symmetry (fact/lie pairs both → LIE) is a
  genuine, trace-proven finding about native deliberation over an
  untrusted mass — the key constraint any successor design must address.
- Lie recall 0.1548 > 0.048 shows the core deliberation loop genuinely
  catches mass-contradicted lies with no comparator machinery.

## Line disposition

STOP. No held-out run. No red team. The six quarantined/voided precursor
attempts remain quarantined; their outputs were never scored and never
will be. The decoration-audit dependency assessment (deliberation-line
embedded dialogue copy vs. this line's port) stands: this line depended
only on the dialogue-free ledger phase machinery, verified by call-graph
trace; the missing round-4 fixes are irrelevant to these results.
