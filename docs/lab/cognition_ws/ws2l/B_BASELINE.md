# B_BASELINE — WS2-L ARM B validation baseline (2026-09-25)

Authority: frozen `docs/lab/cognition_ws/ws2l/PREREG_WS2L.md`; binary rebuilt from
frozen WS2-B2 sources (`toc_b2.zag`, `syn_table.zag`, `lib.zag`,
`R33_NATIVE_*.zag`) with pinned `znc_linux_x86_64_abed8aa1`; synonym table
byte-identical to `SYN_TABLE_V1.txt`
(SHA `bd23d16fe518024d15445299808017b91e4a47c1ef7d075d516363887c22fc7b`).
RNG grep over all three sources: zero hits. Pure Zag mechanism; Python harnesses
only for battery generation (no hand transcription).

## Official-51 replication (frozen battery as-is, v1.1 corpus)
51/51 PASS. Outputs byte-identical to the frozen `WS2B2_PRELIM.md` evidence:
- out:   `b09796e7dbc2d2b1fd81246630cc27a80f0d2762eccbadefe83fcfdbdd1490b4`
- rep:   `a17d10ec3cccae6d6fe780383b6d48351aa1e9b047bd4ce6ad0aa7a9c0d08954`
- grade: `c25fa213da8ef25dd95e0f207b4f374d019cf186c385e24d5cf0ee145f09124b`
Corpus note: frozen `probe_corpus.txt` contains PD01 twice; `init` drops the
duplicate (`items=33 dropped_dup=1`) — frozen behavior, unchanged.

## New batteries (combined corpus: v1.1 + 25 new items, 26 queries)
Validated with the real `tocb` binary; 10 phase-1 leaks rephrased (see
LEAKFIX.md; all changes recorded there, none reverted silently).

| Battery  | Predicted | Attained | Detail |
|----------|-----------|----------|--------|
| FRESH    | 0/6       | 0/6      | all abstain (golds FR01–FR06 unreached) |
| DIST     | 6/6       | **5/6**  | QD1,QD2,QD4,QD5,QD6 abstain ✓; QD3 abstains (gold DOG1) |
| ADV-NEAR | 4/6       | 4/6      | QAN2–QAN5 abstain ✓; QAN1,QAN6 abstain (golds DOG1,SAN1) ✓ |
| MULTI-HOP| 0/4       | 0/4      | all abstain (golds MH1–MH4 unreached) |
| MORPH    | 0/4       | 0/4      | all abstain (golds MO1–MO4 unreached) |

Overall new-battery: 9/26 PASS (a PASS = correct abstain, or correct retrieval).

## Why DIST is 5/6: frozen-prereg contradiction (BLOCKED, not forced)
QD3 (DIST) and QAN1 (ADV-NEAR) are byte-identical queries —
`the canine watched the flock in darkness`, gold DOG1. The frozen synonym table
contains none of dog|canine, guarded|watched, sheep|flock, night|darkness
(verified by table grep), so ARM B abstains on both (confirmed on the binary).
§6 predicts DIST 6/6 (QD3 "must retrieve DOG1 via canine|dog") AND ADV-NEAR 4/6
(QAN1 must miss because the pair is absent). A deterministic mechanism cannot
return different results for identical query text and gold. Making QD3 pass
would require deliberately injecting phase-1 exact overlap — violating the
battery's zero-overlap purpose and "forcing it". Per the task rules, the exact
blocker is reported instead: **the §6 DIST 6/6 prediction is unsatisfiable as
written; attainable DIST is 5/6.** No battery text was altered to chase it.

## Mechanism facts established during validation
- `init` sorts items by ID ascending (byte-lexicographic); ties in
  `cell_score*1000 + own_score` break to the smaller item ID.
- Phase-2 bridge fires only on ≥2 distinct synonym-stem hits with a unique top
  candidate; verified against the binary on all 26 queries (Python mirror:
  26/26 identical).
- Combined-corpus observation (not a battery change): frozen official query
  QP04 ties at tot=1001 with new items BOR1/DS6 on stem "neighbor" and loses the
  ID tie-break (BOR1 < DS6 < PP04) → 50/51 on the combined corpus. OFFICIAL-51
  is defined on the frozen v1.1 corpus (51/51 above). Flagged for the ARM L
  worker's awareness.

## Determinism (3x, fresh init each run)
New batteries (corpus_l.txt, 26 queries):
- out:   `4f8ffe2627755d8f3bc05da4a14b2bf47726356e2dd6eb0bfab943c0426b2c03` (×3)
- rep:   `b25717d5650526e97260275c7e4de5b7175de0adb3ff14d6bdd224735376d6fd` (×3)
- grade: `6e75506739af931ce6eb357e79c1899b6d336e3aeafeb5e8da747c741512c52e` (×3)
Official-51 (v1.1 corpus): out/rep/grade SHAs as above (×3), byte-identical to
the frozen prelim evidence.

## Files in this directory
- `corpus_l.txt` — v1.1 (frozen, byte-identical incl. PD01 dup) + 25 new items
- `queries_ws2l.txt`, `keys_ws2l.txt`, `answers_ws2l.txt` — 26 queries/keys/golds
- `LEAKFIX.md` — all 10 rephrasings + 2 reverted attempts + QD3 note
- `B_BASELINE.md` — this file
- `det/` — 3x determinism run outputs (out/rep/grade) and logs
- `build_ws2l_batteries.py` (in `~/workspace/cognition_ws/ws2l/`, scratch) —
  regenerates the four battery files from the frozen prereg + fix table;
  outputs verified byte-identical to the validated inputs.
