# CURATED ENGLISH VERDICT — pure-Muse curation crew (2026-09-21)

**Question:** Does the curated corpus (232 adopted / 8 withheld, pure-Muse native curation, zero API calls) beat the best separate source (0.9911)?

**Answer: TIE at 0.9911.** The curated corpus matches the best separate source on every metric while teaching 8 fewer contested facts. The withholds did not move the composite needle — explained in §5.

## 1. Curation summary

| item | value |
|---|---|
| Method | Native Muse subagent deliberation; unanimous cross-source agreement on teach value (obs/probe/dump) + mechanical validity + claim-envelope match → adopt; any substantive disagreement/defect → withhold+audit |
| Sources (5, SHAs verified) | gpt-5.6-sol `41aa8f5b…`, grok-4.6 `7f3a2573…`, step-3.7-flash:free `c52e4f52d…`, swe-1-6-slow:free `ca1e7b85…`, Muse-native `1d5c2ede…` |
| Adopted | **232 / 240** |
| Withheld | **8 / 240**: ids 4, 88, 89, 90, 91, 92, 93, 94 |
| Native false-claim flags (audit only) | **12/12 planted falsehoods flagged, 0 false positives, 0 misses** |
| Curated corpus SHA-256 | `6fbbfdb6c87d419de69921f9a0f709b908024f9e0bed7c15fc9671517e67ac62` |
| API/model calls during curation | **0** |

### Withhold reasons (all FACT DISAGREEMENT, documented in CURATION_AUDIT.md)

| id | reason |
|---|---|
| 4 | step dump says 4; other four sources + supplied claim say 5 |
| 88–94 | grok dump values disagree with the other four sources + supplied claims |

Withheld rows carry dead numeric lanes (0); teaching legs skip them via `muse_withheld_at` and never read the lanes.

### Distractor selection (deterministic, mechanical)

The frozen prompt asks each teacher for a different plausible distractor, so distractors may differ by design. Selection: majority vote among mechanically healthy distractors; ties → nearest to observation, then lowest. One repair: id 185 sol `distract_value=64` == observation 64 (defective) → excluded; tie 60/63/66/81 → nearest-to-observation selects **63** (step).

## 2. Class 4 — legA Track-5 M2 composite

Battery: `bind M2 4 rep 1` × 12 reps, `btrap M2 4 rep` × 12 reps, `bind M2 4 0 10` (S10). 25 logs × 5 runs, byte-identical. Curriculum 48/48/48/96.

| metric | curated (mean, 12 reps) | best source | delta |
|---|---|---|---|
| mastery (D1 40 + D2 + D3 120) | 1.0000 | 1.0000 | 0 |
| revisability (rf 12/12, rg 20/20) | 1.0000 | 1.0000 | 0 |
| integrity (7 trap fams + hallu + k1/k2 + refusal) | 1.0000 | 1.0000 | 0 |
| retention | 1.0000 | 1.0000 | 0 |
| cost (esc=0, ops=279, eps=287) | 0.9114 | 0.9113 | +0.0001 |
| **composite (30/25/25/10/10)** | **0.9911** | **0.9911** | **0** |

- Integrity gate: **PASS 12/12**.
- Corpus-replay cross-checks: **24/24 pass**.
- S10 no-degradation: **PASS** (S10 mastery 1.0000 = S1 1.0000; d1 40/40, d2 36/36, d3 120/120 at scale 10).
- D2 battery: 36/36 (36 valid landmarks after withheld exclusions; denominator adjusts).

## 3. Class 4 §B.7 — legB direct (teacher ID 63)

`MUSEB_RUN,96,8,0` → **96/96 flaw hits, 8/8 slices pass, 0 fails**. All slices 12/12 hits, 0 leaks, tripwire silent. N=5 byte-identical.

Teaching: 232/232 episodes, 232/232 slots (8 withheld skipped, verified by `mb_taught_slots`).

## 4. Class 3 — legC teacher leg (teacher ID 62)

`MUSEC_RUN,96,8,160,192,0` → flaw hits **96/96** (8/8 slices pass), 160 clean adopted, final mastery **192/192**, 0 fails. N=5 byte-identical.

- Teacher: 232/232 episodes, holds full 192-fact curriculum (0 missing).
- **LegB/legC teaching digests agree byte-for-byte** (`662b684f…`): the D2 teaching route reproduces the identical state in both legs.

