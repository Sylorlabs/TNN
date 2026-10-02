# Inference Repair Result Report (H-INFER)

**Date:** 2026-09-29
**Prereg:** `rep_v2/PREREG_INFER.md` (commit 276709293, frozen before implementation)
**Implementation:** `rep_v2/fdcr_learn.zag` (sibling step, most-specific-preference)
**Verdict:** H-INFER SURVIVES. K-I1 PASS, K-I2 PASS, K-I3 PASS.

## What was changed

Only the sibling inference step of `fdcr_learn.zag` (~line 1272). Step 0
(direct taught facts) and Step 1 (concept direct lookup) are untouched.

Before: sibling evidence (values of the queried relation found in the
leaf-concept intents of fellow members, plus children members) accumulated
into GLOBAL accumulators across all candidates. Any conflict anywhere forced
WITHHOLD.

After (most-specific-preference):
1. Candidates remain ordered by decreasing score = ctx_match*1000 +
   intent_size (no new specificity measure introduced).
2. Sibling evidence is gathered into PER-CANDIDATE accumulators.
3. The first candidate with consistent non-empty evidence decides the
   answer (ans_kind=3). Stop.
4. Conflicting evidence at that first-with-evidence candidate WITHHOLDs
   immediately; less specific candidates are not consulted.
5. Candidates with no evidence are skipped.

## Kill bar verdicts

### K-I1 (disambiguation): PASS

`compose_fixtures/disambig.txt`: 1/1.
`Q e5 | kind => roller (expected roller) [OK] sib`
The most specific candidate C4 {color=red, shape=round} yields roller via
sibling e1; the conflicting less-specific evidence from C5 {color=red}
(block via e2) and C6 {shape=round} (block via e3) no longer vetoes it.

### K-I2 (no regression): PASS

| Fixture | Score | Baseline | Match |
|---------|-------|----------|-------|
| k5 | 4/4 | 4/4 | yes |
| k2 | 5/5 | 5/5 | yes |
| k4 | 2/2 | 2/2 | yes |
| k3_merge | 5/5 | 5/5 | yes |
| mini_world | 8/8 | 8/8 | yes |
| ctx_test | 3/3 | 3/3 | yes |

Per-probe verdicts identical to the pre-change baseline (captured with the
pre-change binary before editing). The three genuine sibling probes
(mini_world PARA) still answer correctly with the sib marker; the three
NEAR WITHHOLD probes still withhold.

### K-I3 (determinism): PASS

Three consecutive runs of every fixture produce byte-identical stdout
(verified via md5sum).

## Interpretation

H-INFER SURVIVES. The inference-side gap identified by the COMPOSE kill is
repaired: most-specific evidence is no longer vetoed by less-specific
conflicting evidence. The change is minimal and surgical (one step, no new
measures, no concept-formation changes), and the predicted non-regression
held exactly.

This closes the disambiguation probe that killed H-COMPOSE on utility. The
COMPOSE redundancy theorem stands (union-COMPOSE remains unnecessary), and
the genuine fix was in inference, as the COMPOSE report predicted.

## Scope

- Bounded to the sibling inference step. No change to FORM, MERGE, SPLIT,
  GRADE, CONTEXTUALIZE, or COMPOSE operators, nor to Step 0 / Step 1.
- Not L3 evidence. This is an inference-procedure repair, not
  representational invention.
- Pure Zag. No Python used at any stage (analysis via grep/sed/wc/md5sum
  only).

## Raw outputs

- `rep_v2/raw_outputs/INFER_DISAMBIG_RAW.txt`
- `rep_v2/raw_outputs/INFER_k5_RAW.txt`
- `rep_v2/raw_outputs/INFER_k2_RAW.txt`
- `rep_v2/raw_outputs/INFER_k4_RAW.txt`
- `rep_v2/raw_outputs/INFER_k3_merge_RAW.txt`
- `rep_v2/raw_outputs/INFER_mini_world_RAW.txt`
- `rep_v2/raw_outputs/INFER_ctx_test_RAW.txt`

## Commits

- 276709293: prereg H-INFER FROZEN (this result's bar)
- (this commit): implementation + result + raw outputs
