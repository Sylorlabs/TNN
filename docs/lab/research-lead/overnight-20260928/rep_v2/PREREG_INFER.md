# Preregistration: FDCR Most-Specific-Preference Inference (H-INFER)

**Date:** 2026-09-29
**Status:** FROZEN (this commit precedes implementation)
**Parent work:** COMPOSE kill (RESULT_COMPOSE.md) identified the genuine gap as
inference-side: "sibling evidence accumulates globally across candidates, so the
correct specific evidence (via {red,round}) is vetoed by conflicting
less-specific evidence (via {red} and {round})."

## Hypothesis H-INFER

Changing the FDCR sibling inference step from global evidence accumulation to
most-specific-preference will enable the disambiguation probe to pass while
preserving every currently passing score.

## Current mechanism (to be changed)

File: `rep_v2/fdcr_learn.zag`, sibling step (~line 1272).

Candidates are ordered by decreasing score = ctx_match*1000 + intent_size
(most specific first). The sibling step currently accumulates sibling evidence
(values of the queried relation found in the leaf-concept intents of fellow
members, plus children members) into GLOBAL accumulators `seen_o`/`seen_n`
across ALL candidates. Any conflict anywhere (seen_n > 0) forces WITHHOLD.

Consequence: on `compose_fixtures/disambig.txt`, probe `Q e5 | kind` gets
roller from the most specific candidate C4 {color=red, shape=round} (via
sibling e1), but C5 {color=red} and C6 {shape=round} contribute block via e2
and e3, so the global pool conflicts and the probe WITHHOLDs (0/1).

## Proposed mechanism

Most-specific-preference sibling inference:

1. Specificity measure: the existing candidate ordering (score =
   ctx_match*1000 + intent_size, decreasing). No new measure is introduced.
2. For each candidate in order, gather sibling evidence into PER-CANDIDATE
   accumulators (same member loop and children loop as now, but scoped to
   the candidate).
3. The FIRST candidate whose evidence is consistent and non-empty
   (ev_o >= 0, ev_n == 0) decides the answer (ans_kind=3). Stop.
4. If the first candidate with any evidence has CONFLICTING evidence
   (ev_n > 0), WITHHOLD immediately. Do not consult less specific
   candidates. Rationale: the most relevant evidence is ambiguous, so
   weaker evidence cannot resolve it; falling through would be
   cherry-picking.
5. Candidates with no evidence are skipped (fall through to less specific).

Only the sibling step changes. Step 0 (direct taught facts) and Step 1
(concept direct lookup) are untouched.

## Predicted behavior on disambig.txt

`Q e5 | kind`: candidates are C4 (size 2), C5 (size 1), C6 (size 1).
C4's fellow member e1 yields kind=roller, consistent. Answer: roller,
ans_kind=3 (sib). Probe passes.

## Predicted non-regression

The only behavior change versus the current mechanism is in the case:
most specific candidate has consistent evidence X AND some less specific
candidate has evidence conflicting with X. Currently that WITHHOLDs;
under H-INFER it answers X.

Traced by hand, no currently passing probe is in that case:
- mini_world PARA probes (the only genuine sibling probes, 3/3): e.g.
  squeezer/sqz_heat: most specific candidate C1 (leaf, size 3) has no
  sibling evidence (singleton member); next candidate C8 {sqz_emit,
  sqz_glow} yields consistent velx. Same answer under both mechanisms.
- All k5/k2/k4/k3_merge/ctx probes are answered by Step 0 or Step 1
  (per the FDCR red-team finding), so the sibling step never runs for them.
- mini_world NEAR WITHHOLD probes: norpaline and vellux are singleton
  leaves with no fellow members, so no sibling evidence exists at any
  level under either mechanism. Still WITHHOLD.

## Kill bars (frozen)

- K-I1 (disambiguation): `compose_fixtures/disambig.txt` scores 1/1;
  `Q e5 | kind` answers roller with ans_kind=3 (sib marker in output).
- K-I2 (no regression): k5 4/4, k2 5/5, k4 2/2, k3_merge 5/5,
  mini_world 8/8, ctx_test 3/3, all scores and per-probe verdicts
  identical to the pre-change baseline.
- K-I3 (determinism): three consecutive runs of every fixture produce
  byte-identical stdout.

## Failure modes (what would kill H-INFER)

- disambig still WITHHOLDs or answers wrong: K-I1 FAIL, H-INFER KILLED.
- Any fixture score drops or any probe verdict changes: K-I2 FAIL,
  H-INFER KILLED (or the change must be repaired; no bar weakening).
- Non-deterministic output: K-I3 FAIL.

## Scope

- Bounded to the sibling inference step. No change to concept formation
  (FORM/MERGE/SPLIT/GRADE/CONTEXTUALIZE/COMPOSE), Step 0, or Step 1.
- Not L3 evidence. This is an inference-procedure repair, not
  representational invention.
- Pure Zag only. No Python anywhere.
