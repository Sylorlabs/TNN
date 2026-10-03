# ADVERSARY REPORT: H-FDCR-UNIFIED2 Red Team — DOWNGRADED

**Date:** 2026-09-29
**Adversary:** H-FDCR-UNIFIED2 Red Team (independent subagent)
**Target:** H-FDCR-UNIFIED2 SURVIVES (5/5 kill bars, 23/23 preserved)
**Prereg:** `PREREG_FDCR_UNIFIED2_ADV.md`, committed as `d05e7b9e5`
  (strictly before any attack execution)
**Verdict:** DOWNGRADED (not killed). Three preregistered kill
  criteria fired, all under X-FU2-2 (feature accumulation). The
  frozen 5/5 kill bars and 23/23 suite are not invalidated; the
  repairs do what the narrow bars test, but the X-FU2 fragmentation
  class recurs through a trivial variation and the accumulation path
  has silent data-loss gaps.

## 1. Methodology

The adversary assumed the repair claim was false and attacked the
four repairs R1 (majority vote), R2 (feature accumulation), R3
(trace consistency), R4 (bridge concept support).

Harness construction: `fdcr_unified2_adv.zag` = first 1650 lines of
`unified_fdcr2.zag` (everything above the MAIN marker) copied
verbatim, plus a new adversary `main()`. Verbatim check:
`diff <(head -1650 unified_fdcr2.zag) <(head -1650
fdcr_unified2_adv.zag)` produced no output (MECHANISM-VERBATIM-OK).
Only one `fn main` exists in the attack file. A second follow-up
harness `fdcr_unified2_adv2.zag` was built the same way for three
confirmation probes.

Compilation: `znc fdcr_unified2_adv.zag -o /tmp/adv_run1`
(warnings only, non-fatal; binary 150621 bytes, 0 external tools).

Pure Zag: no Python used anywhere. All edits via file tools and
shell; all analysis by reading source and compiled-binary output.

Determinism: three runs of the attack binary byte-identical
(cmp-verified), md5 `01a0a190d1211b06c42b54db6ca56824`.

## 2. X-FU2-1 (majority gaming): HOLDS, with documented boundaries

R1 is implemented exactly as preregistered: per-input concept via
`con_find_member_str`, per-concept counts, top concept selected,
strict `count*2 > nseg`, ties first-seen (strict `>` comparison).

- **X-FU2-1a (duplicate inflation):** First fixture
  (`cat>tac;cat>tac;zzz>zzz`) failed to learn at all: `zzz>zzz`
  contains repeated characters, `pextract` fails on it (the known
  RT2 extractor limitation), direct discovery is skipped, bridge
  induction finds no split, `ULEARN FAIL`. Redo with learnable
  pairs (`cat>tac;cat>tac;zqw>wqz`): direct procedure learned,
  `train_con=0`. Only one distinct entity (cat) is a concept member,
  but the vote counts 2 of 3 inputs by duplication and grants the
  association. This is per-spec (the prereg counts inputs, not
  distinct entities). Informational boundary: the majority is over
  input occurrences, so repeated identical inputs inflate the vote.
  Not a kill; the implementation matches the frozen rule.
- **X-FU2-1b (tie):** Concepts 0={cat,dog} (is_a=pet) and
  1={fish,bird} (is_a=aquatic, distinct features, separate FORM).
  Training `cat>tac;dog>god;fish>hsif;bird>dsfs` produced a bridge
  (direct discovery failed on the 4-pair set; see observation
  below) with emitted `concept=-1`, exactly as the strict-majority
  rule predicts for a 2-vs-2 tie. Informational: the disclosed
  first-seen tie-break is unobservable in principle, because any
  tie for the top count cannot satisfy strict majority. Dead
  disclosure, not a defect.
- **X-FU2-1c (spec fidelity):** `cat>tac;bat>tab` gives -1;
  `cat>tac;dog>god;cat>tac` gives 0. Strict `>` confirmed at the
  boundary.

Observation (out of scope, no kill): direct discovery succeeded
on 2- and 3-pair reversal sets but fell through to bridge induction
on the 4-pair all-reversal set in X-FU2-1b. The vote outcome was
unaffected. The cause was not investigated; it is flagged for the
procedure-invention lane, not this verdict.

Kill criterion (implementation deviating from the preregistered
rule) did not fire. X-FU2-1 HOLDS.

## 3. X-FU2-2 (feature accumulation): THREE KILLS

### 3a. X-FU2-2a: order fragility — KILL-CRITERION MET (DOWNGRADE)

