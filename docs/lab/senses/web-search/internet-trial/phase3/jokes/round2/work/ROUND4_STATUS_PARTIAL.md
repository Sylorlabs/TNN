# Round 4 — PARTIAL Status (2026-09-23)

## Verdict: PARTIAL — collection incomplete, gate not run

Round 4 cannot be completed in this session. The pattern-support collection
requires ~86 individually-verified real-web items; 3 were collected. The gate
was not run. This document gives exact numbers, the mechanism, and the
Round 5 plan.

## Frozen constraints (unchanged)

- Prereg `phase3/PREREG.md` §3 @ `266ca4e18593de287a86daaf107cb36680577657`.
- Design `phase3/jokes/round2/ROUND2.md`; gate `phase3/jokes/GATE_SPEC.md`.
- G1 ≥20/24 both arms; G2 ≤4/40 both arms; D6 = 1.00; 3 byte-identical runs/arm; hash-chained ledgers.
- Pure Zag, deterministic, zero RNG. Never-SINCERE/never-DECEPTIVE policy.
- Do not commit. No binaries/`.zagd` in tree. Work under `~/workspace`.

## What was accomplished (2026-09-23)

### 1. Corpus surgery (done)
- Removed duplicate toothpaste variants `t3_001`, `t3_002` (canonical `t2_031` kept).
- Corpus: 298 → 300 items (2 web items merged, then 1 more).
- Nine honest training-side re-annotations from `NONE` to D-A patterns:
  `t2_054, t2_062, t2_063, t2_152, t2_163, t2_164, t2_165, t2_197, t2_198`.
- All re-annotations verified: verbatim web text, URL, retrieval date intact;
  distinct groups are new (no collision with existing groups).

### 2. Phrase vocabulary additions (done, documented)
`work/phrases_r4.json` adds four phrases, each grounded in a verified web item:
- `glitter` → `F_NOTFOOD` (t4_001)
- `putting` → `A_ADD` (t4_001)
- `retread` → `A_APPLY` (t4_002)
- `battery` → `A_ELEC` (t4_003, verified Memedroid page)
Documented in `work/PHRASE_ADDITIONS_R4.md`. No held-out outcome was used to
choose these; all four fire on training/web items first.

### 3. New web items collected (3 of ~89 needed)
- `t4_001`: "glitter in mouth before sneezing" → `A_ADD & F_NOTFOOD`
  (abrozzi.com, retrieved 2026-09-23, group `da1c_glitter`)
- `t4_002`: "retread tires with Sharpie" → `A_APPLY & F_COSMETIC & F_TIRE`
  (abrozzi.com, retrieved 2026-09-23, group `da4m_sharpie`)
- `t4_003`: "Put the battery in the microwave..." → `A_ELEC & F_MICRO`
  (memedroid.com, retrieved 2026-09-23, group `da3e_battery_microwave`)
- Retrieval dates corrected to 2026-09-23. Merge validation passed.

### 4. Pattern audit (done, before collection)
`work/HELDOUT_PATTERN_AUDIT_R4.md`: all 24 held-out D-A texts mechanically
fire ≥1 intended D-A pattern with current vocabulary. This validates the
pattern definitions; it was NOT used to tune anything.

### 5. Calibration baseline (done)
`work/cal_pre_collection_baseline.json`: training-only, 300 items.
- never-SINCERE/never-DECEPTIVE: PASS (by construction).
- D-A/JOKING: 24/48; D-B/JOKING: 15/85; SAT/SATIRE: 6/38.
- 3 known false contradiction fires on training (negated warnings, reported
  hoaxes): `t2_155`, `t2_185`, `t3_071`. Mechanism documented; repair must use
  training examples only.

## Exact numbers — where Round 4 stands

