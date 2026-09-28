# AUTOPSY — KB4 judgment channels (Team 4)

**Date:** 2026-09-23. **Team:** 4 — KB4 judgment channels (C1 alive vs C2/C3 retired).
**Binding ground truth:** `docs/lab/kb/autopsy/channels2/f2appeal/F2_VERDICT.md`
(branch `tnn-native-lab`, sylorlabs/TNN) — **WRAPS**: F2 permanent retirement of
C2/C3-class judgment-side channels STANDS for the frozen threat model.
**Program context (Team 3, same dir):** PAMs v2 must ACCEPT TRUTHS — 0% false
installs (R2-4 proved reachable) plus installing TRUE judgments at high
confidence. This autopsy decides what channel architecture v2 may build on.

**Scope (G1):** everything below is scoped to the frozen threat model — one
adversary construction (δ≲σ band), two frozen senses, six tasks. It is not a
universal theorem that no judgment-side channel can exist (Sol adjudication,
f2appeal/debate/D3_sol_adjudication.txt §3).

---

## 1. What C1 DOES vs what C2/C3 DID — mechanism level

All three channels take the frozen judge's judgment J on a fixture and emit
INSTALL/WITHHOLD. None takes truth input. The difference is the **information
source** of the verdict.

| | C2 (transform-consistency) | C3 (noisy re-observation) | C1 (scout) |
|---|---|---|---|
| Rule | INSTALL iff J(T(x)) == L(J(x)) | INSTALL iff Jn(x) == J(x) | INSTALL iff A(x) == J(x) |
| Second input | Jt = J(T(x)) — the SAME frozen judge re-queried on the transformed fixture | Jn = J(noised(x)) — the SAME frozen judge re-queried on the noised fixture | A(x) — an INDEPENDENT analytic recomputation from the raw stimulus bytes |
| Source | `kb/autopsy/channels2/src/channel_c2.zag` (+`tcp_transform.zag`) | `src/channel_c3.zag` (+`c3_noise.zag`) | `src/c1scout_channel.zag` (+`c1scout_pitch.zag`) |
| Queries to the judge | 2 (original + transformed) | 2 (original + noised) | 1 (original only) |
| Measured | 0.0000 bits; F4 fired (43.5% false-install) | 0.0049 bits pooled; confidence member 0.0797 bits | **0.9968 bits, 15/15, 0.0% false-install** |

### 1.1 "Non-judgment-side" — operational meaning

"Judgment-side" = the channel's discriminating information comes from the
judge's **own reports under perturbation**: re-reading J on T(x) (C2) or on
noised(x) (C3) and checking self-consistency. Every input to the verdict
predicate is a report of the same compromised judge.

C1 is "non-judgment-side" because its discriminating information comes from
the **stimulus through an independent lens**, not from the judge at all: the
analytic A(x) is a white-box signal computation (pitchdisc: zero-crossing
pitch estimation on the raw .pcm bytes, `c1scout_pitch.zag`) that mirrors the
generator's public rule exactly. The judge is queried exactly once — the query
whose trustworthiness is in question — and never again.

### 1.2 What C1 uses that C2/C3 don't

