# Continuity Round 2 — Results (2026-09-22)

**Prereg:** `imagination_discovery/aud/continuity_round2/PREREG_ROUND2.md`
(frozen, commit `9d1dbf865e36ff3bd13a66c696af60e08fc94d95`).
**Toolchain:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
**Renders:** 2026-09-22. Pure Zag, zero RNG, deterministic state throughout.

## Verdict table

| Hypothesis | Renders | Machine result | Ear status |
|---|---|---|---|
| sol-H1 — 10 ms natural-envelope dips (B-β kids) | 60 | **SURVIVES** (max dip run 990 ms; kill needed ≤10 ms) | **PENDING MICAH** — blind A/B ×3, `ear/h1/` |
| sol-H2 — bridge_world source/room/texture seams (B-γ kids) | 60 | **SURVIVES** (weak: 3/4 medians favor kill; modchange 0.87>0.75 blocks it, p=0.40 n.s.) | **PENDING MICAH** — blind A/B ×3, `ear/h2/` |
| sol-H3 — spatially frozen long-scene world beds (B-γ 5 min) | 24 | **SURVIVES** (no Holm-significant arrangement effect; 60/60 bridge-midpoint floors 0.35–1.57× kids median, kill needed ≥3×) | **PENDING MICAH** — blind A/B/X ×2, `ear/h3/` |
| grok46-G1 — world-bed uniformity under distribution shift | 3 | **SURVIVES** (min boundary-floor ratio 0.12 < 2.4) | machine-only per prereg |
| grok46-G2 — accumulated multi-minute scoring drift | 3 | **SURVIVES** (min boundary-floor ratio 1.19 < 2.7) | machine-only per prereg |
| grok46-G3 — bridge_world authoring seams under density stress | 6 | **INDETERMINATE** (median 125 ms corr 0.303; neither bar met) | machine-only per prereg |

No v4 clips created: H1/H2 v4 decisions await Micah's ear (his ears outrank
metrics). G1/G2/G3 implicate test scores, not flagships.

---

## sol-H1 — 10 ms natural-envelope dips

**Method (frozen §H1):** 20 kids seeds × {normal, permuted, bed-only}. 1 ms RMS
envelope; dip = runs below scene-relative floor. Kill: no normal/permuted dip
run >10 ms AND boundary/overlap dip rates not greater than within-phrase rates.

**Machine result: SURVIVES** (both normal and permuted). Long dip runs exist
everywhere — within phrases, at boundaries, and in overlaps. The boundary-
concentration prediction is contradicted (boundary rates ≤ within rates), but
the kill's hard 10 ms ceiling is exceeded by two orders of magnitude.

Normal (n=20): median within 15.00, boundary 10.25, overlap 9.47 dips/min;
sign test boundary>within 7/20 p=0.9423; overlap>within 8/20 p=0.8684;
max dip run 990 ms. Permuted: median within 14.81, boundary 8.00, overlap 9.35;
same sign tests; max dip run 990 ms. Bed-only descriptive: within 11.21,
boundary 6.00 dips/min; longest bed-only run 280 ms.

Example (k18 normal): 9.13–9.45 s = 320 ms run; 28.87–29.86 s = 990 ms run
(both classified overlap).

**Determinism:** 3/3 byte-identical — 120 rep-renders (r2+r3), 0 mismatches.

**Ear check (PENDING MICAH):** `ear/h1/` — 3 blinded A/B pairs (k18, k13, k11),
normal vs bed-only. Question: "Which clip CUTS OUT vs FLOWS?" Key sealed.

---

## sol-H2 — bridge_world source/room/texture seams

**Method (frozen §H2):** 30 scenes × {standard, control}, 10 nominal bridge
edges each. Edge signature = {1 ms RMS slope, 1 ms spectral flux, 50 ms
spectral distance, 2–20 Hz modulation-centroid change} in ±1 s flanks.
Control edges = the 10 instants the standard scores as ordinary transitions
(same foreground, no bridge). Each bridge edge matched to the loudness-nearest
ordinary transition (±1.5 dB, 10–20 s away). One-sided Mann–Whitney U, bridge >
ordinary.

