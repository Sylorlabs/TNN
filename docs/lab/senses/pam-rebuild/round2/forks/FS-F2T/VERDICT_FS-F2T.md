# VERDICT_FS-F2T.md — crew FS-F2T final verdict

Date: 2026-09-24. Prereg: `PREREG_FS-F2T.md`, frozen and committed alone
(commit `ff90517b29d62d2c1cdf748458f1376ef3def6e6`) BEFORE any fresh
evaluation result was generated.

## Mechanism (what changed)

`src/f2t_form.zag` is FS-E2's `fs2_form.zag` with ONLY the timbredisc path
replaced (PREREG_FS-F2T §3): exact-bin Q20 Goertzel at 440·h Hz (h=1,2,3;
bins k=880h; N=32000; coefficients 2065924/1973170/1821652), input
x = sample/32 (trunc), overflow-safe power
p = s1²+s2²−((s1·s2)/2²⁰)·c, per-mille ratios r2=(p2·1000)/p1,
r3=(p3·1000)/p1, nearest frozen-theory-template
(PURE (0,0), BRIGHT (1960,2560), DARK (78,6), RICH (640,384)), ties to
earliest in PURE→BRIGHT→DARK→RICH order. The five other formation
functions are byte-for-byte semantically unchanged (verified by diff and
by exact reproduction of FS-E2's Phase-0 numbers below). Pure Zag;
zero RNG in any decision path.

## Gating bars (mechanical)

| Bar | Result | Floor | Verdict |
|---|---|---|---|
| (a) timbredisc, fresh deterministic draw n=1000 | **1000/1000 = 100.00%** | ≥ 85.00% | PASS |
| (b) colordisc no-regression (1080) | 1004/1080 = 92.96% | ≥ 91.96% | PASS |
| (b) pitchdisc no-regression (720) | 705/720 = 97.92% | ≥ 96.92% | PASS |
| (b) motiondir no-regression (564) | 545/564 = 96.63% | ≥ 95.63% | PASS |
| (c) byte-identical determinism ×2 | 4/4 TSVs identical (sha256 match); logs identical after run-number redaction | required | PASS |

Fresh-draw confusion (judgment × truth): perfect diagonal — PURE 250/250,
BRIGHT 250/250, DARK 250/250, RICH 250/250. Truth balance 250/class as
specified.

The no-regression batteries reproduce FS-E2's Phase-0 counts EXACTLY
(1004, 705, 545), confirming the other five formation paths are unchanged.

Determinism evidence (evidence/eval/sha256sums.txt):
- run1/run2 `fresh_timbredisc.tsv`: `81933c51…ade` / identical
- run1/run2 `reg_colordisc.tsv`:    `928e4187…3e0` / identical
- run1/run2 `reg_pitchdisc.tsv`:    `1c877fe2…2d0` / identical
- run1/run2 `reg_motiondir.tsv`:    `6a95fc4b…448b4` / identical
- The four `.log` files differ ONLY in the run-numbered output filename
  embedded in the driver's own status line; after `s/run[12]_/runN_/`
  redaction all four are byte-identical. The binary's per-fixture
  judgments (captured in the TSVs) are bit-for-bit identical across runs.

Fresh draw spec (PREREG_FS-F2T §5): frozen `gen_r2a.gen_timbredisc`,
`Rng(stream_seed(20260923, 404, i))`, i in 720..1719, family=0, truth from
the frozen generator. Manifest sha256:
`c6c5539ef51533a42a01823b3fab3c63d138ffe25ae7ee93d3c2d29869b21690`.

## Non-gating diagnostics

- Per-class measured (r2, r3) on the fresh draw and min margin to the
  nearest wrong template: PURE (0,0) / 78.2; BRIGHT [1938,1984]×[2530,2595]
  / 2476.1; DARK (78,78)→(78,6) exact / 78.2; RICH [635,645]×[382,387] /
  667.5. The nearest boundary is 78 template units away; integer
  truncation cannot cross it.
- Adversarial diagnostic (frozen 985-fixture b_adv timbredisc battery,
  same binary): **980/985 = 99.49%**. All 5 misses are truth=DARK →
  judgment=PURE on TMB-3 sub-3 near-PURE distractors (integer r2=39 vs
  the PURE/DARK boundary 39.23 — within 1 template unit of the boundary).
  The high-harmonic family that defeated FS-E1 (33 FI frozen) is otherwise
  clean: no misses on TMB-3 weak-fundamental, extra-3rd, or pushed-bright
  distractors.
- Cross-validation: an independent C implementation of the identical
  integer arithmetic agrees with the Zag binary on 1000/1000 fresh-draw
  judgments.

## Verdict

**ALIVE.** All three gating bars pass: (a) 100.00% ≥ 85% on the fresh
n=1000 draw, (b) no regression on any of the three unchanged tasks
(exact FS-E2 Phase-0 counts), (c) byte-identical determinism across two
full runs. Timbredisc formation improves from FS-E2 Phase-0 38.89%
(280/720) to 100.00% (1000/1000) on fresh controls and is eligible for
FS-E2 install scope.

## Commits

- Prereg (alone, before any fresh result): `ff90517b29d62d2c1cdf748458f1376ef3def6e6`
- Fresh fixtures (2001 files): `e4aff5d49b6c6d352df491eaeffdbd59927ba078`
- Evidence + verdict: <final commit hash — filled at commit time>

## Files

- `PREREG_FS-F2T.md` — frozen preregistration
- `src/f2t_form.zag`, `src/R33_NATIVE_IO_V1.zag` — pure-Zag source
  (built with `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`;
  binary `src/f2t_form` NOT committed)
- `src/gen_fresh.py`, `src/run_phase0.py`, `src/run_eval.sh`,
  `src/score_bars.py` — Python glue/analysis only
- `fixtures_fresh/` — 1000 .r2fx + .truth + manifest.tsv
- `evidence/eval/` — run1/run2 logs+TSVs, sha256sums.txt,
  fresh_timbredisc.list, adv_timbredisc.list, adv_timbredisc.tsv
- `VERDICT_FS-F2T.md` — this file

Nothing in this verdict is UNMEASURED: every number above was measured
by the committed binary on the committed fixtures.