An **independent measurement of the label-defining quantity**. The frozen
adversary fooled sense A by exploiting its coarse JND: on all 15 pitchdisc
test adversarials sense A answered SAME (its effective JND is coarser than the
generator's 0.5% rule). The zero-crossing analytic estimates f0/f1 directly
from the bytes, averaging over ~130–400 crossings, robust to δ≲σ
perturbations — so it recovers the true label on exactly the fixtures where
the sense is fooled. C2/C3 never look at the stimulus through any lens but J;
they have no access to the quantity the label is defined by.

### 1.3 What C1 refrains from doing — the move that killed C2/C3

C1 **never re-queries the compromised judge**. C2/C3's fatal move is treating
the fooled judge as a fresh evidence source on new queries: "ask again under a
transform / under noise and check consistency." But the frozen adversary's
fool is a **fixed point of the perturbation family**:

- **DPI (measured, all four debate camps accepted):** on sense A,
  J(T(x)) == L(J(x)) for all 92 test + 93 calibration fixtures. "Every
  deterministic channel that is a function of (J, Jt) is a function of J alone
  and adds zero information about Y" (TCP_VERDICT.md). C2 is the constant
  INSTALL function.
- **Noise-stability (measured):** judgments are 91.8% noise-stable, and the
  stability is uncorrelated with correctness: P(agree|Y=1)=0.939 vs
  P(agree|Y=0)=0.894. The fool is as deep in its basin as honest judgments.

Re-querying a judge whose compromise is a fixed point of every query you may
ask just re-samples the compromise. C1 refrains from the second query entirely.

---

## 2. KNOWLEDGE vs MACHINERY — the verdict

**Verdict: MACHINERY ceiling** (for the frozen threat model). C2/C3 did not
die for lack of knowledge. They died because the judgment-side architecture's
only information source — the compromised judge's self-reports — is
structurally uninformative against an adversary that fixes the fool across the
channel's whole query family.

### 2.1 The knowledge hypothesis was tested head-on — four times — and refuted

Micah's standing hypothesis is "facts first": failures are knowledge gaps that
teaching can supply. Each preregistered appeal test was a knowledge-flavored
recovery mechanism. All four were refuted (CON signed the refutations,
D3_con_update.md §2):

1. **"C2 didn't know the right transforms" → R3.** Three NEW transforms
   (vflip, signflip, fshift), none in the frozen family, chosen to break the
   DPI identity. The channel was handed the exact law (identity — the simplest
   possible) and F3 ≥95% calibration-legibility gates verified the judge
   stayed legible: signflip A+B 30/30 PASS, vflip-A 48/48 PASS. Result: the DPI
   identity **held on the new transforms anyway** — signflip 60/60 agreement,
   vflip-A 47/47 — and every valid cell scored **0.0000 bits**. Perfect
   knowledge of the transform did not move the needle, because the identity is
   a property of the *adversary's construction* (the fool commutes with the
   transform family), not of the channel's knowledge.
2. **"C3 didn't try the right amplitude" → R1.** Seven amplitudes spanning
   ×48 (±50…±2400 pcm, ±1…±64 img/vid), frozen seeds. Result: agreement curves
   **flat** — no amplitude separates fooled from correct judgments; L5–L6
   collapse to ~0 bits (near-universal WITHHOLD, a vacuous NULL). Best pooled
   0.0296 bits (L4), 5× below the 0.15 bar. If fooled judgments sat closer to a
   decision boundary, the sweep would have found the separating amplitude.
   There is none to know.
3. **"C3 needed more observations" → R2.** Five independent re-observations,
   majority vote at L3/L5. Result: 0.0173 / **0.0000** bits — more data
   squeezed the signal to exactly zero at L5. The fool is the stable mode.
4. **"C3 used the wrong noise structure" → R4.** Block/frame-correlated drift
   (V1) and ternary {−A,0,+A} noise (V2). Result: 0.0102 / 0.0167 bits pooled.
   The NULL is not a noise-choice artifact.

Every false-install sat ≥ 0.267 (R3 signflip lowest at 0.283, bits 0.0000)
against a bar of < 0.15. Maximum pooled signal 0.0296, 5× below bar; maximum
per-sense 0.0541, 2.8× below bar. The NULL is decisive, not marginal.

### 2.2 Why no knowledge augmentation can help — the structural argument

A judgment-side channel computes a predicate over {J(p(x)) : p ∈ P} — reports
of ONE judge over a perturbation family P. The frozen adversary crafts each
fixture so the fool is a fixed point of P:

- transforms: J(T(x)) == L(J(x)) everywhere (DPI, extended by R3 to novel
  transforms wherever the judge stayed legible);
- noise: fool stability == honest stability within the legibility band
  (R1/R4: no separating regime exists).

When Jt is a deterministic function of J, the pair (J, Jt) carries exactly the
information of J — the transform query adds **zero** bits about Y, by
tautology, regardless of what the channel knows about T or L. When noise
stability is uncorrelated with correctness (0.939 vs 0.894), the noise query
adds ~zero bits, regardless of what the channel knows about the noise model.
The channel would need a query the adversary has NOT fixed — i.e., an
information source outside the compromised judge. That is precisely C1, and it
is precisely not judgment-side.

The mechanism demo in `src/mech_demo.zag` (pure Zag, 2× byte-identical) makes
this crisp in miniature: a C2-style channel with **perfect** knowledge of T
and L scores 0.0000 bits (constant INSTALL — the measured F1 result);
DISTINCT_J_JT_PAIRS = 2 proves Jt is a deterministic function of J; the
C1-style independent analytic scores 1.0000 bit. The death is in the input
structure available to the channel family, not in the channel's knowledge.

