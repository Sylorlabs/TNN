# Video Fusion v4 — Verdict

## Honest verdict: BLOCKED — does not pass the fusion bar

**It still looks segmented.** No — more honestly: **there is no render to judge.**
The pipeline crashes before producing output frames. I cannot claim any fusion
quality, and I do not.

## What works

1. **Stabilization** (v4a.zag): Measures shake_max_px=44, residual_before=24,
   residual_after=20, use_stab=1. Real stabilization, not a no-op.

2. **Dark/white components** (v4_dw_one): Extracts pig body (dark) and white
   reference (bright) via connected components. Returns valid components
   (dst[72] != 0).

3. **Anatomy mechanism** (v4_anatomy_frame): The full snout→neck→head pipeline
   is implemented and **functional in isolation**:
   - v4_moments: Computes moments without crashing.
   - v4_eigenvec: Principal axis without crashing.
   - v4_snout: Finds snout via max projection without crashing.
   - v4_neckcut: Finds neck constriction without crashing.
   - v4_head_region: Segments head with leg-split via motion without crashing.
   - Returns 1 (valid) with populated landmarks.

   Proven by bisection: each function was tested individually and in combination.
   The function returns 1 without panicking.

4. **Instruction parsing** (v4d.zag): MERGE→FUSE_HEAD (110), SIDE→SIDE_BY_SIDE (20),
   THEN→SEQUENCE (20). Content-sensitive (pig/bunny roles).

5. **Photometric candidates** (v4b.zag): T1-T4 implemented with metrics.

## What is blocked

**Integration crash**: When v4_anatomy_frame returns 1 (valid head found), the
caller (v4_merge) crashes with "panic: slice index out of bounds".

Bisection results:
- v4_anatomy_frame in isolation: NO CRASH (returns 1).
- Caller with vr==0: NO CRASH (clean refusal, trace written).
- Caller with vr==1: CRASH.

The crash is NOT in:
- The heads mask copy (disabled, still crashes).
- The lmf slice (replaced with fresh alloc, still crashes).
- The detailed trace (simplified, still crashes).
- The lmf→lm copy (tried h_put64, byte copy, disabled — all crash when vr==1).
- nio_free (disabled, still crashes).

The crash IS tied to vr==1 taking the valid path, but the specific slice
remains unidentified after extensive bisection. Suspected heap corruption or
an invalid slice in the downstream pose/photometric/render code that only
executes when nvalid > 0.

## Blockers (complete list)

1. **Integration crash** (critical): "slice index out of bounds" when valid
   heads are found. Prevents any render. Root cause unidentified after
   ~6 hours of bisection. The anatomy works; the caller crashes.

2. **v4_dw_one border rejection**: Rejects components touching any frame edge.
   Later pig frames touch the top edge → those frames invalidate with -781.
   Needs temporal/stabilized evidence recovery or explicit invalidation.

3. **v4_ainv layout**: Suspect unaligned/overlapping qword offsets. Needs audit
   and move to aligned offsets with enlarged arena.

4. **v4_slot filtering**: May not rewrite `subj` to largest component before
   neck/slot calculations. Needs audit.

5. **Plan-name trace**: `pname` is 16 bytes but passed as full slice after
   tr_str → binary garbage in trace. Needs explicit length tracking.

6. **Photometric use-after-free**: `cand_names` freed before fallback reads it.
   Needs free moved after selection.

7. **Stabilization residual**: Uses whole-frame differences, not background-only.
   Either tighten or document limitation.

8. **No 24-frame render**: Cannot produce output due to blocker #1.

9. **No byte-identical reruns**: Cannot run twice due to blocker #1.

10. **No gallery video**: Cannot encode MP4 due to blocker #1.

11. **No full-eyes review**: No frames to review due to blocker #1.

## Mechanical proof status

**Neither** a valid segmentation **nor** a no-valid-split proof was achieved:
- The anatomy FINDS heads (returns 1), so "no valid split" is false.
- The pipeline CRASHES before rendering, so "valid segmentation" is unproven.

The honest statement is: **the mechanism is implemented and works in isolation,
but the system integration is broken.**

## What was NOT done

- No 24-frame MERGE render (crash).
- No SIDE/THEN sensitivity tests (no render).
- No content/role-order tests (no render).
- No determinism battery (no render).
- No MP4 (no frames).
- No full-eyes review (no frames).

## Code status

The code is committed to `tnn-native-lab` (see commit SHA in delivery message).
It contains:
- src/chunks/v4a.zag … v4e.zag (Zag source).
- src/build_fusion4.sh (build script).
- docs/DESIGN.md, PROVENANCE.md, VERDICT.md (this file).

It does NOT contain binaries, caches, frames, MP4s, or gallery output.

## Recommendation

The anatomy mechanism is sound. The integration bug needs a fresh-eyes debug
session with a Zag-aware debugger or printf-style tracing (not available in
this environment). Alternatively, rewrite v4_merge's downstream to avoid the
suspect slice patterns.