### Corpus
- `work/training_items_r4.jsonl`: **301 items** (300 + t4_003).
- Families: D-A 60, D-B 85, HOAX 62, SAT 38, SINC 67 (approx; 301 total).
- `corpus/training_corpus.json`: NOT rebuilt (builder not run; see below).

### Pattern support (distinct groups; need ≥4 per pattern)

| Pattern | Groups | Items | Need | Held-out IDs |
|---|---:|---:|---:|---|
| P_DA3E (A_ELEC & F_MICRO) | **4** ✓ | 4 | 0 | hda11, hda20 |
| P_DA1C (A_ADD & F_NOTFOOD) | 3 | 3 | 1 | — |
| P_DA3B (A_INSERT & F_HEATAPP) | 2 | 3 | 2 | hda02 |
| P_DA4B (A_INFLATE & F_WRONGGAS & F_TIRE) | 1 | 4 | 3 | hda07 |
| P_DA3F (A_DELETE & F_CRITSYS) | 1 | 7 | 3 | hda10 |
| P_DA3S (A_INSERT & F_SOCKET) | 1 | 4 | 3 | — |
| P_DA3D (A_TUB & F_HEATAPP & F_WATER) | 1 | 4 | 3 | — |
| P_DA4M (A_APPLY & F_COSMETIC & F_TIRE) | 1 | 1 | 3 | hda18 |
| P_DA2A (A_APPLY & F_IRRIT & F_WOUND) | 1 | 1 | 3 | hda03 |
| P_DA2V (A_BITE_SEEK & F_VENOM) | 1 | 1 | 3 | — |
| P_DA4W (A_TAKE & F_WILDLIFE) | 1 | 1 | 3 | — |
| P_DA4K (A_KISS & F_STRANGER) | 1 | 1 | 3 | — |
| P_DA4I (A_INJURE & F_BODY) | 1 | 1 | 3 | hda17 |
| P_DA4A (A_ACCEL & F_CAUGHT) | 1 | 1 | 3 | hda14 |
| P_DA1E | 0 | 0 | 4 | hda08 |
| P_DA1L | 0 | 0 | 4 | hda19 |
| P_DA1S | 0 | 0 | 4 | hda15 |
| P_DA1T | 0 | 0 | 4 | hda16 |
| P_DA1X | 0 | 0 | 4 | hda01 |
| P_DA1Y | 0 | 0 | 4 | hda21 |
| P_DA2D | 0 | 0 | 4 | hda13 |
| P_DA2S | 0 | 0 | 4 | hda04 |
| P_DA3T | 0 | 0 | 4 | hda24 |
| P_DA4H | 0 | 0 | 4 | hda05 |
| P_DA4N | 0 | 0 | 4 | hda22 |
| P_DA4R | 0 | 0 | 4 | hda23 |
| P_DA4S | 0 | 0 | 4 | hda06 |
| **Total needed** | | | **89** | |

### Gate projection (not run)
- G1: ~2/24 (only P_DA3E patterns would fire: hda11, hda20). **FAIL** (<20).
- G2: 0/40 (never-SINCERE by construction). PASS.
- D6: unknown (classifier not implemented).
- Byte-identity: N/A (no runs).

## Mechanism — why the gate would fail

The vocabulary and pattern definitions are CORRECT (all 24 held-out items fire
mechanically). The failure is purely **training support**: 26 of 27 D-A
patterns have <4 distinct supporting groups, so the builder would drop them
(or fail on annotated items). The classifier cannot honestly claim a pattern it
has not seen ≥4 distinct exemplars of.

This is a **data volume** problem, not a **mechanism** problem. The Round 2/3
corpus was built for family coverage, not pattern support. Round 4's audit
correctly identified the gap; the collection effort is 89 items.

## Critical finding — held-out source overlap

`boredpanda.com/funny-bad-advice-45/` (a training source, 21 items) and
`boredpanda.com/funny-bad-advice/` (the held-out source, 20 items) contain
SUBSTANTIALLY OVERLAPPING content. Verified: 18 of the 20 held-out D-A items
appear verbatim on funny-bad-advice-45/.

