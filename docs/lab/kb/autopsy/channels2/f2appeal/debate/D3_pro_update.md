# D3 — PRO-WRAPS post-result update

The battery reported. Every prediction below is checked against RESULTS.md §R1–R4.

## 1. Predictions vs measurements

**R1 — noise-amplitude sweep: confirmed (with one hairline).**
L0–L3 predicted bits 0.00–0.05, false-install 0.40–0.50 → measured
0.0184/0.453, 0.0144/0.449, 0.0246/0.443, 0.0215/0.439. All inside the
bands. L4 predicted bits ≤ 0.10, false-install 0.45–0.60 → measured
0.0296/0.420: bits confirmed, false-install 0.420 sits just below the
predicted band's lower edge (a ~3-point miss, and ~3× above the bar —
irrelevant to the verdict). L5–L6 predicted "near-universal WITHHOLD →
bits ≈ 0" → measured 0.0006 and 0.0044. The collapse held, on both runs,
byte-identical. The boundary-distance hypothesis is dead across 7 levels:
no amplitude separates fooled from correct judgments.

**R2 — multi-draw majority: bits mechanics confirmed exactly; one conjunct missed.**
L5 predicted **bits = 0.0000** from the near-constant-vote mechanics →
measured **0.0000** (A: 0.0010, B: 0.0001). L3 predicted bits < 0.02 →
measured 0.0173. The squeeze-toward-zero mechanism worked as predicted.
But we also predicted false-install **≥ 0.90** ("the fooled majority
agrees with itself") → measured **0.442 / 0.463**, barely above the
single-draw level. We got the constant's direction wrong: the vote
becomes near-constant WITHHOLD (reproducing the single draw's
behavior), not INSTALL. Verdict-immaterial (bits carry the bar), but a
real mechanical miss — see §4.

**R3 — alternative transforms: the C2 redux, confirmed to the digit.**
Predicted: on every F3-valid (sense, transform) cell,
J(T(x)) == L(J(x)) everywhere → **0.0000 bits**. Measured: perfect
agreement on (A,vflip), (A,signflip), (B,signflip) → **0.0000 bits on all
three valid cells**, F4 effectively re-fired. The DPI identity extends to
the new transform family exactly as predicted. Involution T(T(x))==x
byte-verified, 0 failures.

**R4 — structured noise: confirmed.**
Predicted pooled bits 0.00–0.02, false-install 0.40–0.50, 2×
byte-identical → measured V1: 0.0102/0.443, V2: 0.0167/0.436, both runs
byte-identical, 0 cross-check errors. The null is about the mechanism
(stability ∥ correctness), not the noise shape — confirmed.

## 2. What surprised us

**The F3 VOID pattern.** We predicted VOID cells generically ("a broken
judge, not a recovered channel") but not the shape: vflip keeps sense-A
legibility 48/48 while destroying sense B (37/48 void, 0.7708); fshift
destroys legibility in *both* senses (4/15 and 6/15 void), leaving zero
valid cells. Two lessons: (a) calibration gates work — they excluded
exactly the cells where the judge is broken, before scoring; (b) our
ability to predict *which* transforms are legible *a priori* is weaker
than our D1 paper implied. Legibility is fragile and asymmetric across
senses — something CON can legitimately hold against us.

**The R2 false-install miss** (covered above; owned, not minimized).

## 3. Verdict under §6, and Sol's objection

**§6 yields WRAPS: 14/14 members NULL.** Maximum pooled bits 0.0296
(R1-L4) — 2.8× below the 0.15 bar; maximum per-sense bits 0.0541 —
still 2.8× below; every false-install ≥ 0.40 against a bar of < 0.15.
G0 passed 370/370, all reruns byte-identical, 0 scorer mismatches. Our
falsifier was explicit: RECOVERY iff bits > 0.15 AND false-install < 0.15
with 2× byte-identical runs. Nothing fired. Our camp's verdict: **WRAPS**.

Note CON's side too: Sol's steelman recorded CON's pre-committed
concession criterion — *no regime fires the frozen recovery bar* →
CON concedes WRAPS for the frozen threat model. That condition is met.

**On Sol's "most damaging objection" (finite battery cannot establish
whole-family exhaustion):** in our view, **G1 fully answers it** — but
precisely because it answers a scope question, not an exhaustion
question. The objection is valid against a claim we do not make:
TCP_VERDICT §3 already concedes retirement is frozen-threat-model only,
and G1 converts that concession into governance — auto-execution is
scoped to the measured regimes, and extending retirement to ANY new
adversary, sense, or task requires a NEW preregistered battery. G1 does
not make the tested regimes exhaustive; it makes the *decision*
non-extrapolating. That is the whole answer: the measurement stands,
the reopening mechanism is specified, Micah decides. **PRO in one line:
WRAPS for what was measured, G1 for what wasn't.**

## 4. One honest concession

Our strongest remaining weakness is one CON always had, now sharpened
by our own miss: **our mechanistic grip on untested regimes is weaker
than our D1 paper advertised.** We predicted the R2 majority-vote
regime's false-install and were materially wrong (≥0.90 predicted vs
~0.44 measured), and we could not predict which transforms would fail
calibration legibility. The verdict does not depend on those predictions
— the frozen rule is mechanical, and it held at every one of 14
members — but CON's point stands untouched for anything outside the
frozen threat model: a finite battery of regimes, plus theory that can
miss its own conjuncts, is not a proof of family exhaustion. That is
exactly why G1 is part of our verdict, not an ornament on it.
