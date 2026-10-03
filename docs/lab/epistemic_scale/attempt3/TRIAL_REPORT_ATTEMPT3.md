# Scale Epistemic Attempt 3 — Trial Report: NO-GO

Date: 2026-09-27
Prereg: `~/workspace/epi_a3/PREREG_ATTEMPT3.md` (SHA-256 `497fe9f8436b0cc761898ad4cbba16926521b2426a5be12ec08859ef19e20c46`, Amendments 1–3)
Verdict: **NO-GO** — do not run held-out. The deliberative loop as specified does not operationalize.

## 1. What was attempted

Attempt 3 replaced attempts 1–2's feedforward classifier with a deliberative epistemic loop: parse claims into premise frames (entity/attribute/value/negation/type) → address premises against the mass by entity∧attribute overlap → compare values in pure Zag → per-premise status (SUPPORTED/CONTRADICTED/CONTESTED/UNADDRESSED) → verdict (opinion → lie → fact → contested → undetermined) with causally-bound NEED emission for unaddressed premises. Designed to fix five white-box defects D1–D5 (see `WHITEBOX.md`).

## 2. Clean-room record

Two implementation lines were quarantined before the valid line:
- **Line 1** (`attempt3/BREACH.md`): train labels directed parser development. Invalidated.
- **Line 2** (`attempt3-clean/QUARANTINE.md`): implementer saw labels via class column + class-encoding ID prefixes. Invalidated.
- **Structural fix**: sanitized blind inputs (opaque IDs, deterministic shuffle seed 1545793672, zero label information); honest-broker scoring (coordinator holds sealed mapping, implementer never scores). The valid line (`attempt3-final/`) was built label-blind under this structure.

## 3. Train-LOO results (coordinator-scored, one-shot)

### 3a. Uncontested-standing (initial)

| Bar (prereg §7) | Value | Attempt-2 baseline | Result |
|---|---|---|---|
| False facts ≤ 30 | 0 | 67 | PASS |
| Lie recall ≥ 0.15 | 5/84 = 0.0595 | 0.048 | **FAIL** |
| Opinion recall ≥ 0.90 | 96/140 = 0.6857 | 0.957 | **FAIL** |
| Fact→lie FPs = 0 | 4 | 0 | **FAIL** → escalation |
| Skepticism forced ≤ 0.15 | 0.0000 | 0.179 | PASS |
| Frame well-formedness ≥ 0.90 | 1.0000 | — | PASS |

Confusion (uncontested): Fact 0/17/4/147; Opinion 0/96/0/44; Lie 0/4/5/75; Skepticism 0/2/0/54.

### 3b. Corroborated-standing (automatic §4.3.3 escalation)

| Bar | Value | Result |
|---|---|---|
| False facts ≤ 30 | 0 | PASS |
| Lie recall ≥ 0.15 | 0/84 = 0.0000 | **FAIL** |
| Opinion recall ≥ 0.90 | 96/140 = 0.6857 | **FAIL** |
| Fact→lie FPs = 0 | 0 | PASS |
| Skepticism forced ≤ 0.15 | 0.0000 | PASS |
| Frame well-formedness ≥ 0.90 | 1.0000 | PASS |

All 9 lie verdicts → undetermined (contradictor fires but none survives corroboration). Byte-identical reruns verified both phases. Frozen hashes in `attempt3-final/LOO_REPORT.md`.

## 4. Mechanism-level causes (why NO-GO)

**M1 — SUPPORT is vacuous (prereg design flaw).** The prereg defines SUPPORT as "same value for same entity+attribute" (implemented as same vkind+vcode+polarity). Zero of 985 train addressing pairs satisfy it (implementer cross-checked in Python). Consequences: fact verdicts unreachable (fact recall 0/168), CONTESTED unreachable, and corroborated-standing empty (no contradictor can ever gain standing). The prereg assumed a mass dense with paraphrases; the 448-item mass has none. D1 ("false facts") is "fixed" only by amputation — zero false facts because zero facts. This is not repair.

**M2 — Contradiction detection barely improved (D2 not fixed).** 11 CONTRADICTED premises out of 684; 9 lie verdicts, 5 correct (uncontested) / 0 (corroborated). Attempt 2's broken detector caught 4/84; the D2 fix (word-number map, predicate-negation scope, expanded antonyms, functional attributes) caught 5/84. The value comparison still misses ~94% of contradictions. Grok's pre-registered prediction (parser/value-comparison is the weakest point) confirmed.

**M3 — Opinion detector regressed (D5 worse).** 96/140 = 0.686 vs attempt 2's 134/140 = 0.957. The constructional signals + mass-addressability test are too conservative; 44 opinions fall through to undetermined. The old lexicon, for all its gaps, outperformed the "architectural" replacement on train.

**M4 — Standing dilemma (grok Q1 confirmed empirically).** Uncontested-standing produced 4 fact→lie FPs: false mass items convicting true claims. Corroborated-standing produces zero lie verdicts (M1). There is no safe operating point for the contradiction path on this mass.

## 5. What this means

The white-box diagnosis (D1–D5) correctly identified attempt 2's defects. But the prescribed redesign does not operationalize: **the bottleneck is semantic parsing and value comparison, not verdict logic.** Extracting (entity, attribute, value) frames and comparing values robustly across paraphrase is the load-bearing substrate, and the prereg's SUPPORT/CONTRADICT definitions assume a parser and mass density that don't exist.

Specific consequences:
- The mass-only lie-recall ceiling (~0.28, from white-box) stands, but attempt 3 reaches 0.06/0.00 — the architecture can't even approach the ceiling.
- **Phase 3b is moot as designed**: if SUPPORT never fires on the mass, retrieved evidence can't SUPPORT either; the NEED→evidence→verdict loop has no working verdict arm.
- The fact gate (P≥0.75, R≥0.70) is structurally unpassable when fact is unreachable.

## 6. What would be needed (not attempted — NO-GO stops the line)

A redesign would need: (a) a SUPPORT notion based on entailment/consistency rather than exact-duplicate detection; (b) a value comparator that handles paraphrase (the actual hard problem); (c) an opinion detector that doesn't regress below the lexical baseline. These are research problems, not implementation fixes — which is why the prereg's NO-GO rule exists.

## 7. Artifacts

- `attempt3-final/`: clean-room implementation, frozen build (FREEZE.sha), `deliberate.zag` (both standing levels), LOO outputs + hashes, LOO_REPORT.md, TABLES.md, takeaways.md (verbatim carry-forward).
- `attempt3/` and `attempt3-clean/`: QUARANTINED (invalid). Not committed.
- `blind/`: sanitized inputs + README (hashes recorded). Sealed mapping retained by coordinator only (covers held-out; not committed).
- Prereg (3 amendments), WHITEBOX.md, this report.

## 8. Gate comparison across attempts (train-LOO)

| Gate | Attempt 2 | Attempt 3 (unc) | Attempt 3 (corr) |
|---|---|---|---|
| False facts | 67 | 0 | 0 |
| Lie recall | 0.048 | 0.060 | 0.000 |
| Opinion recall | 0.957 | 0.686 | 0.686 |
| Fact→lie FPs | 0 | 4 | 0 |
| Skepticism forced | 0.179 | 0.000 | 0.000 |
| Fact recall | 0.845 | 0.000 | 0.000 |

Attempt 3 trades attempt 2's defects for worse ones: it eliminates false facts by eliminating facts, barely moves lie recall, and regresses opinion recall. **The deliberative loop hypothesis is falsified for this specification.**
