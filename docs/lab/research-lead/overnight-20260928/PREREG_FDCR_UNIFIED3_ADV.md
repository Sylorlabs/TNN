# PREREG H-FDCR-UNIFIED3 RED TEAM FROZEN

**Date:** 2026-09-29
**Researcher:** H-FDCR-UNIFIED3 Red Team (independent subagent)
**Target:** H-FDCR-UNIFIED3 SURVIVES (6/6), FDCR_UNIFIED3_RESULT.md
**Builder prereg:** PREREG_FDCR_UNIFIED3.md (commit ff25ebaab)
**Builder result:** b973d35d7
**Status:** FROZEN. Attacks must strictly follow this prereg.
**Toolchain:** znc 2026.07.0-dev (edition 2026). Pure Zag. No Python anywhere.

## Mission

Assume the H-FDCR-UNIFIED3 repair claim is false. Attack it on four
preregistered fronts. The frozen K-FU3-1..6 bars are not re-litigated;
a successful attack DOWNGRADED (narrows the repair claim) rather than
KILLS, because the frozen bars stand as executed.

## Attack harness methodology

`fdcr_unified3_adv.zag` = `unified_fdcr3.zag` with ONLY `main()`
replaced by the attack fixtures below. The mechanism region must be
verified byte-identical to the committed `unified_fdcr3.zag` by
`cmp`/`diff` before any attack run. Determinism: 3/3 byte-identical
runs (cmp) for every attack fixture.

## X-FU3-1: order fragility via the extension path (KILL-target)

**Theory.** R1 repaired order-normalized identity inside `con_form`
only. `handle_concept_learn` pass 2 has a second path: when the
subject is ALREADY a concept member (`existing>=0`), new features
extend that concept's feature set (`con_nfeat` grows) WITHOUT any
set-identity check against other concepts. No concept-merge step
exists anywhere. Prediction: the same total fact set yields 1 vs 2
concepts depending on batch order, i.e. the X-FU2-2a fragmentation
class recurs through a trivial 3-batch variation.

**Fixture A (attack order):**
- Batch 1: `T cat | is_a | pet;T cat | color | orange`
  (C0 = {is_a=pet, color=orange}, members {cat})
- Batch 2: `T dog | color | orange;T dog | is_a | pet;T dog | size | big`
  (dog not a member; con_form nfeat=3 vs C0 nfeat=2, no match;
  C1 = {color=orange, is_a=pet, size=big}, members {dog})
- Batch 3: `T cat | size | big`
  (cat IS a member of C0; extension adds size=big;
  C0 = {is_a=pet, color=orange, size=big})
- End state: C0 and C1 hold the SAME feature set but are 2 concepts.
- Then train procedure `cat>tac;dog>god` and read train_con.

**Fixture B (control order, same total fact set):**
- Batch 1: `T cat | is_a | pet;T cat | color | orange`
- Batch 2: `T cat | size | big` (extension: C0 gains size=big)
- Batch 3: `T dog | color | orange;T dog | is_a | pet;T dog | size | big`
  (con_form nfeat=3, set-identity match with C0; dog joins C0)

**Frozen kill criterion:** X-FU3-1 SUCCEEDS (→ DOWNGRADE) iff
Fixture A yields `con_count==2` AND Fixture B yields
`con_count==1` on the identical total fact set. The train_con
observation is supporting evidence (expect -1 in A from the 1v1
vote split, 0 in B). If Fixture A yields `con_count==1`, the
attack FAILS.

## X-FU3-2: member-cap vote splitting (KILL-target)

**Theory.** R2 made the 8-member cap loud, but loudness is not
repair of downstream learning. The procedure majority voter
(`handle_proc_learn_unified`, strict `best_cnt*2>nseg`) counts
only members (`con_find_member_str>=0`); MATCH-NOADD subjects are
skipped silently at the procedure layer. Prediction: with 8
members + 8 identical-feature non-members, the vote ties 8/8 and
the procedure fails to learn (train_con=-1) despite every subject
sharing the feature set and the procedure being a clean reversal.

**Fixture:**
- One batch of 16 facts: `T qaa | is_a | pet;` ... `T qap | is_a | pet`
  (16 distinct 3-char subjects, identical feature set; fits the
  16-fact cap; 8 become members qaa..qah, qai..qap MATCH-NOADD)
- Train procedure `qaa>aaq;qab>baq;qac>caq;qad>daq;qae>eaq;qaf>faq;qag>gaq;qah>haq;qai>iaq;qaj>jaq;qak>kaq;qal>laq;qam>maq;qan>naq;qao>oaq;qap>paq`
  (3-char reversal, mirrors the proven D-T1 pattern)
- Read train_con from the proc record.

**Frozen kill criterion:** X-FU3-2 SUCCEEDS (→ DOWNGRADE) iff
train_con==-1 while con_count==1 and the procedure was discovered
(rc>=0). This demonstrates silent downstream learning failure:
the WARN lines were loud at concept-learn time, but the procedure
layer reports only `concept=-1` with no explanation. If
train_con==0, the attack FAILS.

## X-FU3-3: regression (control)

Rebuild the committed `unified_fdcr3.zag` unmodified and run:
- md5 must equal the frozen `ae29af93d28171c3e37bdca7bf4393b3`;
- final tally must be 27/27;
- Parts A-C output must be byte-identical to frozen
  `FDCR_UNIFIED2_RAW.txt` lines 3-110 except the renamed banner.
If any check fails, report as a REGRESSION finding (separate from
the downgrade verdicts above). Expected: PASS.

## X-FU3-4: source audit

- Verify `con_form` matches R1/R2 of the frozen builder prereg by
  direct source reading (set-identity check, -2 sentinel, single
  caller).
- Verify R3/R4 warn sites count drops and emit on all four caps.
- Verify no test-answer literals (`cat`, `dog`, `tac`, `god`,
  `m8`, `qaa`, `s0`, `s19`, `u`) appear in the mechanism region
  (outside `main()`).
- Verify the `ci==-2` path never calls `con_nfeat`/`con_feat` on
  the sentinel and never asserts membership.
Any prereg deviation or fixture-specific literal in mechanism
code → DOWNGRADE. Findings that match the prereg exactly → PASS.

## Verdict rules

- X-FU3-1 kill criterion met → H-FDCR-UNIFIED3 DOWNGRADED.
- X-FU3-2 kill criterion met → H-FDCR-UNIFIED3 DOWNGRADED.
- X-FU3-3 failure → REGRESSION finding (escalate, do not fold
  into downgrade).
- X-FU3-4 deviation → H-FDCR-UNIFIED3 DOWNGRADED.
- All attacks fail and audit passes → H-FDCR-UNIFIED3 SURVIVES
  this red team.

## Governance

- This prereg is committed ALONE before any attack code is
  written, compiled, or run. Verify strict-ancestor ordering via
  `git merge-base --is-ancestor` before executing.
- Pure Zag. No Python at any stage (no generators, verifiers,
  analysis, or one-liners).
- Only adversary-owned files staged/committed. No other worker's
  files touched. No binaries committed (builds in /tmp only).
- No em dashes in loop documentation.
