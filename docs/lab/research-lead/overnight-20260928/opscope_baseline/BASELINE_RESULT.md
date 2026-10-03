# BASELINE RESULT: OpScope Step 5 (Simple-Baseline Comparison)

## Verdict: OPSCOPE-BASELINE-PASS

No simple baseline reproduces the learner's sealed pattern
(S1 14/14 NEG, S2 7/7 controls). The sealed result is not
explainable by memorization, nearest-neighbor copying, or constant
prediction.

## Kill bars

- K1 PASS. Prereg `de0db4b64` (PREREG_BASELINE.md) strictly precedes
  the implementation commit (verified: prereg is an ancestor; no
  baseline source existed before it).
- K2 PASS. All three baselines ran on all 21 sealed items with
  per-item (pred, tgt, ok) in the committed logs below.
- K3 PASS. Pure Zag at every stage: hand-authored Zag, znc build,
  shell verification (md5sum, grep, diff). Zero Python anywhere.
  3/3 byte-identical runs (md5
  `c5799dc818d0f10eb0ba0597cb313fff`), exit 0, zero stderr bytes.
  No em or en dash bytes (shell-only check_no_dash.sh clean).

## Baseline scores (identical on all 3 runs)

| Baseline | S1 (NEG 14) | S2 (controls 7) | Hits (12/14, 7/7)? |
|----------|-------------|-----------------|-------------------|
| B-MEM (exact memorization) | 0/14 | 0/7 | No |
| B-NN (nearest neighbor) | 8/14 | 0/7 | No |
| B-CONST (always {tak}) | 14/14 | 0/7 | No |
| Learner (sealed, `7ca508cd0`) | 14/14 | 7/7 | Yes |

## Why each baseline fails

### B-MEM: 0/14, 0/7

No sealed utterance exactly matches any training episode 0-99.
Every sealed item contains "tak" (wid 0) in a novel combination:
"tak not X" and "tak X" for X in {bal,sph,cub,tri,big,biger,smal}
never appear verbatim in training. B-MEM abstains (-1) on all 21.

### B-NN: 8/14, 0/7

Nearest neighbor by word-set overlap (tie-break: lowest episode id).

On NEG items 200-205 ("tak not bal/sph/cub"), B-NN selects
training episodes 0/4/8 (overlap 2 via shared words) whose targets
are 37/69/133, not 1. Wrong.

On NEG items 206-213 ("tak not tri/big/biger/smal"), B-NN selects
training episode 24 ("tak not grn", overlap 2), whose target is 1.
Correct, 8/8.

On all 7 controls ("tak X"), B-NN selects training episodes whose
targets lack the "tak" feature in the right combination (e.g.,
pred=37 vs tgt=33). Wrong, 0/7.

B-NN thus exploits the single training negation "tak not grn" for
a subset of NEG items, but cannot reproduce the full pattern. It
does not discover a general DELETION operation; it copies one
similar episode.

### B-CONST: 14/14, 0/7

Always predicting T=1 ({tak}) trivially matches all 14 NEG targets
(T=1 by construction). It scores 0/7 on controls, whose targets are
33/65/129/257/513/1025/2049. The controls discriminate: the learner
gets 7/7, the constant gets 0/7.

## Verdict rule applied

OPSCOPE-BASELINE-PASS iff no baseline achieves (S1 >= 12 AND
S2 == 7). B-MEM: no. B-NN: no (8/14 < 12, 0/7). B-CONST: no
(0/7). Verdict: OPSCOPE-BASELINE-PASS.

## Honest scope

This is pipeline step 5 of 11. It shows the learner's sealed
pattern survives three specific simple-baseline attacks. It does
not test every conceivable simple rule, and it does not prove the
learner discovered the DELETION operation; it only rules out
verbatim memorization, nearest-training-episode copying, and
constant prediction as sufficient explanations. No L3 claim, no
SURVIVES. Steps 6-11 (alternative-explanation attack, OOD, ablation,
transfer/reuse, independent red team, governance audit) remain open.
BUILD-PASS stands.

## Artifacts (this commit)

- `PREREG_BASELINE.md` (frozen prereg, commit `de0db4b64`)
- `baseline_world.zag` (frozen world code, verbatim copy)
- `baseline_main.zag` (baseline main, sealer-authored)
- `baseline.zag` (assembled: world + main)
- `baseline_bin` (native binary)
- `baseline_build.err` (compiler warnings only)
- `baseline_run1.txt`, `baseline_run2.txt`, `baseline_run3.txt`
  (byte-identical raw outputs)
- `baseline_run1.err`, `baseline_run2.err`, `baseline_run3.err`
  (empty)
- `BASELINE_RESULT.md` (this file)
