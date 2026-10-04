# Integration: Reliability to Substrate to Verification (C181 + C183 + C185)

**Verdict: INTEGRATION-RSV-COMPLETE.**
**Status:** Three mechanisms merged into one system. Prediction reliability
and source reliability both write to the shared consequence substrate.
Verification consults both. Integrated outperforms separate. Ablations
prove each is load-bearing. 3/3 deterministic byte-identical.

## 1. Architecture (One-System Rule)

Prior state: three separate mechanisms with three separate stores.
- C181: reliability in FACT f8 / MAP f12 (pred_score) + PRED tag-31.
- C183: reliability in private tag-61 records (f28=src layout).
- C185: consequences in tag-61 (kt=1/2 layout).

Integrated state: ONE shared substrate (tag-61).
- kt=1 PURSUIT, kt=2 STRATEGY: unchanged (5 behaviors).
- kt=3 RELIABILITY (new): ka=0 prediction-structure, ka=1 source.
  - Prediction: kb=struct node id. Written by pred_resolve_sub.
  - Source: kb=source id (7/8). Written by ev_observe_src_sub.
  - Fields: f20=attempts, f24=successes, f16=consec_fail.
- C183's private rel store is REMOVED. Substrate is the single store.
  Fewer subsystems, not more.
- Verification (6th behavior): rsv_trust consults BOTH reliabilities
  from the substrate before accepting a prediction.

Config bits (extend se tag-904): 32=PRED read, 64=SRC read.
- P (prediction-only): 63. S (source-only): 95. I (integrated): 127.
- 31 (neither): verification withholds (no basis). Safe default.
- Reads gated, writes unconditional (se DESIGN pattern).

## 2. Batteries and results

Run SHA-256: `685a80ffab07b90b91c3f860a3928b476dc704af6c7045f64c9ddf51d8e11484`
3/3 byte-identical. Binary exit 0.

### 2.1 I1: No interference

All three mechanisms operate simultaneously without corruption.

- I1a src_query: 42 (A preferred, 12/12 > 2/12). PASS.
  Source reliability from substrate drives disagreement resolution.
- I1b ev_predict: X=100, Z=300, Y=500. PASS.
  Prediction machinery ranks correctly.
- Substrate census: `1 7 12/12 cf0; 1 8 2/12 cf4; 0 44 4/4 cf0;
  0 50 0/3 cf3; 0 53 4/4 cf0`.
  Both reliability kinds coexist in tag-61, kt=3, no collisions.
- I1c withholding: -2 -2 -2 -3 on untaught (99,99). PASS.
  The 5 substrate behaviors are unaffected by the new kt=3 records.

### 2.2 I2: Synergy

Ground truth:
- X (10,50): pred 4/4, source B 2/12. Predicts 100, true 200. Trust WRONG.
- Z (30,50): pred 0/3, source A 12/12. Predicts 300, true 400. Trust WRONG.
- Y (20,50): pred 4/4, source A 12/12. Predicts 500, true 500. Trust RIGHT.

| Arm | X (10,50) | Z (30,50) | Y (20,50) | Score |
|-----|-----------|-----------|-----------|-------|
| P (63) prediction-only | 100 (trust, WRONG) | -3 (withhold, RIGHT) | 500 (RIGHT) | 2/3 |
| S (95) source-only | -3 (withhold, RIGHT) | 300 (trust, WRONG) | 500 (RIGHT) | 2/3 |
| I (127) integrated | -3 (RIGHT) | -3 (RIGHT) | 500 (RIGHT) | 3/3 |

Synergy: I=3/3 > P=2/3 and I=3/3 > S=2/3. PASS.

The integrated arm avoids P's false trust (X: reliable prediction from
unreliable source) AND S's false trust (Z: unreliable prediction from
reliable source). Neither separate mechanism sees both failure modes.

### 2.3 I3: Ablation

- Ablate PRED (arm S): loses Z (trusts 300, wrong). Proves prediction
  reliability is load-bearing for the Z decision.
- Ablate SRC (arm P): loses X (trusts 100, wrong). Proves source
  reliability is load-bearing for the X decision.
- Ablate both (config 31): rsv_trust returns -3 (withhold).
  Without substrate reliability, verification has no basis and
  withholds safely rather than trusting blindly. PASS.

Each mechanism is necessary. The substrate is necessary.

## 3. Honest boundaries

1. Z's failure history (0/3) was set up via direct sub_note writes,
   not through live pred_resolve_sub cycles. The write path is
   validated by X's real cycles (4/4 via ev_observe_rsv); Z's setup
   is a test condition, not a mechanism demonstration. A live
   negative-history build is future work (the learner adapts after
   contradiction, so sustained failure requires a non-adapting world).
2. Reliability thresholds (att>=3, majority, cf<2; att>=2 for sources)
   are researcher-set. The VALUES are learner-owned.
3. The trust decision structure (which checks, in which order) is
   researcher-authored. What is trusted is learner-determined.
4. src_query_sub was tested (I1a) but the full P1-P5 switching battery
   was not re-run; the substrate-backed rel_sub_get uses the same
   ratio logic as C183's rel_get.
5. Only FACT predictors (kind=1) carry source tags. MAP predictors
   use prediction reliability only.

## 4. Standing metrics

- RESEARCHER-OWNED: kt=3/ka/kb layout, thresholds, config bits,
  trust decision structure, update rules.
- LEARNER-OWNED: all reliability values (12/12, 2/12, 4/4, 0/3),
  which predictor/source is trusted, the I2 accept/withhold judgments.
- SOURCE-ENUMERABLE FORMS: 0.
- SUF DECISIONS: 0.
- REUSE EVENTS: 0. REVISION EVENTS: 0.
- COGNITION LINES: ~280 (rsv_patch.zag).
- MODES: 0. BRIDGES: 0. HANDLERS: 0. SEMANTIC CASES: 0.
- Subsystems removed: 1 (C183 private rel store).

## 5. Answer to the integration question

**Does the integrated system work?** Yes. No interference (I1).
**Does it outperform the separate mechanisms?** Yes. I=3/3 vs P=2/3,
S=2/3 (I2 synergy).
**Ablation: remove one mechanism, do the others still work?** Yes.
Each degrades gracefully to the remaining mechanism; removing both
withholds safely (I3).

The One-System Rule holds: one substrate, six behaviors, one fewer
private store than the sum of the parts.

## 6. Artifacts

`docs/lab/research-lead/overnight-20260928/integration_rsv/`:
- NAMECHECK.md (Step 0 guard, provenance, constraints)
- REPORT.md (this file)
- rsv_base.zag (copy of se_base.zag, reference)
- rsv_machinery.zag (copy of se_machinery.zag, reference)
- rsv_behaviors.zag (copy of se_behaviors.zag, reference)
- rsv_patch.zag (integration: ~280 lines, NEW)
- rsv_driver.zag (batteries I1/I2/I3, NEW)
- rsv_full.zag (assembled, 2116 lines)
- rsv_bin (binary)
- rsv_run1/2/3.txt (SHA-256 685a80ff..., 3/3 identical)
- compile.log

Constraints honored: unfrozen variant only; frozen source read-only;
pure Zag via pinned znc; safebin active; zero Python; zero em/en dashes
byte-verified; paper untouched; nothing pushed; explicit pathspecs.
