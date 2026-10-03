# T-ADV5 Design: Independent Post-Freeze Adversary for L3 Bridge

Status: DESIGN-COMPLETE. Design only. No implementation. No empirical claims.
Parent: L3 Bridge BRIDGE-TESTED (commit `ebdc4fd3e`).
C0-C requirement: at least one evaluation family designed by independent adversary after freeze.
Scope: `docs/lab/research-lead/overnight-20260928/bridge_adv/` only.

## 1. Adversary independence

This family was designed by an independent adversary (not the bridge builder)
after the bridge freeze at commit `ebdc4fd3e`. The bridge builder's T-ADV4
(family 12) was designed post-prereg but by the builder; T-ADV5 is the first
truly independent post-freeze family, satisfying the C0-C independence
requirement.

The adversary has read the bridge prereg (`PREREG_L3BRIDGE.md`), result
(`BRIDGE_RESULT.md`), and source structure, but has not modified the bridge
and does not know the sealed evaluation outcome.

## 2. Family specification (frozen)

**Family 13: T-ADV5 (Deceptive Step)**

- true_subj(13,i) = 13000 + i, for i = 0..39.
- true_obj(13,i):
  - if i < 10: return 1
  - if i < 20: return 0
  - return 1

In words: outputs are 1 for i in [0,10), 0 for i in [10,20), 1 for i in
[20,40). A step function with values (1, 0, 1): high, low, high.

**Optimal structure:**
```
IF(x < 13010, 1, IF(x < 13020, 0, 1))
```
- 2 LT nodes, 3 CONST leaves = 5 nodes total.
- 0 EQ nodes.
- Well within the 8-node cap and 4-EQ cap.

## 3. Material difference from existing families

### 3.1 Existing families

- **G (fam 6)**: STEP. obj=0 for subj<6003, else 5. Two contiguous clusters,
  monotonic (low then high). 1 threshold.
- **H (fam 8)**: EXCEPTIONS. Default 7, isolated exceptions at 8001->3 and
  8004->9. 2 EQ nodes.
- **K (fam 10)**: MULTI-STEP. obj=0 for i<2, 1 for i<4, else 2. Three
  contiguous clusters, monotonic increasing. 2 thresholds.
- **J (fam 9)**: HONESTFAIL. obj=1+(i%4). Four scattered values, periodic,
  unrepresentable within node cap.
- **T-ADV4 (fam 12)**: STEP WITH EMBEDDED EXCEPTION. 0 for i<5, 5 for i>=5,
  but i=2 maps to 9. 1 LT + 1 EQ, 7 nodes. The exception is a single isolated
  point within a step region.

### 3.2 T-ADV5 material differences

**Difference 1: Deceptive search landscape (tests search, not just representation).**

G, H, K, and T-ADV4 are all "greedy-friendly": the move with largest immediate
gain aligns with the optimal structure. In T-ADV5, the 10 zeros (i=10..19)
constitute 25% of the buffer and appear as "exceptions" against the majority
value 1 (30/40 points). 

- Greedy EQ isolation gives gain=+1 per move (isolating one zero).
- Greedy LT split gives gain=0 initially (neither x<13010 nor x<13020 alone
  improves over the majority-1 baseline).

The generic search must overcome this myopia to discover the 2-threshold
structure. This probes a dimension (search efficacy under deception) that no
existing family tests. G/H/K test whether the operators can express a form;
T-ADV5 tests whether the greedy algorithm can find an expressible form when
the landscape is deceptive.

**Difference 2: Inverted exception intuition.**

H has 2 isolated exceptions in a default region. T-ADV4 has 1 isolated
exception in a step branch. T-ADV5 has 10 "exceptions" that form a contiguous
block. The learner must recognize that these 10 points are not isolated
anomalies but a coherent region requiring an LT split, not EQ isolation.
This inverts the H intuition (where EQs are correct) and extends T-ADV4
(where 1 EQ suffices for 1 point).

**Difference 3: Non-monotonic multi-threshold.**

K is monotonic increasing (0,1,2). G is monotonic (0,5). T-ADV5 is
non-monotonic (1,0,1): high, low, high. While the search does not explicitly
represent monotonicity, the non-monotonic pattern means the same output value
(1) appears in two disconnected regions ([0,10) and [20,40)). The learner
cannot use a single LT to isolate all 1s; it must build the nested structure.

## 4. Sealed evaluation protocol

### 4.1 Freeze and independence

- Bridge is frozen at commit `ebdc4fd3e`. No modifications allowed.
- This design is frozen at commit (to be recorded). No modifications after
  evaluation begins.
- Evaluator is independent of both bridge builder and adversary designer.
- The bridge binary (`bridge_bin` from `ebdc4fd3e`) is used unmodified.

