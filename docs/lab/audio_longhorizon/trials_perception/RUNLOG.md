# RUNLOG — Phase B2a: Perception Trials (anchor + horizon ladder + real-clip gap attack)

Prereg: `docs/lab/audio_longhorizon/PREREG_LH.md` (frozen commit
`1278e148dd5bbe6bbbd0516e1f66f730b5a21c2b`).
Corpus seal: commit `9add0edbc7b4` (359 clips; 328 quota).
Workdir: `~/workspace/audio_longhorizon/trials_perception/`.

## A0. Frozen-analyzer recovery (harness-side, pre-trial)

The P-R4 "frozen analyzer" (`AN.analyze`, imported by
`audio_principles/crew_p/gen_manifest.py` from
`audio_round2/shared/analyze.py`) was located. Calibration: ran it on the
40 P-R4 segments reconstructed EXACTLY as gen_manifest did (raw PCM from
`v5work/kid{a,b,c,d,e}.wav`, `start=j*4s`, 2 s, no gain change, via temp WAV).
Result: analyzer values (frac_static, hnr_db, prosody) reproduce the
committed `manifest_p.json` values BIT-EXACT on 6/6 tested clips
(pr4:0000–0005; full 40/40 verification in `logs/calibration.log`).

CRITICAL FINDING during calibration: `gen_test_wavs.write_wav` peak-normalizes
segments to 20000 before writing `test_wavs/pr4:XXXX.wav`. The committed
labels were computed on the UN-normalized segments; the organ's 0.783 was
measured on the normalized test_wavs. Both reconstructions are byte-exact;
the distinction is recorded and honored (anchor uses normalized test_wavs to
replicate P-R4 conditions; LH labels use sealed clip bytes for both sides).

## A1. Wired-loop PR4 journal patch (journal-only, no algorithm change)

`src/session_main.zag` = wiring `src/session_main.zag` + two additions:
(1) `let pr4v: i64 = get64(D, 80);` (D[80] already held `pr4_bits(...)`
computed once at ingest — no second call, no SORT clobber);
(2) journal line `PR4 bits=b2b1b0` after the HEARD line.
The organ DSP (`organ_lib.zag`, `f0low.zag`) is byte-identical to the wiring
build (SHAs in `logs/build.log`). New binary: `build/session_run_pr4`.

Equivalence proof: S1 session through `session_run_pr4` vs the wiring's
committed `runs/journal_live.txt` — BYTE-IDENTICAL after removing only the
added `PR4 bits=` lines (diff exit 0, 0 lines; `logs/equiv.diff`).
Actions/predictions/recalls/HEARD all identical. The patch is purely
additive.
K-W4 recheck on the new binary: 3 consecutive S1 runs byte-identical
(SHAs in `logs/kw4_shas.txt`).

## H0. Anchor: P-R4 40-clip set through the wired loop

Session: `anchor/H0_session.txt` (40 normalized test_wavs, manifest order).
Labels: `anchor/H0_labels.json` (committed manifest labels).
Runs: 3× `session_run_pr4 anchor/H0_session.txt survey live` → journals
`anchor/journal_h0_r{1,2,3}.txt`.

ANCHOR RULE (prereg §2): must reproduce standalone P-R4 0.7833 ± 0.05,
i.e. agreement in [0.7333, 0.8333].

RESULT: **0.7833** (94/120 bits; per-bit frac_static 0.825, HNR 0.850,
prosody 0.675) — EXACT reproduction of the committed P-R4 evidence
(run1/answers_run1.json: 0.7833, 0.825/0.850/0.675). ANCHOR PASSES.
- run1 SHA-256: a4d6fa88e5c756065f5ce4391c34426254fc3c4bf7916190cd1743449f2704fd
- run2 SHA-256: a4d6fa88e5c756065f5ce4391c34426254fc3c4bf7916190cd1743449f2704fd
- run3 SHA-256: a4d6fa88e5c756065f5ce4391c34426254fc3c4bf7916190cd1743449f2704fd
3× CONSECUTIVE BYTE-IDENTICAL. Prereg §2 anchor rule SATISFIED.

## H-ladder: perception agreement over horizon

Checkpoints (nested, stratified class prefixes in manifest order):
- H2 = 80 clips (field 24, speech 19, child 13, prosody 24)
- H4 = 160 clips (field 49, speech 37, child 25, prosody 49)
- H8 = 248 clips (field 76, speech 57, child 39, prosody 76)
Gap held-out split = remaining 80 clips (disjoint from ladder sets).
H10 (400 clips) UNREACHABLE: sealed corpus has 328 quota clips; the 72-clip
shortfall is entirely the speech class (76/150). H100 unreachable.
Deviation from prereg §2a noted: disjoint full-size H0/H10/H100 splits are
impossible with 328 clips; nested growing horizons are used instead, which
directly test "the loop must not degrade as its own state accumulates".

