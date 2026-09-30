# PREREG T-ADV5 RE-EVALUATION: Sealed Re-run on the Fixed Bridge

Status: PREREG-FROZEN. No evaluation has been run at this commit.
Parent design: `bridge_fix/BRIDGE_FIX_DESIGN.md` (commit `791388384`).
Parent fix build: `bridge_fix_impl/BRIDGE_FIX_IMPL_RESULT.md` (commit `d920af162`).
Original adversary design: `bridge_adv/T_ADV5_DESIGN.md` (commit `c36e61d3f`).
Original prereg: `bridge_adv/PREREG_TADV5.md` (commit `3c4350b99`).
Original evaluation: `bridge_adv/T_ADV5_RESULT.md` (commit `d06d2d8e1`), verdict FAIL.
Scope: `docs/lab/research-lead/overnight-20260928/tadv5_reeval/` only.

## 1. What is being evaluated

The fixed L3 bridge (episode-persistent discovery buffer: D1 store VERIFY
examples, D2 no n reset on strike, D3 40-cap, R7 immediate HONESTFAIL on
struck invented form), committed as FIX-BUILT-PASS at `d920af162`, is
evaluated on family 13 (T-ADV5), the independent post-freeze deceptive-step
family that defeated the unfixed bridge.

Family 13 (T-ADV5, Deceptive Step), frozen in the original design:
- true_subj(13,i) = 13000 + i, for i = 0..39.
- true_obj(13,i): 1 for i < 10, 0 for i < 20, 1 for i >= 20.
- Optimal structure: IF(x < 13010, 1, IF(x < 13020, 0, 1)). 5 nodes, 0 EQs.

This is the sealed re-evaluation the fix design (section 8) requires. It
supplies one data point for C0-C (independent post-freeze adversary) on
the FIXED protocol. It does not close C0-C and starts no SURVIVES claim.

## 2. Frozen evaluation protocol

### 2.1 Bridge integrity (seal)

- The fixed mechanism code (four generic operators, construct_search,
  candidate generation, gain rule, behavioral novelty, HONESTFAIL, refit,
  teval, D1-D3/R7 evidence management) is copied verbatim from commit
  `d920af162`. No modifications to the mechanism.
- Family 13 definitions are added to the family dispatch (fam_base,
  true_obj) exactly as in the original evaluation: `if(f==13){return 13000;}`
  and the (1,0,1) true_obj case. This is test-harness code, not mechanism
  code.
- `main()` is replaced with a T-ADV5-specific harness running family 13
  fresh (see section 2.2), mirroring the original `tadv5_eval.zag` harness.
- The C0-A audit M1-M4 properties are preserved: no signature enum, no
  recipe branches, all setnode calls inside the four operators, teval
  unchanged. M1-M4 were verified passing on `d920af162`.
- F-RADV5-SEAL: if the mechanism code differs from `d920af162` in any way
  other than the added family 13 dispatch entries and the replaced
  `main()`, the result is VOID. Verified by diff before running.

### 2.2 Evaluation procedure

1. Fresh state: learner state initialized to zeros (no retained forms).
2. Run family 13 via the standard discovery protocol (run_family):
   - BMAX=40 discovery buffer via true_subj/true_obj.
   - Menu forms 0,1,2 attempted first on the current buffer.
   - If menu exhausted at n=40, inventor hook fires: construct_search.
   - If exact fit, verify under V schedule, then promote.
   - If no exact fit, HONESTFAIL (adopted=-1).
3. Record: adopted, promoted, cost, inv_event (if instrumented), node count,
   EQ node count, final tree structure (node ops and parameters),
   HONESTFAIL trace if applicable.
4. Determinism: 3 runs, byte-identical output required.

### 2.3 Cost accounting

Per bridge prereg section 3: cost = examples observed + candidate tree
simulations during construct_search. Ceiling is 108.

### 2.4 Held-out verification (for F-DECEPT-WRONG)

If a tree is promoted, it is additionally evaluated on held-out points
i=40..49 with the pattern extended (true_subj=13040+i). All held-out
subjects are below 13050, so the expected value is 1 throughout. A promoted
tree that fits the 40-point buffer but is behaviorally wrong on held-out
fires F-DECEPT-WRONG.

## 3. Frozen success and failure bars

Carried verbatim from the original adversary design (section 5) and prereg
(section 3). The fix design's worked prediction (section 5 of the design:
ACCEPTABLE via HONESTFAIL at cost approximately 84) is design validation,
NOT a result, and does not alter these bars.

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
- Clean HONESTFAIL trace (search terminated without exact fit).

### 3.3 FAIL (adversary succeeds)

Any of:
- F-DECEPT-COST: cost > 108.
- F-DECEPT-DEGENERATE: promoted tree uses more than 4 EQ nodes.
- F-DECEPT-NODECAP: promoted tree exceeds 8 nodes.
- F-DECEPT-MEMORIZE: promoted tree achieves exact fit via EQ memorization
  without an LT split separating the zero-block as a region.
- F-DECEPT-WRONG: promoted tree fits buffer but is wrong on held-out.
- F-DECEPT-PREEMPT (carried from the original FAIL): adopted=0 via menu
  CONST with the inventor never firing, i.e. the original failure mode
  recurs on the fixed bridge. This fires if the fix failed to change the
  protocol behavior on this family.

## 4. Kill bars for this evaluation

- K1: this prereg frozen BEFORE any evaluation commit. Satisfied by this
  file's commit.
- K2: evaluation implemented under the sealed protocol of section 2;
  bars of section 3 applied to the measured outcome.
- K3: pure Zag (no Python anywhere including scratch, diagnostics, byte
  checks, verification), no em dashes or en dashes in loop documentation,
  deterministic (byte-identical output across 3 runs).

Evaluator reports STRONG-PASS, ACCEPTABLE, or FAIL with the specific bar
or falsifier that determined the outcome. No SURVIVES claim is made here:
C0-C (independent post-freeze adversary data point count) and C0-D
(cognitive reuse) remain open promotion-pipeline steps.
