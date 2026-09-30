# RESULT: Operator/Scope R1-R4 Build (devlang_opscope)

## Verdict: OPSCOPE-R1R4-PASS

## Kill bars

- K1 PASS. Prereg committed alone as `51c54e262` before any
  implementation file existed. Verified: `git merge-base
  --is-ancestor 51c54e262 <impl>` holds (checked before commit).
- K2 PASS. F1-F5 executed with per-item results vs frozen predictions
  (table below). T1 reported vs the frozen 0/3 baseline; full battery
  vs the 16/20 baseline.
- K3 PASS. Pure Zag, zero Python at every step (implementation,
  harness, world, build, byte checks, verification). 3/3
  byte-identical runs (md5 aec8f51abc7192b0a9857f8b51390d81), exit 0,
  zero stderr. No em dashes (shell-only check_no_dash.sh).

## Falsifier results (frozen predictions vs observed)

| F | Frozen bar | Prediction | Observed | Result |
|---|-----------|------------|----------|--------|
| F1 | T1 109-111 3/3 + white-box OPREC | PASS (3/3 vs 0/3) | 3/3; OPREC trig=1 sig=0 created=40 sup=12 | PASS |
| F2 | T3 scope-shift 109-111 | PASS (3/3) | 3/3 | PASS |
| F3 | source audit 0/0/0 | PASS | 0/0/0 (verbatim below) | PASS |
| F4 | ablation strictly worse on T1 | PASS (0/3 < 3/3; 17/20) | 0/3 < 3/3; 17/20; negdrop=3 | PASS |
| F5 | >=16/20 and SIZE 3/3 | PASS (20/20) | 20/20; SIZE 3/3 | PASS |

Per-item frozen test (pred/tgt as feature masks, all ok=1):
- 100-102 DIRECT "tak grn cub": 3/3
- 103-105 DIRECT "tak blu tri": 3/3
- 106-108 SYN "tak grn sph": 3/3
- 109-111 NEG "tak not grn": 3/3 (frozen baseline 0/3)
- 112-114 REL "tak biger tri": 3/3
- 115-117 SIZE "tak smal tri": 3/3
- 118-119 3WAY "tak big grn bal": 2/2

## R2 discovery trace (observed at the seen=40 check)

```
DIAG w epc reclen sup mtch div cs cb gate
 0 40 1 17 16 4 0 28 0
 1 12 1 12 12 2 40 28 1
 2 18 2 6 0 0 22 28 0
installed_now=1
```

- w=1 (the "not" unit): epcount=12, |record|=1... (reclen=1 is
  popcount of recmask; the unit predicts only its tak co-occurrence
  bit at check time), support=12, consistency 12/12, diversity=2,
  gate 40 > 28 strict. Installed. Matches the prereg prediction
  (created_at=40, support=12) exactly.
- w=0 (positional confound): support=17, matches=16, diversity=4,
  but gate 0 > 28 fails. Killed by the zero-parameter gate as
  predicted. K=2 did not admit the confound.
- installed_now=1 fired only at seen=40; the duplicate-trigger guard
  held at all later checks (single OPREC row in the final table).

Final operator table:

```
k=0 trig=1 scope=0 sig=0 sup=12 created=40 active=1
```

One OPREC. trigger_form=1 resolves via the committed lexicon dump
(LEXICON line in run output) to the "not" unit. signature=DELETION,
created_at=40 > 0, support=12 >= 4.

## F3 verbatim audit

```
$ grep -c "not" opscope_learner.zag
0
$ grep -ci "negat" opscope_learner.zag
0
$ grep -c "is_negator" opscope_learner.zag
0
```

Inspection note: the routing predicate (`find_op`, `learn_update`)
tests only `OPREC.trigger_form` (W+5616+k*24), a runtime-bound unit
id. No branch in `opscope_learner.zag` mentions any word identity.
The word table lives solely in the excluded world file.

## F4 detail

Ablated copy (operator table emptied, records intact), no further
learning: T1 0/3 vs full 3/3 (strictly worse, as required); full
20-item under ablation 17/20 with negdrop=3, i.e. the entire drop is
the 3 NEG items and every other group is unchanged. The operator is
causal for negation and only for negation.

## Per-R assessment

- R1: compositional interpret over spans works as designed. With the
  operator active, "tak not grn" predicts rest ({tak}) UNION empty
  scope records = {tak} = T.
- R2: DELETION discovery fired at seen=40 on the true trigger with
  all bars passing; the gate killed the positional confound.
- R3: scope-conditioned grounding routed correctly; scope O-records
  converged to empty (R = T minus rest_pred = {} on NEG episodes),
  which is the correct deletion behavior.
- R4: all five falsifiers pass against frozen predictions.

## What the learner created vs what is authored

Authored: spans, UNION combiner, OPREC structure, DELETION
signature, residual-attribution routing, binarization rule, all
constants (B0=20, E=10, N_ep=5, Fmax=1, N=4, C=0.75, K=2, OPMAX=8),
the (U,T) interface, oracle unit segmentation. The learner created:
the operator inventory (trigger w=1 bound at runtime, never a source
literal), every record vector, the support counts, the routing
bindings. Bounded L2 direction; no L3 claim. Retirement is specified
but had zero coverage on this battery (disclosed, per the design).

## Implementation notes

- K=2 was frozen in the prereg with written justification before any
  implementation. It is not a weakened bar: the prior build's K=3
  FAIL verdict stands untouched in its own owned path.
- Duplicate-trigger guard (preregistered): proposal_check skips a
  form already bound to an active OPREC. It fired at checks
  seen=50..100 (no duplicate row installed).
- State: 8400 bytes. Determinism: 3/3 md5-identical.

## Artifacts

- opscope_world.zag (frozen battery + (U,T) interface; F3-excluded)
- opscope_learner.zag (R1-R4; F3-audited)
- opscope_harness.zag (training/test/F1-F5; F3-excluded)
- opscope_bin (native binary)
- run1.txt, run2.txt, run3.txt (byte-identical raw outputs)
- PREREG_OPSCOPE_R1R4.md (frozen before implementation)

## Commits

- 51c54e262 prereg (K1; committed alone)
- (implementation + result: this commit)
