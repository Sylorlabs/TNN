# H-FDCR-UNIFIED3 RED TEAM RESULT: DOWNGRADED (not killed)

**Date:** 2026-09-29
**Researcher:** H-FDCR-UNIFIED3 Red Team (independent subagent)
**Target:** H-FDCR-UNIFIED3 SURVIVES (6/6), FDCR_UNIFIED3_RESULT.md
**Adversary prereg:** PREREG_FDCR_UNIFIED3_ADV.md (commit 29805386c,
  frozen BEFORE any attack code was written, compiled, or run)
**Verdict:** DOWNGRADED. Two of two empirical kill criteria met
  (X-FU3-1, X-FU3-2). X-FU3-3 regression control PASSES.
  X-FU3-4 source audit PASSES with findings. The frozen K-FU3-1..6
  bars are not re-litigated and still hold; this downgrade narrows
  the repair claim only, exactly per the FU2-ADV precedent.

## Methodology

Attack harness `fdcr_unified3_adv.zag`: lines 1-1715 of the
committed `unified_fdcr3.zag` copied verbatim (cmp-verified,
MECHANISM-VERBATIM-OK), only `main()` replaced with the four
preregistered attack fixtures. Toolchain znc 2026.07.0-dev;
compilation warnings only, non-fatal. Pure Zag throughout: zero
Python in fixtures, harnesses, or analysis. Determinism: 3/3
byte-identical runs per fixture (cmp), raw md5
`22c011105cc52eec13d1d2ac2141a6c7`.

## X-FU3-1: order fragility via the extension path — KILL MET

R1 repaired order-normalized identity inside `con_form` only.
`handle_concept_learn` pass 2 has a second, unrepaired path: when
the subject is ALREADY a concept member (`existing>=0`), new
features extend that concept's feature set with NO set-identity
check against other concepts, and no concept-merge step exists
anywhere in the file.

**Fixture A (attack order):**
- Batch 1 `T cat | is_a | pet;T cat | color | orange`
  -> C0 = {is_a=pet, color=orange}, members {cat}
- Batch 2 `T dog | color | orange;T dog | is_a | pet;T dog | size | big`
  -> dog not a member; con_form nfeat=3 vs C0 nfeat=2, no match;
  C1 = {color=orange, is_a=pet, size=big}, members {dog}
- Batch 3 `T cat | size | big`
  -> cat IS a member of C0; extension adds size=big;
  C0 = {is_a=pet, color=orange, size=big}

End state: C0 and C1 hold the SAME feature set but are 2
concepts. `con_count=2`, cat=0, dog=1.

**Fixture B (control order, identical total fact set):**
- Batch 1 cat 2 feats -> C0; Batch 2 `T cat | size | big`
  -> extension, C0 gains size=big; Batch 3 dog 3 feats ->
  con_form nfeat=3, set-identity MATCH, dog joins C0.
- `con_count=1`, cat=0, dog=0.

