# BAR-SENSITIVITY AUDIT — red-team attack #5

**Date:** 2026-09-21/22 · **Crew:** BAR-AUDIT · **Status:** PROPOSAL ONLY — no prereg amended.

**Thesis under test:** kill bars are tripwires — 157× slack sampled (self-test overhead bar
2.0 vs measured 0.0127); q1n's 19/19 absorbed had NO bar at all. Perfect scores are the
expected outcome of deterministic code + wide bars, not a miracle.

**Method:** three worker crews extracted every preregistered bar (exact threshold, cited to
prereg file/line) and every measured value (cited to verdict file/line) across the headline
batteries, computed margins, and classified each bar. Headline results with no bar got a
retroactive bar proposal + pass/fail evaluation. Full per-worker tables with line citations:
`scratch/worker_A.md` (principle-detection, new-mechanisms, info-source),
`scratch/worker_B.md` (scale data/params/fewshot, self-test, noisy-teacher ×3),
`scratch/worker_C.md` (rsi, prose v1/v2/v3, mixed-web, coding, dialogue).

**Classification rule:** TIGHT (margin < 2×), COMFORTABLE (2–10×), TRIPWIRE (>10× slack).
For "≤ X" bars, ratio = X/measured. "∞" = measured 0 against a >0 allowance.

**Coverage:** 100% of headline verdicts from the last 7 days: principle-detection,
new-mechanisms (contradiction), info-source, scale-up (data, params, fewshot), self-test,
RSI, prose-learning v1/v2/v3, mixed-web, coding, dialogue, noisy-teacher series
(q1n/tq-noisy25/q1tq-noisy50). ~70 bars audited.

---

## 1. Consolidated margin table

### 1a. Genuine tripwires (>10× slack)

| Battery | Bar | Threshold | Measured | Slack |
|---|---|---|---|---|
| self-test | KB-ST-OVERHEAD: orchestration ops ≤ 2× battery ops | ≤ 2.0 | 0.0127 | **157×** — permits orchestration to cost 200% of the batteries; measured 1.27% |
| scale | KB-SCALING: trip iff mastery drops >2pp below S0 | 2.00pp | 0.00pp | ∞ — tolerates **125,137 wrong facts** at N=6,585,360 before tripping |
| scale | KB-FORGET: trip iff last−first decile gap >3pp | 3.00pp | 0.00pp | ∞ — tolerates **~187,700 forgotten early facts** |
| info-source | KB-SPOOF-RESIDUAL | unfailable by construction | reproduced | **unfailable** — both outcomes (residual appears / not) yield PASS or "surprise, not failure"; a documentation requirement wearing a kill-bar costume |
| principle-detection | KB-PD-FA: false alarms ≤ 0.05 | 0/26 | ∞ mechanical | ∞ is an artifact of measured=0; effective slack is 1.3 items and the bar sits at its floor — the real weakness is binary (says nothing about decision margins) |

### 1b. Comfortable (2–10× slack)

| Battery | Bar | Threshold | Measured | Slack | Note |
|---|---|---|---|---|---|
| dialogue | KB-DLG-STYLE: \|WEIRD−CLEAN\| ≤ 30pp | 30pp | 3.3pp | **9.09×** | lets WEIRD collapse to 70% while clean sits at 100% |
| prose-v1 | KB-QUALITY no-diff band ±0.02 | 0.02 | Q=+0.0022 | 9.09× headroom | **below noise floor** — SE(Q)≈0.024; band edge at ~0.8 SE (§6) |
| RSI | KB2-CORRECT: ≥1 of top-3 reproduced | ≥1 | 3/3 | 3.0× | plus 2× slack in the reproduction criterion (0.5×, §5) |
| coding | KB-C1: T4 novel compile-correct ≥50% | 50% | 100% | 2.0× | coin-flip-level viability bar; would pass a 6/12 learner |

### 1c. Tight (<2×) — the bulk of the suite

Every bar below sits within 2× of its measured value; most are exact-equality binaries
with zero slack. Perfect scores here are the expected outcome of correct deterministic
code, not a miracle — but incorrect code would have tripped them (cf. the confdepth
1.50× trip, which did fire).

