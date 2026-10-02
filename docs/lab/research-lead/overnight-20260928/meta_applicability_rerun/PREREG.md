# PREREG: Meta-Learning Applicability RERUN (UNFROZEN)

Frozen: 2026-10-02, before the fixed implementation is built or run.
This prereg governs the META-APPLICABILITY-RERUN experiment. It replaces
the 2026-10-01 prereg, which is broken by a base change (see below); per
governance, a broken prereg is re-frozen fresh, never amended in place.
Kill bars below are frozen; breaking the prereg voids the run.

## Why a rerun

The 2026-10-01 run (commit 0478b8eaf) verified the APPL mechanism
behavior (K1, K4, K5 PASS; K2, K3, K6 partial) but returned FAIL on K7:
TREAT and NAIVE stall on the 21st problem (C-P5) and C-P5 was unmeasured.
Diagnosis (NAMECHECK.md, REPORT.md): the stall is a base TNN-2 defect,
not a gate defect. Every failed `t2_trial`/rebind candidate leaks its
assembled 4-op ISA graph cells (4 per link) plus one frame node per
verify; the 1024-node arena fills around problem 17-20 of the 21-problem
TREAT/NAIVE sequences (instrumented: 983 nodes live after C-P4; C-P5
needs about 1034). Past the limit, each `alloc_node` falls through to
`evict_node`'s O(1024 x 4096) lowest-bid scan, and C-P5's dozens of
allocs stall the run. FRESH (16 problems) completes just under the
limit. The gate path at the stall point is gate=0 trial-only, so the
defect is isolated to the base miss policy.

## Base change (the only setup delta)

In the rerun copy `ma_base.zag` only (frozen base read-only, untouched):

- New `t2_free_graph(W, root)`: on verification failure, walks the
  failed candidate's SEQ edges (type 12), BRANCHEQ true-targets
  (field12), and private literal nodes (field8, tag 902), removes every
  edge touching a collected cell, and marks collected cells dead.
- `t2_try_verify` calls `t2_free_graph` on the failure path.
- `t2_exec` reclaims its per-verify frame node before returning.

Verified (promoted) graphs are never freed. No verify outcome, trial
count, gate decision, or record changes; the fix only removes arena
pressure. The APPL gate (`ma_patch.zag`) and driver (`ma_driver.zag`)
are unchanged.

## Question (unchanged)

Micah Priority 5: TNN must learn applicability judgments from experience.
Prior experience should accelerate related domains, stay neutral on
irrelevant domains, and be rejected when misleading. No researcher domain
labels. Redteam bound to beat: irrelevant plen-3 experience caused 4x
negative transfer (40 vs 10) because rebind tries everything.

## Mechanism under test: APPL gate (unchanged)

Learner-owned applicability judgment on structural reuse (rebind):

- Problem signature F (8 observable features, no labels): gathered path
  count, max plen, counts of plen-5/4/3/2 paths, count of paths containing
  a non-r1 edge (cx), query relation.
- Consequence records: every reuse attempt stores (F, success/failure).
- Similarity: sim = 10000/(100+2D), D = sum_j w_j*|d_j|, w learned.
- Decision: attempt reuse iff avg_sim_to_successes > avg_sim_to_failures
  + 15 (pessimistic prior margin). Optimistic iff fewer than 3 records.
- Weight learning (consequence-driven): on each attempt, find nearest
  opposite-outcome record; w_j += 25*|F_j - G_j| (clamp 800). Features
  that discriminate success from failure gain weight.

RESEARCHER-OWNED: feature list, sim formula, 15-point margin, ETA=25,
cap 800, optimistic threshold 3, priors (w=100 uniform).
LEARNER-OWNED: all weights, all records, all gate decisions.

## Design (unchanged)

- Phase 1 (Domain A, 5 problems): plen-5 true chains. Learns plen-5 MAPs
  and seeds success records.
- Phase 2a (A-prime, 5): plen-5, fresh literals/subjects. Related.
- Phase 2b (B, 5): true plen-3, plen-5 decoy, query r=6. Irrelevant.
- Phase 2c (C, 6): true plen-4, plen-5 r1 decoy, plen-3 r2 decoy,
  query r=5. Misleadingly similar (surface: c5=1, r=5, max plen 5 like A;
  deep: cx=2 unlike A).

Arms (3/3 byte-identical runs each):
- TREAT: Phase 1 + APPL gate.
- FRESH: no Phase 1 + APPL gate (fair prior-experience baseline).
- NAIVE: Phase 1 + always-attempt rebind (no gate; reproduces redteam).

Metric: per-problem cost = rebind verify-tries + trial verify-tries.

## Predicted transfer matrix (total tries per block)

| Block   | TREAT | FRESH | NAIVE |
|---------|-------|-------|-------|
| A' (x5) | 5     | 10    | 5     |
| B (x5)  | 5     | 5     | 55    |
| C (x6)  | 49    | 44    | 159   |

Derivation: trial costs A=6, B=1, C=4 per problem from scratch; rebind
success = 1 try; C0 burn for TREAT = 25 wasted + 4 trial. NAIVE values
are the 2026-10-01 prereg predictions; the rerun measures them directly
(the 2026-10-01 run could not complete NAIVE).

## Frozen kill bars (unchanged)

- K1 positive transfer: TREAT_A' < FRESH_A'.
- K2 neutral: TREAT_B <= 2*FRESH_B AND TREAT_B < NAIVE_B/3.
- K3 recovery: TREAT_C < NAIVE_C/2 AND last 3 C problems of TREAT are
  trial-only (gate=0 in log).
- K4 no false negatives: TREAT_A' gate=1 on all 5.
- K5 B no-burn: TREAT_B gate=0 on all 5.
- K6 C learns: TREAT_C0 gate=1 (one exploratory burn), w_cx strictly
  increases after C0, TREAT_C1..C5 gate=0.
- K7 determinism: 3/3 byte-identical runs per arm (SHA-256 recorded).
- K8 process: pure Zag, safebin PATH, `which python3 python` empty.

Verdict META-APPLICABILITY-RERUN-COMPLETE requires K1-K8 all PASS.
Any bar failed: verdict is FAIL with the bar named, no reinterpretation.

## FRESH invariance check

The base fix must not change FRESH behavior (FRESH never reached arena
exhaustion in the 2026-10-01 run). The rerun's FRESH 3/3 SHA-256 is
compared against the 2026-10-01 FRESH hash
afe2fff8dc5982ed93e621180822825d51d438d029d8ded75e3e20c0ffadee0d.
A mismatch is reported honestly with the delta; the rerun's own FRESH
then serves as the baseline for K1/K2.
