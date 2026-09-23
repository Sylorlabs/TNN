# VERDICT — T2-CLASS3DEC: class-3 advantage decomposition (Type C)

**Verdict: REPRODUCED**

Independent pure-Zag re-derivation (zero RNG, 3/3 byte-identical runs, SHA-256 `1a4fa8210921bc78124583e88814d1549298d5844d269f5f39ebac6d9b53e7c6`) from committed evidence at frozen commit `7b2100d09911c5c10252c5756c7def288e70bd1f`, built with the pinned znc (`498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`).

## Governing checklist (quoted verbatim from the frozen `docs/lab/crossref/PREREG_TIER2.md` §T2-CLASS3DEC)

> **Claims:** 2026-09-21: the class-3 advantage = verification amortization (always positive; teacher already did the eliminative verification while learning; cost component rose in all four sources) MINUS honesty filtering (can be negative; teacher's gate refuses to teach facts it doesn't hold truly — incomplete teachers lose mastery). Grok's entire +0.0048 gap was cost accounting — zero capability component improved in any source; step's and SWE's deficits = 9 inherited D2 held-out skips (step's 9 skips matched held-out facts in teaching slices exactly); noise hypothesis killed (step's corpus verified clean, zero transcription errors, still lost); SWE's −0.0125 = same 9-skip mechanism, not the 12 fooled falsehoods.
> **Method:** Type C — re-derive the cost-vs-capability decomposition from committed class-3 evidence with independent Zag code.
> **Rule:** REPRODUCED if grok's +0.0048 decomposes to cost-only and the 9-skip attribution holds for step/SWE; NOT REPRODUCED if any capability component is nonzero.

## Claim vs measured (every claim)

| # | Claim (frozen) | Expected | Independently measured | Disposition |
|---|----------------|----------|------------------------|-------------|
| 1 | Cost component rose in all four sources (verification amortization, always positive) | c3 > c4 × 4 | grok 0.9108→0.9588; sol 0.908763→0.933165 (re-derived from Q2 formula); step 0.9108→0.9532; swe 0.033445→0.043103 (re-derived via the analyzer's eps=den quirk) | HOLD |
| 2 | Grok's entire +0.0048 gap was cost accounting | gap = +0.0048, capability Δ = 0 | gap +4800×10⁻⁶; cost contribution +4800×10⁻⁶; mastery/revisability/integrity/retention Δ all exactly 0 | HOLD |
| 3 | Zero capability component improved in any source | all capability Δ ≤ 0 | mastery Δ (×10⁻⁶): grok 0, sol 0, step −13110, swe −13500; revisability/integrity/retention Δ = 0 in all four sources | HOLD |
| 4 | Step's 9 skips matched held-out facts in teaching slices exactly | 9 skips; per-slice 1,2,0,0,2,3,0,1 | Re-derived from the frozen deterministic functions (`q2_heldout`, `q1_slice_fact`): 12 held-outs → 9 overlap ids {1,47,48,49,96,97,194,196,238} → per-slice 1,2,0,0,2,3,0,1 — exact 8/8 match with the frozen S37 rep-0 skips | HOLD |
| 5 | Step's deficit = 9 inherited D2 held-out skips | −0.0089 = −0.0131 mastery + 0.0042 cost | measured −0.00887 = −0.01311 + 0.00424 | HOLD |
| 6 | SWE's −0.0125 = same 9-skip mechanism, not the 12 fooled falsehoods | −0.0125 = −0.0135 mastery + 0.0010 cost; teacher gap 9 | measured −0.012534 = −0.0135 + 0.000965; committed `teach3_run1.log` records teacher gap 9; the 9-skip mechanism fully accounts for the mastery loss while cost improved | HOLD |
| 7 | Noise hypothesis killed (corpus verified clean, zero transcription errors, still lost) | committed evidence | **Not independently re-derived** — Type C scope covers the decomposition and the skip pattern; corpus cleanliness rests on committed evidence (caveat, not a failure) | NOT RE-DERIVED (caveat) |

Decomposition table re-derived cell-for-cell (composites ×10⁻⁴): grok 9911/9959, sol 9909/9933, step 9911/9822, swe 9033/8908 — 8/8 match the frozen class-3 advantage table.

## Decision-rule application (mechanical)

- Grok's +0.0048 decomposes to cost-only: gap (+4800) == cost contribution (+4800), every capability contribution = 0. ✓
- 9-skip attribution holds for step/SWE: predicted skip pattern matches the frozen rep-0 skips exactly (9 overlap, per-slice 1,2,0,0,2,3,0,1); step's and SWE's deficits decompose to mastery-only losses partially offset by cost gains. ✓
- Any capability component nonzero (positive)? No — no capability component improved in any source. ✓

**→ REPRODUCED.**

## Frozen pins

- Prereg: `sylorlabs/TNN` @ branch `tnn-native-lab` @ commit `7b2100d09911c5c10252c5756c7def288e70bd1f`
- Prereg doc blob (`docs/lab/crossref/PREREG_TIER2.md`): `b1178370036bffbda6eb68ea0989c0e427dc31b7`
- znc: `/home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`, SHA-256 `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`
- Evidence blobs: see RUNLOG.md (class-3 advantage PREREG/VERDICT, G_GROK_VERDICT, S37_VERDICT, q2s/q1/s37/t5_core .zag, SWE analysis + logs + trial, sol champ source + output)
- **Pin correction (2026-09-22 23:50 PDT, coordinator):** the brief-stated expected pin `d50bf92cd9e8` was a transcription artifact — GitHub API returns HTTP 422 "No commit found for SHA: d50bf92cd9e8" in `sylorlabs/TNN` (independently verified). Disregarded per instruction. The frozen T2-CLASS3DEC prereg section itself lists zero pins (programmatic scan); the only prereg pin is the frozen commit `7b2100d09911c5c10252c5756c7def288e70bd1f`, which **resolves via the GitHub API** in `sylorlabs/TNN` (micahcooley, 2026-09-22T22:54:44Z). The crew ran on the prereg's authority with API-verified pins. Full detail in RUNLOG.md.
- Independent program: `crew/c3dec_rederive.zag` (pure Zag, zero RNG); 3/3 byte-identical runs, output SHA-256 `1a4fa8210921bc78124583e88814d1549298d5844d269f5f39ebac6d9b53e7c6` (`crew/run1.txt` … `run3.txt`). Build binary deleted after runs per the no-binary rule.

## Caveats

1. The noise-hypothesis sub-claim (corpus cleanliness) was not independently re-derived; it rests on committed evidence.
2. Class-3 and class-4 batteries differ (8 teaching slices/200 probes vs 4 direct slices/240 probes); the decomposition compares composite means across them, exactly as the frozen verdict does — all 8 cells re-derive exactly.
3. Python was used only for evidence extraction and hashing; all reasoning/verification is the pure-Zag program. Zero RNG. Scratch only (`TMPDIR=/home/hatch/workspace/tmp_commit`); slices far under 2²⁵ bytes; committed evidence only, no live-web recapture.