**Kill criterion (frozen):** A yields 2 AND B yields 1 on the
identical total fact set. MET. Batch order changes the concept
count: the X-FU2-2a fragmentation class recurs through a trivial
3-batch variation. The frozen K-FU3-1 bar ("same feature SET in
different fact order must merge to one concept") does not
survive this variation.

**Supporting evidence:** procedure `cat>tac;dog>god` in attack
order -> rc=0, train_con=-1 (1v1 vote split across the two
fragment concepts); in control order -> rc=0, train_con=0.
The downstream vote damage is real, not cosmetic.

## X-FU3-2: member-cap vote splitting — KILL MET

R2 made the 8-member cap loud, but loudness does not repair
downstream learning. The procedure majority voter counts only
members (`con_find_member_str>=0`); MATCH-NOADD subjects are
skipped silently at the procedure layer (strict `best_cnt*2>nseg`).

**Fixture:** one batch of 16 facts, 16 distinct 3-char subjects
qaa..qap, all `is_a=pet` (fits the 16-fact cap). Result:
con_count=1, qaa=0 (member), qap=-1 (MATCH-NOADD), exactly per
the loud-cap design.

**Procedure:** 16-pair 3-char reversal
`qaa>aaq;...;qap>paq` (mirrors the proven D-T1 pattern).
rc=1000 (bridge induction discovered it); train_con read from
the bridge intent record: **train_con=-1**.

**Kill criterion (frozen):** train_con==-1 while con_count==1
and the procedure was discovered. MET. 8 inputs vote concept 0,
8 are skipped, 8*2=16 is not > 16, so the procedure FAILS to
learn despite all 16 subjects sharing the identical feature set
and the procedure being a clean reversal. The WARN lines were
loud at concept-learn time, but the procedure layer reports only
`concept=-1` with no explanation: silent downstream learning
failure. Eviction-policy absence (the repair's disclosed
residual) has a concrete, demonstrated cost.

## X-FU3-3: regression control — PASS

Rebuilt the committed `unified_fdcr3.zag` unmodified:
- md5 `ae29af93d28171c3e37bdca7bf4393b3` reproduces the frozen
  evidence exactly;
- final tally 27/27;
- raw output byte-identical to frozen FDCR_UNIFIED3_RAW.txt;
- Parts A-C (lines 3-110) byte-identical to frozen
  FDCR_UNIFIED2_RAW.txt.
No regression. The builder's 6/6 stand.

## X-FU3-4: source audit — PASS with findings

- `con_form` matches frozen R1/R2 point for point by direct
  source reading: order-normalized set-identity (one-directional
  inclusion + `con_nfeat` equality first; valid because the
  per-subject accumulator dedups and extension checks
  duplicates), -2 MATCH-NOADD sentinel with WARN, exactly one
  caller (line 1647), matching the prereg's frozen contract.
- R3/R4: all four cap sites count drops and emit WARN lines;
  unparseable segments are correctly NOT counted as dropped
  facts.
- No test-answer literals (`cat`, `dog`, `tac`, `god`, `m8`,
  `qaa`, `s0`, `s19`, `u`) anywhere in the mechanism region
  (lines 1-1716).
- The `ci==-2` path never calls `con_nfeat`/`con_feat` on the
  sentinel (guarded by `ci>=0`) and never asserts membership.
- **Finding:** the extension branch (`existing>=0`) performs no
  set-identity check against other concepts and no merge can
  ever run afterward. This is the structural source of the
  X-FU3-1 kill, confirmed by reading, not just by the fixture.

## Revised claim

H-FDCR-UNIFIED3's R1 is a formation-path order-normalization,
not a general order-fragility closure: batch-order still
controls concept count through the extension path (2 vs 1 on
the identical fact set). R2/R3/R4 made the caps loud, but the
8-member cap still silently breaks procedure learning at the
vote layer (train_con=-1 with no procedure-layer explanation)
whenever non-members reach the strict-majority tie point.
Bounded L2 integration, narrowed. No L3 claimed or affected.

## Governance disclosures

1. Adversary prereg committed alone at 29805386c BEFORE any
   attack code was written, compiled, or run. Ordering verified:
   the result commit is a strict descendant.
2. That prereg commit ALSO contains three ROUTER5_* files from a
   concurrent worker, swept in by broad-pathspec staging before
   my commit landed. My prereg file was verified byte-intact
   afterward (`git show HEAD:...` head check). Recorded, not
   hidden: the same broad-staging pattern previously recorded.
3. Attack harness mechanism region verified byte-identical to
   committed `unified_fdcr3.zag` by `cmp` before every run.
4. Pure Zag throughout: no Python at any stage. No binaries
   committed (builds in /tmp only). Only the four
   adversary-owned files staged/committed. No em dashes in loop
   documentation.

## Deliverables (all committed on `tnn-native-lab`)

- `PREREG_FDCR_UNIFIED3_ADV.md` — frozen attack prereg
  (29805386c)
- `fdcr_unified3_adv.zag` — attack harness (mechanism
  byte-verbatim, main replaced)
- `FDCR_UNIFIED3_ADV_RAW.txt` — raw evidence, 3/3 byte-identical
  (md5 `22c011105cc52eec13d1d2ac2141a6c7`)
- `FDCR_UNIFIED3_ADV_RESULT.md` — this report

## Suggested follow-ups for parent

1. H-FDCR-UNIFIED4 repair directions: post-extension
   concept-merge check (after the extension branch grows a
   concept's feature set, test set-identity against all other
   concepts and merge on match), and a member-eviction or
   vote-counting policy so non-members do not silently void
   procedure learning.
2. The X-FU3-1A/B fixture pair is the ready regression test for
   any rework (con_count must be 1 in BOTH orders).
3. The research paper's H-FDCR-UNIFIED3 section needs this
   downgrade entry.
