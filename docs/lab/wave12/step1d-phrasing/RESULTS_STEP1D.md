# Step 1d Results — Deterministic Phrasing Variation

**Date:** 2026-09-20  
**Branch:** `tnn-native-lab`  
**Preregistration:** `ac898c378d3f` (frozen inventory SHA-256 `d33aa44e3f7700755410076d8105145d75d7f3573b62deb9d293932adf822d8d`)  
**Step 1c+1d integration:** PENDING (explicitly out of scope)

## Verdict: GO

All four instruments pass their frozen kill bars. The phrasing function renders
verdicts into varied surface text deterministically: 100/100 oracle checks,
1600/1600 directional adaptivity hits, detector LAWFUL on the real mechanism
with both controls behaving as required, and null-vs-ArmC D=0.97 at p<0.001.

## Instrument 1 — Inventory certification: GO

- `CERTINV`: gate clean (0), blob hash matches frozen `d33aa44e…`, PASS.
- `CERTNEG` (poisoned inventory): 2 gate violations caught, PASS.
- Machinery size: `p1d_inv.zag` (259) + `p1d_phr.zag` (149) = **408 nonblank lines ≤ 500** ✓
- Static checks: no RNG/clocks/floats/threads in machinery; bare `@import`s;
  no slice `==`; all LCG seeds fixed; no time/urandom seeding.

## Instrument 2 — 100-episode trial: GO (no kill fired)

- Gate clean, inventory hash matches.
- Oracle: **100/100** checks pass (O1 subject, O2 verb, O3 reasons verbatim in
  order, O4 no forbidden token in fixed text, O5 template skeleton).
- Replay: **100/100** byte-identical.
- Distinct renderings per class: 20/20/20/20/20 (bar ≥3).
- `TRIAL,PASS,100,100`, exit 0.

**Honest note on O4.** The frozen verdict reasons themselves contain "no"/"not"
(e.g. PROMOTE "no counter-evidence survived elimination"). O3 requires them
verbatim, so O4 is scoped to the function's own fixed text (reason spans
masked) — exactly like template-cert T3 ("in fixed text"). Without this
scoping O4 would be unsatisfiable by construction. This is an interpretation,
not a prereg change: it is the only reading under which O3 and O4 coexist.

## Instrument 3 — Adaptivity metric: GO

**True law (corrected during build).** The phrasing function computes
`ti = phr_fold(state) % 5` (FNV hash, 5 templates), `depth = 1+(ep+store_n+promotes)%3`,
`rot = (ctx+kills+last_op)%3`. An early draft assumed `ti=(ep/150)%4`; the
trial oracle always used the hash form and the code was corrected before any
headline run. There is no mod-4/mod-3 rotation aliasing (rot is mod 3).

| Gate | Pilot (40) | Full (1600) | Novel G4 (600) |
|------|-----------|-------------|----------------|
| G0 replay | 0 mm | 0 mm | 0 mm |
| G1 directional hits | 40/40 | **1600/1600** | **600/600** |
| G1 99.5% CI lower | 1.00 | 1.00 (>0.50 ✓) | 1.00 (>0.50 ✓) |
| G2 protected-output | 0 viol | 0 viol | 0 viol |

**G3 (NMI, Miller–Madow corrected, 1000 permutation nulls):**

| Grid | n | Ks | Kc | NMI | null p99 | bar | Result |
|------|---|----|----|-----|----------|-----|--------|
| Main | 8000 | 64 | 45 | **0.62** | 0.007 | 0.30 | PASS |
| Novel | 4000 | 96 | 45 | **0.34** | 0.018 | 0.30 | PASS |

Bar = max(0.30, 5×null-p99). Both pass.

