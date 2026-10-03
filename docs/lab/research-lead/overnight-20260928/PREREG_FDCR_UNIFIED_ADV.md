# Prereg: H-FDCR-UNIFIED Red Team (FROZEN)

**Date:** 2026-09-29
**Adversary:** H-FDCR-UNIFIED Red Team (independent subagent)
**Target:** H-FDCR-UNIFIED SURVIVES (23/23), commits 7939ffa82 (prereg),
  b517525d7 (implementation), 52d2962fc (result)
**Status:** FROZEN. Attacks must follow this document. No attack may be
  weakened after results. This prereg's commit must strictly precede the
  attack-execution commit.

## Mission

Independently attack the H-FDCR-UNIFIED claim. Assume it is false. If any
attack succeeds by its frozen kill criterion, H-FDCR-UNIFIED is KILLED
or DOWNGRADED as specified. Report honestly; failed attacks are negative
evidence and must be reported as such.

## Target Description (from RESULT_FDCR_UNIFIED.md)

- `unified_fdcr.zag` (1922 lines): unified learner + FORM-only concept store.
- Router code 5 = CONCEPT_LEARN for `T subj | rel | obj` fact lines.
- Concept store: 8 concepts x 76 bytes at CCONCEPT=1804. FORM groups
  entities with identical feature sets.
- Concept boost: +5000 in intent scoring when query and procedure share
  a concept. Procedure score = lm*10000 + cb*5000 + seq. Bridge score =
  cf*20000 + lm*10000 + seq (no concept term).
- `intent_record_proc_con` records train_con = concept of FIRST training
  input only (via con_find_member_str on PAIRBASE input).
- `intent_record_br` always records concept = -1.
- `handle_concept_learn` processes each fact with nfeat=1 (single feature
  per call to con_form).

## Attacks

### X-FU1: First-input-only concept association (DOWNGRADE if succeeds)

**Theory:** `handle_proc_learn_unified` computes train_con from only the
first training pair's input string. A procedure trained on mixed data
(e.g., `cat>tac;zzz>zzz`) receives the full concept boost if the first
input happens to be a concept member, regardless of the remaining
training inputs. The association is coarse and can misattribute.

**Procedure:**
1. Form concept {cat, dog} via `T cat | is_a | pet`, `T dog | is_a | pet`.
2. Train P1 on `cat>tac;zzz>zzz` (two pairs; only first is concept member).
3. Inspect P1's intent record: check concept field.
4. Query `dog`; check whether P1 receives the concept boost.

**Kill criterion (DOWNGRADE):** If P1's intent record shows concept=0
(associated) despite only 1 of 2 training inputs being a concept member,
AND P1 receives the +5000 boost on a `dog` query, then the concept
association is unsound. Verdict: DOWNGRADED (concept association needs
majority or all-inputs rule).

**Predicted outcome:** Attack succeeds (downgrade). The code path is
explicit: only PAIRBASE (first pair) is checked.

### X-FU2: Feature fragmentation across concepts (DOWNGRADE if succeeds)

**Theory:** `handle_concept_learn` calls `con_form` with nfeat=1 per
fact. An entity with multiple facts (e.g., `T cat | is_a | pet` then
`T cat | color | orange`) is fragmented across separate single-feature
concepts instead of accumulating into one multi-feature concept. The
result doc claims "Multi-feature FORM implemented" but the call site
never passes nfeat>1.

**Procedure:**
1. Fresh workspace. `handle_concept_learn(W, "T cat | is_a | pet")`.
2. `handle_concept_learn(W, "T cat | color | orange")`.
3. Check con_count(W). Check con_nfeat for each active concept.
4. Check con_find_member_str(W, "cat"): which concept index is returned?

**Kill criterion (DOWNGRADE):** If con_count=2 (two separate concepts)
instead of 1 concept with nfeat=2, then FORM is fragmented and the
"multi-feature FORM" claim is misleading. Verdict: DOWNGRADED
(concept formation does not accumulate entity features).

