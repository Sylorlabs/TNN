# BUILD LOG — Arm S (recall-driven boundaries)

## 2026-09-21 — Initial implementation attempt (abandoned)

- Wrote `cl/arm.zag` from scratch (~809 lines) implementing the S mechanism with a 36-field `S64` struct.
- Hit a znc parser cascade (`error[E0202]: unknown type '{'` on every function) that resisted ~6 hours of bisection. Root causes found and fixed along the way:
  - C-style ternaries (replaced with if/else).
  - `~` bitwise-not arity confusion (replaced with explicit mask).
  - `jf_int` called with `[]u8` path (should be `*i32` flag).
  - `_zag_print_str` / `_zag_print_i64` do not exist in the substrate (use `_zag_print` / `_zag_i64_to_str`).
  - `_sha256_update` / `_sha256_final` do not exist (use `ns_sha256(input, out32)`).
  - Malformed mixed-paren conditions from bulk regex edits.
- The cascade persisted after all known defects were fixed; file deemed unrecoverable via patching.

## 2026-09-21 — Rewrite on b64 template (shipped)

- Copied the **working, frozen-toolchain-verified** `units/arms/harness/b64/cl/arm.zag` as the base (b64 compiles cleanly with `znc_linux_x86_64_abed8aa1`).
- Adapted for S:
  - Header comment rewritten for the S mechanism.
  - `usage:` string changed `b64` → `s`.
  - `METRIC_JSON` `"arm":"b64"` → `"arm":"s"`.
  - Extended the `B64` struct with S fields: `mrgJ/mrgIa/mrgIb` (per-slot joint/solo recall counters), `epIds/epN` (per-episode recall list), `nMerge/nSplit/nVeto`.
  - `b64_init` allocates and zeroes the new fields; `b64_new` literal extended.
  - `b_recall` appends each successfully recalled ID to `epIds`.
  - New `s_ep_end`: at episode end, updates J/I_a/I_b for adjacent pairs, evaluates merge criteria (`J>=2`, `J*5>=(J+Ia+Ib)*3`), applies the eliminative veto (`Ia+Ib>0` → veto), commits merges via `s_do_merge` (new chunk ID `corpus<<24|0x400000+seq`, tombstone parts with KILL reason 10), and evaluates split criteria (`Ia+Ib>=2*(J+1)`) via `s_do_split` (KILL reason 11, re-add atoms).
  - `probe_reg` (M1) calls `s_ep_end` after each probe episode.
- **Compiler:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (frozen).
- **Build command:** `znc --emit-native units/arms/S/cl/arm.zag -o units/arms/S/.work/arm_s`
- **Result:** clean build, 196,122-byte native binary. Only analyzer warnings (A0102 ignored return values), no errors.
- **Smoke test:** `arm_s m1-1x-prose <corpora/r1>` → `M1,prose.bin,100.0,100.0,84731` + valid `METRIC_JSON` with `"arm":"s"`.

## Substrate

Verbatim copies (required):
- `units/arms/S/substrate/R33_NATIVE_SHA256_V2.zag`
- `units/arms/S/substrate/R33_NATIVE_IO_V1.zag`

Import in `cl/arm.zag` is the bare directive `@import("../substrate/R33_NATIVE_SHA256_V2.zag")` (which pulls `R33_NATIVE_IO_V1.zag`).

## Battery

Full 1× battery (`run_battery.sh`) launched 2026-09-21 against `units/arms/harness/corpora/r1`, workdir `units/arms/S/battery_work`. See `battery_work/battery.log` and the assembled scorecard.

### Bug fixes during battery

1. **ins-queue overflow:** `s_do_merge`/`s_do_split` originally used `b_ingest` (→ `slot_insert` → `ins` append). The `ins` array has fixed capacity (`n+1024`); repeated merges overflowed it → "slice index out of bounds" panic in M2. Fixed by reusing slots in-place: `s_do_merge` reuses `sl_a`'s slot for the merged chunk; `s_do_split` reuses the killed slot for the first atom and scans for dead slots via `s_reuse_dead` (no `ins` appends). `b_kill` was already safe (no `ins` touch).

2. **O(n²) consolidation:** `s_ep_end` did a pairwise scan over all recalled IDs. For M1's 84k-unit bulk verification this was ~7B iterations. Added a performance guard: if `epN > 2000`, skip consolidation (bulk verification episodes don't drive boundary learning; learning happens in selective-recall M2/M3 episodes). Documented in `ARM_SPEC.md` ambiguities.