**Matching:** 299/300 bridge edges matched (scene 15: 9/10 — no ordinary
transition within ±1.5 dB for one edge; documented, not imputed).

**Machine result: SURVIVES.**

| measure | n_br | n_ord | med_br | med_ord | p (one-sided) |
|---|---|---|---|---|---|
| 1 ms slope | 300 | 299 | 0.0912 | 0.0967 | 0.9831 n.s. |
| spectral flux | 300 | 299 | 13.57 | 14.82 | 1.0000 n.s. |
| 50 ms spec distance | 270 | 299 | 8.68 | 9.33 | 0.9995 n.s. |
| modulation change | 270 | 290 | 0.8737 | 0.7513 | 0.4042 n.s. |

No measure significant in the predicted direction. Kill additionally required
every bridge median ≤ ordinary median; modulation change violates it (0.87 >
0.75, n.s.). Control nominal edges are descriptively indistinguishable from
standard (slope 0.1119 vs 0.0912; flux 12.59 vs 13.57).

**Interpretation:** bridge edges are, if anything, *smoother* than ordinary
foreground-event transitions on 3/4 measures. The machine cannot kill only
because of one non-significant median running the wrong way — a weak survival.

**Determinism:** sampled 3/3 (s1/s15/s30 × b0/b1 × r2/r3), byte-identical.

**Ear check (PENDING MICAH):** `ear/h2/` — 3 blinded A/B pairs, bridge-edge
excerpt vs loudness-matched ordinary-transition excerpt (2 s, centered).
Pairs chosen for largest machine-measured seam signature (s5 14.4 s entry,
s30 24.8 s entry, s2 26.8 s exit). Question: "Which excerpt has the
discontinuity?" Key sealed.

---

## sol-H3 — spatially frozen long-scene world beds

**Method (frozen §H3):** 3 world families (familiar kids / dense kids / novel
dream) × 4 seeds × {standard, control}; 5 min scenes, 10 bridge instants each.
Standard vs control differ only in bed grain selection (salt+700000). Measures:
1 s spectral novelty, 10 s novelty, 60 s self-similarity, event-conditioned
200–800 Hz bed response. Paired Wilcoxon + Holm. Kill: no significant
predicted effect AND all 60 standard bridge-midpoint 10 ms floors ≥3× the B-γ
kids median (0.0418).

**Validation:** all 12 pairs — foreground (non-bed-class) placements outside
bridge spans identical across conditions (True 12/12); bed placement logs
present 12/12.

**Machine result: SURVIVES.**

| measure | median std−ctl | p (one-sided, predicted) |
|---|---|---|
| 1 s novelty (std>ctl) | +0.089 | 0.979 n.s. |
| 10 s novelty (std>ctl) | +0.334 | 0.992 n.s. |
| 60 s self-similarity (std>ctl) | +0.0003 | 0.259 n.s. |
| bed response (std<ctl) | −0.0013 | 0.259 n.s. |

Holm-corrected significant: none. All 60 standard bridge-midpoint floors run
0.35–1.57× the kids median (kill needed ≥3×) → kill fails on floors alone.

**Limitation / deviation (material):** the ocean corpus contains only 19 wash
+ 21 wind grains, so the salt+700000 control reuses 95–100% of the standard
bed's source grains in a different order/timing. The prereg's post-hoc
source-id nonadjacency check is unachievable with this corpus. The standard-
vs-control comparison therefore tests bed *arrangement*, not bed *material*.
Mechanism followed the frozen spec exactly; the corpus-size assumption did not
hold. Reported here, not silently adjusted.

**Determinism:** sampled 3/3 (c0_i0 × d0/d1 × r2/r3), byte-identical.

**Ear check (PENDING MICAH):** `ear/h3/` — 2 blinded A/B/X trials, 60 s
excerpts (1:00–2:00), familiar vs novel world. Questions: "Which world feels
ALIVE vs STAGED?" and "Is X A or B?" Key sealed.

---

## grok46-G1 — world-bed uniformity under distribution shift

