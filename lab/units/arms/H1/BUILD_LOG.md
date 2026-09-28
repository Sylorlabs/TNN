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

## Continuation crew (2026-09-21, second session)

### Source changes (additive, committed as part of final binary)
1. **Added `spans-1x-prose` / `spans-1x-code` analysis modes** (`t_spans`): dry
   segmentation dump (`SPAN,offset,length` per unit) using H1's own
   `h1_segment_dry` with the same mask-15 path as M1 ingest. No store effects.
   Used for the coordinator-directed criterion-(i) adjudication (content-keyed,
   offset-independent reuse vs fixed-64B). Spans verified to tile [0,n)
   contiguously; counts match M1 exactly (22,508 prose / 39,501 code);
   double-run byte-identical.
2. **Fixed t_m2 METRIC_JSON framing bug**: the human-readable `M9,...` line was
   printed between the last JSON field and `j_end()`, producing a truncated
   JSON object (missing closing brace) in m2-t1-prose/code fragment.jsonl.
   Moved the M9 print to after `j_end()`. Only t_m2's T1 path was affected
   (T2/T3 emit no M9). Both T1 legs re-ran clean under the final binary.
   Binary v3 (v2 = pre-fix). Proven: v3 m1-1x-prose stdout byte-identical
   to v2 → the fix touches no other code path.
3. **Fixed t_m8 iddk/iddv serialization size** (dcap*8 -> dcap*4; see M8
   status). Final binary: `work/arm_bin_v4`.

### Battery results (final binary, all legs double-run byte-identical)
- m1-1x-prose: 100/100, 22,508 units, 64/64 PROVISIONAL-PENDING-FREEZE PASS,
  0.0% refusal, 253 ops/cut, 0.0% BAR flips (v2 run; v3 equivalence proven).
- m1-1x-code: 100/100, 39,501 units, 64/64 PASS, 0.0% refusal, 252 ops/cut,
  0.0% flips (v3).
- m2 t1/t2/t3: all ETC=1, uncensored, ep0 recall 0.0, final 100/100;
  M9 fast-then-flat (takeoff ep 1, steepness 100.0, late gain 0.0).
- m3-1x: 100% survival, 100% fresh recall, 1,920 mgmt entries, 50/50 weakens, CLEAR.
- m4-1x-prose/code: 100% boundary revision, 100% content revision, 0.0% kill
  rate, no kill-substitution, 1 episode.
- m5-1x: 22,508 units, 5,422,721 source bytes, slot table 658,896 B,
  ledger 44,092 entries (2,821,888 B) → 2.413 B/B (metric bar 1.5: FAIL —
  not a kill criterion); audit 8.326 entries/KB (bar 10: PASS).
- m6-p2c/c2p: 100/100/100 recall/boundary/revision, 0.0 tax both directions.
  Memorizer controls reproduce official B-64 evidence exactly
  (p2c 82.2/27.4/drop 54.8; c2p 27.4/82.2/drop -54.8) → validity gate PASS.
- m7-1x: hit 100.0% / reuse 100.0% both corpora; baselines 32.7% prose /
  40.9% code; kill_i_triggered=false; reread 2,406,170 B.
- m8: **M8GATE PASS** — 5 perturbations x 2, byte-identical artifacts
  (v4 binary; clean/frag/aslr/starve/freelist all rc=0, stdout identical,
  m8_compare.py PASS).

### M8 status (2026-09-21)
- First gate attempt completed clean/run1+run2: stdout empty, stderr
  "panic: slice index out of bounds" — t_m8 panics deterministically on H1.
- Root cause FOUND and fixed: t_m8's store-image dump appended s.iddk/s.iddv
  with size dcap*8, but h1_new allocates both ID-map tables at dcap*4
  (4-byte slots; the 8-byte size was copy-pasted from the dedup-key table).
  Reading 2x past the allocation -> deterministic "panic: slice index out
  of bounds". Located via instrumented debug binary (phase prints bracketed
  the panic to the img-serialization block; size audit vs allocations found
  the mismatch). Fix: dcap*4 for both iddk and iddv. Binary v4.
- After fix, m8-1x clean completes: M8,100.0,100.0,125858 with all artifacts.
- Full M8 gate (clean/frag/aslr/starve/freelist x 2, v4): M8GATE PASS.
  All 10 runs rc=0, stdout M8,100.0,100.0,125858; m8_compare.py confirms
  byte-identical artifacts across all perturbations (ledger/store chains and
  alloc trace identical, incl. the entropy/time-starved run).

### Kill criteria (final adjudication)
- (i) Reuse ≤ B-64+10pp: SAFE. Content-keyed single-ingest dedup:
  prose H1 15.892% vs B-64 0.001% (+15.891pp, bar 10.001%);
  code H1 23.802% vs B-64 0.396% (+23.406pp, bar 10.396%).
  H1's own m7 operationalization agrees (100% vs 32.7%/40.9% baselines).
- (ii) Refusal > 30% AND ops > 1e4: SAFE (0.0%, 252–253 ops; re-verified on
  final binary).
- (iii) BAR ±10% flips > 25%: SAFE (0.0%; re-verified on final binary).

### Files
- Assembler: `work/assemble_h1.py` (H1-specific scorecard builder).
- Reuse analysis: `work/reuse_crit1.py` (script) + spans dumps (ephemeral).
- Battery evidence: `work/battery_full/` (per-leg run1/run2/stdout.txt,
  fragment.jsonl, STATUS.txt).