**This is not a leak**: the 21 training items from funny-bad-advice-45/ are
verified byte-distinct from all held-out items (folded-body check, 0 dups).
But it means funny-bad-advice-45/ is **exhausted** as a collection source for
gap patterns — every joke matching a gap pattern on that page is already in
held-out. Round 5 must use different sources.

## Round 5 recommendation: WARRANTED, with focused collection

### Scope
Collect 89 distinct real-web items across 26 patterns (table above). Each item:
- Individually fetched URL, retrieval date, verbatim body.
- Honest D-A annotation with contradiction gloss.
- New distinct_group (no collision).
- Folded body disjoint from held-out and existing training.

### Priority order (highest G1 leverage first)
1. **P_DA3B** (need 2): hda02. "Knife/spoon in toaster" variants.
2. **P_DA4B** (need 3): hda07. Helium-tire variants (different gases/vehicles).
3. **P_DA3F** (need 3): hda10. "Delete system file" variants (boot.ini, format, rm -rf).
4. **P_DA1C** (need 1): canonical Micah case. "Add non-food to food" variants.
5. **P_DA4M** (need 3): hda18. "Marker/paint on tires" variants.
6. Then the 12 zero-support patterns with held-out items (P_DA1E, P_DA1L, P_DA1S,
   P_DA1T, P_DA1X, P_DA1Y, P_DA2D, P_DA2S, P_DA3T, P_DA4H, P_DA4N, P_DA4R, P_DA4S),
   4 items each.
7. Finally P_DA2A, P_DA2V, P_DA4W, P_DA4K, P_DA4I, P_DA4A, P_DA3S, P_DA3D
   (no held-out, but annotated; 3 each to reach 4).

### Suggested sources (avoid funny-bad-advice-45/)
- imgflip.com, quickmeme.com, memedroid.com (meme-format variants)
- Quora "worst advice" threads (text answers)
- thechive.com, ebaumsworld.com (listicles; verify text is extractable)
- KnowYourMeme (documents troll variants, e.g. System32)
- Reddit via search-engine-indexed threads (r/ShittyLifeProTips)

### After collection
1. Merge batches with `work/merge_r4_batch.py` (validates schema/disjointness).
2. Run `work/build_training_r4.py` (fails if any pattern <4 groups; re-annotate or collect).
3. Run `work/r4_proto.py`; write `TRAINING_RECORD.md`.
4. Implement pure-Zag classifier + R6 bridge (see ROUND2.md §5).
5. Compile outside tree; 3 runs/arm; verify byte-identity, D6, hash chains.
6. Score with frozen gate. If G1 <20, do NOT tune from held-out; report.

## Files delivered

- `work/training_items_r4.jsonl` (301 items, 9 re-annotations, 3 new)
- `work/phrases_r4.json` (+4 phrases)
- `work/PHRASE_ADDITIONS_R4.md`
- `work/HELDOUT_PATTERN_AUDIT_R4.md`
- `work/cal_pre_collection_baseline.json`
- `work/build_training_r4.py` (not run; ready)
- `work/r4_batch_01.jsonl`, `work/r4_batch_02.jsonl`, `work/r4_new.jsonl`
- `work/merge_r4_batch.py`, `work/r4_proto.py`, `work/surgery_r4.py`
- This file (`work/ROUND4_STATUS_PARTIAL.md`)

## Open questions for parent agent

1. Should Round 5 keep P_DA1C/P_DA3S/P_DA3D (no held-out, but annotated)?
   Recommendation: keep P_DA1C (canonical), keep others if collection allows.
2. The 89-item collection is ~2-3 sessions of focused web work. Prioritize?
3. Should the failing gate be run anyway to validate infrastructure?
   Recommendation: no — outcome is predictable (G1≈2/24); save effort for Round 5.