| Battery | Bar | Threshold | Measured | Margin |
|---|---|---|---|---|
| principle-detection | KB-PD-DET | ≥0.90 | 13/13 = 1.0000 | 1.111× (+1.3 items) |
| principle-detection | KB-PD-DET2 | 0 diffs / 5 reps | 0 | exact |
| new-mechanisms | KB-M-RESOLVE | ≥0.90 (≥140/156) | 156/156 | 1.111× (+16) |
| new-mechanisms | KB-M-NOHARM | 96/96 | 96/96 | exact |
| new-mechanisms | KB-M-TIE | 36/36 | 36/36 | exact |
| new-mechanisms | KB-M-COMPOSE | ≥22/24 | 24/24 | 1.091× (+2) |
| new-mechanisms | KB-M-TEMPORAL | ≥22/24 and 12/12 | 24/24, 12/12 | 1.091× / exact |
| new-mechanisms | KB-M-SPOOF | 24/24 | 24/24 | exact |
| new-mechanisms | KB-M-COST | ≤1.10× baseline | 1.00× | 1.10× — ops are integral, so this effectively demands exact equality already |
| new-mechanisms | KB-M-PARITY | identical + digest | digest `1f68e26f…` identical | exact |
| new-mechanisms | KB-M-DET | 5/5 byte-identical | PASS | exact |
| info-source | KB-R0-BASE | ≥10/12 | 12/12 | 1.20× |
| info-source | KB-CATCH | 0/12 installs (R1,R2) | 0/12, 0/12 | exact |
| info-source | KB-CATCH-RATE | ≥10/12 | 12/12 | 1.20× |
| info-source | KB-CORR-INSTALL | ≥10/12 and ≥3/4 | 12/12, 4/4 | 1.20× / 1.333× |
| info-source | KB-CONTEST | 4/4 | 4/4 | exact |
| info-source | KB-DET | 5/5 byte-identical | PASS | exact |
| scale | KB-COST | ratio ≤1.5× | 1.000 | 1.5× |
| scale | KB-DETERMINISM | 0 diffs | 0 | exact |
| scale | KB-FLAW | ≥7/8 slices | 8/8 | 1.14× |
| scale/params | KB-P-DET | 0 diffs, 19/19 configs | 0 | exact |
| scale/params | KB-P-GRACE | taught-subset mastery = 1.0 at 0.5× | 1.0 (also at 0.25×) | exact |
| self-test | KB-ST-AUTO / SKIP / FIDELITY / DET / SCALE | structural | HOLD ×5 | exact/structural |
| self-test | manifest B1/B2/B3/B4/B5/B6 | ≥236/240, =12, ≥92/96, ≥46/48, UNRUNNABLE, digests equal | 240, 12, 96, 48, UNRUNNABLE, equal | 1.017–1.043× / exact |
| RSI | KB1-CONCRETE | ≥3 | 3/3 | 1.00× — zero headroom, fragile not slack |
| RSI | KB3-SAFE / KB4-DET / KB5-NOSKIP | binary | PASS | exact |
| prose-v1 | KB-EXTRACT | ≥0.99 | 1.0000 | 1.0101× |
| prose-v1 | KB-DETERMINISM | 5/5 | 5/5 | exact |
| prose-v2 | KB2-DET | 5/5 | PASS | exact |
| prose-v2 | SUB-PARA | ≥46/48 | 48/48 | 1.0435× |
| prose-v2 | SUB-CONTR | 24/24 | 24/24 | exact |
| prose-v2 | SUB-MULTI | ≥22/24 | 24/24 | 1.0909× |
| prose-v2 | KB2-NOSILENT / SUB-HEDGE / SUB-NEG | 0 leakage | 0 | exact on the letter |
| prose-v3 | KB3-NOSILENT / KB3-DET | binary | PASS | exact |
| mixed-web | KB-MW-WRONG / GUESS / LEDGER / DET | binary | 0 wrong, 0 guesses, 17/17, 5/5 | exact |
| mixed-web | coverage | ≥16 scored | 17 | 1.0625× — one question above UNDERPOWERED |
| mixed-web | VALUE-CONFIRMED | ≥4 | exactly 4 | 1.00× — zero slack; all 4 wins withhold-side |
| dialogue | KB-DLG-TRACK | ≥0.70/type | 1.00 all five | 1.43× — but all at ceiling on an authored battery |
| dialogue | KB-DLG-DET | 5/5 | PASS | exact |
| coding | KB-C3 / KB-C4 | binary | PASS / 6/6 refused | exact |
| coding | KB-C5 | T4m ≥ T4−30pp | 100% vs 100% | 1.43× — below granularity floor (§6) |