Fixture: batch 1 `T cat | is_a | pet;T cat | color | orange`;
batch 2 `T dog | color | orange;T dog | is_a | pet`. Same feature
SET for cat and dog, different fact ORDER.

Result: `con_count=2`, cat in concept 0, dog in concept 1.
`con_form` merges only on positionally identical feature lists
(source lines ~1224-1263 compare `con_feat(W,c,i)` against
`feats[i]` index by index), so `[is_a=pet, color=orange]` does not
match `[color=orange, is_a=pet]` and a second concept is formed.

Downstream damage, all observed:
- Procedure trained on `cat>tac;dog>god` received
  `train_con=-1` (votes split 1 vs 1 across the two fragments,
  strict majority fails), even though both inputs are
  co-categorized entities.
- `intent_trace_emit` on query `dog` shows the procedure candidate
  with `concept_boost=0`, score 10000. The concept signal the
  repair exists to provide is silently absent.

Causal interpretation: R2 accumulates features per subject but
does not normalize feature order before the FORM identity check,
so the X-FU2 fragmentation class the repair claims to close recurs
whenever two batches list the same features in different order. In
a streaming learner fact order is arbitrary; this is a realistic
variation, not a contrived one. The frozen K-FU2-2 bar only tested
same-order accumulation, so the bar passed while the class
survived. This is precisely the failure mode the preregistered
kill criterion targeted, and it fired.

### 3b. X-FU2-2b: silent fact and member caps — KILL-CRITERION MET (DOWNGRADE)

Fixture: one batch of 20 facts for 20 distinct subjects.

Result: `handle_concept_learn` returned `np=16`; the emit line
reads `ULEARN: 16 concept facts`; facts 17-20 (s16..s19) were
dropped with no explicit warning; `con_find_member_str` returns -1
for all of them.

Additionally, an undisclosed second cap was isolated: `con_form`
adds members only while `nm<8` (8 members per concept, no warning).
Probe C (9 subjects, identical features, 9 facts, under the 16-fact
cap): 1 concept formed, but the 9th subject m8 is not a member
(`con_find_member_str("m8")=-1`). The emit line nevertheless
prints `ULEARN concept: subject [m8] nfeat=1 -> concept 0 (total
nfeat=1)`, because `con_form` returns the concept index even when
the member-add was skipped. The white-box trace therefore asserts
a membership that does not exist. This is the same honesty class
as X-FU4b (which R3 repaired for intent traces) recurring in the
concept trace.

In the 20-fact run, s15 (parsed, within the 16) was likewise not
added as a member (8-member cap), while s16..s19 were never parsed
(16-fact cap). Both caps are silent at runtime. Per the X-RV3-3
precedent, silent loss on a disclosed limit is still a design gap
for a continuing learner; the 8-member cap was not disclosed at
all, and its trace line is actively misleading.

### 3c. X-FU2-2c: silent feature cap — KILL-CRITERION MET (DOWNGRADE)

Fixture: one subject with 10 distinct features in one batch.

Result: concept formed with `nfeat=8`; 2 features silently
dropped, no warning. Same precedent as 3b.

## 4. X-FU2-3 (bridge concept): HOLDS, with a noted boundary

- **X-FU2-3a (source fidelity):** The bridge scoring formula in
  `intent_winner` is exactly `cf*20000+lm*10000+cb*5000+seq` as
  preregistered; the trace computes and displays `concept_boost=`
  and the full score identically. `intent_record_br` (old,
  concept=-1) is defined but has no callers in `unified_fdcr2.zag`.
  `intent_init` clears o+8 to -1 for all 20 intent slots (16 proc +
  4 bridge), so no stale-field path exists. Record layout is
  consistent across `intent_record_proc_con` and
  `intent_record_br_con`. No kill criterion fired.
- **X-FU2-3b (behavioral):** First fixture misdesigned (only 2 of 5
  inputs were members, correctly yielding bcon=-1 per the strict
  majority rule). Redo with genuine 3/5 majority
  (`cat>tac;dog>god;cat>tac;xqw>xxx;zzz>zzz`): bridge formed
  (rc=1000), `bcon=0` recorded correctly. Query `dog` (concept
  member): trace shows `concept_boost=1`, score 15000, winner
  kind=1 (bridge), matching `intent_winner`. R3's trace honesty
  holds for bridges. No wrong selection demonstrated; the boost
  behaved as specified.

Boundary noted: `bcon` is a property of the whole bridge (majority
over all training inputs), not of the sub-rule that actually
fires. The boost applies whenever the query is a concept member,
regardless of which side of the (pos,val) split fires. In the
observed fixture the firing side was member-majority, so no harm
resulted; the mechanism does not check this. Informational.