**Predicted outcome:** Attack succeeds (downgrade). Each fact creates a
separate single-feature concept by code inspection.

### X-FU3: Bridge asymmetry, no concept boost for bridge rules (BOUNDARY if succeeds)

**Theory:** Bridge rules learned from concept-member training data
receive concept=-1 via `intent_record_br`. The concept boost applies
only to procedures, not bridges. If the integration point is "concepts
inform procedure intent disambiguation," bridges are a second-class
path with no documented justification.

**Procedure:**
1. Form concept {cat, dog}.
2. Train input that triggers bridge_learn with first input `cat`
   (e.g., data where direct discovery fails but bridge succeeds;
   use the builder's own bridge training shape from Part A tests).
3. Inspect the bridge intent record's concept field.
4. Code inspection: confirm `intent_record_br` hardcodes -1 and the
   bridge scoring line has no cb term.

**Kill criterion (BOUNDARY, not kill):** If the bridge intent record
shows concept=-1 despite training on a concept member, AND code
inspection confirms no concept term in bridge scoring, record as a
declared-asymmetry boundary. This does not violate a frozen bar but
narrows the "concepts inform disambiguation" claim to procedures only.
Verdict: BOUNDARY (informational).

**Predicted outcome:** Attack succeeds as boundary. The code is explicit.

### X-FU4: Source audit and trace consistency (KILL if hardcoding found; DOWNGRADE if trace inconsistent)

**Theory (a):** Verify no hardcoded test values. Check that con_form
compares by string content (not pointer equality), that the +5000 is a
named constant applied uniformly, and that C-T2's expected winner is
not special-cased.

**Theory (b):** `intent_trace_emit` displays procedure scores as
`lm*10000+seq`, omitting the `cb*5000` term that `intent_winner` uses.
The white-box trace therefore does not explain the actual decision
when the concept boost is decisive. This violates the white-box
traceability requirement.

**Procedure:**
1. Grep for literals: `5000`, `cat`, `dog`, `pet` in decision logic
   (excluding test fixtures and emit strings).
2. Run C-T2 scenario with `intent_trace_emit` on the `dog` query.
   Compare the trace's displayed scores with the actual winner.
3. Check whether the trace mentions the concept boost anywhere.

**Kill criterion (a) (KILL):** If any decision-logic literal hardcodes
the C-T1/C-T2 test expectations (e.g., a literal comparison against
"cat"/"dog"/"pet" outside the test fixture section, or a literal 15000
score), H-FDCR-UNIFIED is KILLED as spoofed.

**Downgrade criterion (b) (DOWNGRADE):** If the trace omits the concept
boost from displayed scores while the boost determines the winner,
the white-box traceability claim is violated. Verdict: DOWNGRADED
(trace must include all decisive score terms).

**Predicted outcome:** (a) fails (no hardcoding; the code is generic).
(b) succeeds (downgrade): the trace line `emit(i32s(lm*10000+seq))`
omits cb*5000 by inspection.

## Rules

- Pure Zag only. No Python in attacks, harnesses, or verification.
- Attacks run against the committed `unified_fdcr.zag` at HEAD, or a
  verbatim copy with only `main()` replaced (same pattern as the
  REVISE2 red team). Mechanism functions must not be modified.
- Each attack's raw output committed as evidence.
- Determinism: each attack run 3 times, byte-identical.
- If an attack's fixture is defective (does not test what the prereg
  claims), declare it VOID with evidence, amend transparently, and
  re-freeze before executing the corrected version. Kill criteria
  unchanged by amendments.

## Deliverables

- `PREREG_FDCR_UNIFIED_ADV.md` (this file), committed first.
- `fdcr_unified_adv.zag` (attack harness), `FDCR_UNIFIED_ADV_RAW.txt`
  (raw evidence), `FDCR_UNIFIED_ADV_RESULT.md` (verdict), committed
  after this prereg.

## Commit Order

1. This prereg (PREREG_FDCR_UNIFIED_ADV.md) — frozen before attacks.
2. Attack implementation + evidence + result doc.

Prereg commit must strictly precede attack commit.