Ocean world-first composition (3 runs, byte-identical). 200–800 Hz 10 ms RMS
boundary floors at the 4 bridge exits vs B-γ kids v3 median 0.0418:
floors 0.0051/0.0275/0.0449/0.0212 → ratios 0.12/0.66/1.07/0.51.
**SURVIVES** (min 0.12 < 2.4). The ocean bed dips at bridge exits (2.4 s:
0.66×; 26.8 s: 0.51×) — same family of dip as H1/H3.

## grok46-G2 — accumulated multi-minute scoring drift

B-α v2 control 0–1 kHz 1 ms 5th-percentile floor: 0.00173. long180 180 s
ambient score, 7 bridge boundaries: floors
0.0024/0.0037/0.0021/0.0038/0.0074/0.0040/0.0034 →
ratios 1.38/2.15/1.19/2.18/4.27/2.33/1.99.
**SURVIVES** (min 1.19 < 2.7). No monotonic drift; the minimum sits at a
bridge boundary.

## grok46-G3 — bridge_world authoring seams under density stress

Full (bridges) vs ablation (event-only) × 3 seeds, byte-identical runs.
125 ms windowed correlations: 0.607/0.702/0.271/0.303/0.008 → median 0.303.
Full/control floor ratios: 24.17/39.08/11.66/23.79/11.51;
ablation: 16.37/34.03/17.21/18.75/23.75.
**INDETERMINATE** — neither the survive bar (median corr <0.2) nor the kill
bar (≥0.5 AND full floors ≥2× ablation at every instant) is met. The bridge
authoring changes the signal substantially (corr 0.303) but not separably
from the event-only ablation on floors.

---

## Determinism summary

| battery | reruns | result |
|---|---|---|
| H1 (60) | r2+r3 = 120 | 120/120 byte-identical, 0 mismatches |
| H2 (60) | sample s1/s15/s30 × b0/b1 × r2/r3 = 12 | byte-identical |
| H3 (24) | sample c0_i0 × d0/d1 × r2/r3 = 4 | byte-identical |
| G1/G2/G3 | 3/3 each | byte-identical |

## A-NATIVE diagnostics

R2G deliverables: peaks ≈0.67–0.68, DC ≈ 0, healthy zero-crossing rates. H1
ear clips: peak 0.708, DC −0.00003…−0.00024, low HF energy. No static/hiss in
diagnostics. Micah's ears remain authoritative (H1/H2/H3 pending).

## Ear packages (all PENDING MICAH)

- `ear/h1/BRIEF_H1.md` + `KEY_H1.sealed.txt` — "Which clip CUTS OUT vs FLOWS?"
- `ear/h2/BRIEF_H2.md` + `KEY_H2.sealed.txt` — "Which excerpt has the discontinuity?"
- `ear/h3/BRIEF_H3.md` + `KEY_H3.sealed.txt` — "Which world feels ALIVE vs STAGED?" + "Is X A or B?"
- "No difference" is valid in all briefs. Keys sealed; do not open before judging.

## v4 decision

No v4 clips created in this round. H1/H2 implicate flagship clips (B-β kids,
B-γ kids) but per standing rule Micah's ears outrank metrics — v4 awaits his
verdicts. H3/G1/G2/G3 implicate test scores, not flagships. If his ear confirms
a defect, the fix is a world-first recomposition of only the implicated clip.

## Lineage

- Frozen prereg: `9d1dbf865e36ff3bd13a66c696af60e08fc94d95`
- Baselines: B-γ kids v3
  `18cb055571a8a595fa8f080adbf613188407a3c4f2815dd2e1ce41befc54eb8f`;
  B-β kids v3
  `94349376a35bd7dbc5d31ab5173c309243f19293680a91399674de22082baecb`
- Harness: `continuity_round2/work/r2g/r2g.zag` (+ `work/r2_scores.zag`,
  `work/patch_r2g*.py`); `continuity_round2/work/r2b/` (B-β)
- Analyses: `work/analyze_{common,h1,h2,h3,gx}.py`; raw outputs
  `work/{h1,h2,h3,gx}_results.txt`