**G4 novel states:** S0 reached by real ops (160 kills on empty store, 215 adds,
5 promotes, ticks to ep=50000); 600 pair bases + 4000 grid states via short
lawful paths; range audit 0 violations (ep∈[50000,50200], store_n∈[200,230],
kills∈[150,170]). The 600 pairs were collected from a 720-candidate pool
because lawful preconditions filter; the 600-pair count is the preregistered
number. Composed edit E_EP+E_STORE (δ=+2, S%3==0) included.

**G2 interpretation (documented).** "Ledger bytes" = the 16-word audit entry.
The entry's decision words (all but a5=episode and d1=state-hash, which
legitimately track the state) are identical across each pair's endpoints;
verdict bytes, memop set, and refusal flag are identical. The phrasing function
receives a read-only verdict and cannot touch the ledger; the check verifies
the harness renders both arms consistently.

## Instrument 4 — Arbitrariness detector: GO

900 episodes/input; G1 (≥30 codes, min class ≥25); 300-fit/300-eval split;
predictors: best-constant, 6 bucketed projections, 15-NN, depth-3 decision
list, builder-nominated law. Winner by fit (nomin last, wins ties). G2 needs
lift ≥10pp and exact binomial p<0.01.

**Implementation correction.** The as-built G1 was backwards
(`dist≥4 && minc≥30`); fixed to the frozen `dist≥30 && minc≥25` before any
headline run. Input sampling is hash-aware: the real mechanism's `ti` is
hash-derived, so its 900 episodes use a deterministic balanced fill (36 bins:
ti∈{0..3}×depth×rot, 25 each; ti=4 excluded by sampling design).

| Mechanism | G0 | G1 (dist,min) | Winner (fit/eval) | Lift | p | Verdict |
|-----------|----|---------------|-------------------|------|---|---------|
| Positive (synthetic law) | 0 | 36,25 | nomin 300/300 | 97pp | <0.01 | **LAWFUL ×3** |
| Negative (hash-of-state) | 0 | 36,25 | bucket 29/10 | -1pp | n.s. | **ARBITR ×3** |
| Real phrasing fn | 0 | 36,25 | nomin 300/300 | 95pp | <0.01 | **LAWFUL ×3** |

Controls behave exactly as required (positive passes all three inputs;
negative killed by G2 on all three). The real function is non-arbitrary: its
surface code is a deterministic, nominable function of state.

## Instrument 5 — Null baseline: GO

- `NULLSELF`: 0 bad cells, 0 protection violations, PASS.
- `FREEZE` (200× identical state): 0 bad probes, PASS.
- `ARMC` (null-vs-ArmC, 40 probes × 10 trajs × 20 states):
  - D (mean cluster-count distance) = **0.9685**
  - Bootstrap: 0/1000 resamples ≤ 0 (p < 0.001)
  - Invariance violations: 0; protection violations: 0
  - `ARMC,PASS`

## Costs

- **Latency:** Arm C 0.94ms/render vs null 0.17ms/render (**5.4×**). Exceeds the
  1.5× cost target; absolute cost is sub-millisecond. Cost metric, not a kill bar.
- **Audit:** 64 bytes/episode both arms (one 16-word entry), ratio 1.00.
- **Determinism:** two full builds; all 12 evidence files byte-identical
  across builds (`ALL_RUNS_BYTE_IDENTICAL`).

## Execution-order honesty

Preregistration preceded code. Two deviations from strict plan order are
recorded: (1) an Arm C comparison ran on a stale binary before the kill trial
(discarded; rerun from fixed source above); (2) inventory/phrasing drafts
existed before the null/detector harnesses were written. No frozen bar, metric,
or kill criterion was changed after seeing results. The O4 scoping and G1
detector fix are interpretations/corrections documented above, not prereg
changes.

## Integration

**Step 1c+1d integration is PENDING.** The phrasing function is certified
standalone; wiring it into the Step 1c pipeline has not begun.

## Evidence

- Runner: `run_step1d.sh` (builds twice, runs battery, byte-compares)
- Evidence: `/tmp/step1d_evidence/run_A/` (12 files, byte-identical in run_B)
- Results: this file
