# Workstream B — Untrained Structural Analysis of Novel Inputs

Question: can TNN structurally analyze genuinely novel audio/image/video content
it was never trained to identify?

Method: a pure-Zag, zero-RNG deterministic measurement program (`tnn/uanalyze.zag`)
that computes waveform/pixel/frame statistics first and only then emits
conservative structural sentences. No classification, no naming — measurable
structure only.

Protocol:
1. Six novel inputs acquired fresh 2026-09-26 (archive.org, Wikimedia Commons).
2. Human structural descriptions written from independent plots/views and
   SHA-256-sealed (`human/SEAL.log`) BEFORE any TNN run on the inputs.
3. Analyzer calibrated on synthetic fixtures only (`smoke/`), then frozen
   (`tnn/FROZEN_SHA256.txt`).
4. Each input run twice; all outputs byte-identical.
5. Claim-by-claim comparison (`compare/worksheets.md`), verdict (`compare/VERDICT.md`).

Result: 10 MATCH / 20 MISS / 3 WEAK MISS / 3 PARTIAL / **5 HALLUCINATION**.
The bar FAILS (false positives worse than withholding). Hallucinations:
fabricated 100 ms rhythm on thunder + bell (envelope-autocorr lag-2 artifact),
a phantom second transient layer in the cricket chorus (AM pulses double-counted),
and "smooth, little fine detail" on frost + terraces (texture judged at 80x45,
fine detail averaged away). Honest boundary documented in the verdict.

Layout:
- `tnn/` — analyzer source (frozen copy + SHA-256).
- `human/` — sealed human descriptions (6) + seal log.
- `inputs/` — transport-normalized analyzed fixtures (WAV/PPM/frames).
- `out/` — TNN outputs (run 1 of 2; run 2 byte-identical).
- `smoke/` — synthetic calibration fixtures.
- `compare/` — claim worksheets + verdict.
- `SOURCES.md` — original URLs + SHA-256 (originals not committed).
