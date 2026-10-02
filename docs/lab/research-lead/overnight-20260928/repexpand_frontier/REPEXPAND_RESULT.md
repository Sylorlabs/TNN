# REPEXPAND-1 Result: BUILD-PASS (representational expansion frontier)

Builder verdict: **BUILD-PASS**. This is not a promotion to SURVIVES.
Promotion requires the full pipeline: independent reproduction, baseline
attack, OOD test, ablation, transfer, independent adversary, governance audit.

## Commits (branch tnn-native-lab, local only)

- Prereg frozen alone: `cb3523684` (before any implementation existed;
  verified strict ancestor of the result commit).
- Implementation + raw evidence + this report: committed together after the
  frozen run (see commit hash in the parent log).

## What was built

`repexpand.zag` (pure Zag, no Python at any stage): a world of specifier-run
episodes, the frozen base language L (bounded-template predictors), an
exhaustive impossibility check, and a learner with generic structural-growth
machinery (failure monitor, residual-relation search, node reification,
revision by supersession).

World: episode = observed (spec_sym, n, head[2]) + hidden content runs.
Task: predict (s1,l1,s2,l2) exactly, at the run-structure level (which exactly
determines the sequences; this is the level where the expansion occurs).

Frozen L: ALT of 1..3 branches; each branch a fixed triple (c0,c1,c2),
ci in 1..8, fixed symbols ('#','a','b'). All counts frozen constants. No
production with a runtime-bound parameter slot. Canonical enumeration: 512
singles + 92 diagonal ALTs = 604.

Growth machinery (researcher-supplied substrate, not the claimed invention):
best-L selection on seen episodes; primary = newest active created node else
bestL; consecutive-failure monitor (F=3, frozen); generic relation search over
the last 3 failures (EQ, then MUL(q), then ADD(d), fixed order; symbol slots
bound to head positions); reification of a discovered relation as a new
COUPLED node (type tag 7, outside L's {1,2,3,4}); revision by supersession
with retirement traces.

## Frozen kill bars: 8/8 PASS

- K-RX-1 impossibility: max over all 604 L-expressions on E_1..E_12 = 3 < 12.
  PASS. (Lemma: each branch correct on at most one E_n; at most 3 branches.)
- K-RX-2 creation: 2 nodes created, type tag 7 (outside {1,2,3,4}).
  TRACE-CREATE lines present with episode index, discovered relation, and
  evidence (evid_ns=2,3,5 for v1; evid_ns=3,6,4 for v2). PASS.
- K-RX-3 hidden success: HIDDEN 4/4 (n=9,11,15,17, disjoint from training)
  and EXTENDED 3/3 (n=13,20,30, beyond L's constant range 1..8). PASS.
- K-RX-4 ablation: growth-disabled learner scores 0/4 on HIDDEN (<=1). PASS.
  The ablation learner is the memorization control: an ALT of templates can
  only repeat seen n values.
- K-RX-5 reuse and transfer: TRANSFER 4/4 (new specifier byte '$', new
  alphabet "xy", unscored distractor runs); node-assisted exact predictions
  total = 16 (>= 10). PASS.
- K-RX-6 revision: v1 retired (TRACE-RETIRE, reason=contradicted, by=v2);
  v2 created with a different data-determined relation (EQ on run 1,
  MUL(2) on run 2); FOLLOWUP 2/2 on a^n b^(2n). PASS.
- K-RX-7 determinism: 3/3 byte-identical raw outputs (cmp-verified),
  md5 ed7c79a110742dba862b7db9f06aeaf2. PASS.
- K-RX-8 purity: pure Zag (implementation, builds, runs; shell only for
  compile/cmp/md5); zero em-dash bytes in all authored docs. PASS.

Program verdict line: `RX-VERDICT BUILD-PASS bars_passed=6/6`
(K-RX-7 and K-RX-8 checked by the harness, as preregistered).

## White-box creation trace (quoted from REPEXPAND_RAW.txt)

Inadequacy detection and first creation (TRAIN ep 2):

```
RX-TRACE NOTICE consecutive_failures=3 ep=2
RX-TRACE SEARCH ok=1 rel1=EQ(0) rel2=EQ(0) sym=bind
RX-TRACE CREATE node=3 type=COUPLED v=1 ep=2 evid_ns=2,3,5 rel1=EQ(0) rel2=EQ(0)
```

The three bestL failures (n=2,3,5) were noticed, the residual regularity
(count of run 1 == count of run 0; count of run 2 == count of run 0) was
found by the generic search, and a new COUPLED production was allocated with
runtime-bound length slots. v1 then predicted n=7,4,6, all hidden n, n=30,
and all transfer episodes exactly (14 consecutive exact predictions).

Contradiction and revision (CONTRA ep 29):

```
RX-TRACE NOTICE consecutive_failures=3 ep=29
RX-TRACE SEARCH ok=1 rel1=EQ(0) rel2=MUL(2) sym=bind
RX-TRACE RETIRE node=3 v=1 ep=29 reason=contradicted by=v2
RX-TRACE CREATE node=2 type=COUPLED v=2 ep=29 evid_ns=3,6,4 rel1=EQ(0) rel2=MUL(2)
```

The same code path produced a different node for different residuals
((EQ,EQ) vs (EQ,MUL(2))), showing the node content is data-determined, not
researcher-enumerated. v1 was retired, not patched.

## Why this is claimed as representational expansion (L3 Criterion 0)

1. The old language provably cannot do the task (Theorem + exhaustive check).
2. The new production (COUPLED, tag 7) has no counterpart in L: L's counts
   are frozen constants; the node binds lengths from the observed spec run
   at prediction time. It is not a composition of L forms.
3. The node solves the infinite family (n=13,20,30 exact, beyond every
   frozen constant), not just more cases: 12 bytes cover all n >= 1, where
   L would need one branch per n.
4. The specific relation is discovered, not supplied: identical machinery
   yields (EQ,EQ) on training residuals and (EQ,MUL(2)) on contradiction
   residuals.
5. Ablation destroys the advantage (0/4 hidden); the node transfers across
   changed surface form ('$' specifier, "xy" alphabet, distractors); the
   node is revised/retired on contradiction.

## Pre-registered defense vs the "disguised menu" objection

The EQ/MUL/ADD templates are generic binary relations over observed
features, not solution structures; the reified production (runtime
parameter binding across run positions) is absent from L; the same code
path yields different nodes for different residuals; the ablation shows
the advantage comes from the created node. The independent adversary is
invited to attack exactly this seam.

## Honest limitations

- Synthetic small world; L is the bounded-template family by design. The
  claim is representational expansion, not task difficulty.
- Transfer preserves the abstract shape (spec run + 2 content runs) while
  changing specifier byte, alphabet, and adding distractors.
- The relation search is restricted to source = the observed run and the
  relation family {EQ, MUL, ADD} (disclosed boundary of the growth
  machinery, prereg section 10).
- Baseline comparison beyond the in-program ablation (bestL = ALT of
  templates, the memorization control) is left to the promotion pipeline.
- The node inventory shows v1 retired and v2 active; no node proliferation
  occurred, but proliferation pressure was not stress-tested.

## Remaining for promotion (not done here)

Independent reproduction from the committed blob, simple-baseline
comparison, alternative-explanation attack, OOD test beyond the frozen
sets, independent adversary, governance audit. The raw evidence
(REPEXPAND_RAW.txt, md5 ed7c79a110742dba862b7db9f06aeaf2) and the frozen
source are committed for those stages.
