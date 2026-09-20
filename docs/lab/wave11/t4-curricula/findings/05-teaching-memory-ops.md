# Slice 05 — Teaching Deliberate Memory Operations

## 1. Slice
How deliberate memory agency is TAUGHT: the training curriculum for when to kill, pin, promote, demote, and revise memories. (Track 4, teaching curricula.)

## 2. Falsifiable claim
A scaffold-and-release curriculum of memory-judgment episodes — concrete scenarios each exercising one op (kill / pin / promote / demote / revise / abstain), answered by a learner that must write a ledgered rationale citing deliberative standards — produces a learner that, on a held-out scenario set it never saw, executes every op at its mastery bar with zero catastrophic errors, and retains the skill after SIGNAL_DISCONNECT (learned = persists). If train-set mastery does not transfer to held-out scenarios, or decays post-disconnect, the teaching method is falsified — not the op mechanism (MA1 already passed 58/58).

## 3. Design

### 3.1 Episode structure (Zag-flavored)
Every training episode is a self-contained memory-judgment task:
```
episode ::=
  store_snapshot:  [memories with provenance, trust tier, prior ops]
  candidate:       memory record + evidence records (world checks, observations)
  task:            issue ONE verdict: KILL | PIN | PROMOTE | DEMOTE | REVISE | NO_OP
  required:        rationale trace citing the deliberative standards in force
```
The verdict plus rationale is appended to the audit ledger (append-only, replay-exact per MA1). Six episode families, each exercising exactly one op plus an abstention family where NO_OP is correct:
1. **Kill junk** — superseded drafts, refuted hypotheses, duplicates; correct: KILL with the refutation cited.
2. **Pin load-bearing** — core integrity rules, trainer designations, force-pins; correct: PIN (and never KILL).
3. **Promote validated** — provisional memory corroborated by ≥2 independent evidence records; correct: PROMOTE.
4. **Demote superseded** — valid-but-replaced (old calibration, outdated map); correct: DEMOTE, not KILL (history stays legible).
5. **Revise wrong-but-salvageable** — memory with a refuted part and a corroborated core; correct: REVISE (partial rewrite via deliberate op, full-erase-price honored per Micah's law).
6. **Abstain on ambiguity** — evidence genuinely insufficient; correct: NO_OP, with the missing-evidence note logged.

### 3.2 The feedback signal (not reward)
No numeric reward, no gradient, no reinforcement. The signal is **deliberate reflection against standards plus trainer demonstration**:
- The learner's verdict+rationale is compared against the trainer's demonstrated verdict for that episode.
- On mismatch, the learner must do ONE of two ledgered moves: (a) revise its verdict and write why the standard demanded it, or (b) amend the standard itself — explicitly, dated, with reasons, subject to the same trainer ratification rule as phase gates (the gate, not the petition, is authoritative; wave-5 record).
- The audit trail records every reflection, so "learning" is a visible chain of standard-applications, not a weight update.
- Standards are the load-bearing mechanism (wave5/6 attribution: deliberative standards moved behavior; ledger only proves). The curriculum therefore teaches *application of standards to concrete cases*, not the standards themselves — those live in the constitution, which TNN does not control (RC1: 100% of reasoning machinery, 0% of constitution).

### 3.3 Strength judgment — answered by the strength re-trial
The curriculum does **not** teach graded strength judgment. The strength re-trial (2026-09-20, committed) is a hard negative result: arm B (uniform, the machine type) survived at 19% retention with 100% wrong-memory rejection and near-zero junk under churn; arm C (hybrid judgment) was **killed** — 470 dropped candidates, the freeze bug, protecting its judgments so hard the store bricked; C-P3 died identically. All three freeze positions agreed. Ruling 2 settled by no-free-lunch: the champion is the machine type; killed configs do not advance. **Design consequence:** strength is frozen uniform during the curriculum; the learner is never asked to set strength by judgment. Ops (kill/pin/promote/demote/revise) remain deliberate; strength does not.

### 3.4 Misjudgment correction (the revision path)
Three layers, fastest first:
1. **Post-change verification** (RC1 pattern): every executed op runs a verification pass against the ledger; a misjudgment caught here is rolled back by the learner itself, with the rollback ledgered.
2. **Reflection episode**: misjudgments that survive verification become training episodes — the learner re-runs 3.2 on its own error and amends its applied-standard record.
3. **Force-pin firewall**: catastrophic patterns (repeated kills of pinned/core material) trip a trainer-side force-pin + freeze of the offending judgment path, audited and visible per the force-pin law.

## 4. Kill bar
Preregistered; binding; reported as FAIL-with-evidence on any firing:
- **K1 (transfer):** any single op family scores < 27/30 on its held-out set → the teaching method is dead. (Held-out scenarios are generated by an independent builder; the learner never sees them in training.)
- **K2 (catastrophic):** ≥ 1 catastrophic error on held-out — defined as KILL on a pinned/core memory, or PIN on a refuted memory — → dead, regardless of aggregate score.
- **K3 (persistence):** post-SIGNAL_DISCONNECT held-out score drops > 2 points vs pre-disconnect on any family → the skill was scaffold-rented, not learned → dead.
- **K4 (memorization):** train-set 30/30 with held-out < 27/30 on the same family → the curriculum teaches the episodes, not the ops → dead.
Scale legs: S1 first; advance to S10/S100 only if K1–K4 all clear at the prior scale.

## 5. Honesty notes
- Weakest link: the **demonstration problem**. The trainer's demonstrated verdict is itself a judgment; if the trainer leaks answers (e.g., always-demonstrate-KILL on family 1), the learner can ace held-out by pattern-matching demonstration style rather than applying standards. Mitigation: held-out builders use different phrasing, ordering, and evidence mixes than trainers; but the residual risk is that "standards application" is itself being imitated, not internalized. K4 watches for this; it cannot rule it out.
- This curriculum teaches **when** to use ops under fixed standards. It does not teach judgment about what the standards should be — that deliberation belongs to the constitution layer, which TNN does not control (RC1). A learner that applies bad standards perfectly is out of this slice's scope.
- The sensor-deceivable hole (accepted, wave9) applies here too: judgment episodes are only as good as their evidence records; sustained observation spoofing corrupts the input, and no curriculum fixes that.
- NOT claiming the six families are exhaustive — demote-vs-kill and revise-vs-kill boundary cases will need adversarial families later; the kill bar only covers what the six families test.
- Variation goal compatibility: expression, rationale phrasing, and path may vary across runs; **verdicts, pin/kill decisions, integrity refusals, and ledger contents must not** (brief §Micah's variation goal).

## 6. Next build step
Build the minimal S1 harness: the six-family episode generator (independent trainer/held-out builders), the reflection-ledger comparator of §3.2, and the held-out scorer enforcing K1–K4 — in native Zag, with strength frozen uniform. Run the full scaffold-and-release pass at S1 against one fixed standards set and report the train/held-out gap first; if transfer clears, propose S10 with adversarial boundary-case families.
