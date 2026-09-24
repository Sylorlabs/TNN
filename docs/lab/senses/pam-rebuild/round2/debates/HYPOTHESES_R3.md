# HYPOTHESES R3 — ranked hypothesis slate with frozen kill bars

**Date:** 2026-09-24. **Crew:** PAMs Round-2 debate crew, round 3.
**Branch:** `tnn-native-lab`. **Status of external audit:** PENDING — fable-5.1 batched audit requested
(7 questions, one round); 3 attempts all returned `choices: null` with 0
completion tokens (provider backend generating nothing across models this
session — grok-4.7 3x HTTP 524, gpt-5.6-sol 3x empty). Recorded as pending,
never treated as a verdict. The slate below stands on the native judge's
ruling; the audit appends when the provider recovers.

## What this slate answers

The judge's two-problem split (counsel synthesis, landed): DEFENSE =
correlated-wrong corroborators (the deployment blocker); OFFENSE = the 74.8%
gate-side ceiling (only sense/program changes move it). Round-3 evidence
added: F5 SURVIVED backtest (8/9 blocked, 0/34 over-blocked); G2 and G5
KILLED by the byte-side correlation wall; CC1 known-unsafe with a margin
guard in verification by a parallel crew; H6 won with 0 false installs on the
clean stream — remaining failures are FRONT-END, not gate; sense is 53% on
the 12 sealed novel adversarial families.

Test-first discipline (applies to the slate itself): every hypothesis is
testable in pure Zag, zero RNG, byte-identical determinism (3 runs, sha256
match); frozen prereg committed ALONE before any build.

**Already covered by parallel crews — do NOT double-dispatch:**
- F5 300-near-exemplar-correct-percept red-team (kill if >25% delayed >50
  trials) — in flight.
- CC1 margin-guard verification — in flight. D1's stack battery preregs now,
  runs after the guard lands.
- V4 two-tier corroborated-sequence confirmatory trial — HELD for Micah's
  word (`PREREG_V4_TWOTIER_DRAFT_HELD.md` in this directory); no run
  authorized.

---

## Ranked hypotheses

### R3-1. O1 — Knowledge-delivery repair [OFFENSE] — BUILD FIRST

**Mechanism.** Instrument the path from sense-emitted judgment to gate input
on the frozen RK-3 battery; find and fix the drops. DIAG_VERDICT_R24_RK3 is
the spec: K1 96.4% knowledge present in the system vs K2 74.8% reaching the
gate's input — a 25% delivery gap, ruled KNOWLEDGE (the rule/path is missing,
not the signal). Pure-Zag diagnostics harness, zero RNG.

**Why it survives the evidence.** It respects all four ceilings: no
judgment-side channel (it moves real judgments, not transforms), no pointwise
adjudication (no per-trial install decision changes), and it is the only
offense hypothesis that moves the 74.8% ceiling arithmetically without
touching the sense or the gate. It is the cheapest decisive experiment in the
program: the gap is already measured and frozen.

**Machinery needed:** none new — diagnostics + path repair.

**Frozen kill bar.** KB-O1: re-run the K1/K2 diagnostics harness. KILL if K2
does not rise to within 2pp of K1. KILL if RK-3 does not rise by at least half
the closed delivery gap (delivery is load-bearing only if installs follow —
a K2 rise with no RK-3 rise means the gate withholds delivered percepts for
other reasons, and the hypothesis as stated is dead).

### R3-2. FE1 — Novel-family formation audit (no build) [FRONT-END] — RUN IN PARALLEL

**Mechanism.** White-box the sense on each of the 12 sealed novel adversarial
families where sense accuracy is 53%. Per family, produce either (a) a
separator with ≥80% accuracy on frozen data, or (b) a byte-level
unobservability proof that truth is not recoverable from the family's bytes
(MOT-1 class: truth unobservable from pixels). Families with no signal are
declared out-of-scope for the sense and become defense-scope (refuse by
construction); families with unused signal become FE2 targets. This is the
death-board autopsy method applied forward: it refuted "no detectable signal"
by measurement (9 KNOWLEDGE / 1 MACHINERY / 1 UNRECOVERABLE / 1 BENCHMARK BUG).

**Why it survives the evidence.** The hardening verdict is explicit: remaining
failures are front-end, gate work has diminishing returns. V2-C died because
it calibrated on noise/surrogates and never measured recall on the target
family (D3 fired zero times, D3_DEVIATION.md) — FE1 is the measurement V2-C
skipped. It respects ceiling (2): no adjudication, only measurement.

**Machinery needed:** none — analysis only.

**Frozen kill bar.** KB-FE1: per family, KILL the "sense can learn this
family" claim if neither a ≥80% separator nor an unobservability proof is
produced — the family is then defense-scope, not a front-end target.
Program-level: KILL the audit's usefulness if fewer than 4 of 12 families
resolve to (a) or (b) with byte-level evidence.