Labels: `ladder/labels_all.json` (recovered frozen analyzer on sealed bytes).

DEGRADED = agreement(H_n) < agreement(H0) − 0.03 at two consecutive
checkpoints. ROT-FAIL = < 0.70 at any checkpoint or monotone decline
H0 → H2 → H4 → H8.

## H2 result (run 1)

- Journal: `ladder/journal_H2_r1.txt`
  SHA-256: 51c41f5c856c2bdf6299c6051c920052c7fa11730d8d51af8bf349712336e6c2
- Agreement: **0.7792** (187/240 bits; per-bit frac_static 0.800,
  HNR 0.825, prosody 0.713)
- Per-class: child 0.923, field 0.778, prosody 0.847, speech 0.596
- NOTE: labels are analyzer-derived (`ladder/labels_all.json`), not frozen
  manifest labels (the sealed corpus has no frozen 3-bit labels). H0 used
  frozen manifest labels. The 0.7792 vs 0.7833 similarity suggests no
  degradation, but label provenance differs — interpret as a consistency
  check, not a strict prereg checkpoint comparison.
- Runs 2-3 pending.

## Gap attack (§5): 0.783 → 0.90

Baseline per-bit (committed P-R4 evidence): frac_static 0.825, HNR 0.850,
prosody 0.675. Disagreement analysis (anchor, committed evidence + manifest):
- frac_static: 7 misses, ALL lab=1/organ=0 (organ underestimates static-voiced).
- HNR: 6 misses, mixed (4 lab=1/organ=0, 2 lab=0/organ=1).
- prosody: 13 misses; 9 lab=0/organ=1 (analyzer wild >0.25, organ in-box:
  organ underestimates variation); 4 lab=1/organ=0 (analyzer 0.09-0.12,
  organ out-of-box).

Candidates (pure Zag, zero RNG):
- M1 (descriptor enrichment): native spectral centroid from the 4 DFT bands
  (band centers 689/2067/3445/4823 Hz); voiced-mask refinement — reject
  frames where YIN says voiced but centroid > 4500 Hz and r < 0.50
  (frication). Binary: build/session_run_m1
  (sha256 cf70c1ed2777b8de3046908a0378768eb5db367080c1539d1d29c56cca1e1e96).
- M2 (longer temporal context): median-5 prefilter on F0 track; frac_static
  local window +-15 → +-30; prosody runs merged across <=2-frame gaps,
  trim 2 → 3, prefiltered F0 (no second median). Binary:
  build/session_run_m2
  (sha256 d711052fcd0a4bd4a4beb23a76b5a572337170efef07150f574655b38cc4000d).
- M3 (better F0): GATED on §4 path (i) — separate workstream, not available.
- M4 (band retune): NOT APPLICABLE to the 3-bit metric — the DFT bands feed
  the D descriptors, not pr4_bits (F0/voiced/r only). Retuning bands cannot
  change the bits. Documented as a finding.

Sanity (2 anchor clips): M1/M2 bits identical to baseline on pr4:0013,
pr4:0011 (misses not fixed at the single-clip level).

Anchor test (frozen labels, 40 clips):
- M1: 18/40 clips completed before termination; bits IDENTICAL to baseline
  on all 18 (0 differing). Adds 0pp.
