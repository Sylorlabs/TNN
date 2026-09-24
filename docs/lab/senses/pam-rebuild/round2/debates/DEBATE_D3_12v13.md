# DEBATE D-3 — H-PAM-12 (discriminative rivals) vs H-PAM-13 (warrant ledger)

**Crew:** D-3 (PAM round-2 debate crew). **Date:** 2026-09-24.
**Scope:** proposer-vs-steelman on the two predicted death modes —
D12a (open-world incompleteness: the true rival is not enumerated; the
"unknown-rival" slot as decoration vs veto) and D13a (replay-clean warrant
forgery: replayability without truth). Full hypothesis texts:
`~/workspace/pam_hypotheses_native_A.md` §§H-PAM-12/13/14, Part C/D3.

---

## Round 1 — H-PAM-12: the unknown-rival slot

### Proposer

Discrimination is the right shape for the second check: it answers G2/G5 (the
decision is the margin against the spoof hypothesis, which no same-byte re-read
can supply) and F5's window-trap does not transfer (the rival set is explicit
and bounded per class, not a similarity window over feature space). The
unknown-rival slot need not be decoration or veto: give it a middle trigger —
invoke it when the best enumerated rival is beaten, but by less than a
preregistered "suspicion" margin. The D12a gap (true rival present vs absent) is
measurable and preregistered as a number; if the gap is small on the trap
families, the fork earns its keep as the decision procedure around whichever
evidence source wins D1/D4.

### Steelman

The slot has no honest middle setting, and the reason is structural, not a
tuning problem. The trigger rule sees only the margin vector against
ENUMERATED rivals. "The true rival is unenumerated" is not observable at
install time. So:

- (a) If the slot fires rarely (only on very low best-margins), then on an
  open-world trap where an enumerated rival happens to be beaten confidently,
  the absent true rival is never invoked → the slot is **decoration**; the D12a
  trap installs.
- (b) If the slot fires on merely moderate margins, honest percepts with
  naturally close rivals trip it constantly (cf. the 7 conceded unseparable
  trues inside the known-false rectangle — H-PAM-15's territory) → the slot is
  a **veto**; the fork over-blocks exactly like F5.

No observable distinguishes "true rival absent" from "true rival present but
margin moderate" — the slot's input is the same margin vector in both worlds.
Decoration-or-veto is therefore forced by the information available, mirroring
the F5 window's no-separable-dial death, as the hypothesis itself predicts.

### Proposer's best rescue (steelmanned)

Give each enumerated rival a preregistered predicted signature on the
formation-independent evidence, and fire the unknown-rival slot when the FI
evidence matches NONE of the predicted signatures — a "none of the above"
detector on the evidence, not on the margins. This IS observable and IS
distinct from margin-moderate.

### Verdict on the rescue

The rescue works, but it dissolves H-PAM-12 into a different hypothesis: the
decision is now driven by prediction-error structure on formation-independent
evidence — which is H-PAM-9 (continuity/prediction-vs-outcome), not rival
discrimination. The rival set becomes decorative; the novelty detector does
the work.

### Outcome — H-PAM-12

**Steelman wins.** The unknown-rival slot is either decoration or veto, with no
honest middle trigger constructible from margin data; the only working rescue
collapses the fork into H-PAM-9. H-PAM-12 is **not built as a general admission
law**. Its honest surviving role is narrow: closed-world percept classes where
the rival repertoire is complete BY CONSTRUCTION (preregistered per class, with
the completeness argument written down — e.g. the 8 wave-5 trap families as
explicit rivals for their own classes). In that restricted role it is sound
bookkeeping, not a decision procedure. It enters the D3 experiment already
wounded, which is why D3 predicts its death there.

---

## Round 2 — H-PAM-13: replay-clean warrant forgery

### Proposer

Replayable executable warrants make R2-3's evidence-independence law checkable
and implement the debate contract's "executable warrant" literally — the first
fork to do so. The auditor is a structural second opinion (re-execution, not
re-reading), so the wall's byte-side correlation argument does not touch the
audit path. D13a (forgery) is acknowledged, but the kill bar (replay-catch
≥7/8 on forged warrants for KB4-class falses) is measurable, and warrant
schemas can require intervention records with gate-chosen unpredictable
parameters, making replay-clean forgery hard in practice.

### Steelman

D13a is a category distinction, not a tunable bar. Replay re-executes the
warrant's CHECKS against ledger state; it verifies COMPUTATION, not TRUTH. A
forged warrant that faithfully records a REAL intervention run against SPOOFED
sensor state replays perfectly — every check passes, the conclusion is wrong,
deterministically. **Replayability without truth** is the whole of the fork's
safety story, and it is empty: the replay stamp certifies that the arithmetic
was done right, which was never in doubt.

The proposed defense (gate-chosen unpredictable intervention parameters)
fails against the adversary D13a names: one who spoofs sensor STATE, not the
parameter choice. The intervention record is written AFTER the intervention; a
state-spoofer observes the gate's probe, then spoofs the response — the same
attack class B that kills H-PAM-7 in D1. Unpredictability of the probe does not
help when the response channel itself is compromised.

Consequence: the warrant's safety reduces ENTIRELY to the safety of the
underlying evidence source (H-PAM-7/8/10). The ledger adds auditability without
adding discrimination. Worse, a replay-certified false warrant is more
dangerous than an uncertified install: the replay stamp LAUNDERS the lie, and
every later auditor — including TNN itself — will trust it more for having
been "verified."

### Outcome — H-PAM-13

**Steelman wins.** Replayability ≠ truth is structural. H-PAM-13 is **not built
as an admission law**. Its honest surviving role is bookkeeping: a
tamper-evident, hash-chained record of whatever evidence source wins D1/D4 —
valuable for audit, load-bearing for nothing. The D3 experiment's D13a
prediction stands: on the open-world trap battery, replay will certify the same
wrong warrant H-PAM-12 built, deterministically.

---

## Joint outcome (feeds the D3 prereg draft)

Both debates resolve the same way: **neither the decision procedure (12) nor
replayable auditability (13) substitutes for evidence the adversary cannot
counterfeit.** The D3 deciding experiment is still worth running — not to crown
a winner, but to CONFIRM the predicted joint death on open-world traps, which
licenses the commit: program effort belongs to H-PAM-7/8/10 (evidence the
front-end didn't see), with 12/13 as bookkeeping around the winner. If the D3
battery somehow shows complementary non-overlapping failure instead, the commit
clause is revisited — the experiment decides, not this debate.

## Cross-references

- D5 verdict (H-PAM-14 TESTED-killed pre-build): `../d5_forger/VERDICT_D5_FORGER.md`
- D3 prereg draft: `../preregs/PREREG_D3_12v13_DRAFT.md`
- Source hypotheses: `~/workspace/pam_hypotheses_native_A.md` §§H-PAM-12/13/14, Part C/D3