### 2.3 What teaching could and couldn't do

Teaching the *channel* more facts about transforms/noise cannot help: R1–R4
supplied exactly those facts and the NULL persisted. Teaching the *judge*
is out of scope — the judge is frozen by design, and "invert the adversary's
perturbation per fixture" is building a better judge, not a channel. The only
teaching-relevant move is the C1-class one: teach/build an **independent
analytic** per task family — a different mechanism the adversary did not
construct against. That is a machinery change (new information source), not a
knowledge patch to the old machinery.

### 2.4 Scope discipline

Per Sol's adjudication and G1: this is a machinery ceiling **for the frozen
threat model**, not a universal theorem. A different adversary construction —
one whose fools are NOT transform-consistent or NOT noise-stable — could in
principle be caught by a C2/C3-class channel, which is exactly why G1 requires
a new preregistered battery for any new construction, sense, or task family.
The CON camp's remaining objection (finite-battery non-exhaustion) is a scope
limit, not a verdict-changer.

---

## 3. The v2 question — judgment-channel recommendation for PAMs v2

**PAMs v2 must ACCEPT TRUTHS: ~0% false installs AND high true-install rate.**
C1's profile (0.9968 bits, 0.0% false-install) matches that bar; C2/C3's
(0.0000/0.0049 bits, 27–49% false-install) anti-matches it.

**Does C1's scout architecture generalize to a truth-accepting
judgment-side channel? No — and the question's framing is the trap.** The
judgment-side family (self-consistency of one judge under perturbation) is
dead by DPI + the appeal. What generalizes is not a judgment-side channel but
the C1-CLASS principle. **A new channel architecture is needed:**

### Candidate: independent-corroboration channel (C1-class)

**Rule:** INSTALL a candidate truth/judgment iff an **independent analytic
judgment** — computed from the raw evidence by a mechanism diverse from, and
not controlled by, the proposer — agrees with the proposed judgment.

Concrete v2 spec (per task/knowledge family):

1. **Frozen analytic probe** (pure Zag, zero RNG), one per family, mirroring
   that family's label-defining rule the way `c1scout_pitch.zag` mirrors the
   generator's pitch rule: white-box, deterministic, robust to in-band
   perturbations by construction (averaging / direct measurement, not
   learned perception).
2. **Channel rule:** INSTALL iff analytic(evidence) == proposed judgment;
   else WITHHOLD. The proposer (TNN's judgment path) is queried once; the
   analytic never consults the proposer.
3. **Bar:** per-family ≥ 0.15 bits AND < 0.15 false-install on a frozen
   adversarial battery, 2× byte-identical, Zag/Python cross-check 0
   mismatches — the frozen deploy criterion, unchanged.
4. **Governance (G1):** each new family gets its own preregistered battery;
   no extrapolation of a probe across families.

### Why this is the right candidate

- It is the **only** channel class with a live existence proof at the v2
  bar: 0.9968 bits saturating H(Y), 15/15, zero false installs.
- Its mechanism directly addresses the autopsy finding: the information
  source is outside the compromised judge, so the fixed-point argument
  cannot touch it. The adversary must fool **two diverse mechanisms**
  simultaneously with one in-band perturbation.
- It composes with Team 3's R2-3 admission law (WITHHOLD iff jf != jg on
  disjoint evidence): the analytic is the natural "second evidence path."

### Honest limits (must be carried into the v2 build)

1. **C1's evidence is pitchdisc-only (15 fixtures).** The six-task C1 build
   (per-task scout-then-build, 0.15-bit bar) is the open next step named in
   TCP_VERDICT.md — v2 inherits this debt: every family needs its probe.
2. **C1-class needs a white-box label rule per family.** Where no public /
   analytic rule exists for a knowledge family, the probe cannot be built
   this way — that family needs its own preregistered approach, not a
   stretched pitch probe.
3. **Adaptive adversary fallback:** an adversary that optimizes against the
   analytic too breaks the single-probe channel. TCP_VERDICT.md names the
   fallback: Sol's human-verification/second-sensor — i.e., a *second*
   independent mechanism. v2 should design for corroboration depth ≥ 2 on
   high-stakes families.
