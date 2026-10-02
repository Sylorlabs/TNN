# PREREG: H-FDCR-UNIFIED2 RED TEAM (X-FU2-1 .. X-FU2-4) FROZEN

**Date:** 2026-09-29
**Adversary:** H-FDCR-UNIFIED2 Red Team (independent subagent)
**Target:** H-FDCR-UNIFIED2 SURVIVES (5/5 kill bars, 23/23 preserved;
  FDCR_UNIFIED2_RESULT.md)
**Assumption:** The repair claim is false. Attack accordingly.
**Status:** FROZEN. No attack runs before this prereg is committed.

## Rules

- Pure Zag. No Python in fixtures, harnesses, or analysis.
- Attack fixtures live in a copy of `unified_fdcr2.zag` with only
  `main()` replaced (mechanism functions verbatim). New file:
  `fdcr_unified2_adv.zag`.
- Determinism: 3/3 byte-identical runs (cmp-verified).
- If any attack meets its kill criterion, H-FDCR-UNIFIED2 is KILLED
  or DOWNGRADED as stated. Report honestly either way.

## X-FU2-1 (Majority gaming): can a wrong majority be manufactured?

R1 rule under test (from PREREG_FDCR_UNIFIED2.md): for each training
input compute concept via `con_find_member_str`; count per distinct
concept; select top; require strict majority `count*2 > nseg`;
ties: first-seen wins (disclosed).

- **X-FU2-1a (duplicate inflation):** Fresh W. Concept 0 = {cat, dog}
  via one batch `T cat | is_a | pet;T dog | is_a | pet`. Train
  `cat>tac;cat>tac;zzz>zzz`. Read train_con via
  `intent_proc_base(W,slot)+8`. Predicted per-spec: cnt=2, 2*2>3,
  train_con=0. This documents that the vote counts duplicate inputs,
  not distinct entities. Informational boundary unless the
  implementation deviates from spec.
- **X-FU2-1b (tie-break unobservable):** Fresh W. Concept 0 = {cat,
  dog} (is_a=pet), concept 1 = {fish, bird} (is_a=aquatic, distinct
  features so FORM creates a second concept). Train
  `cat>tac;dog>god;fish>hsif;bird>dsfs`. Predicted per-spec: top
  count ties 2 vs 2, 2*2>4 false, train_con=-1. Informational: the
  disclosed first-seen tie-break can never affect the outcome,
  because any tie for the top count fails strict majority.
- **X-FU2-1c (spec fidelity):** Re-run the K-FU2-1a boundary
  (`cat>tac;bat>tab` -> -1) and a 3/3 member case
  (`cat>tac;dog>god;cat>tac` -> 0) to verify the strict `>` and
  `count*2>nseg` are implemented as preregistered.
- **Kill criterion:** DOWNGRADE if the implementation deviates from
  the preregistered rule (e.g. `>=` instead of `>`, first-input-only
  fallback, or a majority manufactured from non-member inputs).

## X-FU2-2 (Feature accumulation): grouping failures and silent loss

R2 rule under test: two-pass accumulation, dedup, cross-batch
extension via `con_find_member_str`, else `con_form` once with the
full set; `con_form` merges only on positionally identical feature
lists (observed in source at con_form, lines ~1224-1263).

- **X-FU2-2a (order fragility):** Fresh W. Batch 1:
  `T cat | is_a | pet;T cat | color | orange`. Batch 2:
  `T dog | color | orange;T dog | is_a | pet` (same feature SET,
  different order). Observe `con_count(W)`,
  `con_find_member_str(W,"cat")`, `con_find_member_str(W,"dog")`.
  Then train `cat>tac;dog>god` and read train_con; run
  `intent_trace_emit(W,"dog")` and observe the candidate's
  concept_boost. Predicted: con_count==2 (fragmentation recurs via
  order), cat->0, dog->1, train_con==-1, concept_boost=0 on the dog
  query. **Kill criterion: DOWNGRADE if con_count==2.** The X-FU2
  fragmentation class the repair claims to close recurs whenever
  feature order differs; the "multi-feature FORM" grouping is
  order-fragile, and the majority vote then fails on genuinely
  co-categorized entities.
- **X-FU2-2b (16-fact batch cap):** Fresh W. One batch of 20 facts
  for 20 distinct subjects (`T s0 | is_a | pet;...;T s19 | is_a |
  pet`). Observe the return value of `handle_concept_learn`, the
  emitted text, and whether s16..s19 are concept members via
  `con_find_member_str`. **Kill criterion: DOWNGRADE if facts beyond
  16 are silently dropped with no explicit drop warning** (robustness
  gap; X-RV3-3 precedent: silent loss on a disclosed limit is still
  a design gap for a continuing learner).
- **X-FU2-2c (8-feature cap):** Fresh W. One subject with 10 distinct
  features in one batch. Observe `con_nfeat` for its concept.
  **Kill criterion: DOWNGRADE if features beyond 8 are silently
  dropped with no explicit warning** (same precedent as 2b).

## X-FU2-3 (Bridge concept): does the boost cause wrong selection?

R4 rule under test: `intent_record_br_con` stores majority-vote
concept for bridges; `intent_winner` bridge score is
`cf*20000+lm*10000+cb*5000+seq`; trace shows the boost.

- **X-FU2-3a (source fidelity):** Verify the bridge scoring formula,
  the trace formula, and the record layout exactly match the prereg;
  verify `intent_record_br` (old, concept=-1) has no callers in
  `unified_fdcr2.zag`; verify `intent_init` clears o+8 for all 20
  slots. **Kill criterion: KILL if the boost is hardcoded to a
  fixture (e.g. literal concept index or literal score); DOWNGRADE
  if the formula deviates from the prereg.**
- **X-FU2-3b (behavioral):** Attempt to form a bridge whose training
  inputs have a concept majority, record bcon via
  `intent_br_base(W,bslot)+8`, then run `intent_winner` and
  `intent_trace_emit` on a concept-member query and check the
  displayed winner matches the actual winner and the boost term is
  the only score difference vs the prereg formula. **Kill criterion:
  DOWNGRADE if the boost produces a winner that the trace
  contradicts, or a concept-associated bridge beats a procedure with
  verbatim training evidence for the same query.** If no bridge
  fixture is achievable with reasonable effort, record BOUNDARY:
  R4's decision impact is unvalidated by any frozen test (no 23/23
  or kill-bar test exercises a concept-boosted bridge in
  competition).

## X-FU2-4 (Source audit)

- **X-FU2-4a:** No test-answer literals (`cat`, `dog`, `pet`,
  `tac`, `god`, `fish`, `bird`) in mechanism code (everything above
  the MAIN marker). Fixtures in main() are allowed.
- **X-FU2-4b:** R1/R2/R3/R4 implementations match the frozen prereg
  text; no fixture-specific branches.
- **Kill criterion: KILL if mechanism code contains test-answer
  literals or fixture-specific branches; DOWNGRADE on any other
  prereg deviation.**

## Governance

- Prereg commit strictly precedes any attack execution.
- New files only: `PREREG_FDCR_UNIFIED2_ADV.md` (this file),
  `fdcr_unified2_adv.zag` (attack harness),
  `FDCR_UNIFIED2_ADV_RAW.txt` (attack output, run 1),
  `FDCR_UNIFIED2_ADV_RESULT.md` (adversary report).
- No em dashes in documentation.
