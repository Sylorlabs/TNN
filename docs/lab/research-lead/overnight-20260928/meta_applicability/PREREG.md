# PREREG: Meta-Learning Applicability (UNFROZEN)

Frozen: 2026-10-01, before implementation. This prereg governs the
META-APPLICABILITY experiment. Kill bars below are frozen; breaking the
prereg voids the run.

## Question

Micah Priority 5: TNN must learn applicability judgments from experience.
Prior experience should accelerate related domains, stay neutral on
irrelevant domains, and be rejected when misleading. No researcher domain
labels. Redteam bound to beat: irrelevant plen-3 experience caused 4x
negative transfer (40 vs 10) because rebind tries everything.

## Mechanism under test: APPL gate

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

## Design

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
success = 1 try; C0 burn for TREAT = 25 wasted + 4 trial.

## Frozen kill bars

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

Verdict META-APPLICABILITY-COMPLETE requires K1-K8 all PASS.
Any bar failed: verdict is FAIL with the bar named, no reinterpretation.
