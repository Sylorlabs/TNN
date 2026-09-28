# Phase-3 Preregistration — Audio Semantic Growth (Impulse-Channel + Joint Factorization)

**Order:** Micah, 2026-09-26 ~12:52 PDT ("the gate's good — now the next frontier").
**Goal:** shrink the RESIDUAL SHARE (the lossless closure cost) by growing the
semantic model's UNDERSTANDING. A gain that doesn't shrink the residual is not
understanding.
**Gate (inviolable):** `reemit` mode 10 stays 359/359 byte-identical (`cmp` on
WAVs). The contract is the gate, not the format — the v6 extension layout may
change. Determinism: two runs byte-identical.

## Baseline (adopted, verified 2026-09-26)

`results/baseline_decomp.json` — 359 clips, 5 classes. Semantic-only RMS
(output domain, LSB): field 214.4, child 199.2, speech 152.0, prosody 212.0,
lowf0 126.0. Semantic corr 0.9923–0.9976. Residual (closure) RMS per class in
`results/decompose_summary.txt`.

## Where the semantic error lives (measured, waveform-first)

| # | Locus | Measurement | Per-class numbers |
|---|---|---|---|
| 1 | **Tail events** (quantizer misses) | 67–76% of excitation-domain quantization-error energy sits in \|e_q\|>4σ outliers. Median 817–1690 events/clip, 6–8 samples long, ~11 kHz centroid, −0.8 Np/ms decay: brief HF transients (onsets/clicks), not long clang tails. | all classes |
| 2 | **HF hash** | Semantic render carries EXCESS HF vs source (not dullness — the "gap-8 dullness" hypothesis is FALSIFIED): child 16k+ +4.8×, prosody 12–16k +36×, speech 12–16k +2.1×. White quantizer error through LPC HF resonances. | child, prosody, speech |
| 3 | **Harmonic near-dead** | boost=1.00 for 341/359 clips; gate (1.5,10.0) admits 11; use_h=1 on 11/359 clips. The PLM mechanism contributes ~nothing corpus-wide. | all classes |
| 4 | **amp fitted-but-unused, wrongly fitted** | hear fits amp[per] against raw res, IGNORING the proto[q] the semantic path also renders → double-counting. Naive "use amp in mode 11" REGRESSES (−48%…−331% excitation RMS, measured). The intake's q is NOT pure nearest-prototype (1.5–2% differ) → q must NOT be refit (frozen knowledge). | 11 use_h clips |
| 5 | **Envelope** | 10 ms env_corr 0.9978–0.9995. NOT an error locus. No mechanism. | — |

## Deliberation records (white-box: what the model "notices" about itself)

**D1 — on tails:** "My scalar vocabulary voices the body of the excitation,
but chokes on onsets. An onset is not a scalar level — it is an EVENT: a
position and an amplitude. I will hear events explicitly: after the vocabulary
and the harmonic have spoken, I take the M largest remaining errors as
transient events (position, amplitude), so the dense residual keeps only what
no structure explains. This is the pulse-codebook half of excitation, which
my model was missing." → **H1 transient-event channel.**

**D2 — on amp:** "I fit the harmonic's per-period amplitude against the raw
residual, but my semantic render adds the vocabulary's voice too — so the
amplitude I fit is not the amplitude of what remains. I must fit the
amplitude against what the vocabulary LEAVES (res − proto[q]), jointly, the
same factorization in hear and emit." → **H2 joint per-period amplitude.**

**D3 — on refusal:** "My gate refuses the harmonic for 19 pitched clips.
For most, the harmonic explains nothing (r2≈0.02) — refusing is correct, and
forcing it would hallucinate. I will accept a refused clip ONLY if the
jointly-fit harmonic explains >10% of the remaining variance, and I will
verify per-clip that the semantic render improves — otherwise the refusal
stands." → **H4 r2-gated acceptance (test, likely kill).**

**D4 — on HF:** "My render is too bright above 12 kHz, not too dull. The
excess is white quantization noise amplified by my LPC's HF resonances —
and the largest white errors are exactly the tail events D1 removes. I will
re-measure HF bands after H1+H2 before designing any HF mechanism."
→ **H5 contingent on measurement.**

## Candidates (keep-or-kill by measurement)

| ID | Mechanism | Expected gain | Keep bar | Kill bar |
|---|---|---|---|---|
| H1 | Transient events: top-M (M=max(16, nr/500)) samples of \|res−proto[q]−amp·plm\| stored as (pos i64, amp f64); semantic excitation += impulses; residual = res − all | 16–44% excitation-RMS reduction (measured 0.1%); 21–51% at 0.2% | residual RMS shrinks ≥10%/class AND mode-10 green | residual unchanged or gate red |
| H2 | Joint amp: amp[per]=LS((res−proto[q]) ~ plm[hb]); mode-11 renders amp·plm; hear/emit same factorization | 0–6% on 11 use_h clips, never negative (measured) | no clip regresses in mode-11 | any clip regresses |
| H3 | +16 scalar tail levels at tail quantiles | 1–4% (measured) — SUBSUMED by H1 | — | **KILLED pre-implementation** |
| H4 | Accept refused (pT>0,use_h=0) clips iff r2(joint amp·plm on res−proto[q]) > 0.10 | 2–3 clips accepted, tiny aggregate | per-clip mode-11 improves for every accepted clip | any accepted clip regresses → KILL |
| H5 | HF shaping | contingent | 12k+ excess >+1.0 after H1+H2 | excess closed by H1 → CLOSE |

**Scalar tail levels (H3) are KILLED without implementation:** 16 extra levels
give 1–4% while the event channel gives 16–51% on the same error. Two
mechanisms for one locus is not understanding — the event model wins outright.

## What the model learns (plain language)

After H1+H2, the semantic model's theory of excitation is: *a harmonic part
with per-period amplitude + a scalar-voiced body + sparse transient events
for onsets* — instead of *harmonic + scalar body and hope*. The residual
keeps only dense unstructured hash. The model learns that onsets are events,
not levels.

## Metrics (all reported per class, before→after)

1. Semantic-only RMS + corr (mode 11) vs baseline table above.
2. Residual RMS (f64 nres) before→after — the closure cost. MUST shrink.
3. Residual information: gzip bytes of the nres section before→after; total
   v6 file bytes before→after (impulse overhead vs residual shrinkage).
4. Gate: 359/359 `cmp`-identical mode-10 WAVs; determinism: run twice.

## Implementation

Pure Zag, zero RNG, pinned toolchain
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
New binaries `phase3/src/resid3.zag` (hear) + `phase3/src/reemit63.zag`
(emit), derived from the phase-2 sources. Extension layout gains an impulse
section; magic `V6IMP!` (distinct from `V6EXACT!` so old/new files never
mix). q is COPIED (frozen intake knowledge), never refit. Impulse selection
is a deterministic min-heap (fixed tie-break: larger |rem| wins, then lower
index), output sorted by position.
