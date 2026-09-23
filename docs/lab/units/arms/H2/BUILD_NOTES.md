# H2 BUILD_NOTES.md — continuation attempt 2, 2026-09-21

## Toolchain

- Pure Zag on Linux VM. Frozen compiler:
  `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- Build: `znc_linux_x86_64_abed8aa1 cl/arm.zag -o work/h2`
- Build time ~90 s. Warnings only (unused vars, shadowed names); no errors.
- Rebuilt 2026-09-21 08:40 UTC after the budget-mechanism correction.
- Source: `cl/arm.zag` (73,412 bytes post-correction). Single-file arm +
  trial harness; dispatcher on `argv[1]`.

## Correction applied this continuation (in place, not a rewrite)

Pre-correction inspection found the source did NOT implement the frozen H2
budget mechanism despite declaring it: it evaluated up to 16 candidates in
position-sorted order, never enforced B=8, never bulk-refused, never counted
fallback windows. Corrected in `h2_window`:

1. Removed the position re-sort; evaluation in frozen priority order.
2. Hard cap: at most B=8 candidate evaluations per window (`evaled>=8` break).
3. On exhaustion with candidates remaining: one bulk `OP_CUT_REFUSE`
   (`bulk_ref` counter, `OPA_BULK` audit word), then the fixed-midpoint
   coarse fallback for the remaining window region (`F_FALLBACK` flag).
4. Added `win_n`, `fallback_win`, `bulk_ref` counters; M1 JSON fields
   `m1_windows`, `m1_fallback_win`, `m1_fallback_rate_tenths`,
   `m1_bulk_refused`.
5. M7 H2 kill reporting: per-corpus hit-rate advantage over fixed-64B
   baseline, companion ID-stable reuse advantage, `m7_h2_kill_reuse_both`
   and `m7_h2_kill_reuse_either` flags.

Pre-correction evidence (M1 prose 1x, 219 s, 100% recall) is INVALID as H2
evidence and is not used in the verdict; it is superseded by the corrected
runs.

## Bugs found and fixed

- `t_m6` transfer-revision loop used the wrong index (`iget(cidsy,i*4)` with
  `i` left at `nychunks` from an earlier loop instead of the loop variable
  `j`). Fixed to `iget(cidsy,idx*4)` on the intended 100-unit schedule.
  Rebuilt and M6 smoke-verified (100.0/100.0/100.0/0.0 both directions).
- `t_m8` store-image sizing (found 2026-09-21 ~10:05 UTC during the first
  valid M8 attempt): the artifact code allocated the image as
  `cap*28+dcap*28` and appended `s.iddk`/`s.iddv` with `dcap*8`, but
  `h2_new` allocates the ID maps as `dcap*4` each → `img_append` read
  `dcap*4` bytes past the allocation → `panic: slice index out of bounds`
  after all four ingests completed. Fixed to `cap*28+dcap*20` with
  `dcap*4` appends for both ID maps (semantically correct: id→slot maps
  are i32→i32). The pre-fix M8 code never produced any artifact, so no
  baseline is invalidated.
- `t_m8` dispatcher (found earlier same day): the pre-existing guarded reads
  `if(_zag_argc()>=4){od=_zag_arg(3);}` / `if(_zag_argc()>=5){pt=_zag_arg(4);}`
  were suspected dead because of ZNC-2026-09-21-007 (argc always 0).
  Empirically re-tested 2026-09-21 ~10:45 UTC on the frozen toolchain:
  `_zag_argc()` returns the REAL count (5 for 4 user args) and
  `_zag_arg(3)` returns the correct value. The guarded reads work fine;
  no unconditional-read change was needed. The five M8 regimes genuinely
  received their outdir/perturbation args (artifacts landed in the right
  dirs; frag/aslr perturbation code paths execute).
- `work/run_m8.sh`: invoked nonexistent `m8-<pert>` modes (binary only
  dispatches `m8-1x`); corrected to `h2 m8-1x CORPUS OUTDIR PERT`.
  Comparison file list corrected to t_m8's actual artifacts
  (`store_hashes.txt`, `store_chain.txt`, `ledger.bin`,
  `ledger_chain.txt`, `alloc_trace.txt`).
- Post-rebuild smoke (2026-09-21 10:18 UTC): `m1-1x-prose` byte-identical
  to the 1x evidence after the t_m8-only repair — no collateral change.

## znc workarounds already in source (from prior crew, kept)

- `[]u8` arenas with explicit `t_put32`/`t_get32` accessors everywhere
  (ZNC-2026-09-21-007: no `as []i32`-style indexed casts in this source).
- Slice-field aliasing routed through pointers (ZNC-2026-09-21-004).
- Audit ledger chunked under the 2^25-byte index limit.
- `_zag_arg` read unconditionally (ZNC-2026-09-21-007 argc=0).
- Hoisted shift-out-of-`&`-test (ZNC-2026-09-21-008).

## Determinism

- Zero randomness in every AI decision path and in all harness paths
  (no RNG, no clock reads; T3/churn corpora are seeded deterministic
  environment inputs, fixed in the corpus MANIFEST).
- Double 1x runs compared byte-for-byte on stdout (see VERDICT.md).
- M8 five-regime gate compares stdout, chunk bytes, chunk sha256 chain,
  ledger bytes, and allocator trace byte-for-byte.

## Known gaps (not fixed; documented, no bar depends on them)

- `t_m5baseline` is dead code (never dispatched); see AMBIGUITIES.md A7.
- `h2_verify` folds boundary fidelity into the recall pass (A3).
- ID-remap probe is provisional pending the ID arm freeze (A10).
