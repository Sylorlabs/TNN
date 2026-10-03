# PREREG: OpScope Step 6 Alternative-Explanation Attack

## Status
FROZEN. Committed alone before any attack code, build script, binary, or run exists.

## Step 0: standing-rules name-check
Read the standing-rules block at the top of `LOOP_STATE.md` in the repository root:
the `## Standing owner rules` section, the `## Standing owner rule: fork testing`
section, the `## Standing ruling: pure-Zag red line scope` section, and the
`## Standing rule: shell-only byte checks` section.

Rules in force and how they are honored for this task:
1. PURE ZAG ONLY. All attack code is hand-authored Zag. Builds use the repo `znc`
   only. Verification uses shell tools (md5sum, sha256sum, grep, diff, cmp) and
   git only. No Python is invoked at any stage, including scratch, analysis,
   and byte checks. Disclosure does not cure use, so there is nothing to disclose.
2. Image judge rule: not applicable (no images).
3. Fork testing: noted; this task does not create branches or forks.
4. Pure-Zag scope: the attack episodes are constructed by hand-authored Zag code
   (fixture provisioning counts as loop work and is Zag-only).
5. Shell-only byte checks: dash checks use
   `docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh`,
   never python3.

## Pipeline context
Steps 1-5 complete for OpScope (operator/scope developmental language):
- Step 1 prereg: `1fd2f0752`. Step 2 implementation: `837c02c59` (OPSCOPE-REBUILD-PASS).
- Step 3 sealed eval: `7ca508cd0` (SEALED-PASS; S1 14/14, S2 7/7, S3 OPREC trig=1 DELETION sup=12).
- Step 4 repro: `daafbebbb` (OPSCOPE-REPRO-PASS).
- Step 5 baseline: `4c4287c50` (OPSCOPE-BASELINE-PASS; B-MEM 0/14, B-NN 8/14, B-CONST 14/14 but 0/7 controls).

## Claim under attack
The learner discovered a negation operator: a lexically triggered binding
(trigger word 1 = "not" -> DELETION) that deletes the negated word's feature
while preserving the other words' features. Evidence: sealed S1/S2/S3 and the
OPREC table (7 active entries, all trig=1, sig=0 DELETION).

## Alternative explanations
- H1 (suffix suppression): the learner implements not-triggered suffix
  suppression. It outputs the DEFAULT prototype features of words before "not"
  and contributes nothing for words at/after "not". It does NOT bind the
  deletion to the specific negated word. On the training/sealed distribution
  ("not" always followed by exactly one content word) H1 is extensionally
  identical to word-scoped deletion, but it is strictly simpler (no need to
  identify which word is negated; the negated word is ignored, so its feature
  never needs to be known).
- H2 (not-to-1 shortcut): the learner outputs T=1 whenever "not" appears,
  without computing the prefix features.
- H3 (positional trigger): the trigger fires on word position, not on the
  word "not". (Mechanism code shows lexical scan, but this is tested
  behaviorally anyway via a mid-utterance "not".)

## Attack battery
All probes use the frozen trained learner (training replicated exactly per the
sealed harness: episodes 0-99 from `gen_episodes` with seed 123456789, one-pass
online, learning ON), then scored with learning OFF. Training reproduction is
verified: the training-section output through TRAIN_DONE must be byte-identical
to the committed sealed `sealed_run1.txt` training section.

Probe episodes are hand-constructed scenes (not from any generator). Each scene
has 3 objects; object 0 is the target (tgt=0). Other objects are fixed
distractors: obj1 = (color 1, shape 2, size 1), obj2 = (color 2, shape 2,
size 0). Episode type byte = 5 (attack marker; unread by learner and world_T).
Round-trip (`world_recover_U` + `world_verify_U`) must hold (vrt=1) for every
probe, else the probe is VOID.

Word ids: 0=tak 1=not 5=bal 7=cub.

### ATK1: scope of deletion (H0 vs H1 discriminator)
- Utterance: "tak not bal cub" (wids 0,1,5,7), n=4, ulen=12.
- Scene: target = (color 0, shape 1, size 0) [a cube].
- world_T: tak->bit0, not->0, bal->0 (shape!=0), cub->bit7. T = 65.
- H0 (word-scoped deletion) predicts 65 ({tak, cub}).
- H1 (suffix suppression) predicts 1 ({tak}).
- Mechanism analysis predicts the learner outputs 1.

