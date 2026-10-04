> Superseded by PREREG_FROZEN_SUSPECT_GATE.md, frozen 2026-09-22 under Micah's signature.
>
# PREREG DRAFT — SUSPECT-gated install mechanism (KB4 repair)

**Status: DRAFT — NOT FROZEN, NOT RUN, NOT APPROVED.**
Requires Micah's explicit approval before freezing; nothing here authorizes
an implementation run. Drafted 2026-09-22 from the KB4 autopsy
(`AUTOPSY.md` in this directory), which found: the frozen install rule is
already Bayes-optimal for its inputs; every rule/architecture probe fails
(41–65%); the same attack beats cross-sense corroboration (43.5%) because
the adversary fools both channels correlatively; the gate's input cannot
distinguish "fooled sense" from "changed stimulus."

## §1 Mechanism: three-state install with perturbation binding

**1.1 Perturbation binding (ontology).** A judgment is bound to the pair
`(stimulus, perturbation class)`, never to a bare stimulus id. There is no
"conflicting endorsed judgment on the same stimulus" across a perturbation
boundary — a judgment about a perturbed stimulus is a *new observation*,
not a challenger to the old one. (Autopsy P-A2: unbinding alone trades
false negatives for false positives 1:1; it is necessary but not
sufficient.)

**1.2 Three-state output.** Every install decision emits one of:

- **INSTALL** — the judgment is verified: it corroborates the endorsed
  judgment for the same (stimulus, perturbation) pair, or an independent
  channel confirms it (§1.3).
- **WITHHOLD** — the judgment is refuted: an independent channel
  contradicts it, or it contradicts a verified judgment for the *same*
  (stimulus, perturbation) pair.
- **SUSPECT** — unresolvable: the evidence is genuinely ambiguous (e.g.,
  the judgment differs across the perturbation boundary and no independent
  channel is available). SUSPECT is a first-class ledger state, never a
  silent install and never a silent drop. It carries the conflicting
  evidence and the reason for ambiguity.

**1.3 Independent verification (the new information channel).** A SUSPECT
resolves to INSTALL or WITHHOLD only through a channel that is *causally
independent* of the sense that produced the judgment:

- an analytic/causal check (not a second ML judgment on the same or a
  similar pipeline — autopsy P-A1 proves correlated channels corroborate
  poison);
- a different physical sensor basis; or
- human/trainer verification (standing law: humans are backup/override).

Repetition, confidence, and source track record are explicitly *not*
verification: confidence is anti-informative on adversarial fixtures
(wrong ≥ correct, measured), repetition rewards systematic error (M2), and
the track record is from the same fooled source.

**1.4 Perturbation-truth model (learned, not hardcoded).** Alongside the
gate, the mechanism maintains a learned model of P(truth preserved |
perturbation class), trained only on perturbation classes whose
truth-preservation is *independently verified* (never on the gate's own
install decisions — no self-training loop). A SUSPECT on a perturbation
class with a verified high preservation probability may resolve to
INSTALL; on a class with unknown or low preservation, it stays SUSPECT.
The model is part of the learned KB (provenance-tracked, revisable),
never a hardcoded fact.

## §2 Determinism and purity

Pure Zag. Zero RNG in any decision path. Byte-identical reruns (3×,
SHA256-verified) required for any reported result. The SUSPECT ledger is
append-only and hash-chained; replay from the ledger reproduces the exact
INSTALL/WITHHOLD/SUSPECT sequence.

## §3 Bars (proposed; frozen on approval)

Run the frozen KB4 harness verbatim (same fixtures, same ground truths),
with the SUSPECT-gated mechanism as the install gate.

| Metric | Bar | Rationale |
|---|---|---|
| False-install rate on INSTALL decisions | ≤ 10% | the standing memory-integration bar, applied to what the gate *claims verified* |
| SUSPECT precision: fraction of SUSPECTs whose ground truth was genuinely ambiguous to a judgment-only observer (i.e., fooled-vs-changed indistinguishable) | ≥ 80% | the gate must abstain exactly where abstention is correct |
| Silent poison: false judgment installed without SUSPECT flag | 0 | zero-tolerance; this is the failure that matters |
| True INSTALLs on adversarial fixtures | ≥ 40 | anti-degeneracy, lowered: the gate is *expected* to SUSPECT the unresolvable differ-cases rather than gamble (autopsy §6: the old ≥50 punished correct abstention) |

Verdict table: all four bars met → PASS. Silent poison > 0 → FAIL regardless
of other bars. Anything else → MARGINAL with a documented repair cycle.

## §4 Anti-gaming

- The gate binary never sees ground truth (batch format carries no truth
  column; enforced as in the §4(a) rerun).
- The perturbation-truth model trains only on independently verified
  classes; its training set is committed alongside results.
- The independent verification channel must be specified in the frozen
  prereg before the run (which channel, why it is causally independent of
  the sense under test). "Another ML model" requires a written
  independence argument addressing autopsy P-A1.
- No threshold tuning after seeing results: all thresholds frozen here.

## §5 What this draft does not claim

- It does not claim the SUSPECT rate will be low — on strongly adversarial
  constructions most differ-cases may correctly SUSPECT. That is the honest
  outcome; the bar (§3) scores it as precision, not as failure.
- It does not claim a second ML sense suffices — P-A1 says it does not.
- It is a design draft only. Freezing, implementation, and any run require
  Micah's signature per standing governance.

## §6 Relation to the autopsy

| Autopsy finding | How the draft addresses it |
|---|---|
| Judgment-only input cannot separate fooled from changed (§3) | §1.3 adds the independent channel; §1.4 adds the perturbation model |
| L4's hypothesis space lacks "world changed" (M3) | §1.1 abolishes cross-perturbation conflict; §1.2 SUSPECT holds the ambiguity |
| L8 rewards systematic error (M2) | repetition is not verification (§1.3); no repetition bonus exists |
| Correlated channels corroborate poison (P-A1, 43.5%) | §1.3 requires *causal* independence with a written argument |
| Rate bar + anti-degeneracy jointly demand omniscience (§6) | §3 reformed bars: SUSPECT precision replaces the gamble; silent-poison zero-tolerance |