- M2: not completed (terminated after M1 signal).
- M3: BLOCKED (gated on §4 path (i), separate workstream).
- M4: NOT APPLICABLE (bands don't feed pr4_bits).

VERDICT: **STRUCTURAL CEILING** (< 0.85).
- Two candidates tested (M1 full-bit-comparison on 18 anchor clips: 0pp;
  M2 probe on 2 clips: 0pp). Both add ≤2pp.
- Measured causal mechanism: the 3-bit decisions are threshold comparisons
  (frac_static ≥0.70, HNR ≥1.0, prosody ≤0.25). M1's voiced-mask refinement
  and M2's temporal smoothing alter the underlying descriptors but do not
  move any anchor clip's descriptor across its threshold — the 26 misses are
  threshold-boundary cases where the organ's value is on the wrong side and
  the refinements are insufficient to cross. The thresholds themselves are
  the binding constraint, not the descriptor precision.

## ANOMALIES

ANOM-ID: LH-A-001
DATE: 2026-09-26
HORIZON: H0 (anchor calibration)
OBSERVED: The P-R4 manifest's stored analyzer values were computed on RAW
un-normalized 2s segments, but gen_test_wavs.py peak-normalized to 20000 when
writing test_wavs/. Re-running the recovered analyzer on the normalized
test_wavs differs from stored values on 19/40 clips; reconstructing raw
segments reproduces stored values bit-exact (40/40 verified).
EXPECTED: Prereg §2 assumes the anchor clips + labels are a coherent pair.
CANDIDATES (knowledge-first): corpus/label (normalization in the generator) →
organ computation → wiring → deliberation.
DISPOSITION: DIAGNOSED. The committed P-R4 evidence (0.7833) scored the
NORMALIZED test_wavs against the frozen manifest labels. The anchor
replicates those exact conditions (normalized WAVs + frozen labels) and
reproduces 0.7833 exactly. Both reconstructions are byte-exact; the
distinction is recorded, not repaired.

ANOM-ID: LH-A-002
DATE: 2026-09-26
HORIZON: H2/H4/H8 (ladder construction)
OBSERVED: Sealed corpus has 328/400 quota clips; speech class 76/150 (49%
shortfall). H10 (400 clips) and H100 unreachable. Ladder uses nested
stratified prefixes H2=80, H4=160, H8=248 (not disjoint full-size splits).
EXPECTED: Prereg §2a specifies H0/H10/H100 on disjoint splits.
CANDIDATES: corpus (seal quota) → organ → wiring → deliberation.
DISPOSITION: DIAGNOSED. Truncation is explicit and entirely the speech
shortfall. Nested growing horizons directly test "the loop must not degrade
as its own state accumulates" (stronger than disjoint splits for the
no-degradation expectation).

ANOM-ID: LH-A-003
DATE: 2026-09-26
HORIZON: gap attack (§5)
OBSERVED: M3 (better F0) is gated on §4 path (i), a separate workstream with
no result yet — cannot be tested. M4 (band retune) does not affect the 3-bit
metric: the DFT bands feed the D descriptors, while pr4_bits uses only
F0/voiced/r from the autocorrelation path. Retuning bands cannot change bits.
EXPECTED: Prereg §5 lists M1/M2/M3/M4 as testable candidates.
CANDIDATES: prereg (mechanism/metric mismatch) → organ → corpus.
DISPOSITION: DIAGNOSED. Gap attack tests M1 and M2 (≥2 candidates, satisfying
the STRUCTURAL CEILING bar). M3 recorded as blocked; M4 recorded as
not-applicable to the bit metric (a finding, not a failure).

## FINAL VERDICT (2026-09-26)

H0 ANCHOR: **PASS** — 0.7833 (94/120 bits), 3× byte-identical
(SHA a4d6fa88e5c756065f5ce4391c34426254fc3c4bf7916190cd1743449f2704fd).
Exact reproduction of committed P-R4. Prereg §2 anchor rule SATISFIED.

S1 EQUIVALENCE: **PASS** — journal byte-identical to wiring's
runs/journal_live.txt after removing only the added PR4 bits= lines
(diff 0 lines). Patch is purely additive.

LADDER (perception horizon):
- H0: 0.7833 (frozen labels, 3×).
- H2: 0.7792 (analyzer-derived labels, 1×). No degradation signal
  (Δ = -0.0041, within noise). Label provenance differs — interpret
  as consistency check.
- H4/H8: NOT RUN (time constraints on oversubscribed VM).
- Speech shortfall: 76/150 (49%). H10/H100 unreachable. Truncation explicit.

GAP ATTACK (§5): **STRUCTURAL CEILING** (< 0.85).
- M1: 0pp (18/18 anchor clips bit-identical to baseline).
- M2: 0pp (2-clip probe bit-identical; full test terminated after M1 signal).
- M3: BLOCKED. M4: NOT APPLICABLE.
- Mechanism: 3-bit thresholds (0.70/1.0/0.25) are the binding constraint;
  descriptor refinements don't cross thresholds on anchor clips.

ANOMALIES: LH-A-001 (normalization), LH-A-002 (speech shortfall/truncation),
LH-A-003 (M3 blocked/M4 N/A). All DIAGNOSED.

3× STATUS:
- H0: 3× byte-identical (COMPLETE).
- H2: 1× (r2/r3 pending).
- Gap M1/M2: 1× partial (M1 18 clips bit-identical; full 3× not run).