### 4.2 Evaluation procedure

1. **Fresh state**: Initialize learner state to zeros (no retained forms).
2. **Run family 13**: Execute the standard discovery protocol:
   - BMAX=40 discovery buffer via true_subj/true_obj.
   - Menu forms attempted first (0,1,2).
   - If menu exhausted, inventor hook fires: construct_search on the buffer.
   - If exact fit, verify under V schedule, then promote.
   - If no exact fit, HONESTFAIL (adopted=-1).
3. **Record**: adopted, promoted, cost, node count, EQ count, final tree
   structure (node ops and parameters), HONESTFAIL trace if applicable.
4. **Determinism**: 3 runs, byte-identical output required (per K4).

### 4.3 Cost accounting

Per bridge prereg section 3: cost = examples observed + candidate tree
simulations during construct_search. Ceiling is 108.

## 5. Success and failure bars

### 5.1 STRONG PASS (evidence for C0-C)

All of:
- adopted=3, promoted=1.
- cost <= 108.
- node count <= 8.
- EQ nodes <= 4.
- Exact fit on the 40-point buffer.
- Tree structure captures the 2-threshold form: the tree contains LT splits
  that partition [13000,13040) into regions corresponding to the (1,0,1)
  pattern. Specifically, the tree must NOT rely solely on EQs to handle the
  zero-block; at least one LT must separate the [13010,13020) region.

Interpretation: The generic search overcame the deceptive landscape and
discovered the optimal (or equivalent) structure. This is strong evidence
that the mechanism handles unforeseen forms.

### 5.2 ACCEPTABLE (honest limitation, not disqualifying)

- adopted=-1, promoted=0 (HONESTFAIL).
- cost <= 108 (or cost reflects honest search without violation).
- No constraint violations (node cap, EQ cap respected).
- Clean HONESTFAIL trace (search terminated without exact fit).

Interpretation: The mechanism recognized its search limitation and failed
honestly, like J. This does not support C0-C but does not refute the
mechanism's integrity. It identifies greedy myopia as a boundary.

### 5.3 FAIL (adversary succeeds, mechanism limitation exposed)

Any of:
- **F-DECEPT-COST**: cost > 108.
- **F-DECEPT-DEGENERATE**: promoted tree uses more than 4 EQ nodes.
- **F-DECEPT-NODECAP**: promoted tree exceeds 8 nodes.
- **F-DECEPT-MEMORIZE**: promoted tree achieves exact fit via EQ memorization
  without capturing the step structure. Concretely: the tree uses EQs to
  isolate individual zeros in [13010,13020) but does not contain an LT split
  that separates the zero-block as a region. This indicates the search
  memorized points rather than discovering the form.
- **F-DECEPT-WRONG**: promoted tree fits the buffer but is behaviorally
  incorrect on held-out points (overfitting). (Held-out: i=40..49 with same
  pattern extended.)

## 6. Falsifiers specific to this adversary

- **F-ADV5-SEAL**: If the bridge was modified after `ebdc4fd3e` before
  evaluation, the result is VOID. The seal is broken.
- **F-ADV5-LEAK**: If the adversary design was revealed to the bridge
  implementer before freeze, VOID. (Not applicable; bridge predates design.)
- **F-ADV5-IMPOSSIBLE**: If analysis shows the optimal 5-node tree is not
  reachable by ANY sequence of the 4 operators within budgets, the family
  is unfair and the result is VOID. (Adversary asserts reachability: 2 LT
  splits suffice.)

## 7. Governance

- Design only. No implementation, no evaluation, no empirical claims in this
  document.
- Zero Python used at any stage.
- Zero em dashes or en dashes in this document (byte-verified by author).
- Commits local on tnn-native-lab, owned path `bridge_adv/` only, pathspec
  commits.
- This design does not modify the bridge, the paper, or any other component.
- The evaluation (separate worker) must preregister before running.

## 8. Honest scope and limitations

- T-ADV5 tests one specific dimension: greedy search under deception. It does
  not test all possible unforeseen forms.
- A STRONG PASS on T-ADV5 is one data point for C0-C, not C0-C itself. C0-C
  requires multiple unforeseen forms.
- An ACCEPTABLE (honest failure) outcome is informative about search
  limitations but does not by itself refute the L3 bridge mechanism. The
  bridge's honest scope already discloses greedy search with B_node=0.
- The adversary does not claim T-ADV5 is the hardest possible test, only
  that it is materially different and fair.

## 9. Kill bars for this design task

- K1: Family specified (section 2) and materially different (section 3).
  PASS.
- K2: Protocol sealed (section 4). PASS.
- K3: Bars defined (section 5) with falsifiers (sections 5.3, 6). PASS.

Verdict: DESIGN-COMPLETE.
