# PREREG: Per-Candidate (Per-MAP) Applicability (UNFROZEN)

Frozen: 2026-10-02, before the per-candidate implementation is written,
built, or run. This prereg governs the APPLICABILITY-PERMAP experiment.
It is a fresh preregistration, not an amendment. Kill bars below are
frozen; breaking the prereg voids the run.

## Problem (from the meta-applicability rerun, 2026-10-02)

The rerun fixed the node-leak bug and reached K7, but FAILED K3:
TREAT_C=49 vs NAIVE_C/2=29.5. Diagnosis (rerun REPORT.md, K3 analysis):
the APPL gate judges problem-level applicability ("attempt reuse at
all?") but cannot express per-candidate applicability ("reuse WHICH
structure?"). After the C0 burn it refuses all reuse on C-like problems
(gate=0 on C1..C5, paying trial cost 4 each), missing that the
C0-promoted plen-4 MAP is reusable at 1 try each, which naive discovers
by blind search. The gate wins every block total (A' 5 vs 10, B 5 vs 25,
C 49 vs 59) but leaves the per-candidate win on the table.

## Mechanism under test: APPL-PERMAP

Extension of the APPL gate from problem-level to per-candidate
(per-MAP-shape) applicability judgments:

- Consequence records are partitioned by the candidate MAP's observable
  shape: rb_chain_plen of the candidate's promoted graph root (computed
  from graph structure, zero domain labels). Rebind already matches
  candidates to paths by exact plen, so applicability is inherently
  shape-partitioned in this substrate.
- Per-shape decision rule: for candidate shape p on problem features F,
  let n_p be the record count for shape p. If n_p < 3, attempt
  (optimistic, same threshold as the problem gate). Else attempt iff
  avg similarity of F to shape-p success records exceeds avg similarity
  to shape-p failure records by the 15-point pessimistic margin.
- Similarity uses the SAME 8 observable features as the rerun
  ([np, pmax, c5, c4, c3, c2, cx, r]), the same formula
  (sim = 10000/(100+2D), D = sum w_j*|d_j|), and the same
  consequence-driven weight rule (nearest opposite-outcome record over
  all records, w_j += 25*|F_j - G_j|, clamp 800). The shape key is the
  per-MAP extension: an exact-match partition, not a 9th similarity
  feature.
- Each attempted candidate records its own consequence (F, shape,
  success/failure, verify-try cost). Trial promotions are not recorded.
- Candidate order is unchanged (two-pass: linked newest-first, then id
  order); candidates whose per-shape gate is 0 are skipped.

RESEARCHER-OWNED: feature list, sim formula, 15-point margin, ETA=25,
cap 800, optimism threshold 3, shape-partition rule, uniform w=100
priors. LEARNER-OWNED: all weights, all records, all per-candidate
decisions. No domain labels anywhere. 0 new modes/bridges/handlers.

## Design

Same 21-problem sequence as the rerun (Phase 1 A x5, A' x5, B x5,
C x6). Four arms, 3/3 byte-identical runs each:

- PERMAP: Phase 1 + per-candidate gate (new implementation).
- TREAT: Phase 1 + problem-level gate (rerun sources verbatim; control).
- NAIVE: Phase 1 + always-attempt rebind (rerun sources verbatim).
- FRESH: no Phase 1 + problem-level gate (rerun sources verbatim).

Metric: per-problem cost = rebind verify-tries + trial verify-tries.

## Predicted transfer matrix (total tries per block)

| Block   | PERMAP | TREAT | NAIVE | FRESH |
|---------|--------|-------|-------|-------|
| A' (x5) | 5      | 5     | 5     | 10    |
| B (x5)  | 5      | 5     | 25    | 5     |
| C (x6)  | 10     | 49    | 59    | 44    |

Derivation of PERMAP_C=10: on C0 the plen-5 per-shape gate is 1 (same 9
A/A' success records and uniform weights as the problem gate's C0=1, so
the first plen-5 MAP is attempted and fails, 1 try); the second plen-5
MAP already sees avf=100 and is skipped; plen-3 MAPs are skipped outright
(n_p=4 B-success records, avs<=9.1 < 15 by the feature deltas c4/c2/cx/r
with uniform weights, independent of np); trial costs 4 and promotes the
plen-4 MAP. C0 = 1 + 4 = 5. On C1 the plen-4 shape has 0 records, so the
optimistic rule attempts the C0-promoted MAP: 1 try, success. C2..C5:
plen-4 records accumulate (1, 2, then 3+ with avs=100), each 1 try;
plen-5 and plen-3 shapes stay gated 0 on C features. C1..C5 = 1 each.
Total C = 5 + 5 = 10.

TREAT/NAIVE/FRESH predictions are the frozen measured rerun values
(49/59/44); the rebuilt controls must reproduce them byte-identically.

## Frozen kill bars

- P1 C-block recovery: PERMAP_C < TREAT_C AND PERMAP_C < NAIVE_C.
- P2 per-candidate identification: C1..C5 each total=1 with rb=1 and
  trial=0; the run log shows the attempted candidate has plen=4 on each
  of C1..C5; per-shape replay on saved C0 features under final weights:
  plen-5 gate=0 AND plen-4 gate=1.
- P3 A' no false negatives: PERMAP_A' = 5, plen-5 attempted on all 5.
- P4 B neutral: PERMAP_B <= 10; plen-5 never attempted on B (log shows
  per-shape gate=0 for every plen-5 candidate on B0..B4).
- P5 C0 burn bounded: PERMAP_C0 < 29 (the problem-gate C0 burn).
- P6 determinism: 3/3 byte-identical runs per arm (SHA-256 recorded).
- P7 process: pure Zag, safebin PATH, `which python3 python` empty.
- P8 architecture: 0 new modes/bridges/handlers; no researcher domain
  labels; weights/records/decisions learner-owned.

Verdict APPLICABILITY-PERMAP-COMPLETE requires P1-P8 all PASS. Any bar
failed: verdict is FAIL with the bar named, no reinterpretation.

## Falsification notes

- If PERMAP_C >= 49, per-candidate partitioning bought nothing over the
  problem gate: FAIL P1, mechanism rejected.
- If the plen-4 MAP is attempted but costs more than 1 try on C1..C5,
  the "reusable at 1 try each" claim fails: FAIL P2.
- If any control arm's output hash differs from the frozen rerun hash,
  the setup changed and the comparison is void: reported, not silently
  adopted.
