# Native-authorship trial 1 — broker verdict (P2 honest broker)

**Verdict: NO-GO. Stop before P3.** Four of seven kill bars fail (K1, K2, K3, K4).
No red team, no P3. This is a kill, not a void.

**Trial:** does Arm D (deliberative chooser, commit `ab79f1a5c7d`) beat the frozen
lookup Arm L (`e74271015`) on the sealed 26-trap battery (`af629be25`)?
**Answer: no.** D ties L at 16/26; the deliberation adds nothing measurable.

## Scorecard (oracle-grounded: correct ⟺ emitted ans == sealed oracle exp)

| Bar | Statement (frozen PREREG.md) | Result | Pass? |
|---|---|---|---|
| K1 — beats the lookup | D − L ≥ 5 on 26 traps | 16 − 16 = **0** | **NO** |
| K2 — choice quality | D ≥ ceil(0.8 × oracle ceiling) | 16 < ceil(0.8×26) = 21 | **NO** |
| K3a — feature-scramble | constant-fold features flips ≥80% of choices | 21/26 = 80.8% | yes |
| K3b — choice-matters | force choice→candidate 3 changes score by ≥3 | \|16−16\| = **0** | **NO** |
| K3 overall | (a) and (b) | (b) fails | **NO** |
| K4 — no disguised lookup | ≥90% of traps show ≥2 candidates w/ input-specific evidence; 10-trace audit finds none reducible to kind→candidate | 21/26 = 80.8% < 90% | **NO** |
| K5 — no regressions | D = 57/57 on frozen 57Q production battery | 57/57, 0 fallback | yes |
| K6 — determinism | byte-identical reruns + rebuild reproduction; zero RNG | all hold | yes |
| K7 — no oracle leakage | D binary has no oracle bytes; seal predates implementation | both hold | yes |
| Void check | VOID iff L > oracle − 5 | 16 > 21? No | not void |

Oracle ceiling independently confirmed: **26/26** on both arms' candidate machinery
(best-of-9 per trap), matching the generator's sealed claim.

## Per-question summary

L = 16/26: crashes q10, q14, q17 (W25 t[-1] panic class on empty text); wrong q19–q25
(F6 strict-index traps: lookup clamps, oracle demands `?`).
D = 16/26: crash q10; clean refusals q14 (`?`✓), q15, q16 (oracle `0`, refusal `?` ✗),
q17 (`?`✓); wrong q19–q25 — the deliberator picks clampers (CHAR/WORD>CHAR) on every
strict-index trap instead of the strict candidates the oracle rewards.

D differs from L on q9 (END_DIRECT vs WORD>CHAR), q13 (CHAR vs WORD>CHAR),
q15/q16 (refuse vs answer), q18 (WORD?CHARSCAN vs BOTH_ENDS) — but the totals tie.

## Neuter probes (§6)

- **P-feat** (constant-fold all 14 features): 21/26 choice flips (80.8%) → K3a passes,
  barely. Score under folded features: 17/26.
- **P-def** (override choice→candidate 3 post-deliberation): 16/26, delta **0** → K3b
  fails. Caveat: candidate 3 (WORD>CHAR) internally kind-routes via
  `zoom_choose(kind,shape)`, so forcing w=3 does not fix the mechanism — the bar as
  written is satisfied, but it tests less than its author likely intended.
  Supplementary: forcing the truly-fixed candidate 1 (pure CHAR) scores 19/26
  (delta 3) — the deliberation underperforms the best fixed candidate here.
- **P-trace** (blank deliberation trace): 26/26 behaviorally identical
  (exit code, executed chunk, answer) — the trace is instrumentation, steers nothing.

## Trace audit (K4)

- Coverage: 21/26 traps show ≥2 candidates with input-specific evidence (all 9).
  q10 (crash) and q14–q17 (clean pre-deliberation refusals) have no candidate
  evidence → 80.8% < 90% → bar fails as written.
- Deterministic 10-trace audit (qids 0–9): all 10 show genuine input-specific
  deliberation — elimination paths differ by non-kind input properties
  (e.g. S1-shape-single fires only on spaceless texts), terminal rules are keyed on
  non-kind features (ans_unit, addr_depth, edge, needle_hit, count_unit); none is
  a kind→candidate lookup. Caveat: on this battery the winner is observationally
  perfectly predicted by kind (no within-kind winner variation exists), so the
  battery cannot empirically exhibit a non-kind feature flipping a choice.
  See TRACE_AUDIT.md.

## Integrity notes (broker-found, not arm faults)

1. **Arm self-scoring bug (D):** the clean-refusal path hardcodes `correct=0`
   (`chooser.zag` D0 guard). The oracle manifest explicitly blesses `?` for D1/D4.
   Broker scores oracle-grounded (ans == exp): D = 16/26, not the 14/26 the arm
   reports. This correction does not change any bar outcome.
2. **Candidate-machinery delta (D vs frozen L):** D's `dlib.zag` carries
   implementer-added `DEGENERATE GUARD 2026-09-26` empty-span guards absent from
   frozen `intake.zag`; D's candidates refuse cleanly where L's panic
   (q17 c3/c4). A robustness difference in shared machinery, not in the choice rule.
3. **Disk crisis:** home hit 100% mid-sweep; 73 oracle_D runs (c7–c9) were
   invalidated (empty param.bin) and re-run cleanly afterward. Final dataset:
   520/520 runs integrity-verified (param echo, BROKER id match, exit codes).
   One K6 rebuild under ENOSPC produced a 0-byte binary (discarded); the clean
   rebuild reproduces byte-identical output.

## Method

Pure-Zag param-file drivers (`drvL`/`drvD`), one isolated process per
(arm, question); crashes count incorrect. Sources extracted via `git show` from
frozen commits; toolchain SHA-256
`498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef` verified.
Full protocol, pins, and build commands: METHOD.md. Per-question data: SCORES.tsv.
Neuter data: NEUTERS.tsv. Trace audit: TRACE_AUDIT.md. Broker driver sources:
`src/`.

## Bottom line

The deliberative chooser ties the frozen lookup (16–16, need +5), reaches only
16/26 against a 21 bar, gains nothing from its choices over forcing candidate 3,
and its traces cover only 80.8% of traps against a 90% bar. K5–K7 pass, but they
are hygiene bars. **Recommendation: STOP. Do not proceed to P3/red-team.**
