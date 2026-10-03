# REPORT.md -- IVWC-ORACLE-FREE: verification with zero consequence observations

## Verdict: BUILD-PASS (K1..K8 all PASS)

The learner verifies its own work with NO consequence observations
at all -- no train phase, no true-world execution before verdicts.
Arm A (internal-model consequence prediction: each committed plan
stepped through the learner's OWN beliefs, PASS iff predicted eff
>= the learner-computed internal bar T_pred) discriminates sealed
outcomes (K3: mean PASS eff 23.6 > mean FAIL eff 11.6; K4: 10/12 >
7/12) and beats expand3's consequence-trained bucket table at
wp=15 (10/12 vs 9/12). The belief-content ablation collapses
accuracy (K6: 7/12 < 10/12). The verifier's edge degrades under
law change (K7: +3 -> -3). And the predicted limit holds exactly:
the verifier's false-PASS cases carry strictly more belief error
than its true-PASS cases (K8: mean err 9.5 > 4.6). Deterministic
3/3. No oracle token anywhere; the true-world stepper occurs
exactly once in the source, in the harness scoring block.

## What was built

`src/ivwc_oraclefree.zag` (pure Zag, single file, ~830 lines,
pinned znc), `bin/ivwc_oraclefree` (frozen binary). World
generator, belief generator, NAV+GATHER composer, step physics,
and all seeds are copied verbatim from IVWC-EXPAND3; the sealed
setup is identical, so all 36 sealed (bucket, eff) pairs are
bit-identical to expand3's run1 (verified per shift in shell).
New learner-side machinery (beliefs + plans only): `belief_execute`
(internal-model consequence prediction on belief arrays),
`learner_compose_rev` / `learner_compose_nn` (independent
re-derivation composers), `gather_cells` (gather-set extraction),
`belief_scramble` (Fisher-Yates belief ablation). There is NO
train phase: the program is sealed setup -> VERDICT COMMIT ->
harness SCORING.

Build: `src/tools/toolchain/znc_linux_x86_64_abed8aa1
src/ivwc_oraclefree.zag -o bin/ivwc_oraclefree`. Analyzer: one
informational zagd-unavailable notice only, no warnings.

## Kill-bar results

- K1 (commit before signal): PASS. K1S-STRUCT-PASS at sh=0/1/2
  (world-call counter unchanged across each VERDICT COMMIT).
  A1: commit-block call sites (571, 573, 579, 580, 606, 607) all
  precede the scoring block's world_execute (664). A2: zero
  world_buf/world_off in the LEARNER section.
- K2 (oracle-free diet): PASS. A3: zero expected|answer|key|target.
  A4: zero correct|reference_plan|gold. A6: `world_execute(`
  occurs exactly twice in the source (definition at 196, single
  call site at 664 in the SCORING block); WC-FINAL=36 (12x3).
  A7: zero `world_` tokens in the LEARNER section. The verifier's
  entire information diet is beliefs + plans.
- K3 (Arm A discriminates, wp=15): PASS. np=7 sp=165 nf=5 sf=58;
  165*5=825 > 58*7=406 (mean PASS eff 23.6 > mean FAIL 11.6).
- K4 (Arm A beats trivial, wp=15): PASS. acc=10/12 > maj=7/12,
  class = (eff >= T_pred) with T_pred=28 learner-computed (mean
  predicted eff over the sealed batch; no researcher constant).
- K5 (determinism): PASS. 3/3 byte-identical, sha256
  d0b6c4f6a9bbf805ac0b2b1930d7c1d52d198ecf741c9cd3e7b35358ed5a12d3.
- K6 (belief-content ablation, wp=15): PASS. acc_ab=7/12 < acc=10/12
  (strict). Scrambling beliefs (marginals preserved, mapping
  broken) collapses the verdict accuracy: belief CONTENT drives it.
- K7 (edge degrades under law change): PASS. (8-11) < (10-7),
  i.e. -3 < +3 (strict). The internal model's edge over the
  trivial rule erodes from +3 at wp=15 to -3 at wp=45.
- K8 (failures concentrate on belief error, wp=15): PASS.
  |FP|=2, |TP|=5; 19*5=95 > 23*2=46 (mean FP err 9.5 > mean TP
  err 4.6, strict). The internal model fails exactly where its
  beliefs are most wrong -- the principled limit of oracle-free
  verification: it cannot see its own belief errors.

## Mechanism detail (white box)

Two analytical results, both verified empirically on the 36
sealed cases:

1. **Prediction reduces to plan density.** Because the composer
   only appends legs through believed-clear intervals, the
   belief-simulated execution never bumps and every gather hits:
   predicted eff = 100*g/L = the composer's own raw_conf, for all
   36 cases (0 mismatches). "Consequence prediction in the
   internal model" is therefore exactly "the plan is dense in my
   model" -- the mechanism is legible, with no hidden state.
