# PREREG R2-13 Amendment A2 (pre-results): exact N=10,000 manifest + same-contract ablation

**Date:** 2026-09-23
**Status:** PRE-RESULTS amendment. No valid evaluation battery has been run under
any compliant prereg. This amendment supersedes:
- PREREG_R2-13.md §6 (N=9,925, coarse one-sided ablation), AND
- PREREG_R2-13_AMEND_A1.md (N=10,425, ablation left unchanged).

Both prior documents are preserved in history for transparency; neither
authorizes the evaluation below.

## Defects being corrected

1. **Trial count.** Debate D §7 FS-F bar 1 requires "≤1% false installs on **exactly
   10,000** adversarial trials". The original prereg froze 9,925 (a partial
   filesystem observation). A1 corrected toward the authoritative ledger but
   froze 10,425 — also not 10,000. Neither number satisfies the debate's exact
   wording.

2. **Ablation (bar 3).** Debate D §7 FS-F bar 3 requires: "ablation: coarse vs
   attack-aware features on the design families — refined features must cut
   design-family false installs ≥50% (proves the features did work, so a holdout
   failure indicts the property, not the engineering)". The original prereg's
   "coarse" mode differs from FULL in features, bank usage, and contract path —
   it is a one-sided historical baseline, not a controlled ablation. A1 left it
   unchanged. The required ablation is the **same contract differing only by
   removal of attack-specific features/clauses**: identical exemplars, identical
   false bank, identical decision rule (`dt + 150 < df`), identical margin —
   with ONLY the three attack-specific clauses disabled (TMB-2 harmonic boost,
   SHP-1 occlusion bar, MOT-1 reversed-video). This isolates the causal
   contribution of the attack-aware engineering.

## Frozen exact-10,000 manifest

From the 10,425 SHA-verified adversarial fixtures listed in
`senses/pam-rebuild/round2/forks/R2-7/fixtures_R2A/gen_ledger.jsonl`
(splits `r2a`/`r2a2`; 50 stray on-disk files excluded by ledger-membership as
in A1), the evaluation set is the **first 10,000 in deterministic
byte-sorted path order**.

- Manifest file: `senses/pam-rebuild/round2/work/FS-F/manifest_10000.json`
- Manifest SHA-256: `797e0e44facd1e215ee3b4a501d73eadad5cb2f110d9f16845b38b0d42f999f9`
- Selection rule: sort all 10,425 ledger-listed adversarial paths
  byte-wise; take the first 10,000. Zero RNG. Fully reproducible from the
  ledger.

## Amended bar wordings

- **Bar 1:** ≤1% false installs on **exactly 10,000** adversarial trials
  (≤100 false installs).
- **Bar 2:** unchanged — six novel holdout families frozen in the original
  prereg (COL-1, COL-2, CCN-1, SHP-3, PTC-1, TMB-1); ≤2% false installs per
  family and ≤1% pooled.
- **Bar 3 (corrected):** same-contract attack-feature/clauses-removed ablation
  on the design families (TMB-2, SHP-1, MOT-1). The refined FULL variant must
  cut design-family false installs by ≥50% relative to the ablation. The
  ablation differs from FULL **only** by disabling the three attack-specific
  clauses; all features, exemplars, bank, rule, and margin are identical.

## What did NOT change

Hypothesis, mechanism sketch, feature definitions, contract rule
(`dt + 150 < df`), margin (150), bank construction (12 entries), holdout
family list, scoring definitions (false install = install=1 AND class ≠
truth), determinism requirements (zero RNG, byte-identical reruns,
hash-chained ledger), and the Debate D §7 verdict rule ("if novelty still
kills at >2%/family after genuine feature work, the property is the
ceiling") are unchanged.

## Evaluation plan (frozen)

1. Build FULL binary from the frozen source; smoke-test one fixture per task.
2. Run FULL battery twice over the exact-10,000 manifest (runs A and B);
   `cmp` ledgers byte-identical; independently verify both hash chains.
3. Run the same-contract ablation (mode `noclause`) once over the same
   10,000.
4. Score: overall false-install rate (denominator exactly 10,000); per-family
   and pooled rates on the six holdouts; design-family FULL vs ablation.
5. Verdict ALIVE/DEAD per Debate D: dies on any bar.

## Transparency note

Two noncompliant prereg commits precede this amendment:
- Original: `a809feef45f1301f8fdd67c42488d9c17aa579ed` (N=9,925; coarse ablation)
- A1: `1995e605889ca0fe8b5e1bf60770361334c703aa` (N=10,425; ablation unchanged)

No valid evaluation was run under either. All prior battery attempts used
noncompliant N or noncompliant binaries and are discarded as evidence;
their ledgers are quarantined, not scored.
