# PREREG — Deliberate Recall trial (written BEFORE any run, 2026-09-19)

## Hypothesis

A retrieval mechanism built as **deliberate choice** — declare an
information need as an audited hypothesis, then select traces by a fixed
conjunction of symbolic predicates (entity coverage ∧ op entailment ∧
provenance gate ∧ freshness bound), each per-trace decision ledgered —
achieves strictly higher precision than a similarity+top-k baseline at
equal recall on an adversarially-designed curriculum, with every decision
reproducible from the audit ledger and zero randomness anywhere.

## Mechanics

Native Zag trial (`trial/`): `recall_core.zag` (needs table, symbolic
descriptors, NEED_DECLARE, RECALL, recall-ledger replay) imports the
proven MA1 `memory_core.zag`; `recall_trial.zag` is the driver with a
marked SYSTEM / EVALUATOR boundary. Store: 16 slots, layout exactly as
RECALL_DESIGN.md §4. Stage: MANAGE(2). All recalls run at clock=17 (no ma
mutations during the recall phase; pins happen after, batched).

Need formation is protocol-fixed (task → need parameters by fixed table);
the tested claim is the **selection rule**.

## Preregistered expectations (per episode)

Ground-truth relevant sets (EVALUATOR-only constants, never passed to the
system): EP0:{7} EP1:{8} EP2:{9} EP3:{10} EP4:{12,13}.

| ep | deliberate sel | P | R | baseline sel | P | R | deliberate act | baseline act |
|---|---|---|---|---|---|---|---|---|
| EP0 | {7} | 1.0 | 1.0 | {7} | 1.0 | 1.0 | ACT0 ✓ | ACT0 ✓ |
| EP1 | {8} | 1.0 | 1.0 | {1} | 0.0 | 0.0 | ACT1 ✓ | ACT9 ✗ |
| EP2 | {9} | 1.0 | 1.0 | {2} | 0.0 | 0.0 | ACT2 ✓ | ABSTAIN (retrieved ops {B} ⊉ {B,C}) |
| EP3 | {10} | 1.0 | 1.0 | {0} | 0.0 | 0.0 | ACT3 ✓ | ACT0 ✗ |
| EP4 | {12,13} | 1.0 | 1.0 | {0,8} | 0.0 | 0.0 | ACT4 ✓ | ABSTAIN (act codes 10 vs 11 disagree) |

Expected τ-sweep: no single τ ∈ 0..6 reaches (mean P = 1.0, mean R = 1.0);
best τ = 4 with mean F1 = 0.461, mean P = 0.428 (τ=4 admits the tied
distractors: EP1 P=1/3, EP2 P=1/2, EP3 P=1/2; EP0/EP4 select nothing).
Deliberate mean P over EP1–EP4 = 1.0; baseline mean P = 0.0; margin = 1.0.

## Falsification criteria

- **F1 (primary).** Mean precision over adversarial episodes EP1–EP4:
  `meanP_delib − meanP_base ≥ 0.25` AND `meanP_delib ≥ 0.9`. FAIL →
  verdict NEGATIVE (deliberate recall does not beat similarity).
- **F2 (recall guard).** Deliberate recall on every ground-truth required
  set = 1.0. FAIL → verdict at best MIXED (precision bought with recall).
- **F3 (extra-steps).** Best single τ (post-hoc, all episodes): if its
  (mean P, mean R) both ≥ deliberate's → verdict NEGATIVE — the "logic"
  was thresholded similarity with extra steps.
- **F4 (audit).** `ma_replay_check == MA_OK` AND `rc_replay_check`
  passes (descriptors/needs reconstruct exactly; every scan bitmask
  recomputes; every selection rule-consistent; every attached slot
  scanned once per need). FAIL → verdict BLOCKED (apparatus broken, not
  a result about recall).
- **F5 (determinism).** Two runs byte-identical stdout; static grep finds
  no `rng|random|seed|_zag_arg` in trial sources. FAIL → BLOCKED.
- **F6 (predicate coverage).** Each of P2, P3, P4 must be the excluding
  predicate on ≥1 episode (P1 throughout). If a predicate never fires,
  verdict MIXED and the design is thinner than claimed.

## Verdict mapping

- **POSITIVE:** F1 ∧ F2 ∧ ¬F3-fail ∧ F4 ∧ F5 ∧ F6 all hold.
- **NEGATIVE:** F1 fails, or F3 replicates deliberate.
- **MIXED:** F1 holds but F2 or F6 fails (report which).
- **BLOCKED:** F4 or F5 fails, or the trial cannot build/run.

The verdict distinguishes **system determinism** (F5: the system is a
fixed logic; reruns are identical) from **test adversity** (the episodes
are designed to be adversarial; §4 of the design doc). A POSITIVE verdict
means "this deterministic logic beats compensatory scoring on designed
adversarial cases" — not "the world was easy".

## Scale prereg (program law §1)

Trial: S=16, 5 episodes, per-recall O(S). Claim: selection logic is
S-independent (constant predicate work per slot). Next scale test
(preregistered now): **10x distractor scale** — replicate filler and
distractor families ×10 (160 traces; same 5 relevant traces, same needs):
assert identical precision/recall per episode and per-episode recall time
≤ 15x trial time. Known scaling parameter: `RC_AUDIT_CAP` ∝ S·recalls
(100x needs the cap raised; documented, not a redesign).

## No-RNG compliance (program law §2)

No RNG in system decision paths (there is no RNG in the harness either —
adversity is by designed curriculum). Verified by static grep + double-run
identity (F5). No amendment needed: the design was RNG-free from inception.

## What it does NOT show

That need *formation* is good (protocol-fixed here); that the
justification codes ground to anything (they are labels); anything about
natural-language queries; that similarity can never work (only that the
standard compensatory form fails these traps and no single threshold on
the obvious score replicates the logic).
