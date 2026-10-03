# VERDICT SHEET — R0 crew CORE: native Zag reimplementation of the R31 dual-route endogenous chunker

**Date:** 2026-09-21
**Track:** R0 (PREREG_FREEZE.md §2, FROZEN 2026-09-21, Micah signed)
**Scope:** core mechanism only (ChunkBank / segment / split-merge / support-gap /
dual route / two parameter legs / module API). The five R0 batteries
(tournament, ablation, dose, dynamics-at-scale, support-gap battery) are
battery-crew scope and are NOT claimed here.

## Verdict: CORE BUILT — M8 smoke PASS, ready for battery crews

## What was built

`docs/lab/units/r0/impl/core/` (local: `~/workspace/tnn-lab/units/r0/impl/core/`):

- **`r0_core.zag`** (~700 lines, pure Zag, zero RNG) — the reimplementation:
  1. **ChunkBank**: `r0_observe_span` enumerates spans 2..8 at every position
     (R-2 L_max≤8), FNV-1a hash, counts, 4-bin grounded-consequence label
     histograms (R-1: bit0 recall success, bit1 discrimination consistency),
     saturating continuation-diversity. `r0_promote` applies
     seen≥S AND purity≥P AND utility>0 with
     `utility = gain*0.02 + max(0,purity−0.2)*log1p(seen)*len` in i32
     fixed point (scale 1000); `gain=(n−1)*seen−(n+3)` **verbatim** from the
     recovered spec; compression term **capped** (1000/500) per the R-2
     anti-giant-span-exploit clause. 700/1024-chunk caps; candidates ranked
     by utility, stored longest-first; IDs never reused.
  2. **Segment**: greedy longest-match (ties → lowest ID); unmatched bytes →
     single-byte literal fallback, negative IDs (`-1-byte`); `r0_reconstruct`
     gives exact round-trip (loud −1 on unknown ID — K-R5).
  3. **Split/merge** (ledger-audited): `r0_maybe_split` fires iff use≥3 AND
     conflict≥learned_conflict AND utility≤learned_utility_floor (splits at
     len/2; halves utility/labels to children); `r0_maybe_merge` fires iff
     pair_seen≥learned_pair_seen AND joint_gain−separate_regret≥learned_gain
     (len≤8). Parent IDs tombstoned with successor recorded; bytes retained.
  4. **Support-gap recruitment**: greedy coverage, largest unsupported raw
     span recruited iff support≥learned_min_support AND beats runner-up by
     learned_margin, else **abstain (−1)** with ledger reason code.
  5. **Dual route**: `r0_dual_score` / `r0_dual_trust_update` port the
     recovered trust-weight machinery; weights move only on delayed
     downstream evidence; the raw route is always queryable — chunking never
     erases evidence.
  6. **Stable IDs**: monotonic issuance, tombstone-with-lineage revision,
     `r0_tombstone_ratio1000` for the K-R3 bar. Ghost IDs impossible by
     construction (every issued ID resolves to retained bytes).
  7. **Two legs, one binary, argv-selected** (R-7/R-8): leg 0 recovered
     parameters (seen≥5, purity≥0.34 majority-label, 700 cap, …); leg 1
     re-derived (seen≥6, purity≥0.40 joint-success, compression cap 0.5,
     1024 cap, stricter learned thresholds).
  8. **API** documented in `API.md` (signatures, ID semantics, ledger op
     codes, determinism notes).
- **`r0_smoke.zag`** — M8 smoke driver: deterministic corpus
  (repeated text-like + code-like + noise), online smoke-grade grounded
  labels, promote → segment → round-trip assert → constructed split / merge /
  recruit / abstain demos → dual-trust shift; prints canonical summary +
  ledger hash chain.
- **`run_smoke.sh`** — builds once, runs perturb modes 0..4 per leg (N=5),
  diffs normalized stdout; any diff or stderr = FAIL.

## M8 smoke result: PASS

```
M8_SMOKE_PASS   (5 perturbation modes × 2 legs, byte-identical per leg;
                 perturb=0 rerun also identical; zero stderr)
```

Observed behavior (canonical run, leg 0): 3,136 spans observed → 224 chunks
promoted → 113 units segmented → ROUNDTRIP 1; split fired (parent successor
recorded); merge fired (pair_seen=8, joint_gain 900); recruit fired on the
unsupported span; abstain (−1) on the fully-covered stream; trust weights
shifted 1000/1000 → 1100/1500 under delayed evidence; tombstone/live = 0.75
(K-R3 bar is < 2). Leg 1 (re-derived) promotes only 6 chunks — the stricter
bars bite as designed; all dynamics still fire.

Determinism basis: FNV-1a over bytes only (never pointers); insertion-ordered
proposal scan; promotion ties broken by (len desc, hash asc); segment ties by
lowest ID; arena explicitly zeroed at init; no clock/RNG/allocator-state
reads. Perturbation modes: pre-fragmentation, free-list reversal, large
transient heap pressure, mid-run churn.

## Replication-fidelity notes (for the battery crews)

- Ordering bars B-T1…B-T5 are **battery scope**, not claimed here. The core
  supplies the mechanism the batteries measure.
- The old tournament's giant-span exploit is barred in-core: L_max=8 plus
  the compression-term cap (grounding dominates — e.g. a max-frequency
  8-span's compression term is capped at 1.0/0.5 while its grounded term is
  ~10 at the purity bar).
- Smoke-grade grounded labels (re-encountered ⇒ bit0; varying continuation
  ⇒ bit1) are a documented stand-in. The battery harness owns the full R-1
  probe-episode protocol (recall success + downstream discrimination
  consistency per span occurrence).

## Frozen-bar ambiguities — FLAGGED, not reinterpreted

1. **A-3 opcode unification**: prereg says "unify to ONE scheme (scheme choice
   is Micah's)". No explicit scheme value was frozen, so R0 adopted crew-1's
   `CUT_*=0xC0…` vocabulary (the arm-D flagship scheme this track feeds) plus
   documented R0 extensions `0xC9–0xCC`. If the coordinator unifies
   differently, the op-code table in `API.md` is remapped by amendment.
2. **A-4 chunk ID width**: prereg allows per-arm explicit mapping; R0 uses
   monotonic u32 (i32) issuance, never reused — documented in `API.md`.
3. **Split point**: the recovered spec takes `split_at` as a parameter; R0's
   policy wrapper `r0_maybe_split` uses len/2 deterministically (documented).
   Battery crews may call `r0_split_at` with an explicit offset.
4. **Learned-threshold initial values** (learned_conflict 400/500,
   learned_pair_seen 3/4, learned_gain 0/500, min_support 3/4, margin 2/3)
   are judgment calls placed in the two legs per RULE-2 (test both), with
   deterministic audited adaptation via `r0_learn_thresholds` (emits
   `R0_OP_THRESH`).
5. **Predictive-surprise cut signal** (82nd percentile, 256-entry inventory,
   R-8) is **battery scope** (tournament arm), not core scope — the core
   exposes the bank the signal recruits into. Flagged so it isn't lost.

## Commits

- `r0_core.zag` + `API.md` → `eeb3fe890a5a` (parent `5e68b184e149`)
- `r0_smoke.zag` + `run_smoke.sh` + `SMOKE_EVIDENCE.txt` → `dd4a4c8156b1` (parent `8d5abded004a`)
- this verdict sheet → commit below

(all on `tnn-native-lab`, under `docs/lab/units/r0/impl/core/`; no binaries,
no `.zagd`/`.zag-cache` committed)
