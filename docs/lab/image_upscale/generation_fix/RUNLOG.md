# RUNLOG — Crew A: key-ambiguity fix, generation path

Date: 2026-09-27. Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
Workdir: `docs/lab/image_upscale/generation_fix/`. No commits by this crew (coordinator commits).

## 0. Preregistration

[PREREG.md](PREREG.md) was written BEFORE any arm was implemented or run. It freezes
the three arm designs, TNN-deliberation design, and all kill criteria. Corrections
to the record: PREREG.md is dated 2026-09-26 in its header; the session ran
2026-09-27 UTC. Content is unaffected.

Corpus constants (measured from `vocab.bin` by `src/corpstat.zag`, two
byte-identical runs, SHA `57bfffc855640851b62c7e2341d5b7cd05c3c63844d4f41638f0a3d8456f9aaa`):

| Constant | Value | Meaning |
|---|---|---|
| τ_min | 2,985,492 | 25th percentile of atom key-variance-per-value ×1000 (scales 0–3) |
| τ_mid | 4,411,296 | 75th percentile (reference only; RUNLOG corrects an earlier "50th" label) |
| R_band | 1,153 | 75th percentile of corpus full-resolution/key-energy ratio ×1000 (band used by Arm 2) |

Independent Python cross-check (2026-09-27, truncating integer channel means
matching Zag's `/` semantics, signed i16 keys): nv=176, nt=172,
τ_min=2,985,492, τ_mid=4,411,296, R_band=1,153 — **exact agreement on all six
values**. The earlier Python pass (τ_min=2,985,074) used float means; the
difference was the mean convention, not the data. Zag values are authoritative
(the arms use them).

## 1. TNN deliberation (before implementation)

`src/delib.zag` replicates the baseline SHAPES fit EXACTLY (full 32→4 recursion,
SHAPES-first, raw input) and then measures, per take: block smoothness,
key ambiguity (atoms within 2× winner SSD), winner correlation P, each
arm-rule's verdict, and the take's own 2×-construction SSE vs GT.

Replication check: takes=35, nofits=11, G=18343607 — byte-exact vs the
baseline's `GEN_TRACE.txt`. Analysis best-atom matched the recorded take atom
on all 35 takes (0 mismatches).

Trace: `runs/delib_out2/DELIB_TRACE.txt`
(SHA-256 `11d60e626d56b8e9dcd0aa20500d43dff014c3a3007efe55c8118a8768f1ff1c`,
two byte-identical runs).

Findings (bridge):

- The worst take is x=192,y=32, 32×32, si=0, **atom 42 (brick wall)**,
  own-construction SSE 45,688,705 vs GT — the single largest error source.
  The four si=0 atom-42 takes sum to ≈162M of 268M total SSE (60%).
- **The bad block is NOT smooth** by the corpus τ_min: σ²_B×1000 = 3,575,392
  > τ_min = 2,985,492. The "smooth arch" description in HONEST_RESULT.md was
  imprecise; the block has mid-range variance.
- Key ambiguity is extreme: **25 of 63 atoms within 2× of the winner's SSD**.
- Arm-rule verdicts on the bad take: A1=take (fine winner IS in coarse top-3),
  A2=take (block not smooth → rule passes through), **A3=reject** (<2 of the
  top-3 candidates have positive correlation).
- Collateral (takes each rule would reject of 35): A1=6, A2=21, A3=23.
- **Advisory vote: Arm 3.** Vote is advisory — the head-to-head test decides.
  CORRECTION (2026-09-27, instrumented debug build): the trace's REASON prose
  ("the worst take's winner fails the correlation double-validation — its
  high-frequency directions are absent from the input block") is contradicted
  by the recorded data and is RETRACTED. Instrumented values for the bad take:
  top-3 candidates t1=42, t2=0, t3=0; correlations p1=+4,391,538, p2=p3=0;
  nsurv=1; winner's SSD wsse=9,988,165; gain over nofit e−wsse=995,440 ≥
  bar=27,648 (the bar would have passed). Atom 42 was the SOLE candidate
  beating the nofit baseline, so the top-3 set had one member; the winner
  correlates POSITIVELY, but the double-validation requires ≥2 survivors
  (nsurv=1<2) — the match is rejected as UNCORROBORATED, not as contradicted. The advisory vote (Arm 3) stands;
  only the explanation is corrected. The frozen trace file is preserved as-is;
  this note is the correction of record.

## 2. Arm implementations

Generated from the pristine baseline copy `src/azgen_a0.zag` by
`src/gen_arms.py` (scripted edits, auditable diffs). All arms mediate the take
decision through `ubest`/`ugain`; the scan, split logic, commit, render, and
metrics paths are untouched. All three arms are weakly stricter than baseline
on individual takes (none can take where baseline didn't).

- **Arm 1** (`azgen_a1.zag`): cross-scale key agreement. The fine-key winner
  must rank in the coarse-key (2×2-downscaled, deviation-space) top-3, else
  the take is rejected (ugain=0; split may still win). Auto-pass if the coarse
  key is degenerate (<2 in either dim).
- **Arm 2** (`azgen_a2.zag`): smooth-region energy-band gate. Smooth ⟺
  e×1000 < τ_min×nval. A smooth block may take atom ai only if
  eA_full_perval_x1000[si][ai]×nval ≤ e×R_band (eA measured from vocab at
  startup); NULL always allowed; take iff the band-restricted best clears the
  9/value bar. Non-smooth matching unchanged.
- **Arm 3** (`azgen_a3.zag`): Fable's discipline. Smooth → reject. Else top-3
  key-SSD candidates, positive-correlation double-validation, require ≥2
  survivors, strict 18/value bar when the survivor winner differs from the
  original key winner; rejection falls back to measured means (nofit
  mean-fill). No bicubic anywhere in the pipeline.

All four binaries built with 0 errors. `azgen_a0` reproduces the frozen
baseline outputs byte-identically (bridge
`2028ba1dd5cf12e25300c759b72febacab4853a03d1c1302656a7a7a3afa4135`,
sky `842558193c0a56fc73dd86ea160406df8c7cd5023450b687b77043939a8e2408`).

## 3. Bridge + sky results (per binary, two byte-identical reruns each)

| Image | Arm | Gen PSNR | Gen SSIM | Bicubic PSNR | Bicubic SSIM | Δgen vs a0 | SHAPES takes/nofits |
|---|---|---|---|---|---|---|---|
| bridge | a0 (baseline) | 18.47 | 0.4620 | 25.89 | 0.8157 | — | 35 / 11 |
| bridge | a1 | 18.48 | 0.4624 | 25.89 | 0.8157 | +0.01 | 27 / 11 |
| bridge | a2 | 18.16 | 0.4475 | 25.89 | 0.8157 | −0.31 | 14 / 13 |
| bridge | a3 | 18.91 | 0.4781 | 25.89 | 0.8157 | **+0.44** | 15 / 13 |
| sky | a0 (baseline) | 22.75 | 0.5890 | 33.20 | 0.9176 | — | 24 / 84 |
| sky | a1 | 22.75 | 0.5890 | 33.20 | 0.9176 | +0.00 | 23 / 84 |
| sky | a2 | 22.36 | 0.5775 | 33.20 | 0.9176 | −0.39 | 5 / 92 |
| sky | a3 | 26.27 | 0.7114 | 33.20 | 0.9176 | **+3.52** | 4 / 93 |

Rerun SHAs (upscale_gen.bmp, run1 = run2 byte-identical for every arm/image).
Full 64-hex SHAs retained: a0 bridge/sky (below) and all four arms' diverse
r1 logs (`runs/shas_a*_diverse_r1.txt`; a0/a3 r2 logs also retained). a1/a2/a3
bridge/sky reruns were SHA-compared byte-identical with 16-hex prefixes
retained in `runs/scores_sofar.txt`; a1/a2 diverse r2 SHA logs were compared
inline (all IDENTICAL, recorded here) with only r1 logs retained.

- a0: bridge `2028ba1dd5cf12e25300c759b72febacab4853a03d1c1302656a7a7a3afa4135`
  (matches frozen baseline), sky
  `842558193c0a56fc73dd86ea160406df8c7cd5023450b687b77043939a8e2408` (matches).

Kill-bar evaluation (bridge/sky):

- Arm 3 bridge improvement: 18.91 − 18.47 = **+0.44 dB < 2 dB → Fable's kill
  criterion FIRES** (PREREG §kill, "improves <2 dB over 18.47 dB on bridge").
- Arm 3 top-level rejection: incremental nofit fraction at si=0 =
  (13−11)/24 = **8.3% < 30%** → rejection prong does not fire. (Definition:
  the prereg's ">30% (nofits fraction)" can only be read incrementally — the
  baseline itself sits at 11/24 = 45.8%, so an absolute reading would kill a
  no-op arm. Documented here for auditability.)
- Arm 1: +0.01/+0.00 dB — no meaningful beat. Arm 2: loses on both images.

## 4. Diverse held-out set (9 sealed photos, Crew B)

Harness: `diverse_set/eval_all.py` (frozen metrics.py, 2×2 box round-half-up
inputs). a0 r1 reproduces Crew B's `results/RESULTS.tsv` on all 9 rows exactly.
Each arm binary ran the full set TWICE; per-image `upscale_gen.bmp` SHAs
compared r1 vs r2 (all IDENTICAL — see `runs/shas_a*_diverse_*.txt`).

| Image | a0 gen | a1 gen | a2 gen | a3 gen | Bicubic |
|---|---|---|---|---|---|
| fabric | 21.47 / 0.3662 | 21.47 / 0.3662 | 21.47 / 0.3662 | 21.47 / 0.3662 | 26.73 / 0.6588 |
| woodgrain | 18.37 / 0.5408 | 18.40 / 0.5409 | 18.23 / 0.5252 | 18.59 / 0.5359 | 25.51 / 0.9065 |
| treebark | 18.94 / 0.5375 | 18.92 / 0.5362 | 18.44 / 0.5036 | 18.54 / 0.5094 | 27.97 / 0.9287 |
| calmwaters | 19.46 / 0.6327 | 19.42 / 0.6295 | 19.21 / 0.6147 | 19.29 / 0.6166 | 22.06 / 0.7532 |
| portrait | 21.19 / 0.4391 | 21.17 / 0.4370 | 20.61 / 0.4060 | 20.76 / 0.4093 | 27.46 / 0.6767 |
| car | 22.92 / 0.6698 | 22.96 / 0.6703 | 22.30 / 0.6406 | 22.39 / 0.6423 | 32.44 / 0.9178 |
| building | 14.96 / 0.2675 | 15.00 / 0.2681 | 15.00 / 0.2681 | 15.00 / 0.2681 | 16.29 / 0.3187 |
| cat | 16.60 / 0.3594 | 16.57 / 0.3559 | 16.38 / 0.3392 | 16.43 / 0.3422 | 20.15 / 0.5626 |
| market | 18.36 / 0.4343 | 18.31 / 0.4291 | 17.86 / 0.3953 | 17.89 / 0.3976 | 22.92 / 0.7812 |

Deltas vs a0 (gen PSNR dB): a1 ∈ [−0.05, +0.04] (inert); a2 loses 8/9
(worst −0.62 car); a3 loses 7/9 (worst −0.53 car, best +0.22 woodgrain).
Full TSVs: `runs/scores_a{0,1,2,3}_diverse.tsv`.
Note: a1's first r1 (8 rows, market killed by ENOSPC) is preserved as
`runs/scores_a1_diverse_r1_partial.tsv`; the full double-run was redone.

## 5. Mechanism analysis

1. **Input-resolution fit does not predict high-resolution correctness**
   (confirmed again): the rejected takes had high input-res gain (e.g. 324
   dB/value on the bad block); the damage appears only at 2× construction.
2. **The failure is key ambiguity + correlation mismatch, not smoothness.**
   The worst take's block is mid-variance (not smooth by τ_min), matched 25
   near-equivalent keys, and its winner's correlation structure didn't
   validate. Arms 1 and 2 target premises that don't hold on the actual
   failure: the bad winner IS in the coarse top-3 (A1 passes it), and the bad
   block is NOT smooth (A2 passes it through).
3. **Arm 1 is inert**: the coarse key agrees with the fine key even on the bad
   match — cross-scale consistency doesn't discriminate this failure mode.
4. **Arm 2 hurts**: τ_min mislabels mid-variance blocks as smooth, and the
   band-restricted replacements (or mean-fill) are worse than the takes they
   replace (−0.31/−0.39 dB).
5. **Arm 3 is the only helping direction** (+0.44/+3.52), matching the
   deliberation's advisory vote — but its bridge gain (+0.44 dB) is far below
   Fable's 2 dB bar.
6. **The 2 dB bar looks miscalibrated against the mechanism.** The four brick
   takes total ≈162M of 268M SSE, but rejecting them only nets 26M (mean-fill
   and LINES refills on those footprints are barely better than the bad
   takes). A rejection-only rule was unlikely to ever deliver 2 dB
   (≈37% SSE cut) on bridge. This is flagged as analysis for the coordinator,
   not as an override: the prereg is frozen and the kill is reported as
   written.

## 6. Disk incident (2026-09-27 ~02:52 UTC)

Home disk hit 100% (other crews filling it concurrently) during the a1
diverse r1 run: the market.jpg output wrote 0 bytes ("gen bmp write failed",
rc=1 — the binary correctly reported the failure; eval_all.py then failed on
the empty BMP). No silent corruption: the failure was loud. After freeing
~330 MB of my own scratch, all runs were redone sequentially with a low-disk
profile (r1 cleaned before r2). The 8 completed a1 r1 rows were valid and were
kept as `runs/scores_a1_diverse_r1_partial.tsv`; the full double-run was
redone afterward.