### R3-3. D2 — F5 confirmation path [DEFENSE] — BUILD IN PARALLEL

**Mechanism.** Build the unbuilt half of F5: the "three deliberate
re-inspections from three temporal crops" confirmation organ. The backtest
(SURVIVE) covered only the block predicate; confirmation was never
exercised. Hypothesis: deliberate re-inspection correctly confirms blocked
TRUE candidates (releases them) while keeping blocked FALSE candidates
blocked. This is the program-law endgame: the brain deliberately re-inspects
before installing.

**Why it survives the evidence.** F5's block direction is safe (delay only);
the risk is all in the release direction. The byte-side wall does not apply:
re-inspection from three temporal crops reads different bytes, and the
confirmation decision is made by a separate deliberate organ, not by
re-scoring the same judgment. Ceiling (1) is respected because the
re-inspection is a new measurement, not a deterministic transform of the
blocked judgment.

**Machinery needed:** UNBUILT — a true deliberate re-inspection organ
(three temporal crops, deliberate re-judgment). Nothing in the committed
evidence demonstrates this machinery exists.

**Frozen kill bar.** KB-D2: on the 8 blocked false accepts, confirmation
releases ≥1 → KILL the confirmation path (keep F5 block-only). On ≥20
blocked true percepts (drawn from the 300-percept red-team fixtures, in
flight), <50% released within 3 re-inspections → the path is decorative;
KILL as a release mechanism, keep block-only.

### R3-4. D1 — Defense stack battery: F5 + margin guard + H6 [DEFENSE] — PREREG NOW, RUN AFTER GUARD LANDS

**Mechanism.** Test the three refusal layers as one battery on the 43
V2-D ACCEPT_INSTALL trials and the 12 sustained TMB-5 cross-span wrongs:
F5 negative-bank block (historical evidence), CC1 margin guard (relational
evidence — refuses thin-margin agreement), H6 no-provisional (temporal
evidence — withholds until corroborated second observation). A candidate
installs only if it survives all three.

**Why it survives the evidence.** The byte-side wall killed mechanisms that
re-read the same bytes for the same judgment; these three read different
facts (distance to known wrongs, agreement margin, corroboration absence).
Committed: H6 already 0 false installs on the clean stream; F5 8/9 blocked at
0/34 true cost. The question is the conjunction's residual, not any layer's.

**Machinery needed:** the CC1 margin guard (in verification, parallel crew).

**Frozen kill bar.** KB-D1: any false install through the full stack on the
frozen trials → KILL the stack as sufficient (return to per-layer analysis).
True-install retention <26/34 with the margin guard at its verified setting
→ KILL the conjunction as too costly; layers must be re-tuned separately.

### R3-5. O3 — Disjoint-window second sense [OFFENSE] — BUILD AFTER O1

**Mechanism.** NOT G5. Runs ONLY on the frozen 278 never-PASS trials
(correct high-conf, never reached PASS), using byte windows DISJOINT from
the first sense's formation windows (frozen disjointness proof required in
the prereg), emitting PASS under the existing numerical bar or abstaining.
It cannot touch already-PASS items and cannot install — the gate installs on
its PASS exactly as on any sense PASS.

