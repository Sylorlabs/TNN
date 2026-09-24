# CREW A — base battery (§2+§3), fresh builds 2026-09-24

Pinned toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
Binaries: `src/render_a` (contender_a/src/render_a.zag), `src/form_par`
(contender_a/src/form_par.zag), `src/render_nat` (fork_ar/src/render_ar.zag,
servo-AR tournament baseline). Pure Zag, zero RNG. Fixture:
`bytegen/fixture/plan_v1.txt`. All identity comparisons at MIX level
(WAV mastering is global per gamma.zag lesson).

## DET
- 2× `render_a plan_v1` → byte-identical (`cmp` clean).
  SHA-256 both: `a30c6577e265152d0a3df1ffb77eb724321f5e5a1a39a49e1cf625a42b494117`
  (5,292,000 bytes). PASS. (Native also byte-identical on rerun.)

## QUALITY (9 V10 bars, A's global peak-normalized WAV writer)
| bar | value | limit | verdict |
|---|---|---|---|
| G-PER | 0.340 | ≤ 0.350 | PASS |
| G-STA | 1.826 | ≤ 3.000 | PASS |
| G-LURCH | 2.362 | ≤ 5.000 | PASS |
| G-DRIFT | 480.284 | ≤ 800 | PASS |
| G-FLUXm | 241.824 | ≤ 350 | PASS |
| G-SIL1 | 0.000 | ≤ 0.020 | PASS |
| G-SIL2 | 0.000 | ≤ 0.500 | PASS |
| G-CLIP | 0.849 | ≤ 0.950 | PASS |
| G-CREST | 3.863 | ≤ 14 | PASS |
**9/9 PASS**, reproducing the dive's values exactly.
Converter note: `render_a` mix words are i16-scale samples in s32 slots
(full-scale s32 shift produced near-silence; corrected). Raw unmastered
fixture peak = 43,337 (1.3225 i16FS); quality uses the renderer's documented
global mastering, identity stays mix-level.

## CHOP (independent 296-timestamp complete event list)
- CHOP-1: 0 hard discontinuities — PASS.
- CHOP-2: no ≥150 ms gaps — PASS.
- CHOP-3: 29 flux spikes, 0 unexplained — PASS.
(Prereg cited 321 timestamps; the independent generator yields 296 — same
discrepancy the characterization disclosed. Substantive result unchanged.)

## COHERENCE (motif 2.0–5.4 s vs 24.0–27.4 s)
- Windows byte-identical; zero-lag normalized xcorr **1.0000000000**.
- Max-lag ±50 ms: **1.000000 at lag 0**.
- Pitch contour correlation: 1.000000000 (per-note pitches identical; note 7's
  estimator locks to the 110 Hz bed in BOTH motifs — symmetric, not a finding).
- IOI contour: constant 0.400 s by plan in both windows — correlation is
  degenerate on constant sequences (floating-point noise gave a meaningless
  −0.6448 Pearson); honest statement is exact vector identity, tie by
  construction.
- Dive reference: native 0.736557 / 0.999630. **A wins coherence.**

## COST (same machine, interleaved)
- Wall (6-run, quiet): A median 6.75 s vs native 4.29 s (1.57×).
- Wall (10-run, contended VM): A 5.57 s vs native 5.33 s (noisy).
- **CPU via wait4 (8-run, contention-free): A median 0.92 s (0.90–0.93 tight)
  vs native 0.80 s (0.79–0.81 tight) → 1.15×.**
- Peak RSS: A 15.3 MB vs native 15.4 MB — tie.
- Verdict: **native wins COST** (single-threaded). The fair number is CPU
  (1.15×); wall ratios inflate under VM contention. Architectural price
  confirmed: per-sample integer-division phase recompute vs carried add.

## RT-LONG (RESPOND trap, ZCR-isolated + bed-subtraction pitch meter)
- A, nominal 880 → formation resolves 440; rendered response **440.00 Hz,
  +0.01 cents**. A, near-miss nominal 460 → **440.00 Hz, −0.00 cents**.
  Residual outside response window: max 0 (clean isolation).
- Native (fed the ORIGINAL RESPOND theme, not A's resolved plan):
  ZCR-measures its own cue → 454.00 Hz (+54.23¢); renders 454.38 Hz (+55.69¢);
  announces `AR RESPOND measured`.
- **A wins RT-LONG.** (Whole-mix autocorrelation is bed-dominated at 110 Hz
  and is NOT the honest response reading — disclosed.)

## RT-CASCADE (faults injected mid-render @ mix level)
| model | pre | window | post |
|---|---|---|---|
| A single-bit @3 s | 0 | 1/1 | **0 / 1,190,699** |
| A burst 44,100 @10 s | 0 | 44,100 | **0 / 837,900** |
| A dropout 44,100 @10 s | 0 | 44,098/44,100 (2 clean-zero) | **0 / 837,900** |
| A DC shift 44,100 @10 s | 0 | 44,100 | **0 / 837,900** |
| Native single-bit @3 s | 0 | 1/1 | **5,854 / 1,190,699** |
- **A: zero post-fault cascade on all four models. Native: 5,854.**
  (Dive cited 5,791; current build gives 5,854 — same phenomenon, use the
  fresh number. Native fault rerun byte-identical.)

## RT-EDGE (truncation @15 s)
- DUR_S-15 truncated plan vs full[0,15): **0 / 661,500 diffs** — no cut
  discontinuity.
- DUR_S-30 plan with events ≥15 s removed vs full: 481,918 diffs, ALL in
  [16.0, 29.3) = exactly the removed events' spans (reproduces the
  characterization's 481,918 exactly); 0 before 16 s. Legitimate-only.
- The dive's VERDICT_AUDIO "4,397 diffs in [14.9,15.0)" did NOT reproduce
  (0 on the identical comparison) — possibly their truncated plan differed
  in an unrecorded way. Both fresh comparisons show legitimate-only diffs:
  **bar passes.**
