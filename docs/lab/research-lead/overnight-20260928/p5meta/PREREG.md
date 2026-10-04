# PREREG: P5-META-LEARNING (charter 23) -- EXPERIENCE -> LEARN-TO-LEARN

Lane: `p5meta`. Claim block: **C5xx**. Prereg frozen BEFORE any implementation
file exists. All computation pure Zag; shell/git orchestration only.

## 0. THE QUESTION

Charter 23: *previous experience should improve later learning because TNN
ACQUIRED useful learning structure, not merely because it memorised facts.*

Charter 23 ablation requirement: *ablate the proposed learned meta-structure.
If the advantage REMAINS after ablation, the claimed meta-learning structure
is NOT causal -- the result is just "more data."*

So this prereg freezes (a) a learner that acquires a two-level meta-structure
on a family with an underlying regularity, (b) five new families that stress
the structure in five different ways, (c) four ablations that separate
"meta-structure" from "more data", and (d) numeric kill bars.

## 1. WHAT IS LEARNED (the candidate meta-structure)

### 1.1 The learner state is the frozen COGOPS learner-state arena

Learner state is one flat arena `L` of 24576 bytes using the frozen COGOPS
offsets from `docs/ops/ZAG_LANGUAGE_AND_WORKER_BRIEF.md` section 7 / the
`cogops_learnosc2/c8_learn.zag` header:

| region | offset | size | role in this lane |
|---|---|---|---|
| BIND | 12744 | 8 x 32 B | learned bindings: arity ladder, op alphabet, domain seen |
| PLAN | 13000 | 4 x 56 B | stored VERIFIED procedures (the reusable structure) |
| STATS | 13224 | 256 B | cumulative counters |
| DETC | 15900 | 64 B | detection / adaptation counters |
| STRATT | 16600 + (s-1)*12 | 7 x 12 B | per-strategy `[uses, wins, cost]` |
| CTXT | 17000 + slot*56 | 12 x 56 B | per-slot context records |

**ARCHITECTURE IS FROZEN.** The arena, the region sizes, the hypothesis
grammar, the enumeration order, the search budget, the round schedule and the
verification protocol are all fixed in source BEFORE any result is seen. No
region, field, operator, arity, or protocol is added or resized in response to
data. The ONLY things that change across families are *values written into*
these fixed regions.

### 1.2 Hypothesis grammar (FROZEN, researcher-authored -- see section 9)

