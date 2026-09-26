# Workstream B — Untrained Structural Analysis of Novel Inputs

> **STATUS: EXPLORATORY — INVALID FOR THE CONFIRMATORY BAR.**
> This directory records the 2026-09-26 exploratory run. A checkpoint review
> found protocol violations that invalidate it as a binding verdict:
> (1) the analyzer source was changed AFTER exposure to the real inputs
> (the RIFF LIST-chunk fix, the isort_copy fix, and the dynamic-range
> zero-poisoning fix were all triggered by real-input results and the same
> inputs were rerun afterward) — violating the required freeze-before-real-runs
> separation; (2) the committed smoke fixture `smoke/loudclick.wav` was
> generated with `np.random.RandomState(7).randn`, violating the zero-RNG law;
> (3) the analyzer carried arbitrary caller read caps (4,000,000 / 2,000,000 /
> 300,000 bytes); (4) the novelty audit was methodologically invalid (raw
> SHA-256 passed to `git cat-file`, but the repo uses Git object IDs).
> The five hallucinations found here remain valuable diagnostics, but the
> verdict below is NOT a binding Workstream B result.
> The binding confirmatory run (frozen-then-fresh protocol, remediated
> analyzer, correct novelty audit) is in `c2/`.

Question: can TNN structurally analyze genuinely novel audio/image/video content
it was never trained to identify?

Method: a pure-Zag, zero-RNG deterministic measurement program (`tnn/uanalyze.zag`)
that computes waveform/pixel/frame statistics first and only then emits
conservative structural sentences. No classification, no naming — measurable
structure only.

Protocol (as run — see STATUS note above for violations):
1. Six novel inputs acquired fresh 2026-09-26 (archive.org, Wikimedia Commons).
2. Human structural descriptions written from independent plots/views and
   SHA-256-sealed (`human/SEAL.log`) BEFORE any TNN run on the inputs.
3. Analyzer calibrated on synthetic fixtures only (`smoke/`), then frozen
   (`tnn/FROZEN_SHA256.txt`).
4. Each input run twice; all outputs byte-identical.
5. Claim-by-claim comparison (`compare/worksheets.md`), verdict (`compare/VERDICT.md`).

Exploratory result: 10 MATCH / 20 MISS / 3 WEAK MISS / 3 PARTIAL / **5 HALLUCINATION**.
Hallucinations: fabricated 100 ms rhythm on thunder + bell (envelope-autocorr
lag-2 artifact), a phantom second transient layer in the cricket chorus
(AM pulses double-counted), and "smooth, little fine detail" on frost +
terraces (texture judged at 80x45, fine detail averaged away).
Honest boundary documented in the verdict.

Layout:
- `tnn/` — exploratory analyzer source (frozen copy + SHA-256).
- `human/` — sealed human descriptions (6) + seal log.
- `inputs/` — transport-normalized analyzed fixtures (WAV/PPM/frames).
- `out/` — TNN outputs (run 1 of 2; run 2 byte-identical).
- `smoke/` — synthetic calibration fixtures (NOTE: `loudclick.wav` was
  RNG-generated; replaced by an analytical fixture in `c2/smoke/`).
- `compare/` — claim worksheets + exploratory verdict.
- `SOURCES.md` — original URLs + SHA-256 (originals not committed).
- `c2/` — BINDING confirmatory run (remediated analyzer, fresh inputs,
  frozen-before-exposure protocol, correct Git-blob novelty audit).
