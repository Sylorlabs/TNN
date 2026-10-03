# RESULT: OpScope Step 6 Alternative-Explanation Attack

## Verdict: OPSCOPE-ATTACK-KILLS

FA-SUFFIX fired. The alternative explanation H1 (not-triggered suffix
suppression) is confirmed; the word-scoped negation claim (H0) is refuted.

## Kill bars

- K1 PASS. Attack prereg `eeca946f4` (PREREG_ATTACK.md) was committed alone
  before any attack code, build script, binary, or run existed. Amendment 1
  (`afde02d2d`, PREREG_ATTACK_AMEND1.md) corrected an objective arithmetic
  error (1<<7=128, not 64) and was committed before the corrected re-run.
  Both are strict ancestors of the implementation commit (verified via
  `git log` ancestry; the prereg contains no attack code and the attack code
  did not exist at prereg time).
- K2 PASS. All 4 attack probes ran against the frozen trained learner with
  learning OFF. Per-probe (pred, world_T) results below. 3/3 byte-identical
  runs (md5 `f5d36286f84ac64ce818a1df16db929c`), exit 0, zero stderr bytes.
  Training reproduction: the training section (CHECK seen=20 through the
  OPREC table) is byte-identical to the committed sealed `sealed_run1.txt`
  (diff empty). Round-trip holds for all 4 probes (vrt=1) and all 120
  training episodes.
- K3 PASS. Pure Zag at every stage: hand-authored Zag attack code, znc build,
  shell-only verification (md5sum, sha256sum, grep, diff, cmp, git). Zero
  Python invocations at any stage, including scratch and verification. No em
  or en dash bytes (shell-only `check_no_dash.sh`). 3/3 byte-identical stdout.

## Per-probe results (identical on all 3 runs)

| Probe | Utterance | Learner pred | world_T | Finding |
|-------|-----------|--------------|---------|---------|
| ATK1 | "tak not bal cub" (0,1,5,7) | 1 | 129 | FA-SUFFIX fires |
| ATK2 | "cub not bal" (7,1,5) | 129 | 128 | FA-CONST silent |
| ATK3 | "tak cub not bal" (0,7,1,5) | 129 | 129 | FA-POS silent |
| ATK4 | "tak bal not cub" (0,5,1,7) | 33 | 33 | FA-PREFIX silent |

Scenes: ATK1/2/3 target = cube (shape 1); ATK4 target = ball (shape 0).
Distractors fixed: obj1=(color 1, shape 2, size 1), obj2=(color 2, shape 2, size 0).

## What was killed

H0 (word-scoped deletion): the claim that the learner's "not" operator deletes
the feature of the specific negated word while preserving other words'
features. ATK1 discriminates: on "tak not bal cub" with a cube target,
word-scoped deletion predicts 129 ({tak, cub}); the learner predicts 1
({tak}). The learner does not bind the deletion to the negated word.

## What was confirmed (H1)

H1 (not-triggered suffix suppression): the learner outputs the DEFAULT
prototype features of words before "not" and contributes nothing for words
at/after "not". Mechanism: `interpret` = or_default(prefix) | or_op(suffix),
and every operator record learned the empty residual (training NEG episodes
always had empty residual R = T ^ (T & rp)), so or_op is vacuous. The learner
never needs to know the negated word's feature; it ignores the suffix. On the
training/sealed distribution ("not" always followed by exactly one content
word) H1 is extensionally identical to negation, which is why S1/S2/S3 passed.

## What survives (secondary characterization)

- H2 (not-to-1 shortcut) REFUTED: ATK2 "cub not bal" predicts 129
  (= recmask(cub) = {bit0, bit7}), not 1. The prefix is genuinely computed.
  (The 129 vs 128 gap to world_T is the ubiquitous-tak prototype artifact:
  bit0 appears in every word prototype because "tak" is in every training
  utterance and always satisfies. Documented, not a negation failure.)
- H3 (positional trigger) REFUTED: ATK3 "tak cub not bal" predicts 129 = 129.
  The trigger is lexical (scans for word id 1) with a positional prefix/suffix
  split; it works mid-utterance.
- ATK4 "tak bal not cub" predicts 33 = 33: the operator composes correctly
  with a non-trivial prefix.

Net: the learner discovered a genuine compositional operator (lexically
triggered by "not", positional split, generalizes to new words and positions),
but the operator is suffix suppression, not word-scoped feature deletion.
The sealed S3 white-box evidence (OPREC trig=1 -> DELETION) is consistent with
both readings; this attack resolves the ambiguity against the word-scoped
reading.

## Amendment history (transparency)

The first attack run used the prereg's hand-computed T values (65/64/65/33),
which contained an arithmetic error: cub is word 7, so its feature is bit7 =
128, not 64. The program's frozen world_T correctly output (129/128/129/33),
causing the falsifier flags to mis-fire on the first run (FA-SUFFIX flag 0
despite ATK1 pred=1; spurious FA-POS). The substantive finding (ATK1 pred=1,
confirming H1) was unaffected. Amendment 1 corrected the constants
(129/128/129/33) without changing hypotheses, probe constructions, or verdict
logic, was committed before the corrected re-run, and the corrected run's
flags agree with the verdict. The original prereg commit is retained
unmodified for audit.

## Honest scope

Step 6 of 11 only. This kills the word-scoped reading of the negation claim
and replaces it with the suffix-suppression characterization (a bounded-L2
mechanism). It does not test every alternative explanation, does not promote
or retire the mechanism, and makes no L3 claim. Steps 7-11 (OOD, ablation,
transfer/reuse, independent red team, governance audit) remain open.
BUILD-PASS stands for the mechanism under its corrected characterization.

## Artifacts (this commit)

- `attack_items.zag` (attacker-authored probe constructors)
- `attack_harness_main.zag` (attacker-authored; training loop exact replica)
- `opscope_attack.zag` (assembled: frozen world verbatim + frozen learner
  verbatim + attacker parts; sha256
  `ea490df8f8c13177db55cc77c2dbea17ea9d8e0794e75b6aefbec06d930ab824`)
- `attack_bin` (sha256
  `d90dcc50155b3f6b077e6449f645b30c911537c075ffd2121ae1f8037c4c8e95`)
- `attack_build.err`, `attack_run1/2/3.txt`, `attack_run1/2/3.err`
- Frozen inputs reused verbatim: `../opscope_rebuild/opscope_world.zag`
  (sha256 `a17f033bf46572a8fac734f14f861d825c84c020b5bb036b51bf253d9ea54542`),
  `../opscope_rebuild/opscope_learner.zag` (sha256
  `d12325c1bcc7d30c193498f6a33fd3fe4a6f2593c606115bfc4414926dfd35f7`)
