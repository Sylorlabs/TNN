# Shared Consequence Substrate: Build Record

## Variant

Base: frozen `sc_base.zag` (substrate_consolidation), SHA-256
a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd.
The base is used read-only; the variant is assembled by concatenation,
never by editing the base.

## Components

- `sb_base_nofn.zag`: base lines 1-794 + 836-1304 (excludes
  miss_inquire, ev_query, run_all, main).
- `sb_substrate.zag`: generic substrate machinery (sub_find, sub_get,
  sub_note, sub_consec, from consolidation) + new `sub_best_action`
  + `sb_resolve_aw` + `ev_observe_aw` + replacement `miss_inquire`
  (substrate policy read) + replacement `ev_query` (substrate
  withholding).
- `sb_driver.zag`: Experiment A (policy) + Experiment B (withhold).
- `sb_frozen_fns.zag`: frozen miss_inquire + ev_query (for Arm A).
- `sb_frozen_query.zag`: frozen ev_query only (for Arm B).
- `sb_dedup_fn.zag`: dedup gate miss_inquire (for Arm B).
- `sb_driver_w.zag`: withhold-only driver (for Arms A/B).

## Assembled binaries

- `sb_bin` (Arm C): sb_base_nofn + sb_substrate + sb_driver.
  Full unification test (policy + withholding in one binary).
- `armA_bin`: sb_base_nofn + sb_frozen_fns + sb_driver_w.
  Baseline (frozen behavior).
- `armB_bin`: sb_base_nofn + sb_frozen_query + sb_dedup_fn +
  sb_driver_w. Dedup only.
- `armA2k_bin`, `armB2k_bin`, `armC2k_bin`: 2-key versions for
  fair compute comparison (smaller scale to avoid trial slowdown).

## One-System Rule audit (build)

- New modes: 0.
- New bridges: 0.
- New handlers: 0.
- New semantic cases: 0.
- New node tag: 61 (storage only, reused from consolidation).
- New edge types: 0.
- Cognition source lines added: ~150 (substrate machinery reused
  from consolidation; new: sub_best_action, sb_resolve_aw,
  ev_observe_aw, replacement miss_inquire/ev_query).
- The substrate is infrastructure (keyed store), not a cognitive
  subsystem. Both behaviors are read rules on shared state.

## Toolchain

Pinned znc `src/tools/toolchain/znc_linux_x86_64_abed8aa1`.
Safebin PATH, no python. All builds deterministic.
