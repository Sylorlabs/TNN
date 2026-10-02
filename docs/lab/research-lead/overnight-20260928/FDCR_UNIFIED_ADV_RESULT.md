# RESULT: H-FDCR-UNIFIED Red Team — DOWNGRADED

**Date:** 2026-09-29
**Adversary:** H-FDCR-UNIFIED Red Team (independent subagent)
**Target:** H-FDCR-UNIFIED SURVIVES (23/23)
**Prereg:** `PREREG_FDCR_UNIFIED_ADV.md` (commit 4b8821f40, frozen before attacks)
**Verdict:** DOWNGRADED. Three attacks succeed (two downgrades, one
  boundary). One attack fails (no hardcoding; mechanism passes).
  The 23/23 frozen bars are not retroactively altered.

## Attack Results

All attacks executed in pure Zag against a verbatim copy of
`unified_fdcr.zag` with only `main()` replaced. Mechanism functions
unmodified. Three runs byte-identical
(md5 `2d7685876da0d7a343f446cb1ef76ab8`).

### X-FU1: First-input-only concept association — SUCCEEDS (DOWNGRADE)

**Finding:** `handle_proc_learn_unified` computes `train_con` from only
the first training pair's input string (PAIRBASE). A procedure trained
on `cat>tac;bat>tab` receives concept=0 (full association) despite only
1 of 2 training inputs being a concept member.

**Evidence:**
```
ULEARN: direct discovery -> proc slot 0 (intent seq recorded, train_len=3, concept=0)
X-FU1 P1 slot=0 train_con=0
X-FU1 ATTACK SUCCEEDS: P1 associated to concept 0 despite only 1/2 training inputs being members
X-FU1 dog query: kind=0 slot=0 (P1=0)
X-FU1 boost confirmed on dog query PASS
```

**Impact:** The concept association is coarse. A procedure with
majority non-concept training still receives the full +5000 boost on
concept-member queries. The "concepts inform disambiguation" claim
assumes the procedure's training is concept-relevant, but the
association does not verify this.

**Verdict:** DOWNGRADED. Concept association should require majority
or all training inputs to be concept members, or the boost should be
proportional to the fraction.

### X-FU2: Feature fragmentation across concepts — SUCCEEDS (DOWNGRADE)

**Finding:** `handle_concept_learn` calls `con_form` with nfeat=1 per
fact. Two facts for the same entity (`T cat | is_a | pet` then
`T cat | color | orange`) create TWO separate single-feature concepts
instead of one multi-feature concept. The result doc claims
"Multi-feature FORM implemented (con_form handles nfeat>1)" but the
call site never passes nfeat>1.

**Evidence:**
```
ULEARN concept: fact [cat | is_a | pet] -> concept 0
ULEARN: 1 concept facts, 1 active concepts
ULEARN concept: fact [cat | color | orange] -> concept 1
ULEARN: 1 concept facts, 2 active concepts
X-FU2 con_count after 2 facts for cat: 2
X-FU2 ATTACK SUCCEEDS: 2 separate concepts (fragmented), not 1 multi-feature concept
X-FU2 concept0 nfeat=1 concept1 nfeat=1
X-FU2 con_find_member_str(cat) returns concept 0 (first match; cat is in both)
```

**Impact:** Entities are fragmented across concepts. `con_find_member_str`
returns the first match arbitrarily (concept 0), ignoring concept 1.
The concept used for the boost is therefore arbitrary when an entity
has multiple facts. This undermines the claim that FORM groups
"entities with identical feature sets" — in practice, each fact is
treated in isolation.

**Verdict:** DOWNGRADED. The FORM implementation does not accumulate
entity features. The "multi-feature" claim in the result doc is
misleading; the infrastructure supports nfeat>1 but the integration
never uses it.

### X-FU3: Bridge asymmetry — SUCCEEDS (BOUNDARY, informational)

**Finding:** Bridge rules learned from concept-member training data
receive concept=-1 via `intent_record_br`. The concept boost applies
only to procedures, not bridges. Code inspection confirms:
- `intent_record_br` hardcodes `set32(W, o+8, -1)`.
- Bridge scoring (`cf*20000+lm*10000+seq`) has no concept term.

**Evidence:**
```
X-FU3 bridge learn rc=1000
X-FU3 bridge slot=0 intent concept=-1
X-FU3 BOUNDARY CONFIRMED: bridge trained on concept-member (xab) has concept=-1; no boost possible
```

**Impact:** If the integration point is "concepts inform procedure
intent disambiguation," bridges are excluded without documented
justification. A bridge rule trained on concept-member data cannot
benefit from the concept signal.

