# RETIREMENT CERTIFICATE — Arm B-8 (fixed 8-byte chunks)

**Verdict: RETIRED (KILLED at size level)** — 2026-09-21
**Arm:** B-8 · **Round:** r1 · **Scale:** 1x · **Family:** CTRL (fixed-size chunks)
**Frozen prereg:** `units/PREREG_FREEZE.md` commit `b0b9140c0eda` (branch `tnn-native-lab`)
**Brief:** `units/arms/briefs/B-8.json`

## The binding criterion that fired

Brief B-8.json, kill field (verbatim):

> A size retires when another B size strictly dominates it on M1/M2/M3 both corpora.

B-16 strictly dominates B-8:

| Metric | B-8 | B-16 | Relation |
|---|---|---|---|
| M1 prose (recall/boundary) | 100.0 / 100.0 | 100.0 / 100.0 | tied |
| M1 code (recall/boundary) | 100.0 / 100.0 | 100.0 / 100.0 | tied |
| M2 T1/T2 prose+code, T3 synth (ETC) | 1 / 1 / 1 / 1 / 1, final 100/100 | 1 / 1 / 1 / 1 / 1, final 100/100 | tied |
| M3 (survival / fresh) | 100.0 / **67.6, FROZEN-UNDER-PRESSURE → cell 0** | 100.0 / **100.0, CLEAR** | B-16 strictly better |

B-16 is verified from its own committed scorecard
(`units/arms/B-16/scorecard_r1_1x.json`): M1 100/100 both corpora, M2 ETC=1
every tier × corpus with final 100/100 and ep0=0.0, M3 survival 100.0 /
fresh 100.0 / CLEAR / 8,050 mgmt entries. B-64 (the harness validator) likewise
holds M3 at 100/100 CLEAR per the prior crew's inspection. B-8 is therefore
strictly dominated on M3 with M1/M2 tied at ceiling on both corpora. **The
retirement rule fires. B-8 is retired as a size.**

(B as a family is NOT killed by this: the family-kill bar requires a smart
arm to beat the best B size by ≥2x on M3 at equal-or-better M1. That is the
coordinator's comparison to run.)

## Why B-8 fails M3 — adjudicated, not assumed

The r1 battery measured M3 = `100.0, 67.6, 64050, 50, FROZEN-UNDER-PRESSURE`.
The follow-up adjudication (this crew, 2026-09-21) confirmed the 67.6 is a
**real measurement of the real mechanism under the correct protocol**, not a
build defect in the metric path:

1. **Protocol reading verified against the frozen prereg.** PREREG_FREEZE.md
   M3: "the churn phases ingest 7,000 fresh units … 500-unit fresh sample must
   show recall ≥ 80%". The churn fixture `churn_fresh.bin` is exactly 7,000
   64B spans (3,000 + 4,000), so the prereg's "units" in the churn phases are
   the fixture's 64B spans — the crew's span-based phases and 500-span fresh
   sample implement the frozen spec literally. (V = 1,000 units stays in
   arm-native 8B chunks: V is drawn from the prose/code corpora, where the
   arm's unit is the chunk.)
2. **Independent reproduction.** Current source rebuilt with the frozen
   toolchain (`znc_linux_x86_64_abed8aa1`); M3 run twice, byte-identical
   metric lines: `M3,100.0,67.6,64050,50,FROZEN-UNDER-PRESSURE`.
3. **Mechanism (eviction-victim log).** A 50,000-victim instrumented run shows
   eviction is block-level FIFO: phase-3 victims are chunks 24000–50999 plus
   2,000 hash-scattered victims in 51000–53999; live set is
   51001–55999 (3,000 chunks). The 500-span fresh sample (chunks 52000–55999
   = 4,000 chunks) therefore recalls 2,706/4,000 = 67.6%.

**The freeze is genuine granularity pressure.** C_M3 = 4,000 slots holds 4,000
chunk units; V pins 1,000; only 3,000 fresh chunks can survive. The fresh
sample demands 4,000. Even insertion-order-perfect FIFO would score 3,000 /
4,000 = **75.0% < 80%** — the FROZEN-UNDER-PRESSURE flag (survival ≥ 90 AND
fresh < 80 → M3 = 0) fires regardless. B-8's 8×-finer granularity costs it 8
slots per fixture span where B-64 spends 1; that capacity cost is exactly what
the distinguisher is built to surface. The arm manages honestly (64,050
management entries, 50/50 weaken ops processed per policy, V survival 100.0)
— it is not frozen, it is out of room. The flag's letter fires; its intent
(undeclared freezing) does not match; the rule is applied literally per the
frozen spec.

**Secondary wart (verdict-irrelevant, logged not fixed):** the insertion queue
stores slot numbers, so stale entries alias reused slots and within-block
victim selection is hash-scattered rather than insertion-ordered (this is the
67.6 vs 75.0 gap). It changes no flag and no verdict — both numbers sit below
the 80% bar — so production source was left untouched (no behavior change
without a verdict at stake).

## What B-8 proved (kept for the record)

- Boundary placement truly does not matter for recall: M1 100/100 on both
  corpora, M2 ETC=1 everywhere, M4 100/100 revision both classes both
  corpora, M6 100/100/100 both directions with the 15-point validity gate
  PASS, M8 determinism gate PASS. The "does boundary placement matter, or just
  existence?" question (§3 mechanism) is answered: existence is enough.
- The cost of 8B granularity is capacity under pressure (M3 cell 0) and
  per-byte cost (M5 memory 6.065 B/B vs 1.5× bar; audit 128.2 entries/KB vs
  10/KB bar) — both FAILs are honest measurements of the same granularity
  price, not defects.
- B-8's r1 row stands as committed evidence: `run/battery_r1/scorecard_r1_1x.json`.

## Disposition

- B-8 retires as a size. Its evidence stays in the repo; no further scales or
  rounds for B-8.
- The B family continues with B-16/B-64 (and any surviving sizes) until the
  family-kill bar is adjudicated by the coordinator.
- Production source `cl/arm.zag` unchanged by the adjudication (the wart is
  documented, not patched — patching a retired arm's non-verdict-affecting
  wart would invalidate the committed evidence for zero gain).

Committed to `tnn-native-lab` with code, evidence, and scorecard per the crew
contract. Dead arms die in public.