### ATK2: prefix genuineness (H2 discriminator)
- Utterance: "cub not bal" (wids 7,1,5), n=3, ulen=9.
- Scene: target = (color 0, shape 1, size 0) [a cube].
- world_T: cub->bit7, not->0, bal->0. T = 64.
- H2 (not->1 shortcut) predicts 1.
- Genuine prefix computation predicts recmask(cub) = {bit0, bit7} = 65
  (bit0 is in every word prototype because "tak" appears in every training
  utterance and always satisfies; bit7 is cub's feature, present in all 17
  training occurrences of cub).
- Decision: predict==1 confirms H2. predict==65 refutes H2 (the 65 vs 64 gap
  to world_T is the ubiquitous-tak prototype artifact, documented here, not a
  negation failure).

### ATK3: mid-utterance trigger (H3 discriminator)
- Utterance: "tak cub not bal" (wids 0,7,1,5), n=4, ulen=12.
- Scene: target = (color 0, shape 1, size 0) [a cube].
- world_T: tak->bit0, cub->bit7, not->0, bal->0. T = 65.
- Lexical trigger with positional split predicts 65.
- Mechanism analysis predicts the learner outputs 65.

### ATK4: rich prefix with negation
- Utterance: "tak bal not cub" (wids 0,5,1,7), n=4, ulen=12.
- Scene: target = (color 0, shape 0, size 0) [a ball].
- world_T: tak->bit0, bal->bit5, not->0, cub->0 (shape!=1). T = 33.
- Mechanism analysis predicts the learner outputs 33
  (or_default([tak,bal]) = recmask(tak)|recmask(bal) = 1|33 = 33; suffix [cub]
  contributes nothing).

## Verdict rule
Apply in order:
1. If ATK1 predicts 1 (and world_T=65, round-trip holds): H1 CONFIRMED, H0
   REFUTED. Verdict: OPSCOPE-ATTACK-KILLS. The word-scoped negation claim is
   killed. The surviving characterization is a not-triggered suffix-suppression
   operator (bounded-L2 mechanism, still lexically triggered and compositional,
   but not word-scoped deletion). ATK2/3/4 are reported as secondary
   characterization.
2. Else if ATK1 predicts 65: H0 survives ATK1. Then:
   a. If ATK2 predicts 1: OPSCOPE-ATTACK-KILLS (H2 confirmed: not->1 shortcut).
   b. Else if ATK3 != 65 or ATK4 != 33: OPSCOPE-ATTACK-KILLS (state which probe
      and the observed vs expected values).
   c. Else: OPSCOPE-ATTACK-SURVIVES.
3. If any probe's round-trip fails (vrt=0) or training does not reproduce
   byte-identically, the affected probe is VOID and the verdict is
   OPSCOPE-ATTACK-INCONCLUSIVE with the defect documented. (This is a
   methodology guard, not a pass.)

## Falsifier/attack labels
- FA-SUFFIX: fires iff ATK1 predicts 1 while world_T=65 (H1 confirmed).
- FA-CONST: fires iff ATK2 predicts 1 (H2 confirmed).
- FA-POS: fires iff ATK3 != 65 (trigger not lexical/positional-split broken).
- FA-PREFIX: fires iff ATK4 != 33 (prefix computation broken under negation).

## Kill bars
- K1: This prereg is committed alone before any attack implementation, build
  script, binary, or run exists. Verified via `git log` ancestry.
- K2: All 4 attack probes run against the frozen trained learner with learning
  OFF; per-probe (pred, world_T, ok-vs-mechanism) results committed; 3/3
  byte-identical runs.
- K3: Pure Zag at every stage (hand-authored Zag, znc build, shell verification
  only). Zero Python invocations. No em/en dash bytes (shell-only checker).
  3/3 byte-identical stdout, exit 0, zero stderr bytes.

## Honest scope
Step 6 of 11 only. This attacks the word-scoped reading of the negation claim.
It does not test every alternative explanation and does not by itself promote
or retire the mechanism. No L3 claim is made or tested here. BUILD-PASS stands
unless the verdict rule fires KILLS, in which case the word-scoped negation
claim is killed and replaced by the suffix-suppression characterization.

## Commits
- This prereg: committed alone under
  `docs/lab/research-lead/overnight-20260928/opscope_attack/PREREG_ATTACK.md`.
- Implementation + result: separate later commit(s) under the same owned path.