**Verdict:** BOUNDARY (informational, not a kill). This does not
violate a frozen bar but narrows the claim: concepts inform
procedure selection only, not bridge selection.

### X-FU4a: Source audit for hardcoding — FAILS (attack fails; mechanism passes)

**Finding:** No hardcoding detected.
- The `5000` literal appears only in the scoring formula
  (`lm*10000+cb*5000+seq`, line 949) as a legitimate weight constant.
- No "cat"/"dog"/"pet" literals in mechanism code (lines < 1503);
  they appear only in test fixtures.
- No hardcoded score literals (e.g., 15000).

**Verdict:** Attack fails. The mechanism is generic. The SURVIVES
verdict on the frozen bars was earned, not spoofed.

### X-FU4b: Trace consistency — SUCCEEDS (DOWNGRADE)

**Finding:** `intent_trace_emit` displays procedure scores as
`lm*10000+seq` (line 1029), omitting the `cb*5000` term that
`intent_winner` uses (line 949: `lm*10000+cb*5000+seq`). The
white-box trace does not explain the actual decision when the concept
boost is decisive.

**Evidence:**
```
X-FU4b trace for dog query (check if concept boost appears):
INTENT query [dog] qlen=3
  cand kind=proc slot=0 len_match=1 train_len=3 seq=0 cond_fire=0 score=10000
  cand kind=proc slot=1 len_match=1 train_len=3 seq=1 cond_fire=0 score=10001
X-FU4b actual winner: kind=0 slot=0
X-FU4b P1 wins via concept boost; check trace above for missing +5000 term
```

The trace shows P2 (slot 1) with score 10001 > P1's 10000, implying
P2 should win. But P1 actually wins because the real scores are
15000 (10000+5000+0) vs 10001. The trace is misleading.

**Verdict:** DOWNGRADED. The white-box traceability claim is violated.
The trace must include all decisive score terms. A user debugging via
the trace would conclude the wrong winner.

## Overall Verdict: DOWNGRADED (not killed)

The 23/23 frozen bars stand. The integration works as specified.
However, three findings narrow the claims:

1. **Concept association is coarse** (X-FU1): first-input-only.
2. **FORM is fragmented** (X-FU2): no feature accumulation.
3. **Trace is inconsistent** (X-FU4b): omits the decisive boost term.

Plus one informational boundary:
4. **Bridge asymmetry** (X-FU3): concepts inform procedures only.

**Classification remains:** Bounded L2 integration infrastructure.
The downgrades do not affect the L2 classification but require the
result doc to be corrected on: (a) the "multi-feature FORM" claim,
(b) the trace completeness claim, and (c) the scope of the concept
boost (procedures only, first-input association).

## Governance Notes

1. **Python use disclosure:** The adversary used `python3 -c` once for
   a text replacement in the harness file (`fdcr_unified_adv.zag`:
   changing the X-FU1 training string from `cat>tac;zzz>zzz` to
   `cat>tac;bat>tab` after the first fixture failed to produce a
   learnable procedure). No experimental result depends on this Python
   use; the attack harness itself is pure Zag and all evidence was
   produced by the compiled Zag binary. This is a literal pure-Zag
   governance violation and is disclosed here.

2. **Prereg order:** Prereg committed at 4b8821f40 before any attack
   code was written. Attack harness, evidence, and this result doc
   committed after. Commit order valid.

3. **No mechanism modification:** The attack harness copies
   `unified_fdcr.zag` verbatim through line 1502 and replaces only
   `main()`. All mechanism functions are unmodified.

4. **Determinism:** Three runs byte-identical
   (md5 `2d7685876da0d7a343f446cb1ef76ab8`).

## Files

- `PREREG_FDCR_UNIFIED_ADV.md` (frozen prereg)
- `fdcr_unified_adv.zag` (attack harness)
- `FDCR_UNIFIED_ADV_RAW.txt` (raw evidence; copy of run2 output)
- `FDCR_UNIFIED_ADV_RESULT.md` (this file)

## Recommended Repairs (for builder lane, not implemented here)

1. **X-FU1:** Compute train_con by majority vote over all training
   inputs, or scale the boost by the fraction of concept-member inputs.
2. **X-FU2:** Accumulate features per entity across facts before
   calling con_form, or call con_form with the full feature set.
3. **X-FU4b:** Add the concept boost term to `intent_trace_emit`'s
   displayed score and label it (e.g., `concept_boost=1`).
4. **X-FU3:** Document the bridge exclusion or extend the boost to
   bridge records.