No frozen test exercises a concept-boosted bridge in competition,
so R4's decision impact remains thinly validated, but the
implementation is faithful to the prereg.

## 5. X-FU2-4 (source audit): HOLDS

- **X-FU2-4a:** `grep` over the mechanism region (lines 1-1650 of
  `unified_fdcr2.zag`) for the test-answer literals `cat`, `dog`,
  `pet`, `tac`, `god`, `fish`, `bird`, `aquatic`, `orange` returned
  no matches. No hardcoding in mechanism code. Fixtures appear
  only in `main()` test code, which is allowed.
- **X-FU2-4b:** R1, R2, R3, R4 implementations match the frozen
  prereg text point for point (verified by direct source reading:
  majority loop lines ~1380-1412, two-pass accumulation lines
  ~1466-1617, trace boost lines ~1018-1089, bridge record and
  scoring lines ~920-975). No fixture-specific branches.

## 6. Verdict rationale

DOWNGRADED, not killed. The distinction matters:

- The 5 frozen kill bars (K-FU2-1..5) and the 23/23 suite are not
  challenged by these findings; the repairs do what the narrow
  bars test.
- But the repair claim was that the three H-FDCR-UNIFIED
  downgrades are repaired. X-FU2-2a shows the fragmentation repair
  fails on a realistic order variation with silent downstream
  damage (lost association, zeroed boost). X-FU2-2b/2c show the
  accumulation path silently loses facts, features, and members,
  with one trace line asserting a false membership. These are
  DOWNGRADE-grade: the mechanism is a bounded L2 integration whose
  concept layer is order-fragile and lossy under caps, not a
  repaired fragmentation story.

Honest classification after this red team: bounded L2 integration
with working majority-vote association on the tested paths,
faithful bridge concept support, and honest intent traces; but
feature-set identity is order-dependent, three silent capacity
caps exist (16 facts/batch, 8 features/concept, 8 members/concept,
the last undisclosed), and one concept-trace line misreports
membership. No L3 is claimed or affected.

## 7. Governance disclosures

1. Prereg `PREREG_FDCR_UNIFIED2_ADV.md` committed as `d05e7b9e5`
   strictly before any attack binary was built or run.
2. Attack harnesses copy mechanism code verbatim (diff-verified);
   only `main()` replaced. No mechanism file was modified.
3. Pure Zag throughout: no Python in fixtures, harnesses, or
   analysis.
4. Two attack fixtures initially misfired for reasons unrelated to
   the repairs (`zzz>zzz` unlearnable due to the known repeated-
   character extractor limitation; a 2/5-majority bridge fixture
   yielding the correctly-computed bcon=-1). Both were redone with
   corrected fixtures and are reported as such; the misfires are
   preserved in `FDCR_UNIFIED2_ADV_RAW.txt`.
5. The direct-discovery fallthrough on the 4-pair reversal set
   (section 2) is an out-of-scope observation, flagged without
   affecting this verdict.

## 8. Commit lineage and files

- Prereg: `PREREG_FDCR_UNIFIED2_ADV.md` (`d05e7b9e5`)
- Attack harness: `fdcr_unified2_adv.zag` (mechanism verbatim,
  adversary main)
- Follow-up harness: `fdcr_unified2_adv2.zag`
- Raw evidence run 1: `FDCR_UNIFIED2_ADV_RAW.txt`
  (determinism md5 `01a0a190d1211b06c42b54db6ca56824`, 3/3
  byte-identical)
- Raw evidence run 2: `FDCR_UNIFIED2_ADV_RAW2.txt`
- This report: `FDCR_UNIFIED2_ADV_RESULT.md`

## 9. Post-report governance note (commit sweep)

After this report was written, a concurrent worker (H-SEG3-ADV red
team) committed the staged adversary files inside its own commit
`c3aaac6b3` ("PREREG H-SEG3-ADV FROZEN") via broad staging. All five
evidence files (`fdcr_unified2_adv.zag`, `fdcr_unified2_adv2.zag`,
`FDCR_UNIFIED2_ADV_RAW.txt`, `FDCR_UNIFIED2_ADV_RAW2.txt`,
`FDCR_UNIFIED2_ADV_RESULT.md`) are present in `c3aaac6b3`,
byte-identical to the adversary's working copies (verified with
`git diff HEAD`). The prereg (`d05e7b9e5`) strictly precedes the
evidence commit, so prereg ordering is preserved; the commit message
is mislabeled, which is a hygiene issue, not a prereg violation.
This addendum documents the sweep so the lineage stays traceable.
