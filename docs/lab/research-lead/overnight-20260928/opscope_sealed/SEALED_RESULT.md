# SEALED RESULT: OpScope Step 3 (Sealed Evaluation)

## Verdict: SEALED-PASS

## Kill bars

- K1 PASS. Sealed-eval prereg `b5e3df03e` (SEALED_EVAL_PREREG.md) is a
  strict ancestor of the sealed world commit `7f24f2f9d`
  (verified: `git merge-base --is-ancestor`). No sealed item or sealed
  world file existed before the prereg.
- K2 PASS. All 21 sealed items executed with per-item results below.
- K3 PASS. Pure Zag at every stage: world authoring (hand-written Zag),
  build (znc), runs, byte checks (shell-only `check_no_dash.sh`),
  verification (md5sum, sha256sum, grep, diff, cmp), committing (git).
  No Python at any stage, including scratch and verification. 3/3
  byte-identical runs (md5 `88524b3ec6181c60411fa09b09c6d744`), exit 0,
  zero stderr bytes. No em or en dash bytes in any new file.

## Sealed world (committed before any learner run)

- Commit `7f24f2f9d`: `sealed_gen.zag` (sha256
  `8668e4a9933a99ee73a05661148fae7f33ad0d4bd95b73ba7607c994b04f682f`),
  parts `sealed_items.zag` + `sealed_gen_main.zag`, binary, and
  `sealed_episodes.txt` reference output.
- Sealed seed: 987654321 (chosen at execution time, disclosed here).
- World mechanics (rng, word table, gen_*, build_utt, world_recover_U,
  world_verify_U, world_T) copied verbatim from the frozen world
  `opscope_rebuild/opscope_world.zag` via shell `cat`; only episode
  constructors for 200-220 are new (sealer-authored).
- Oracle audit of the sealed world: all 21 episodes round-trip
  (vrt=1). All 14 NEG targets exclude the negated word's feature
  (T=1 {tak} on every NEG item: the DELETION consequence holds by
  construction). All 7 controls include the word's feature
  (T=33/65/129/257/513/1025/2049).

## Harness fidelity

- `opscope_sealed.zag` = frozen world (verbatim) + frozen learner
  (verbatim) + `sealed_items.zag` + harness main assembled from
  verbatim `sed`-extracted sections of the frozen harness
  (dump fns, frozen world+oracle, learner+training) plus two new
  sealer blocks (sealed oracle, sealed scoring).
- Training reproduction check: the training section output
  (through TRAIN_DONE) is byte-identical to the committed frozen
  `run1.txt` (103 lines, diff empty). The evaluated learner is exactly
  the committed K=2 rebuild learner.
- Cross-check: all 21 sealed items as scored (ids, U sequences, T
  masks) match the committed `sealed_episodes.txt` exactly.

## Sealed falsifier results

| Bar | Frozen requirement | Result |
|-----|--------------------|--------|
| S1 | sealed NEG >= 12/14 | 14/14 PASS |
| S2 | controls == 7/7 | 7/7 PASS |
| S3 | white-box OPREC trig=1, DELETION, sup>=4 | PASS (sup=12) |

Per-item sealed NEG (pred/tgt as feature masks), identical on all 3 runs:
- 200-201 "tak not bal": 2/2 (pred=1 {tak})
- 202-203 "tak not sph": 2/2 (pred=1 {tak})
- 204-205 "tak not cub": 2/2 (pred=1 {tak})
- 206-207 "tak not tri": 2/2 (pred=1 {tak})
- 208-209 "tak not big": 2/2 (pred=1 {tak})
- 210-211 "tak not biger": 2/2 (pred=1 {tak})
- 212-213 "tak not smal": 2/2 (pred=1 {tak})

Per-item controls:
- 214 "tak bal": pred=33 tgt=33 ok
- 215 "tak sph": pred=65 tgt=65 ok
- 216 "tak cub": pred=129 tgt=129 ok
- 217 "tak tri": pred=257 tgt=257 ok
- 218 "tak big": pred=513 tgt=513 ok
- 219 "tak biger": pred=1025 tgt=1025 ok
- 220 "tak smal": pred=2049 tgt=2049 ok

S3 detail: OPREC table shows 7 active entries, all trig=1/sig=0
(DELETION), sup 12/12/12/12/12/14/16, created_at 40..100. The binding
discovered online (trigger unit 1 -> DELETION) is the active router
for every sealed NEG item.

No sealed falsifier fired: SF-NEG silent (14/14), SF-CTRL silent
(7/7, sealed world not defective), SF-WHITEBOX silent (S3 holds).

## Honest scope

SEALED-PASS is pipeline step 3 of 11. It shows the discovered
negator binding generalizes to 7 never-negated familiar words
(including shape, size, and relational biger forms) under a sealed,
sealer-generated world the builder never saw. It claims no L3, no
SURVIVES. Steps 4-11 (independent reproduction, baseline,
alternative-explanation attack, OOD beyond this sealed set,
ablation, transfer/reuse, independent red team, governance audit)
remain open. BUILD-PASS stands.

## Artifacts (this commit)

- `sealed_items.zag`, `sealed_block.zag`, `sealed_score.zag`
  (sealer-authored parts)
- `sealed_harness_main.zag` (assembled main)
- `opscope_sealed.zag` (full sealed harness source)
- `sealed_bin` (147760-byte native binary)
- `sealed_build.err` (compiler warnings only)
- `sealed_run1.txt`, `sealed_run2.txt`, `sealed_run3.txt`
  (byte-identical raw outputs)
- `sealed_run1.err`, `sealed_run2.err`, `sealed_run3.err` (empty)
- `SEALED_RESULT.md` (this file)

## Commits

- `7f24f2f9d` sealed world (K1: after prereg `b5e3df03e`, before any
  learner run)
- (this result commit)