## 5. Why the withholds did not move the needle

The composite is **identical** (0.9911 vs 0.9911). The 8 withholds changed no metric. Three reasons:

1. **Metrics are curriculum-relative.** D1/D2/D3, the R-set, the trap batteries, and the Q1 probe universe all draw from the *adopted* set. Withheld ids are excluded from every probe universe (common 216→208, pool 186→179, Q1_PROBE_N 228→220, D2 landmarks). An untaught id can never score wrong because it is never probed.

2. **The adopted 232 are unanimous and learned perfectly.** All five sources agree on obs/probe/dump for every adopted id; the learner's eliminative verification passes everywhere (trial `withheld` metric = 0 verify-failures on all reps). There is no "hard" adopted fact whose removal would have helped.

3. **Cost is per-episode normalized.** 8 fewer teaches per rep (220 vs 228) reduces ops (279 vs 287) and eps (287 vs 295) proportionally; cost moves only 0.9113→0.9114 (+0.0001), which does not survive the 30/25/25/10/10 weighting.

The curation's value is **hygiene, not score**: the 8 contested facts (where the sources genuinely disagree on the teach value) are not taught, per the agree-before-add rule. The test proves this hygiene is **free** — zero metric cost for refusing to teach contested facts.

## 6. Static gates

| gate | result |
|---|---|
| No-RNG scan (`norng_scan.py`) | **PASS** over 42 compiled `.zag` sources (0 violations; 1 dead-reference-only note, same as source boxes) |
| Determinism | N=5 byte-identical runs per leg (legA: 25 logs × 5; legB, legC: full stdout × 5) |
| Corpus SHA attested | `6fbbfdb6…` in every log; analyzer asserts model `curated-english` |
| Teacher IDs | Direct probe 63, teacher leg 62 (exhaustively audited; no stale 53/43) |

## 7. Evidence inventory

| artifact | path / SHA |
|---|---|
| Curated corpus | `curated/curated_corpus.json` — sha256 `6fbbfdb6c87d419de69921f9a0f709b908024f9e0bed7c15fc9671517e67ac62` |
| Curation audit | `curated/CURATION_AUDIT.md` (all 8 withholds, 5-source values, distractor selection, 232 adopted IDs) |
| Native flags | `curated/native_flags.json` (12/12, reasons) |
| Test tree | `curated/tnn/` (legs A/B/C, shared) |
| LegA logs (25) | `curated/tnn/legA/evidence/logs/` + SHA256SUMS.txt |
| LegB log | `curated/tnn/legB/evidence/logs/museb_direct.log` |
| LegC log | `curated/tnn/legC/evidence/logs/musec_teacher.log` |
| LegA analysis | `curated/tnn/legA/analysis/analyze_m2.py` → `leg-A analysis OK` |

## 8. Implementation notes (withheld machinery, first live exercise)

The source boxes defined `muse_withheld_at` but never exercised it (`MUSE_WITHHELD_N=0`). This box is the first with nonzero withholds. Changes, all mirrored trial↔analysis:

- Teaching loops skip `muse_withheld_at(id)==1` (legA `q2_phase1`, shared `muse_t_phase1`); teach-one fns guard defensively.
- Set geometry: pool 186→179, common 216→208, Q1 probe universe 228→220; D2 `q2_lm_valid` excludes withheld landmarks/rulers.
- Seeds unchanged (withheld seed 90 stays a seed; seeds only carve the held-out pool).
- LegB/legC episode checks 240→232; added taught-slots checks (232/232).
- Phase-0 D1 planting skips withheld (never plants dead 0s).

## Verdict

| item | curated | best source | delta |
|---|---|---|---|
| class-4 Track-5 composite | 0.9911 | 0.9911 | 0 |
| class-4 §B.7 (direct, tid 63) | 96/96 | 96/96 | 0 |
| class-3 §B.7 (teacher, tid 62) | 96/96 | 96/96 | 0 |
| class-3 mastery | 192/192 | 192/192 | 0 |
| S10 no-degradation | PASS | PASS | — |
| no-RNG scan | PASS | PASS | — |

**The pure-Muse curation crew works.** 232/240 adopted by unanimous agreement, 8 contested facts withheld with full audit, 12/12 native falsehood flags, and the curated corpus **ties the best separate source at 0.9911** — proving that agree-before-add hygiene costs nothing on the metrics.