A hypothesis `h` is `(arity a, slot tuple (i0<i1<i2<i3), op)`.
- `a` in 1..4, slots from 0..11, `op` in 0..3.
- Prediction on a presented example `x` (already projected to bits):
  `s = sum of the `a` projected bits; then
  `op0 -> s mod 2` (PARITY), `op1 -> (s>=2)` (QUORUM),
  `op2 -> (s==1)` (EXACTLY-ONE), `op3 -> (s==0)` (NOR).
- Hypothesis count: 3*(12 + 66 + 220 + 495) = 2379. Enumeration order is a
  deterministic function of CTXT slot relevance (see 1.3).

### 1.3 LEVEL-1 (L1): per-slot relevance, `CTXT[j].rel`

For every hypothesis that reaches criterion, the learner's `h` is recorded and
the tuple members have `CTXT[j].rel += 1`. Slot relevance order `ORD[0..11]`
= slots sorted by `rel` descending, ties by index ascending.

L1 is **domain-specific**: it is a statement about *which of these twelve
opaque slot indices mattered in the past*.

### 1.4 LEVEL-2 (L2): search policy, `BIND` + `STRATT`

Two quantities, both derived from training records only:

- **L2-arity** `AR[0..3]`: permutation of the arity ladder 1..4 obtained by
  sorting arities by `STRATT[arity].wins` descending, ties by arity ascending.
  This is the order in which arity tiers are *enabled* and *searched*.
- **L2-verif** `V`: `2 + (mean number of failed verification attempts that
  preceded the first successful verification across training episodes)`,
  clamped to 2..16. How many held-out examples must agree before a
  zero-in-sample hypothesis is trusted.

L2 is **domain-free**: a permutation of a domain-independent size ladder and
a count of examples. It carries no statement about slot identity.

### 1.5 Why L1/L2 must dissociate

- On a **slot-relabelled** domain, L1 is provably inert (section 4.5) while L2
  still applies. So a DOMAIN-2 speedup that survives L1 ablation but dies
  under L2 ablation is caused by L2.
- On a **slot-adversarial** family, L1 is actively harmful while L2 is
  harmless. So a MISLEADING slowdown that dies under L1 ablation is caused
  by L1.
This dissociation is the pre-registered scientific core.

## 2. TRAINING PHASE (frozen)

Two learner states are trained by the SAME machinery on the SAME number of
episodes (8 each). Only the families differ.

- **PRIOR state**: 8 `dom0` families, arity 3 in episodes {0,1,3,4,5,7} and
  arity 2 in {2,6}. Op = `episode mod 4`. Active slots drawn from the fixed
  pool **TrainA = {1,3,4,6,8,9,11}** as `pool[(3e+i) mod 7]`, distinct.
- **DATA state**: 8 `dom0` **noise** families (label = PRNG bit, independent
  of the inputs), same machinery, same episode count, same code path. This is
  the "more data" control: identical volume of experience, zero regularity.

`TrainA` has 7 slots; its complement in 0..11 is **COLD = {0,2,5,7,10}**.

## 3. TEST PHASE -- FIVE FROZEN CONDITIONS (6 families each)

All families get a deterministic stream of presented examples; **all arms see
byte-identical example streams for a given family** (common random numbers),
so arm differences are attributable to search order only.

| condition | fids | encoding | active set | label rule |
|---|---|---|---|---|
| RELATED | 16..21 | dom0 | 3 distinct slots from 0..11 | op = (fid-16) mod 4, arity 3 |
| MISLEADING | 22..27 | dom0 | 3 distinct slots from **COLD** | op = (fid-22) mod 4, arity 3 |
| PARTIAL | 28..33 | dom0 | 2 from TrainA + 1 from COLD | op = (fid-28) mod 4, arity 3 |
| IRRELEVANT | 34..39 | dom0 | none | label = PRNG bit, independent of inputs |
| DOMAIN2 | 40..45 | **dom2** | 3 distinct slots from **COLD** | op = (fid-40) mod 4, arity 3 |

### 3.1 Encodings (the "structurally different domain")

- **dom0**: 12 slots, binary values 0/1, projected bit = the value. Label
  emitted directly.
- **dom2**: 12 slots, ternary values 0,1,2, projected bit = `1 iff value==2`.
  All 12 slots are live (no inert header slots). **The label is emitted
  INVERTED** (`y_present = 1 - y_rule`). Different value alphabet, different
  projection, different label polarity, different arity ladder usage
  (`u_feat_k`-style value transform, as in `hook_phase1/hq_module.zag`).

dom2 is "structurally different" in the operational sense that matters for the
claim: a different feature alphabet, a different projection of features onto
the rule-relevant bit, and an inverted output channel. Nothing in the learner
is told which part is which.

### 3.2 The critical DOMAIN-2 construction guarantee

Every DOMAIN-2 family's active set is a 3-subset of **COLD**, and COLD is
disjoint from **TrainA**. Therefore **no DOMAIN-2 active slot ever occurred in
any training family**, so `CTXT[j].rel == 0` for every DOMAIN-2 active slot.
L1 is not merely unhelpful on DOMAIN-2, it is **provably uninformative**.
This is stated here so the DOMAIN-2 ablation can be read as a causal test
rather than a suggestive one. The cost of this guarantee is disclosed: DOM2
active sets are drawn from only 5 slots, so DOM2 families are *less* slot-
overlapped with training than RELATED families, not more.

### 3.3 Epoch/arity disclosure

Training uses arity 3 in 6/8 episodes and arity 2 in 2/8, so the learned arity
permutation is non-degenerate. All five test conditions use arity 3, matched
to the training-dominant arity, so that the L2-arity channel is applicable.
**This is a disclosed design choice that flatters L2-arity.** It is made so
that the DOMAIN-2 test isolates the L1/L2 dissociation instead of being
confounded by an arity mismatch. The MISLEADING and IRRELEVANT conditions
cannot be helped by L2-arity at all (their rules are, respectively,
slot-invisible and absent), which is why they remain valid controls.

## 4. THE LEARNING EPISODE PROTOCOL (FROZEN, identical in every arm)

Round `r = 1 .. RMAX(64)`:

1. `E_r = 4*r` in-sample examples are consumed. The in-sample buffer is always
   stream positions `0 .. E_r-1`, so it is arm-independent.
2. **Reuse phase (round 1 only).** Every stored PLAN entry (<=4) is evaluated
   against the in-sample buffer. Each proposal counts one *reuse attempt*
   (`RA`). If it has zero in-sample mismatches it goes to steps 3-4; a
   failure there counts one *rejected reuse* (`RR`).
3. **Search phase.** Up to `SB = 24` **new** hypotheses are evaluated. Enabled
   arity tiers are visited in `AR` order (L2-arity; cold order = 1,2,3,4).
   Tier with rank `q` becomes enabled at round `q+1`. Within a tier,
   hypotheses are enumerated in `ORD`-lexicographic tuple order (L1; cold
   order = slot index ascending). A per-tier cursor persists across rounds,
   so the search is a single forward walk of the order and the per-round
   budget is what makes order *matter*.
4. **Verification.** The first hypothesis with zero in-sample mismatches
   proposes `V` fresh held-out examples (drawn from a stream keyed by
   (family, round, index), hence arm-independent). All must be predicted
   correctly, else `VA += 1`.
5. **Audit.** A verification survivor must additionally predict 16 fresh audit
   examples (stream keyed by (family, round+1000, index)) all correctly. Audit
   failure counts as `VA += 1` and the search continues. **Criterion reached
   iff audit passes.** The audit is in every arm; it exists so that a
   zero-in-sample coincidence on IRRELEVANT cannot be mistaken for criterion.
6. On criterion: write `h` into the PLAN table (replacing the entry with the
   fewest `uses`), increment `CTXT[j].rel` for its members,
   `STRATT[arity].uses/wins`, and `DETC.newplans`.
7. On `RMAX` without criterion: commit the constant-majority predictor.
   `DETC.novel_arity` is incremented the first time a tier is enabled that was
   never enabled during training (this is the "newly created structure" event).

### 4.1 Arm definitions

| arm | L1 | L2 | what it isolates |
|---|---|---|---|
| PRIOR | trained | trained | the full acquired meta-structure |
| L1 | **ablated** | trained | removes slot relevance only |
| L2 | trained | **ablated** | removes search policy only |
| V | **ablated** | verif-size only | the "how careful" channel only |
| A | **ablated** | arity-perm only | the "how to search" channel only |
| COLD | **ablated** | **ablated** | control: architecture, no experience |
| DATA | as trained on NOISE families | | "more data, no structure" control |

`COLD` is the control for every speedup claim. `DATA` is the control for the
charter-23 "it is just more data" objection.

### 4.2 Metrics (charter 23)

Per (condition, arm), summed or averaged over the 6 families:
- `EX` examples-to-criterion (256 on IRRELEVANT = 4*64, the RMAX budget)
- `SA` search attempts (hypotheses evaluated, including verify/audit predictions)
- `VA` verification attempts (failed verification or audit)
- `C` = `SA + 4*VA` (scalar cost proxy, all computed in Zag)
- `RU` structural reuse (stored plans that reached criterion)
- `RR` rejected reuse attempts
- `NS` newly created structure (PLAN writes + novel arity tiers enabled)
- `NT` negative transfer = `C(PRIOR) - C(COLD)` and `EX(PRIOR) - EX(COLD)`
- `FC` final correctness (1 iff criterion-reached and audit passed; for
  non-reaching episodes, 1 iff the committed constant predictor scores <=70%
  on a fresh 32-example audit, i.e. "correctly detected no structure")

## 5. PREREGISTERED PREDICTIONS (from the frozen cost model of section 4)

The model: a hypothesis at enumeration position `p` is reached at round
`ceil(p/24)`; `EX = 4*ceil(p/24)`. Positions are computed from the L1/L2 order.
For a 3-subset at lex-rank `r` inside a tier of 220/660 triples:

| condition | EX(PRIOR) | EX(COLD) | ratio |
|---|---|---|---|
| RELATED | ~8 | ~96 | ~12 |
| IRRELEVANT | 256 | 256 | 1.00 exactly |
| MISLEADING | ~108 | ~56 | ~1.9 |
| PARTIAL | ~16 | ~56 | ~3.5 |
| DOMAIN2 | ~56 | ~96 | ~1.7 |

Arm-level predictions: `EX(L1)` on RELATED ~44; `EX(A)` on RELATED ~56;
`EX(L2)` on DOMAIN2 ~96 (= COLD); `EX(L1)` on DOMAIN2 ~56 (= PRIOR, L1 inert);
`EX(L1)` on MISLEADING ~56 (= COLD).

## 6. FROZEN KILL BARS

- **K1 COMMIT-ORDER**: prereg commit is an ancestor of every implementation
  commit and contains no `.zag` file.
- **K2 TOOLCHAIN**: `tnn_pure_zag_report` = PURE-ZAG-CLEAN; zero forbidden
  executables; output via `_zag_print`/`_zag_println` only, never
  `_zag_raw_syscall` (brief 4.0); output asserted non-empty.
- **K3 DETERMINISM**: 3/3 byte-identical stdout.
- **K4 FLOOR**: every (condition, arm) episode terminates; `FC = 1` for every
  criterion-reaching episode; no VOID.
- **K5 RELATED SPEEDUP (primary)**: `EX(COLD) / EX(PRIOR) >= 2.0`.
- **K6 IRRELEVANT NEUTRAL**: `EX(PRIOR) == EX(COLD)` on 6/6 noise families,
  **and** `(SA(PRIOR) - SA(COLD)) / SA(COLD) <= 0.25`.
  A speedup on IRRELEVANT is a FAILURE, not a bonus.
- **K7 MISLEADING REJECT/REVISE**: `EX(PRIOR) > EX(COLD)` (harm is real),
  `EX(PRIOR) <= 2.5 * EX(COLD)` (harm is bounded), `FC = 1` on 6/6 (it
  recovers), and `RR >= 6` (it actually attempted reuse and rejected it).
- **K8 PARTIAL SELECTIVE**: `EX(PRIOR, PARTIAL) > EX(PRIOR, RELATED)` **and**
  `EX(PRIOR, PARTIAL) < EX(COLD, PARTIAL)`. Reuse without wholesale import.
- **K9 DOMAIN2 ABSTRACT TRANSFER**: `EX(COLD) / EX(PRIOR) >= 1.5`.
- **K10 ABLATION-L1-DISCRIMINATION (DOMAIN2)**: `EX(PRIOR,DOMAIN2) /
  EX(L1,DOMAIN2) <= 1.25` (slot relevance is not the cause of the
  domain-2 speedup) **and** `EX(PRIOR,DOMAIN2) / EX(L2,DOMAIN2) >= 1.4`
  (removing the search policy kills it).
- **K11 ABLATION-L1-NECESSARY (RELATED)**: `EX(L1,RELATED) >= 1.5 *
  EX(PRIOR,RELATED)`. The related speedup is NOT reproducible without the
  slot relevance that was acquired from experience.
- **K12 ABLATION-L1-HARMFUL (MISLEADING)**: `EX(L1,MISLEADING) <=
  EX(PRIOR,MISLEADING)` and `EX(A,MISLEADING) >= EX(COLD,MISLEADING) * 0.9`
  (the search-policy channel is harmless where slot relevance is harmful).
- **K13 NOT-MORE-DATA**: `EX(DATA,c) >= 0.95 * EX(COLD,c)` for **all five**
  conditions c. If the DATA arm is fast anywhere, the advantage was volume,
  not structure, and the headline verdict is FAIL.
- **K14 DECOMPOSITION (secondary, preregistered)**: `EX(V,c) <= EX(COLD,c)`
  and `EX(A,c) <= EX(COLD,c)` for c in {RELATED, DOMAIN2} -- both L2 channels
  must contribute something, so the L2 result is not a single scalar artefact.

## 7. VERDICT MAPPING (frozen)

- K1,K2,K3,K4 must all PASS or the run is INFRA/VOID.
- **META-LEARNING TRANSFER DEMONSTRATED** iff K5,K6,K7,K8,K9,K10,K11,K12,K13,K14
  all PASS.
- **PARTIAL** iff K5 and K9 pass, K6 passes, but any of K7,K8,K10,K11,K12,K13
  fails.
- **NO META-LEARNING (this design)** if K5 fails, or if K13 fails (the
  advantage is volume), or if K10 fails (the domain-2 advantage is not caused
  by the claimed meta-structure).
- Any outcome is reported as measured. No bar will be moved or reinterpreted
  after results are seen.

## 8. ABLATION IS THE EXPERIMENT

K10/K11/K12 are the load-bearing bars. K11 says the RELATED speedup is
*contingent* on the acquired slot relevance. K10 says the DOMAIN-2 speedup is
*contingent on the acquired search policy* and *not* on slot relevance. K13
says the speedup is not obtainable from the same volume of experience without
the regularity. If K11 or K10 fail, the honest conclusion is that the
meta-structure is NOT causal, regardless of K5.

## 9. HONEST ADMISSIONS, WRITTEN BEFORE ANY RESULT

These are stated now, not discovered later.

1. **The hypothesis grammar is researcher-authored** (section 1.2). The
   learner selects among 2379 researcher-written operators. Per
   `ZAG_LANGUAGE_AND_WORKER_BRIEF.md` section 9 this is explicitly **not L3**.
   No L2/L3 claim is made. The claim tested is about *transfer of acquired
   structure*, not about invention of the space.
2. **The meta-structure's FORM is researcher-supplied.** `ORD` is "sort by
   count", `AR` is "sort by win count", `V` is "average prior failures plus
   two". The learned quantities are the *values written into those forms*.
   This is exactly the boundary admitted by C456 (LM1) -- empirical-Bayes
   prior-mean learning, estimator form fixed -- and by C408's MP-3 ledger
   entry. **If this lane's result has the same shape, it must be said so.** It
   does have the same shape. What differs is the load-bearing test: K10/K11
   ask whether the learned values are *causal* for transfer across domains
   and whether they are falsifiable to ablation, which LM1/LM2 did not test.
3. **The BIND/PLAN/STRATT/CTXT geometry is the frozen COGOPS learner-state
   layout**, reused at its frozen sizes. Semantics of the words inside those
   regions are this lane's; the sizes and offsets are the frozen core's. No
   region is added or resized.
4. **Arity is matched to the training-dominant arity in all five test
   conditions** (section 3.3). This flatters L2-arity and is disclosed.
5. **DOMAIN-2 active slots are disjoint from TrainA by construction**
   (section 3.2). This is deliberate: it makes L1 provably inert so the
   K10 dissociation is a causal test rather than a suggestive one. It also
   means DOMAIN2 families share no slot identity with training at all, which
   is a stronger separation than "different domain" strictly requires.
6. **Six families per condition, one frozen seed set, one frozen
   distribution.** No generality over other seeds or distributions is claimed.
7. **`V` (verification batch size) is a single learned scalar.** If the L2
   result rests on `V` alone rather than on `AR`, K14's `A` arm detects it.
8. **IRRELEVANT is defined as label-noise, not as "a different but learnable
   regularity".** A different-but-learnable regularity would be a RELATED
   family with a new op, and the op ladder is not learned, so it is excluded
   by design. Stated here because it narrows what K6 tests.
9. **The COGOPS frozen prefix is used for its learner-state memory model and
   byte-offset conventions, not as the hypothesis search engine.** This lane
   does not exercise `ret_spec/vfy_spec/cnt_spec/execute_plan_iter`; it does
   not claim the COGOPS composition machinery is meta-learned.

## 10. ARTIFACTS TO COMMIT

`PREREG.md` (this file, alone, first), `NAMECHECK.md`, then
`p5.zag` + `p5_bin` + `run1.txt`/`run2.txt`/`run3.txt` + `REPORT.md`.
Commits use explicit pathspecs, never `git commit -a`, never pushed.
