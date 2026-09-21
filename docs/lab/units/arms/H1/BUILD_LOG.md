# H1 — BUILD_LOG

**Arm:** H1 (Full deliberation per boundary)
**Date:** 2026-09-21
**Builder:** ARM CREW H1 (Track A)

## Summary

Implemented the full H1 mechanism in pure Zag (~1,700 lines), compiled with the frozen toolchain, and ran the 1x battery. The implementation follows the frozen prereg: boundaries as cognitive acts via inspect/propose/commit with a frozen noticer list and integer evidence weights.

## Timeline

### Pre-existing state (before 2026-09-21 session)
- A partial implementation existed at `cl/arm.zag` (~886 lines) with the core H1 machinery (struct, noticers, commit, recall, defects, repair, swap probe) but:
  - No metric modes (M1–M8) or main dispatcher.
  - `h1_led` arity bugs (16 args instead of 17) in 12 call sites.
  - `let s:H1;` bare struct declaration (triggers ZNC-2026-09-21-004).
  - Bootstrap trace allocation bug (halloc before s.trace exists).

### 2026-09-21 session work

1. **Appended metric modes** (lines 890+): Implemented `t_m1` through `t_m8` and the `main` dispatcher covering all 1x modes:
   - `m1-1x-prose`, `m1-1x-code`
   - `m2-t1-prose`, `m2-t1-code`, `m2-t2-prose`, `m2-t2-code`, `m2-t3-1x`
   - `m3-1x`, `m4-1x-prose`, `m4-1x-code`
   - `m5-1x`, `m5-baseline`
   - `m6-p2c-1x`, `m6-c2p-1x`
   - `m7-1x`
   - `m8-1x <corpus-root> <outdir> <perturbation>`

2. **Fixed h1_led arity** (12 sites): Added the missing 17th argument (a5) to all `h1_led` calls. The frozen layout is 16 words: op@0, slot@4, rc@8, b1..b5@12..28, a1..a5@32..48, stage@52, d1@56, d2@60.

3. **Fixed ZNC-2026-09-21-004** (slice-let off local struct):
   - Replaced `let s:H1;` with full struct literal `H1{...}` in `h1_new`.
   - Fixed bootstrap: allocate trace via `nio_alloc` directly (not `halloc`) to avoid tracing into non-existent buffer.
   - Routed `let led:[]u8=s.led` through pointer in `t_m3`.
   - Routed slot-table aliases through pointer in `t_m5baseline`.

4. **Removed duplicate** `write_hex_line` (was defined twice).

5. **Fixed A15 probe count**: Changed from modulo schedule (could yield 63) to guaranteed-64 stride `(pi*nchunks)/64`.

6. **Compiled**: `znc_linux_x86_64_abed8aa1 cl/arm.zag -o work/arm_bin` → 233K binary, zero errors (warnings only).

7. **Smoke tests**:
   - `m1-1x-prose`: 100.0% recall, 100.0% boundary, 22,508 units, 64/64 probes PASS, 0.0 refusal, 253 ops/cut, 0.0 bar flips.
   - `m3-1x`: 100.0% survival, 100.0% fresh recall, 1,920 mgmt entries, 50 weakens handled, CLEAR.

8. **Full 1x battery**: Launched via `run_battery.sh` with absolute corpus path. (In progress at time of writing.)

## znc Bugs Encountered

- **ZNC-2026-09-21-004**: `let s:H1;` (bare struct) → "aggregate let needs an aggregate initializer". Fixed with struct literal. Also affects `let p:[]u8=s.field` where s is local — must route through `*H1` pointer.
- **Arity checking**: Strict 17-arg enforcement on `h1_led`; pre-existing code had 16-arg calls.

## Files

- Source: `~/workspace/tnn-lab/units/arms/H1/cl/arm.zag`
- Binary: `~/workspace/tnn-lab/units/arms/H1/work/arm_bin` (not committed)
- Docs: `~/workspace/docs/lab/units/arms/H1/ARM_SPEC.md` (this dir)
- Battery: `~/workspace/tnn-lab/units/arms/H1/work/battery_r1_1x/`

## Open Issues (from summary, not yet verified fixed)

1. Span-key collision when `len=4096` (packing `(cid<<36)|(off<<12)|len`).
2. Nomination overflow: 256-entry cap per 4 KiB window may truncate before top-16 selection.
3. M3 operation counts: verify arm chunks literally realize 3k-add/3k-kill/4k-add schedule.
4. M7 semantics vs frozen §7 and provisional C′ schedule.
5. M8 capacity: uses large combined capacity; compare with frozen M8 spec.
6. 10x: no chunk-safe ingestion yet (2^25 slice limit); 10x code is ~95MB.