4. **Never rebuild C2/C3-class for the frozen threat model** (F2, WRAPS).
   Any C* reopening is member-by-member under a new battery.

---

## 4. Mechanism demo — `src/mech_demo.zag`

Pure-Zag miniature of the measured DPI structure (NOT new evidence; an
illustration of §2.2). N=64 deterministic items; frozen judge fooled
(flipped) on the adversarial half; transform T(i)=i^1 with law L=identity
under which the fool is an exact fixed point; C3-style deterministic ~8%
flip pattern; C1-style analytic recovering the true label by construction.

```
N 64
DPI_VIOLATIONS 0
DISTINCT_J_JT_PAIRS 2
C2 n00 n01 n10 n11 0 0 32 32
C3 n00 n01 n10 n11 3 2 29 30
C1 n00 n01 n10 n11 32 0 0 32
```

Python glue (ratios/MI only, per the frozen division of labor):
C2 I(V;Y)=**0.0000** bits, C3 I(V;Y)=**0.0025** bits, C1 I(V;Y)=**1.0000**
bits, H(Y)=1.0000. The C2 channel has perfect knowledge of T and L and still
scores zero — the death is structural.

Build (from `senses/pam-rebuild/v2/autopsy/`; @import resolves relative to
the source path's directory, so spell the source as `src/...`):
```
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 \
  src/mech_demo.zag --no-zagd --no-analyze --no-foreground-cache -o /tmp/mech_demo
```
2× runs byte-identical (see `src/BUILD_MECH_DEMO.txt`). Binary and `.zagd`
never committed.

---

## 5. Evidence index (frozen, read-only)

- Binding verdict: `docs/lab/kb/autopsy/channels2/f2appeal/F2_VERDICT.md`
  @ `tnn-native-lab` (WRAPS; 14/14 NULL; max pooled 0.0296 bits, 5× below
  bar; all false-installs ≥ 0.267 vs < 0.15 bar).
- Frozen appeal prereg: `.../f2appeal/PREREG_FROZEN_F2APPEAL.md`.
- PACKAGE 3 verdict (DPI consequence, C1/C2/C3 numbers):
  `docs/lab/kb/autopsy/channels2/TCP_VERDICT.md`.
- Debate: `.../f2appeal/debate/` — D1 (pre-result papers), D2 (Sol
  steelman), D3 (CON signs WRAPS; Sol adjudication: "WRAPS, mechanically
  and conclusively under §6 for the frozen threat model"; G1 sufficient),
  D4 (rebuttals).
- Channel sources (mechanism reference, §1):
  `kb/autopsy/channels2/src/channel_c2.zag`,
  `kb/autopsy/channels2/src/channel_c3.zag`,
  `kb/autopsy/channels2/src/c3_noise.zag`,
  `kb/autopsy/channels2/src/c1scout_channel.zag`,
  `kb/autopsy/channels2/src/c1scout_pitch.zag`.
- Appeal scores: `.../f2appeal/scores_f2.json` (+`brief_r1..r4.txt`,
  `truth_rows_f2.txt`); G0 370/370 reproductions, 2× byte-identical;
  scorer Zag/Python cross-check 0 mismatches (14/14).

## 6. Bottom line for the parent orchestrator

1. **C1 lives because it never trusts the judge twice**: one query to the
   judge, verdict from an independent analytic measuring the label-defining
   quantity. C2/C3 died because they re-queried a fooled judge whose fool is
   a fixed point of every perturbation they may apply.
2. **Knowledge-vs-machinery: MACHINERY** (frozen-threat-model scoped).
   Four preregistered knowledge augmentations (new transforms, amplitude
   sweep ×48, multi-draw majority, structured noise) all returned decisive
   NULLs. The DPI identity held on novel transforms where legibility was
   verified — the fool's fixed-point structure belongs to the adversary's
   construction, and no channel-side knowledge changes a tautology.
3. **PAMs v2 recommendation: do NOT build a judgment-side acceptance
   channel. Build the C1-class independent-corroboration channel**:
   INSTALL iff a frozen, pure-Zag analytic probe — diverse from and
   uncontrolled by the proposer — agrees with the proposed judgment, per
   family, each under its own preregistered battery (G1). Design high-stakes
   families for corroboration depth ≥ 2 (adaptive-adversary fallback).
