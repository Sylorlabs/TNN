# PREREG H-FDCR-UNIFIED3 FROZEN

**Date:** 2026-09-29
**Researcher:** H-FDCR-UNIFIED3 Repair Researcher (independent subagent)
**Target:** H-FDCR-UNIFIED2 DOWNGRADED (red team: FDCR_UNIFIED2_ADV_RESULT.md)
**Status:** FROZEN. Implementation must strictly follow this prereg.
**Toolchain:** znc 2026.07.0-dev (edition 2026). Pure Zag. No Python anywhere.

## Hypothesis

The three H-FDCR-UNIFIED2 red-team downgrades under X-FU2-2 can be
repaired without breaking the 5/5 frozen H-FDCR-UNIFIED2 kill bars or
the 23/23 suite:

- X-FU2-2a (order fragility): repair with order-normalized
  feature-set identity in `con_form`. Same feature SET in different
  fact order must merge to one concept.
- X-FU2-2b (silent fact/member caps, misleading emit): repair with
  explicit drop warnings on all caps and an honest emit when a
  subject matches a feature set but is not added as a member.
- X-FU2-2c (silent feature cap): repair with explicit drop warning
  when features are lost to the accumulation/extension caps.

Honest residual (disclosed, not repaired): the caps themselves
(16 facts/batch, 8 features per subject accumulation, 8 features
per concept, 8 members per concept) remain; this repair makes them
loud, not larger. Enlargement/eviction policy is future work.

## Repairs (frozen)

Implementation file: `unified_fdcr3.zag` = `unified_fdcr2.zag`
copied verbatim, then the changes below. `unified_fdcr2.zag` is
NOT modified.

### R1: Order-normalized feature-set identity (X-FU2-2a)

In `fn con_form`, replace the positional identity check
(`con_feat(W,c,i)` vs `feats[i]` for each i) with a set-identity
check: for each incoming feature in `feats[0..nfeat)`, search the
candidate concept's full feature list `con_feat(W,c,0..nfeat)` for
a content-equal string (`streq`). The match requires all incoming
features found; `con_nfeat(W,c)==nfeat` is still enforced first,
so the two sets have equal cardinality and mutual inclusion
reduces to one-directional inclusion.

Positional comparison is removed. Nothing else in `con_form`
changes.

### R2: Honest member-cap handling (X-FU2-2b, member cap + emit)

`con_form` return contract (frozen): it has exactly one caller
(`handle_concept_learn`, line 1595 of unified_fdcr2.zag).

- On feature-set match WITH member added: return the concept
  index (unchanged).
- On feature-set match with member-add skipped (`nm>=8`, 8-member
  cap): return the sentinel `-2` (MATCH-NOADD). Also emit an
  explicit warning line from `con_form`:
  `ULEARN concept: WARN member cap 8 reached on concept N; subject
  NOT added`.
- No match: create new concept as before (unchanged); return -1
  only if no free concept slot (unchanged).

In `handle_concept_learn` pass 2, where `ci=con_form(...)` is
called, handle `ci==-2` explicitly: emit the subject line as
`ULEARN concept: subject [S] nfeat=F -> MATCH concept N (feature
set known; subject NOT added: 8-member cap)`. The line must NOT
assert `-> concept N` membership for a subject that was not added.
`con_find_member_str` will return -1 for such subjects (honest:
no membership exists).

### R3: Loud fact cap (X-FU2-2b, fact cap)

In `handle_concept_learn` pass 1, the `np<16` guard currently
silently skips facts. Add a counter `ndropped_facts`: increment
when a parseable fact is skipped because `np>=16`. After pass 1,
if `ndropped_facts>0`, emit:
`ULEARN concept: WARN fact cap 16 reached; M facts dropped`.
Return value `np` is unchanged (16 max). All other parse behavior
unchanged.

### R4: Loud feature caps (X-FU2-2c + extension path)

Two silent feature-drop sites:

1. Per-subject accumulation (`nfacc<8` guard in pass 2): add
   counter `ndropped_feat` per subject; increment when a
   deduplicated feature is skipped because `nfacc>=8`. If >0,
   emit `ULEARN concept: WARN feature cap 8 reached for subject
   [S]; M features dropped`.
2. Cross-batch concept extension (`con_nfeat(W,ci)<8` guard):
   add counter `ndropped_ext`; increment when a new feature is
   skipped because the concept is at 8 features. If >0, emit
   `ULEARN concept: WARN feature cap 8 reached on concept N; M
   features dropped`.

All other accumulation/extension behavior unchanged. Dedup
semantics unchanged.

### R5: Documentation

The result doc must list all four caps explicitly with their
values and the new warning behavior:
16 facts per batch, 8 features per subject accumulation,
8 features per concept, 8 members per concept.

## Kill bars (frozen)

All tests run via a new `main()` in `unified_fdcr3.zag` replacing
the old test main; mechanism functions unchanged except R1-R4.
Determinism harness: 3 consecutive runs of each fixture,
byte-identical (cmp).

- **K-FU3-1 (order fragility closed):** Batch 1:
  `T cat | is_a | pet;T cat | color | orange`. Batch 2:
  `T dog | color | orange;T dog | is_a | pet`. PASS requires
  `con_count=1` (was 2 under H-FDCR-UNIFIED2), cat and dog in the
  same concept, AND procedure trained on `cat>tac;dog>god` yields
  `train_con=0` (was -1). The exact X-FU2-2a red-team fixture is
  the regression test.
- **K-FU3-2 (fact cap is loud):** One batch of 20 facts for 20
  distinct subjects. PASS requires `np=16` (unchanged), facts
  17-20 not members (`con_find_member_str` -1), AND a
  `WARN fact cap 16` line appears in output naming 4 dropped.
- **K-FU3-3 (member cap is honest):** 9 subjects with identical
  features (under the 16-fact cap). PASS requires exactly 1
  concept formed, the 9th subject NOT a member
  (`con_find_member_str("m8")=-1`), a `WARN member cap 8` line in
  output, AND the subject emit line for the 9th subject does NOT
  assert membership (no `-> concept 0` claim for it; the
  MATCH-NOADD honest line is used instead).
- **K-FU3-4 (feature cap is loud):** One subject with 10 distinct
  features in one batch. PASS requires the concept formed with
  `nfeat=8`, AND a `WARN feature cap 8` line appears naming
  2 dropped features.
- **K-FU3-5 (regression):** All 5 frozen H-FDCR-UNIFIED2 kill
  bars (K-FU2-1 majority 2/2, K-FU2-2 accumulation 2/2,
  K-FU2-3 trace 1/1, K-FU2-4 suite 23/23, K-FU2-5 determinism)
  still PASS. Outcome bars (train_con values, con_count,
  concept indices, scores, winners) must hold exactly; new WARN
  lines are allowed in output only where the old output had no
  cap-triggering fixture (the frozen fixtures never trigger
  caps, so their raw output must remain byte-identical to the
  H-FDCR-UNIFIED2 evidence except where R1 changes order
  behavior on frozen inputs, which must be documented if it
  occurs).
- **K-FU3-6 (determinism):** 3 consecutive runs of the full
  H-FDCR-UNIFIED3 harness byte-identical (cmp).

## Classification target

Bounded L2 integration repair. No L3 claimed. The caps remain;
they are now explicit rather than silent.

## Governance

- Prereg strictly precedes implementation (this commit contains
  only this prereg file; implementation comes in a later commit
  with a strict-ancestor relationship).
- Pure Zag. No Python at any stage.
- Only owned files staged/committed. No other worker's files
  touched. No binaries committed.
- No em dashes in loop documentation.
