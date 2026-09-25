# WS2-L VERDICT — ARM L (learned synonyms)

All K1–K7 pass. Primary S_L=69/69 ≥ S_B=60/69. **ADOPT L.**

## K-gates

| Gate | Bar | Observed | Verdict |
|------|-----|----------|---------|
| K1 provenance | every relation traces to ≥1 corpus evidence matching its rule | 112/112, 0 errors (independent Python audit); 4 veto pairs absent | PASS |
| K2 no curated leakage | no curated pair strings in L code or binaries | 0 hits in learn.zag, toc_l.zag, learn_bin, tocl_bin | PASS |
| K3 determinism | 3 clean repetitions byte-identical | out/rep identical ×3 (official + new) | PASS |
| K4 primary | S_L ≥ S_B=60/69 | S_L=69/69 (51+6+6+6) | PASS |
| K5 no regression | official unchanged | 51/51, out/rep/grade SHAs byte-identical to frozen B baseline | PASS |
| K6 beats B per battery | L > B on all five | FRESH 6/6>0/6, DIST 6/6>5/6, ADV-NEAR 6/6>4/6, MULTI-HOP 4/4>0/4, MORPH 3/4>0/4 | PASS |
| K7 non-degeneracy | 50 ≤ store ≤ 200 | 112 relations | PASS |

## Scores

- OFFICIAL-51 (v1.1, QP04-compliant): 51/51. out
  `b09796e7…` rep `a17d10ec…` grade `c25fa213…` — byte-identical to B.
- FRESH: 6/6. DIST: 6/6 (QD3→DOG1, QD1/2/4/5/6 correctly empty).
  ADV-NEAR: 6/6 (QAN1→DOG1, QAN6→SAN1). QD3 and QAN1 both resolve DOG1.
- MULTI-HOP: 4/4. MORPH: 3/4 — QMO3 FAILS (predicted): MH3 and MO3 tie
  at phase-2 score 2002, unique-top override does not fire. Exact
  predicted failure, reported not forced.
- GEN (post-freeze): 7 evidences → 7 relations; 112/112 old intact;
  QGN1→GN1, QGN2→GN2 (2/2).

## Frozen store

- `store_l/synlearn.txt` (112 relations):
  `3b5062cbf6a4c5996bf3bded81b07893ca4a2b4ad2053f3c0c8a50fca9d7da1f`
- `store_l/synveto.txt` (4 vetoes):
  `95ae8c7aa37f6388df3f6b2b26a15d82fa760e7a0ba8ad92bda87141c2e3cf96`
- Learning: `learn: ok lines=276 relations=112 vetoes=4 suppressed=0`
  from empty store (dump proven 0 relations first).

## Bugs found and fixed (before batteries)

1. R2 matcher word positions wrong (never fired; 8 MORPH pairs missing).
2. Lid provenance flat (start,count) layout misattributed R3 lids when
   relations interleaved; replaced with per-relation linked list.
   Both fixed, store re-learned from empty, K1 re-audited clean.

## Adoption

All K1–K7 pass and S_L=69/69 ≥ 60/69. Per PREREG_WS2L.md §6 step 12:
delete `docs/lab/cognition_ws/ws2/SYN_TABLE_V1.txt` and
`docs/lab/cognition_ws/ws2/src/syn_table.zag`. Done in this commit.
