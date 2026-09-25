# BUILD_HYB.md — Math R2 engine (a) HYB: build notes

## What was built

`hyb.zag` + `common/` implement the HYB engine (SPEC_HYB.md): ONE's
deterministic BFS match-and-bind derivation runs verbatim; an integrated
derivation-event ledger records every step's inference licenses; after
derivation the referee weighs each contradictory pair H / not(H) by
premise quality (learned license trust), derivation depth, corroboration
(premise-disjoint paths), and premise-disjoint independence. Strictly
better wins; the loser is marked `REFUTED-BY-WEIGHING` (kept visible);
ties withhold only that claim. Trust starts uniform (1000) and is learned
from lost weighings; nothing is hardcoded.

## Source layout (all under `round2/engines/hyb/`)

- `hyb.zag` — engine driver: `hyb_run` (mirrors ONE's run phases),
  `hyb_emit` (ONE's output + `TRUST:`, `WEIGHINGS:`, weighing marks),
  `main` (sealed guard, 3x in-process reruns, divergence check).
- `common/cx_str.zag`, `cx_claim.zag`, `cx_match.zag`, `cx_store.zag`,
  `cx_schemas.zag`, `cx_io.zag` — **byte-identical copies** of the round-1
  sources. `cxs_*` derivation semantics are untouched.
- `common/cx_ev.zag` (new) — derivation-event ledger (`CXRE`), PBC
  subproof snapshots (`CXRS`), contradiction records. Additive: it calls
  the verbatim `cxs_add`, then records.
- `common/cx_fwd.zag` — round-1 forward core + surgical deltas:
  `one_mp/one_ui/one_pbc_direct/one_bfs` take the ledger and log licensed
  events via `cxr_add`; `one_pbc_for` replaced by `hyb_pbc_for`
  (snapshots the subproof's `false`-paths before truncation, adds the
  discharged claim with ONE's exact audit text, logs a synthetic event).
  Match-and-bind logic, BFS order, and audit strings are unchanged.
- `common/cx_hyb.zag` (new) — referee: trust ledger (`HYBL`), memoized
  derivation-path walks (`HYBM`), evidence scoring, contrastive weighing.
- `one_baseline.zag` — verbatim round-1 `one.zag`, kept for
  derivation-identity diffing (not part of the engine).
- `vendor/` — byte-identical copies of the two self-contained harness
  sources (`R33_NATIVE_IO_V1.zag`, `dlb_util.zag`); see item 7 above.
- `SCHEMA_TRUST.md` — frozen trust/scoring arithmetic and provenance.
- `BUILD_HYB.md` — this file.

## Toolchain

Pinned compiler: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.

```
cd ~/workspace/tnn-lab/math_logic/round2/engines/hyb
znc_linux_x86_64_abed8aa1 hyb.zag --no-zagd --no-analyze \
    --no-foreground-cache -o /tmp/hyb_build/hyb_bin
```

No binaries, `.zagd`, or cache artifacts are committed (sources only).

## Compiler/import errors encountered and workarounds

1. **`@import` resolves relative to the importing file, not the CWD.**
   The workspace `AGENTS.md` note claiming CWD-relative behavior is stale
   (a minimal probe — `a/main.zag` importing `../lib/util.zag` — compiled
   identically from `a/` and from its parent). Fix: in `hyb.zag`
   (at `engines/hyb/`) the harness imports are
   `../../../deliberation_depth/harness/...` (three levels, same as
   round-1 `one.zag`); in `common/cx_fwd.zag` they are
   `../../../../deliberation_depth/harness/...` (four levels — this tree
   has one extra `round2/` level vs round-1). Local imports from `hyb.zag`
   are `common/cx_*.zag`; from inside `common/` they are `../common/...`
   (which resolves to `common/` itself). First builds failed with
   `zag: error: @import cannot read '../../deliberation_depth/harness/
   R33_NATIVE_IO_V1.zag'` (twice, once per file) before the depths were
   corrected. No architecture was changed — only import-path literals.
2. **No `cx_sch_hash` function exists.** The committed schema hashes are
   exposed as canonical bytes (`cx_sch_bytes(id)`) plus hex
   (`cx_sch_hex(id)`); the engine hashes canonical bytes with `cx_fnv1a`
   (same primitive the startup assertion uses). `onep_init` sets
   `p.hmp/hpbc/hui = cx_fnv1a(cx_sch_bytes(0/1/2))`.
3. **Ceremony defect (reported, not silently edited):**
   `COMMIT_SCHEMAS.md` prints S_PBC's hash with a spurious leading zero
   (`0369efe53016bbe1a`, 17 chars — not a valid 64-bit hex). The engine
   asserts the true FNV-1a-64 `369efe53016bbe1a`, as round-1 did.
4. **Discharged-assumption snapshot fix (real bug found in testing):**
   the first `cxr_snap_enum` excluded the PBC assumption claim from
   snapshot paths, which produced *empty* snapshots whenever `false`
   was derived through the assumption (the common case) and made
   `hyb_pbc_for` fail. The assumption is now treated as identity (it is
   discharged by the PBC step, so it contributes no premise leaf) —
   subproof paths carry the outer premises, per-step licenses, and the
   `S_PBC` license. Derivation behavior is unchanged; only the ledger's
   snapshot completeness was fixed.
5. **Snapshot cross-product cursor bug (real bug found in testing):**
   `cxr_snap_step`'s two-premise case temp-collected the first premise's
   paths in the shared snapshot arenas, then *restored the cursors*,
   discarding the merged paths it had just committed — so every
   two-premise snapshot came out empty and `hyb_pbc_for` returned -1.
   Fixed by capturing the temp-region boundary and compacting (shifting
   merged path records down over the temp region; leaf/license offsets
   stay valid, temp leaves are orphaned). Single-premise and leaf cases
   were already correct.
6. **Path-memo contamination bugs (real bugs found in testing):**
   (a) `hyb_paths` captured the memo `first` index *before* recursively
   ensuring premise memos, so a claim's memo range included its premises'
   paths; combined with (b) the trivial premise path being committed with
   an *empty* leaf set (the premise's own index was never inserted), the
   greedy premise-disjoint scorer counted every path (empty leaves are
   trivially "disjoint") and produced inflated, inverted scores
   (e.g. a 1-step vs 1-step tie scored 2.5M vs 1.5M instead of 500k vs
   500k). Fixed with a two-pass `hyb_paths` (pass 1 ensures premise
   memos; pass 2 appends only the claim's own paths, contiguous) and by
   inserting the premise index as the trivial path's single leaf.
   After the fix all four contradiction probes score exactly as the
   frozen arithmetic predicts.
7. **Vendored harness (self-contained tree):** the task requires the
   build to live only under `round2/engines/hyb/`, so the two harness
   sources (`R33_NATIVE_IO_V1.zag`, `dlb_util.zag` — self-contained, no
   imports of their own) are copied byte-identical into `vendor/`
   (SHA-256 `e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8`
   verified equal). `hyb.zag` / `one_baseline.zag` import `vendor/...`;
   `common/cx_fwd.zag` imports `../vendor/...`. The vendored build
   produces byte-identical output to the external-harness build
   (B2_03 SHA-256 unchanged).

## znc hazard compliance

- No `as []i32` / `as []u32` / `as []u16` indexed casts anywhere in the
  new code (ZNC-2026-09-21-007): all tables are `[]u8` arenas with
  `au_get32/au_put32/au_get64/au_put64` accessors.
- No slice larger than 2^25 bytes is allocated; all arenas grow by
  doubling with an explicit 33,554,432-byte ceiling check that fails
  closed (returns -1) instead of panicking.
- New structs are flat and small (`CXRE` 7 fields, `CXRS` 9, `HYBL` 8,
  `HYBM` 7); all used via pointer, never copied by value, never nested.
- No `try` identifier, no `};`, `return;` with semicolon in void fns,
  no slice `==` comparisons.

## Verification performed (all observed 2026-09-25, pinned znc)

- **Build:** `znc: wrote native binary /tmp/hyb_build/hyb_bin`
  (278,933 bytes; vendored build).
- **B2_03 (≤3-step MP) formal smoke:** target `s` via two MP steps.
  `VERDICT: DERIVED`, `CONFIDENCE: 1`, audit byte-identical to round-1
  ONE (diff of `AUDIT:` sections empty). Three external runs,
  byte-identical:
  `24c585d2d98439790b1c6b06c607a930d367ab0add1cbe04bf3623476a7c2aec`
  (all three).
- **Contradiction probes** (custom `.form` files, all pass):
  - asymmetric (1-step `q` vs 2-step `not(q)`): `DERIVED-WEIGHED`,
    `q`, scores `500000 vs 333333` — shorter derivation wins.
  - exact tie (1-step vs 1-step): `WITHHELD`, scores `500000 vs 500000`
    `TIE` — equal evidence withholds only that claim.
  - PBC (`imp(not(q),r)`, `imp(r,false)` ⊢ `q`): `DERIVED` via
    subproof snapshot — the discharged assumption contributes no
    premise leaf; the `S_PBC`-licensed snapshot path scores and wins.
  - false-short (2-step `q` vs 1-step `not(q)`): `REFUTED-WEIGHED`,
    `not(q)`, scores `333333 vs 500000` — the better-evidenced side
    wins even when it is the negation of the target.
  - Trust learning observed: losing side's distinctive licenses drop
    `1000 → 900`, winner's rise `1000 → 1100` (visible in `TRUST:`).
- **Sealed-path guard:** problem file containing `SEALED: 1` →
  `hyb: sealed guard tripped on problem file`, exit code **3**.
- **Zero-RNG grep:** no `random`/`seed`/`rng` outside "zero RNG"
  comments; no executable RNG use.
- **znc hazards:** no `as []i32/u32/u16`; largest single alloc 1 MiB
  (ceiling guards at 33,554,432 fail closed); no `.zagd`, no binaries
  in the source tree.
- **In-process determinism:** `main` runs the derivation 3× and
  byte-compares; any divergence aborts (never triggered).