### 1d. Miscalibrated — tight on the wrong target (the sharper pathology)

| Battery | Bar | What it measures | What the leg asks | Finding |
|---|---|---|---|---|
| noisy-teacher ×3 | §B.7 ≥10/12 per slice (1.2×, tight) | proposal *form* (spans, confidence, grounding) | knowledge *truth* (does judgment filter falsehoods?) | stayed 96/96 at 51.75% teacher noise with **51.6% of taught knowledge false** (93/192 true mastery). A tight bar on the wrong instrument manufactures false confidence. |
| scale/params | KB-P-EMERGE: absorption < 1.0 → EMERGENT flag | fired on slot025/slot05/jsmall | truth-detection emergence | fired on the wrong partition — the shortfall was untaught facts (capacity drops), not truth detection; cleared by discretionary analyst judgment overriding a mechanical bar. A bar that fires-then-requires-human-clearance has a hole in it. |

### 1e. Procedure tier — passes by construction (expected 100%s, not evidence)

DET / NOSKIP / NOSILENT / LEDGER / SAFE / gate-refusal / EXTRACT bars (~15–20 of the
~70) are anti-cheat/anti-regression checks. For deterministic code they carry ~zero
informational content about the scientific claim. They are correctly read as tripwires
against cheating, not as evidence of capability. No slack finding attaches — their
strictness is already maximal.
## 2. Honest-fails (retroactive — the bar that should have existed)

These are headline results that FAIL under a reasonable bar that was never preregistered.
Retroactive bars are proposals for future preregs, not amendments to past verdicts.

| # | Battery | Result | Bar that should have existed | Retroactive verdict |
|---|---|---|---|---|
| H1 | principle-detection | Arch B INSTALLED the planted lie on F45 (weak principle P19 conf 40 < teacher 50 → ACCEPT "cobra produces milk") | install rate = 0 on principle-contradicting false claims, all architectures | **HONEST-FAIL** for Arch B. The verdict reported it as "a design choice" while headlining B alongside A's 13/13. |
| H2 | scale/params | flaw battery 96/96 at slot025/slot05/jsmall | probe ids must span the full taught id range; configs with <100% coverage mark DEGRADED | **HONEST-FAIL** on table presentation — the battery samples ids in [0, n/4) only, blind to capacity loss beyond 4×. Caveat discloses; table does not. |
| H3 | scale/fewshot | flaw "96/96*" at N=4/2/1 (distinct ids = 1) | the verdict's own prereg rule: "not presented as a 96-probe result" | **HONEST-FAIL** on presentation — shown as 96/96 with a footnote, violating the letter of its own prereg. |
| H4 | noisy-teacher ×3 | world-true mastery collapse: 173/192, 143/192, 93/192 (drops of 9.9/25.5/51.6pp vs control) | drop > 2pp vs clean control → TRIP (the scale-up standard) | **HONEST-FAIL** on all three legs. No mechanical bar captured it; the only bar in force stayed green throughout. |
| H5 | noisy-teacher ×3 | wrong-span REVISE adopts the teacher's false value *while scoring a hit* | REVISE-path adoptions must carry teacher-true values, else scored as misses | **HONEST-FAIL** under value-aware scoring. The battery does not merely miss the falsehood — it **rewards its installation**. |
| H6 | prose-v2 | SUB-HEDGE passes 19/24 while hedged-only retrieval is 7/12 | hedged-only probes return HEDGED on ≥10/12 | **HONEST-FAIL**. The prereg bar tests leakage only; the quarantine fails to label nearly half its hedged items. |
| H7 | coding | KB-C2 report narrows preregistered T3+T4 to T3 only, claims "PASS (loop essential)" | the frozen rule: final-correct(A) ≥ 2×final-correct(B) on T3+T4 | **HONEST-FAIL under the frozen rule** — A=22, B=12, 2×B=24 > 22 → FAIL (or the bar is unmeasured if B never ran T4). Narrowed without amendment. |
| H8 | prose-v3 | tier-3 wrong-value rate 8→30/912 (0.9%→3.29%) | tier-3-introduced wrong-value rate ≤2% on the clean set | **HONEST-FAIL at ≤2%** (passes at ≤5%). The "C4 carried the recovery" headline is recall-only; the precision price is unbarred. |

