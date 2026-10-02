# PREREG: Meta-Learning Applicability V2 (UNFROZEN)

Frozen: 2026-10-02, before v2 implementation. This prereg governs the
META-APPLICABILITY-V2 rerun. Kill bars below are frozen; breaking the
prereg voids the run.

## Background (v1)

V1 (PREREG_V1.md, frozen 2026-10-01) FAILED K7. Root cause diagnosed
2026-10-02 via instrumented rerun (`ma_diag_bin`):

- Workspace: 1024 nodes (hardcoded `NN()=1024`, 30 occurrences in base).
- Trial candidate graphs accumulate with no reclamation (~40-50 nodes/problem).
- TREAT (21 problems): C-P3 nodes=932, C-P4 nodes=983, C-P5 nodes=1022.
- At C-P5 (1022/1024), `alloc_node` triggers `evict_node` mid-trial,
  corrupting live state. Trial=11 tries, ans=-2 WRONG.
- FRESH (16 problems) stayed under the limit; all 16 OK.

**Verdict on v1 failure:** Harness capacity artifact, NOT a mechanism
failure. The APPL gate itself worked (K1/K4/K5 PASS; K2/K3/K6 partial).
The 21-problem design exceeds the 1024-node harness. This is documented,
not hidden.

## V2 design change (harness only, science unchanged)

Same mechanism (APPL gate, verbatim `ma_patch.zag`). Same domains.
Reduced problem counts so the 21-problem sequence fits in 1024 nodes:

- Phase 1 (Domain A): 4 problems (was 5). Seeds plen-5 MAPs + gate records.
- Phase 2a (A-prime): 4 problems (was 5). Related domain.
- Phase 2b (B): 4 problems (was 5). Irrelevant domain.
- Phase 2c (C): 5 problems (was 6). Misleading domain.
- Total: 17 problems (was 21). Estimated peak nodes ~800 < 1024.

No base changes. No patch changes. Only the driver problem counts and
literal bases change. The scientific question (applicability judgments
from experience, no domain labels) is unchanged.

## Predicted transfer matrix (total tries per block)

Derivation (from v1 prereg): trial costs A=6, B=1, C=4 per problem from
scratch; rebind success = 1 try; C0 burn for TREAT = 25 wasted + 4 trial.

| Block  | TREAT | FRESH | NAIVE |
|--------|-------|-------|-------|
| A' (x4)| 4     | 9     | 4     |
| B (x4) | 4     | 4     | ~44   |
| C (x5) | 45    | 40    | ~132  |

FRESH_A' = 6+1+1+1 = 9 (cold start on AP-P0, then rebind).
NAIVE estimates scale from v1 redteam bound (ADV-L2L-IRREL 4x).

## Frozen kill bars (adapted counts, same bars)

- K1 positive transfer: TREAT_A' < FRESH_A'.
- K2 neutral: TREAT_B <= 2*FRESH_B AND TREAT_B < NAIVE_B/3.
- K3 recovery: TREAT_C < NAIVE_C/2 AND last 3 C problems of TREAT are
  trial-only (gate=0 in log).
- K4 no false negatives: TREAT_A' gate=1 on all 4.
- K5 B no-burn: TREAT_B gate=0 on all 4.
- K6 C learns: TREAT_C0 gate=1 (one exploratory burn), w_cx strictly
  increases after C0, TREAT_C1..C4 gate=0.
- K7 determinism: 3/3 byte-identical runs per arm (SHA-256 recorded).
- K8 process: pure Zag, safebin PATH, `which python3 python` empty.

Verdict META-APPLICABILITY-V2-COMPLETE requires K1-K8 all PASS.
Any bar failed: verdict is FAIL with the bar named, no reinterpretation.

## Trial node reclamation (noted frontier, not in v2)

The base `t2_trial` leaks candidate graph nodes (~40-50/problem). The
base `evict_node` handles a full workspace but corrupts in-flight trials.
Structural trial memory reclamation is a separate frontier (identified in
v1). V2 sizes the harness to fit; it does not fix the leak.
