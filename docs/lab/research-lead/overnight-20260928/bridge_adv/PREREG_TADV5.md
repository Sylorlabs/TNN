# PREREG T-ADV5: Independent Post-Freeze Adversary Evaluation for L3 Bridge

Status: PREREG-FROZEN. No evaluation has been run at this commit.
Parent design: `bridge_adv/T_ADV5_DESIGN.md` (commit `c36e61d3f`).
Parent bridge: BRIDGE-TESTED (commit `ebdc4fd3e`).
Scope: `docs/lab/research-lead/overnight-20260928/bridge_adv/` only.

## 1. What is being evaluated

The L3 bridge mechanism (generic construction replacing recipes), frozen at
commit `ebdc4fd3e`, is evaluated on family 13 (T-ADV5), an independent
post-freeze adversary family designed after the bridge freeze.

Family 13 (T-ADV5, Deceptive Step), frozen in the design:
- true_subj(13,i) = 13000 + i, for i = 0..39.
- true_obj(13,i): 1 for i < 10, 0 for i < 20, 1 for i >= 20.
- Optimal structure: IF(x < 13010, 1, IF(x < 13020, 0, 1)). 5 nodes, 0 EQs.

This evaluation supplies one data point for C0-C (independent post-freeze
adversary). It does not close C0-C and starts no SURVIVES claim.

## 2. Frozen evaluation protocol

### 2.1 Bridge integrity

- The bridge mechanism code (four generic operators, construct_search,
  candidate generation, novelty, HONESTFAIL, refit) is copied verbatim from
  commit `ebdc4fd3e`. No modifications to the mechanism.
- Family 13 definitions are added to the family dispatch (fam_base,
  true_obj). This is test-harness code, not mechanism code.
- The C0-A audit M1-M4 properties are preserved: no signature enum, no
  recipe branches, all setnode calls inside the four operators, teval
  unchanged.
- F-ADV5-SEAL: if the mechanism code differs from `ebdc4fd3e` in any way
  other than the added family 13 dispatch entries, the result is VOID.

### 2.2 Evaluation procedure

1. Fresh state: learner state initialized to zeros (no retained forms).
2. Run family 13 via the standard discovery protocol (run_family):
   - BMAX=40 discovery buffer via true_subj/true_obj.
   - Menu forms 0,1,2 attempted first.
   - If menu exhausted at n=40, inventor hook fires: construct_search.
   - If exact fit, verify under V schedule, then promote.
   - If no exact fit, HONESTFAIL (adopted=-1).
3. Record: adopted, promoted, cost, node count, EQ node count, final tree
   structure, HONESTFAIL trace if applicable.
4. Determinism: 3 runs, byte-identical output required.

### 2.3 Cost accounting

Per bridge prereg section 3: cost = examples observed + candidate tree
simulations during construct_search. Ceiling is 108.

### 2.4 Held-out verification (for F-DECEPT-WRONG)

If a tree is promoted, it is additionally evaluated on held-out points
i=40..49 with the pattern extended (true_subj=13040+i, true_obj follows the
same 1,0,1 pattern: 1 for i<10 i.e. subj<13050, 0 for subj in
[13050,13060), 1 for subj>=13060). A promoted tree that fits the 40-point
buffer but is behaviorally wrong on held-out fires F-DECEPT-WRONG.

## 3. Frozen success and failure bars

### 3.1 STRONG PASS (evidence for C0-C)

All of:
- adopted=3, promoted=1.
- cost <= 108.
- node count <= 8.
- EQ nodes <= 4.
- Exact fit on the 40-point buffer.
- Tree captures the 2-threshold form: at least one LT node separates the
  [13010,13020) zero-block as a region. The tree must NOT rely solely on
  EQs to handle the zero-block.

### 3.2 ACCEPTABLE (honest limitation)

- adopted=-1, promoted=0 (HONESTFAIL).
- cost <= 108.
- No constraint violations.
- Clean HONESTFAIL trace.

### 3.3 FAIL (adversary succeeds)

Any of:
- F-DECEPT-COST: cost > 108.
- F-DECEPT-DEGENERATE: promoted tree uses more than 4 EQ nodes.
- F-DECEPT-NODECAP: promoted tree exceeds 8 nodes.
- F-DECEPT-MEMORIZE: promoted tree achieves exact fit via EQ memorization
  without an LT split separating the zero-block as a region.
- F-DECEPT-WRONG: promoted tree fits buffer but is wrong on held-out.

## 4. Kill bars for this evaluation

- K1: this prereg frozen BEFORE any evaluation commit. Satisfied by this
  file's commit.
- K2: evaluation implemented; bars of section 3 applied to the measured
  outcome.
- K3: pure Zag (no Python anywhere), no em dashes, deterministic
  (byte-identical output across 3 runs).

Evaluator reports STRONG-PASS, ACCEPTABLE, or FAIL with the specific bar
or falsifier that determined the outcome. No SURVIVES claim is made here.