## 3. Disclosed gaps (not fails — need fixing)

1. self-test B6: 50 of 400 s10 fidelity verdicts are oracle-asserted, not recomputed
   ("independent oracle" overclaims by 50 verdicts).
2. self-test fault injection: 1 of 3 needed fault classes (silent skip only; verdict
   tampering and count/coverage mismatch untested).
3. The §B.7 ≥10/12 bar is **PROPOSED, never frozen** (units/PREREG_FREEZE.md) — freeze it
   or stop citing it as "the bar".
4. new-mechanisms KB-M-COST: no rule on post-trip repair-and-retry (first confdepth build
   tripped at 1.50×, was repaired, re-run to 1.00× inside the same verdict — disclosed, so
   not hidden, but a kill bar that permits iterate-until-pass is weaker than advertised;
   future preregs need a single-shot vs repair-allowed rule).
5. info-source KB-CONTEST is blind to semantic correctness (C2 "tallest mountain" passed
   mechanically while arguably wrong — self-flagged in the verdict's caveats).
6. info-source KB-CATCH-RATE / KB-CORR-INSTALL: the 10/12-vs-12/12 distinction sits within
   one live envelope's variability (8.3pp at n=12); "works on the live web" needs its own
   bar with fresh envelopes.
7. prose-v3 oracle bar literally tripped (26/28 vs "every leg") — PASS via documented A0
   exemption; bar-status must read "PASS with documented A0 exemption".
8. prose-v3 §11 prereg deviation confounds the C2 ablation attribution (6/11 CORE items from
   the unpreregistered trigger expansion, 5 from the preregistered order change).
9. prose-v3 verdict splits conjunctive KB3-VIABLE into VIABLE(FAIL)+RETAIN(PASS) — RETAIN is
   not a prereg bar; the split softens the FAIL.
10. dialogue COMPOSE-NOVEL is self-attested — the oracle does not independently verify
    novelty; the "understands, doesn't merely repeat" headline rests on a self-reported flag.
11. RSI cost predictions (×1.0/×1.5/×3.0) never measured against implementation; the
    reproduction criterion (actual ≥ 0.5×predicted) has 2× slack; the negative control is
    unscored.
12. coding prereg §6 metrics largely missing from the report: iterations-to-correct
    distribution, wall-clock timings, arm D (manual delta), arm E ablation, the 12
    multi-hop interference probes, manual-only item splits.
13. prose-v2 falsehood rows superseded by frozen ABS-3 (9,11,11,11) — the verdict's "far
    fewer (0–4/12)" headline used the probe metric; under ABS-3 v2 installs 9–11/12 lies as
    asserted vs v1's 12/12. Measurement-only bar, so no pass/fail changes, but the
    interpretive claim must carry the ABS-3 correction.
14. prose-v2 NEG battery duplicate probes (18/30, 19/31 identical strings, conflicting
    expects) — 36/36 impossible by construction; KB2-NOSILENT passes "as written" while 2
    expect-unknown probes returned VALUE.

## 4. Noise-floor flags

| # | Bar | Finding |
|---|---|---|
| F-a | prose-v1/v2 KB-QUALITY ±0.02 band | Binomial SE(Q)≈0.024 at n=228 — the bin edge sits at ~0.8 SE; a true-zero Q escapes the NO-DIFFERENTIATION bin by noise alone ~40% of the time. Correct to **±0.05** (≈2 SE). |
| F-b | coding KB-C5 (T4m ≥ T4−30pp) | n=4 → 25pp/item; the 30pp band cannot resolve a single failure (75% still passes). One full item of built-in slack. Double n, narrow the band. |

No other bar sits below its measurement noise floor — all mastery/absorption/flaw counts
are exact deterministic counts (noise floor = 1 unit). The lab's failure mode is excess
slack and wrong-target instruments, not sub-noise thresholds.

## 5. Prereg internal inconsistencies (documented, not amended)

- new-mechanisms KB-M-RESOLVE: "≥ 0.90 (≥140/156)" — 140/156 = 0.8974 < 0.90; the
  parenthetical contradicts the ratio (honest count: 141/156).
- new-mechanisms kind-5: battery table says n=24; kill bar says 12/12; verdict scores 12
  (resolution total 156 confirms 12) — typo in the battery table; scoring was consistent.
- principle-detection: "0.90" (n=13) and "5%" (n=26) are written below count resolution —
  honest forms are "≥12/13" and "≤1 item".

## 6. No-bar results that PASS retroactively (for the record)

Refinement 4/4, A-vs-B agreement 43/43, cost ≤30 ops/fact, emergence contrast 12/12−0/12
(Fisher p<0.0001), baseline-resolution sanity ≤30%, contested-cost ≤3.0×, RSI diagnosis
3/3, convergence/negative-control, v1 oracle 0-diff, v2 rebuild sha256-identical, MW
discriminative power (A guesses 4/4), coding one-shot 30/30, dialogue total 99.7% —
all pass reasonable retroactive bars. The audit's comfort: most unbarred headlines
survive real bars.

## 7. Verdict on the thesis

Attack #5 is **CONFIRMED WITH REFINEMENT**, not as a blanket claim:

1. **Confirmed:** 4 genuine tripwires (KB-ST-OVERHEAD 157×, KB-SCALING ∞, KB-FORGET ∞,
   KB-SPOOF-RESIDUAL unfailable) + 1 mechanical (KB-PD-FA ∞, effective slack 1.3 items).
2. **Refined:** the sharper pathology is TIGHT BARS ON THE WRONG TARGET — the noisy-teacher
   §B.7 bar (1.2×, tight) measures proposal form while the leg asks about knowledge truth;
   every bar passed at 51.75% noise while 51.6% of taught knowledge went false, and the
   battery actively rewarded falsehood installation via REVISE. Tight bars on the wrong
   instrument manufacture false confidence — worse than loose bars.
3. **Rejected in part:** most numeric bars are TIGHT (1.01–1.5×), many exact-equality;
   17+ bars applied as designed; and the effect bars that mattered **failed loudly** when
   ideas were wrong — v1/v2/v3 VIABLE all tripped (v2 at 28.5% of a slack-free ceiling),
   SUB-CORE at 50%, SUB-DISTR at 28.5%, QUALITY refuted twice. Wide-margin failures of
   tight bars are the opposite of tripwires — they are the bars working.
4. **Coverage gaps, not threshold gaps:** the audit's honest-fails are almost all *missing*
   bars (F45 weak-principle install, mastery-collapse, value-aware REVISE, hedged
   retrieval, novelty independence, cost verification), not loose ones.

Net: the bar suite is two-tier. A procedure tier (~15–20 bars) passes by construction and
is correctly read as anti-cheat, not evidence. An effect tier is mostly tight, sometimes
fragile-at-exactly-measured (RSI KB1, MW VALUE-CONFIRMED at 1.00× — the opposite problem:
one flipped item voids the headline), twice below the noise floor, and carrying the
divergences above. The proposed tightened bars (`PROPOSED_BARS.md`) address the slack,
the wrong-target instruments, and the missing bars — as a proposal awaiting Micah's
signature, not as an amendment.
