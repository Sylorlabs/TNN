# R-3 SENSITIVITY MAP — fork exhaustion (B-T2: ε × compression-ratio floor)

Fork-exhaustion crew · Track R0 · 2026-09-21
Harness: `fork_exhaustion.py` (deterministic arithmetic on frozen numbers; no RNG).
Raw cell data: `r3_raw.json`.

## Grid

- ε ∈ {0, 5, 10, 15, 25, 50}/1000 × ratio floor ∈ {1.000, 1.100, 1.150, 1.200, 1.300}
- Boundary forks: ε `≤` vs `<`; ratio `≥` vs `>`
- Structural forks: chunk conjunct `binary` (chunk<dual,raw) vs `margin` (raw−chunk > ε)
  vs `dropped` (no chunk conjunct — contradicts frozen prereg, tested anyway)

Measured (formal legs): leg0 Δ=0 ratio 1.417 chunk 550; leg1 Δ=0 ratio 1.195 chunk 250; raw 950 both.

## Map 1 — mismatches vs normative, base variant (≤, ≥, binary chunk)

Rows ε, columns ratio floor. 0 = matches every normative judgment.

| ε\floor | 1.000 | 1.100 | 1.150 | 1.200 | 1.300 |
|---|---|---|---|---|---|
| 0 | 2 | **0** | **0** | 1 | 1 |
| 5 | 2 | **0** | **0** | 1 | 1 |
| 10 | 2 | **0** | **0** | 1 | 1 |
| 15 | 2 | **0** | **0** | 1 | 1 |
| 25 | 2 | **0** | **0** | 1 | 1 |
| 50 | 3 | 1 | 1 | 2 | 2 |

Zero-mismatch region (inherited suite): ε ∈ {0,5,10,15,25} × floor ∈ {1.1, 1.15}.

## Knife-edges (which scenario kills which cell)

| Cell | Mismatching scenarios | Meaning |
|---|---|---|
| floor = 1.000 (any ε) | A1 degenerate dual-is-raw PASSES; A2 trivial 1.02 PASSES | Anti-degeneracy failure: the floor lets a verbatim store and a 2% compression through |
| floor ≥ 1.200 (any ε) | N1 leg-1 measured FAILS (1.195 < floor) | Rejects the pre-registered legitimate tighter-gate regime — a bug in the bar |
| ε = 50 (any floor) | A3 dual-30-worse (6-label miss) PASSES | Tolerates a 6-probe degradation — too lax |
| ε ≤ 15, floor ∈ {1.1,1.15} | 0 mismatches on inherited suite | Indistinguishable from ε=25 on inherited normatives |

## The ε fork that appeared: materiality-quantum alignment

The inherited suite cannot discriminate ε ∈ {0,5,10,15,25} (Δ=0 measured).
New probes:

| Probe | ε=0..15 | ε=25 | ε=50 |
|---|---|---|---|
| A9: dual 25/1000 worse (5-label miss) | FAIL | **PASS** | PASS |
| A3: dual 30/1000 worse (6-label miss) | FAIL | **FAIL** | PASS |

Independent grounding for A9→PASS / A3→FAIL as normative:
- R-3's own probe resolution: scores are g·1000/200 → 5/1000 per label; 25/1000 = 5 labels = "within a handful of labels" (debate-2 resolution note).
- R-4's independent derivation: 25/1000 = one average consistent span's occurrence budget = the battery's materiality quantum; a 30/1000 (6-probe) loss fails there too (T4b).
- With A9→PASS, A3→FAIL adopted as normative, **ε=25 is the unique zero-mismatch value** in the grid. Without them, the choice among {0,5,10,15,25} is disclosed judgment; the recommendation's 25 is the future-proof end of that interval and keeps the descriptive crew's unsigned ε.

## Boundary-semantics forks

| Variant | Cells with 0 mismatches | Finding |
|---|---|---|
| base (≤, ≥) | 10/30 | — |
| ε strict `<` | 0/30 | KILLED: A4 (dual exactly at ε) fails everywhere; at ε=0 even the measured legs (Δ=0) fail. `≤` is forced, not stylistic. |
| ratio strict `>` | 10/30 | Same zero-region as base. At floor=1.0 it rescues A1 (1000>1000 fails correctly) but A2 (1.02) still passes — the floor must still sit above ~1.02. Does not move the recommendation. |

## Structural forks

| Variant | Finding |
|---|---|
| chunk `margin` (raw−chunk > ε) | Inert on all evidence: measured deficits (400, 700) exceed every grid ε. Behaviorally distinct only for hypothetical small-deficit regimes (probe A10: chunk deficit 30). No cell changes. Kept binary per frozen bar text ("must lose" — no margin stated). |
| chunk conjunct dropped | 0/30 clean — KILLED: A5 (chunk=dual=raw) passes every cell, contradicting the frozen prereg's explicit chunk-rejection clause. Tested because Micah said test all forks; dead by prereg. |

## Headroom probe (1.1 vs 1.15 — the disclosed judgment)

| Future regime | floor 1.1 | floor 1.15 |
|---|---|---|
| ratio 1.10 (tighter gate than leg 1) | PASS | FAIL |
| ratio 1.125 | PASS | FAIL |

No normative verdict exists for unregistered future regimes — this is the
judgment call the swarm disclosed: 1.15 is the largest round number with
genuine (~4%) headroom below leg 1's 1.195 and a non-vacuous ≥13%-saving
claim; 1.1 (≈9.1% saving) remains the evidence-compatible fallback if Micah
wants more headroom against future re-derivations. The sweep cannot and does
not discriminate them; both are in the zero-mismatch region.

## Verdict on R-3

**CONFIRM.** (ε ≤ 25/1000, ratio ≥ 1.15, ≤/≥ boundaries, binary chunk
conjunct) sits inside the zero-mismatch region; ε=25 is uniquely picked out
once the cross-swarm materiality quantum (5 probes) is adopted as normative;
every neighboring fork is killed by a named scenario (A1/A2 → floor>1.02,
N1-leg1 → floor<1.2, A3 → ε<50, A4 → ≤ boundary, A5 → keep chunk conjunct).
No fork moves the recommendation.