2. **Re-derivation is near-vacuous (Arm B finding).** For this
   composer family the gather set is order-invariant: any
   visit-in-some-order / take-if-believed-reachable composer
   yields exactly {c : believed item at c, believed [start,c]
   clear}. Reverse-scan and nearest-first agree with forward scan
   on 35/36 cases. The single disagreement (sh=0, s=11) is the
   energy cap: the forward plan hit EBUD=36 (L=36) while the
   re-derivations came in at 35 -- truncation, not derivation
   instability, breaks the invariance. So of the task's suggested
   oracle-free methods, internal-model prediction works and
   re-derivation self-consistency is vacuous here (honest
   negative: re-derivation can only catch derivation
   instability, and this deterministic composer has none).

Oracle-free vs consequence-trained (expand3's bucket table,
same 36 sealed pairs): wp=15: 10/12 vs 9/12 (oracle-free wins --
the density signal is finer than the bucket signal; e.g. s=5,
bkt=3, correctly PASSED at eff=33 where the table said FAIL, and
s=10, bkt=1, correctly FAILED at eff=25 < T_pred=28 where the
table said PASS). wp=30: 8/12 vs 8/12 (tie). wp=45: 8/12 vs
10/12 (oracle-free loses -- under strong law change the
internal model's fidelity collapses faster than the
consequence-trained table's). Verdict agreement (Arm A vs
bucket==1 rule): 9/7/10 across the dial.

The crispest illustration of the K8 limit: s=3 at wp=15 is a
2-action plan (preff=50) that collected nothing -- a phantom item
(err=8). The internal model structurally cannot represent
phantom risk; no amount of internal simulation detects it.

## Honest caveats

1. One wall-density law-change axis; item law, belief noise, and
   energy budget fixed. Other axes may break the mechanisms at
   different points.
2. T_pred is computed over the sealed batch (transductive), but
   from predictions only -- no world data enters the bar.
3. At wp=45 the ablation accuracy is degenerate (12/12): under
   extreme law change nearly every plan fails, so the collapsed
   always-FAIL verdicts score well by matching. Reported, not
   barred; the ablation bar is wp=15 only.
4. The belief-error measure for K8 is whole-map (40 cells,
   includes harmless errors); the FP/TP separation held anyway
   (9.5 vs 4.6).
5. Mechanism test, not a composition-novelty or L3 claim (per
   PREREG section 3). The composer is fixed; the claims concern
   the oracle-free verdict loop, what drives it, and where it
   breaks.

## What "verification" means without ground truth

This wave's operational answer to priority #4: verification =
the plan succeeds in the learner's own model of the world, and
its worth = the model's fidelity. That quantity is measurable
without any oracle: it discriminated sealed outcomes 10/12 vs a
7/12 trivial baseline with zero consequence observations, its
accuracy is driven by belief content (ablation 7/12), and its
failures concentrate exactly on belief error (K8) -- which is
also its boundary: internal verification catches plan-quality
defects visible in the model, never belief defects. The
dissociation with expand3/veto: consequence training buys
robustness under law change (wp=45: 10/12 vs 8/12); internal
prediction buys finer in-distribution discrimination (wp=15:
10/12 vs 9/12) at zero observation cost.

## Reproduction

```
cd docs/lab/research-lead/overnight-20260928/ivwc_oracle_free
~/workspace/tnn-rsi-gpi3/src/tools/toolchain/znc_linux_x86_64_abed8aa1 src/ivwc_oraclefree.zag -o bin/ivwc_oraclefree
./bin/ivwc_oraclefree | sha256sum   # expect d0b6c4f6a9bbf805ac0b2b1930d7c1d52d198ecf741c9cd3e7b35358ed5a12d3
```

Frozen audits (PREREG section 4): A1 ordering 571/573/579/580/
606/607 < 664; A2 count 0; A3 count 0; A4 count 0; A5 sha256
equality across runs/ivwc_oraclefree-run{1,2,3}.txt; A6
`world_execute(` count 2, call site 664, WC-FINAL=36; A7 count 0.
Sealed (bucket, eff) bit-identity vs ivwc_expand3 run1 verified
per shift (36/36).

Probe note: a pre-prereg /tmp probe (uncommitted) confirmed bar
non-degeneracy only; bar directions were theory-fixed before it.
The committed source differs from the probe in diagnostics only
(V-line L/Lr/Ln fields, in-program PROV verdicts, comment
hygiene); the mechanism, seeds, and all committed-run numbers
are unaffected (the post-comment-fix rebuild reproduced the
identical sha256, confirming the fix was comment-only).

## Branch note

Work committed on `tnn-native-lab` (the shared checkout this
worker was spawned on). Prereg commit 8a563fa52 strictly precedes
the implementation commit. All commits use explicit pathspecs
confined to `ivwc_oracle_free/`. Local only, never pushed. Git
writes via /usr/bin/git directly.