**Why it survives the evidence — contested.** G5 died re-reading the same
bytes for the same judgment. O3's claim is that disjoint formation windows
are a different measurement, not a re-read: the 278 are correct percepts
whose truth IS in the bytes (they are correct), so the wall's premise
(spoofed bytes) does not hold for them. The defense kill bars travel with it
(counsel G5's): the heavier sense must not learn spoof features.

**Machinery needed:** UNBUILT — a second sense with provably disjoint
formation windows; no such organ is committed.

**Frozen kill bar.** KB-O3: KILL if <100 of the 278 convert to true PASS
(the 85%-bar arithmetic needs ≥113; 100–112 = real effect, insufficient).
KILL if false-PASS on the 12 sealed families rises >2 points above today's
rate. KILL if the second sense re-emits PASS on ≥2 of the six timbredisc
wrongs (it learned the spoof features — the wall applies after all).
KILL if RK-3 drops below 88.48%.

### R3-6. D3 — Joint-error bin refusal [DEFENSE]

**Mechanism.** Corroboration disabled in raw-byte bins whose historical
joint-wrong rate exceeds a frozen threshold, pending deliberate re-sense
(G6 folded into the F5 stack per the counsel judge). The only mechanism that
denies a sustained error the property it fakes (corroborability).

**Why it survives the evidence.** The 12 sustained TMB-5 wrongs are a
bin-shaped phenomenon (timbredisc, RICH, conf 764–832, G-span agreeing 9/12);
bins are where the joint-wrong signal lives. Respects ceiling (2): it refuses
corroboration, never adjudicates a trial.

**Machinery needed:** none new — bin statistics + refusal rule in the gate.

**Frozen kill bar.** KB-D3: on the 12 TMB-5 wrongs, bins that would have
refused them also refuse >10% of the 34 true installs → granularity too
coarse, KILL. KILL if the bin rule refuses any correct install on the clean
stream that F5 alone would have allowed (no marginal gain, only marginal
cost).

### R3-7. O2 — Two-tier corroborated-revision live machinery [OFFENSE] — PREREG ONLY UNTIL V4 RELEASED

**Mechanism.** The live form of the 621/621 offline replay: revision permitted
only on ≥2 agreeing high-conf PASS challengers, AND the pair passes the CC1
margin guard, AND neither challenger is within F5 exemplar distance of the
negative bank. This is the machinery behind the 86.6% claim — explicitly
marked UNBUILT.

**Why it survives the evidence — conditionally.** The offline replay proved
the rule recovers every withheld truth at 0 false installs; the contradiction
matrix proved the live form false-installs WITHOUT the margin guard and F5
preconditions. The hypothesis is that the preconditions close the CC1 hole.
It respects ceiling (2) because revision is historical (sequence-level), never
per-trial.

**Machinery needed:** UNBUILT — no live two-tier gate with margin guard and
F5 preconditions exists. V4 confirmatory trial HELD — this hypothesis may be
prereged but not built or run until Micah releases V4.

**Frozen kill bar.** KB-O2: RK-3 < 85% → KILL (the machinery exists only to
reach the bar). Any false install on the frozen decoy/install streams →
KILL. Any REVISED_INSTALL on the CC1 wrong-pair trials → KILL (the hole
re-opened). Runs not byte-identical → VOID.

### R3-8. FE2 — Family structural detectors [FRONT-END] — GATED ON FE1

**Mechanism.** For each novel family where FE1 exhibits a separator, build a
pure-Zag structural detector over the sense's formation inputs (the V2-C D1
pattern: D1 cut PTC-2 400→0; texture correlation rescued 86% of CCN-1 — the
one front-end intervention class with measured wins).

**Why it survives the evidence.** V2-C died as a system but D1 worked as a
detector; the failure was calibration-on-surrogates (D3_DEVIATION.md), which
FE1's frozen-target measurement repairs before any detector is built.

**Machinery needed:** none new — pure-Zag predicates.

**Frozen kill bar.** KB-FE2: per family, KILL the detector if it does not cut
that family's confident-wrong rate by ≥50% on frozen data at ≤5pp cost to
that family's true-PASS rate.

### R3-9. FE3 — Deliberate error-driven sense revision [FRONT-END] — LONG-HORIZON

**Mechanism.** The six timbredisc wrongs + the 12 TMB-5 wrongs become the
sense's training signal: a native sense-training loop that revises formation
weights from deliberate re-inspection reversals. The program-law endgame for
the front end: the brain learns from its caught mistakes deliberately, not by
background accumulation.

**Why it survives the evidence.** It is the only front-end hypothesis that
addresses the 53% novelty number at its root (formation) rather than at its
symptoms (detection). Every other front-end line concedes the sense's
formation as fixed.

**Machinery needed:** UNBUILT — no native sense-training loop exists in pure
Zag with byte-identical reruns. This is the largest machinery gap on the
slate.

**Frozen kill bar.** KB-FE3: KILL if the loop cannot be built in pure Zag
with byte-identical reruns. KILL if the retrained sense does not cut
held-out same-family confident-wrongs by ≥50% without RK-3 dropping >3pt.

---

## Build order (judge's recommendation)

1. **R3-1 (O1) first** — cheapest decisive experiment; the gap is measured.
2. **R3-2 (FE1) in parallel** — no build; de-risks R3-8 and scopes defense.
3. **R3-3 (D2) in parallel** — the program-law endgame for defense; F5's
   unbuilt half.
4. **R3-4 (D1) prereg now, run when the margin guard lands.**
5. **R3-5 (O3) after O1** — do not build a second sense before the delivery
   path is repaired.
6. **R3-6 (D3), R3-8 (FE2, gated on FE1), R3-9 (FE3, long-horizon)** in that
   order.
7. **R3-7 (O2)** stays prereg-only until Micah releases V4.

## What the slate marks UNBUILT (machinery nobody has built)

R3-3 (deliberate re-inspection organ), R3-5 (disjoint-window second sense),
R3-7 (live two-tier gate with guard + bank preconditions), R3-9 (native
sense-training loop). Each carries a build-feasibility kill bar first.

## Fable-5.1 audit outcome

PENDING — 3 batched-audit attempts, all `choices: null` / 0 completion
tokens (provider outage window, 2026-09-24). The 7-question audit prompt is
preserved at the crew's scratch (`~/workspace/tmp_commit/pam_r3/
fable_audit_prompt.txt`); re-run it when the provider recovers and append
the verdict here. The slate above stands on the native judge's ruling.
