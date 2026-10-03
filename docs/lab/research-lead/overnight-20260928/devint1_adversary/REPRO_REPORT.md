# DEVINT1 Independent Reproduction Report

Worker: independent reproduction + adversary subagent.
Date: 2026-09-30.
Target: DEVINT1, builder commit `476c24b3d`, prereg `4b50ff7d4`.

## Verdict: REPRODUCED

## Evidence

1. **Source provenance (from committed blob, never working tree):**
   `devint1.zag` (1079 lines) extracted via
   `git show 476c24b3d:.../devint_worker1/devint1.zag` to `/tmp/devint1_repro/`.

2. **Prereg lineage:** `git merge-base --is-ancestor 4b50ff7d4 476c24b3d`
   -> YES, strict ancestor verified.

3. **Compilation:** frozen toolchain `znc 2026.07.0-dev (edition 2026)`
   compiled the committed source successfully (exit 0).

4. **Determinism:** 3 runs, all exit 0, zero stderr bytes, `cmp` byte-identical
   3/3. md5 `612205f6e8a36f7f6e04134f3ef8014e`, exact match to the builder's
   claimed raw md5. Output also byte-identical to the committed
   `DEVINT1_RAW.txt` blob.

5. **Purity:** zero `.py` files in the `4b50ff7d4..476c24b3d` range.
   Verification used znc, bash, git, grep, cmp, md5sum only. No Python.

6. **Kill bars (all 4, checked against the committed raw output):**
   - B1 persistence: 11 `STATE-CONT` lines, one process, counts
     non-decreasing (4,8,29 -> ... -> 13,20,127). PASS.
   - B2 stage function: S1 12 episodes; S2 6/6 correct segmentations;
     S3 4 concepts (bik:11 gup:14 zol:10 tav:10); S4 12 bigrams;
     S5 4 ACTIVE rules; S6 treat=4 ctrl=5, held-out 5/5 both;
     S7 4 rule-contradictions + 2 boundary-violations;
     S8 INQUIRY ctx=bik A=bik->gup B=bik->zol, episode bikzoltav fed,
     accuracy 1/6 both; S9 1 rollback (bik->gup), survivor bik->zol,
     accuracy treat 3/6; S10 evictions treat=17 ctrl=18, probe 8/12 vs 0/12;
     S11 recognition 17/17, procedure reuse 3/3. PASS.
   - B3 synergy: S1 4<5 positive; S2 8/12>0/12 positive; S3 refine 1v0
     positive (ctrl degenerate 0/0 honestly reported); S4 neutral
     (treat-k=5=ctrl-k=5, disclosed width match). PASS.
   - B4 governance: pure Zag throughout; no em-dash bytes in owned docs.
     PASS.
   Result: **4/4 reproduced from committed source.**

## Key observations for the adversary phase

- The S1 lexicon is built from all 12 episodes before segmentation is used
  downstream (disclosed deviation 2). Attack A1 tests the online variant.
- The S4 control is fixed-width-3, matching the true morpheme width
  (disclosed). Attack A2 adds fw2/fw4/random-width controls.
- The S3 control denominator is degenerate (0/0); the builder reported this
  honestly. Attack A3 reimplements independently.
- Synergy is currently correlational (treat-vs-ctrl gaps). Attack A4 ablates
  each upstream structure independently.
- Interference before S11 is 20 episodes. Attack A5 uses 240.
- No restart test exists. Attack A6 serializes state across process death.

This is a reproduction verdict only (step: independent reproduction). It does
not promote DEVINT1; the six adversarial attacks (prereg `60701a55f`) are
running. Do NOT call DEVINT1 SURVIVES before they complete.
