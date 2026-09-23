# KB4 — Investigation Swarm on the Whys

**Date:** 2026-09-22
**Scope:** analysis of frozen evidence ONLY. No new architecture built or
tested; no frozen bar modified. The SUSPECT-gate redesign
(`PREREG_DRAFT_SUSPECT_GATE.md`) remains unsigned and untouched — read for
context only by one crew, depended on by none.
**Parent document:** `AUTOPSY.md` in this directory (commit
`66fbb329aa831c14f3f3100a20e177bbb12e27b1`), which found the frozen install
rule Bayes-optimal for its inputs and every rule/architecture probe failing
at 41–65%. This swarm goes deeper on *why*, with new hypotheses, formal
derivations, and falsifier tests against the frozen ledger.
**Method:** five crews (W1 observational identity, W2 minimal signal, W3 L8
complicity, W4 binding trade, W5 falsifier audit) working in parallel on
read-only frozen inputs:
`prose-learning/epistemic_wave/kb4_rerun/`
(`batch_{A,B}.txt`, `out_{A,B}_rep1.txt`, `truth.json`, `mappings.json`,
`epi_kb4_scores.json`) and `kb/autopsy/probes/` (all probe outputs,
`pa1_truth.json`, `probe_scores.json`). Zero RNG anywhere; every
recomputation rerun 3× byte-identical; all 3 gate-output reps are
SHA256-identical so rep1 suffices. Working sections and scripts live in
`~/workspace/kb4-why/` (W1..W5 `.md` + analysis scripts, intermediate
scratch — NOT committed; this report is the committed deliverable).

## 0. Verdict in plain language

The KB4 gate fails because it is asked to answer a question its input
cannot answer. On the judgment stream alone, "my sense was fooled" and
"the world really changed" look **identical** — measured at 0.02–0.03 bits
of information out of ~1 bit needed (W1). The frozen rule is already the
best possible rule for that input: on approach A it sits *exactly* on the
provable accuracy ceiling (W1, W5). Every probe the autopsy ran — deleting
the repetition bonus, deleting the conflict rule, fixing the stimulus
binding, adding a second corroborating sense — fails, because none of them
adds the one thing missing: an independent observation of the adversarial
stimulus (or a causal model of what the perturbation does to the truth).
Two crews independently proved the failure ceiling is algebraic, not a
search gap: even a perfect truth-preservation oracle cannot make a binary
gate clear both bars (W2 brute force over all 16 rules; W5 linear-program
proof over the whole policy simplex, including stochastic rules). That is
why the SUSPECT third state in the draft prereg is load-bearing, not
optional — but it is still unsigned, so nothing here builds it.

## 1. Ranking of the whys

Ranked by explanatory power: if this why were false, how much of the
41–46% failure would be left unexplained.

| Rank | Why | Explains | Falsifier | Ledger evidence | Status |
|---|---|---|---|---|---|
| 1 | **Observational identity / information starvation.** (fooled sense, truth unchanged) vs (changed stimulus, sense correct) are identical on the judgment stream. | The whole irreducible gap: optimal rule fails at 41.25%/44.09% vs the 15% bar (~26–29pp no rule can recover). | Some measurable statistic of the gate's observation separates the two hypotheses across strata. | I(match-bit; H) = 0.019 bits (A) / 0.033 bits (B). 42 (A) / 51 (B) twin pairs; B `colordisc/p000` vs `colordisc/p015` byte-identical O=(SAME,SAME,950,950), one truth one poison. 12 O-features tested, none separates; `task` is fixture-plan memorization; confidence sign-flips across strata; even the hidden truth-change flag is anti-informative (53.8%/55.7%). | HOLDS |
| 2 | **Wrong ontology: stimulus bound across the perturbation boundary.** The gate files the adversarial judgment under the primary stimulus id, manufacturing a "conflict" that doesn't exist. | Where the gate mislocates the problem; every 8-cell mode is defined relative to this binding. | A binding choice on gate-available inputs that reduces total errors below 77/73. | P-A2 (re-slotted) decision streams 0 mismatches vs P-L2 (924/924 A, 925/925 B). All 5 slot partitions simulated: minima 77 (A, frozen) / 73 (B). | HOLDS |
| 3 | **L4's single-hypothesis conflict model; no "world changed", no SUSPECT.** L4 is the only working defense AND the sole author of M3. | M3 truth-withheld: 44/184 A (23.9%), 31/185 B — direct cause of A's DEGENERATE. | Removing L4 leaves M3 cells non-zero, or doesn't raise the rate. | P-L2: rate 41.25→50.54% (A), 46.46→54.59% (B); M3 cells 44→0, 31→0 exactly. | HOLDS |
| 4 | **Correlated-channel vulnerability.** Cross-sense corroboration installs poison with two witnesses. | Why the natural architectural repair fails *worse* (43.48% vs 41.25%). | The both-fooled-and-agreeing count ≠ 50/184, or the gate didn't install them. | `pa1_truth.json`: 50/184 (27.2%) both wrong and agreeing; installed 50/50. `probe_scores.json`: 115 installs / 50 false / 65 true. | HOLDS |
| 5 | **Confidence admitted as evidence despite being anti-informative.** | Real design error; small measured rate contribution. | mean conf(correct) ≥ mean conf(wrong) on either approach. | A: wrong 439.1 ≥ correct 429.8 (+9.3); B: wrong 861.4 ≥ correct 849.4 (+12.0). B's 6 evidence-rule deviants cost +2.4pp; A never moved by confidence. | HOLDS |
| 6 | **L8 repetition bonus equates consistency with correctness.** | Fallacy is real in the rule's design but decision-irrelevant. | Any M2 fixture whose decision flips without L8. | A: 0/924 lines flip (P-L1 byte-identical decisions). B: 6 conflict lines flip (5 poison installs averted, 1 true install lost) — via the rejected-judgment attractor channel, not M2. | HOLDS (with correction below) |

## 2. Why-by-why, with the new evidence

### 2.1 Rank 1 — Observational identity (W1)

The gate's observation vector per fixture is
O = (primary judgment, adversarial judgment, 2 confidences, source,
source track record, stimulus history, batch position) — and three of
those are degenerate on the frozen ledger (single sense; `src_bad` never
flips on A; fixed batch order). Likelihood ratios P(O|changed)/P(O|fooled)
for the only live feature (match/differ): 1.46 / 0.75 (A), 1.52 / 0.64
(B) — every observation occurs under both hypotheses, none rules either
out. For any deterministic rule, errors ≥ Σ_g min(n₀,n₁) over observation
groups: accuracy ceiling **58.15% (A) / 60.54% (B)**. The frozen gate is at
58.15% / 58.38% — on A it is *provably* the Bayes-optimal judgment-only
rule. All four deterministic match-bit rules fail both bars by exhaustion;
the ceiling is structural.

### 2.2 Rank 2 — The binding trade is conservation, not correction (W4)

P-A2 ≡ P-L2 is not an aggregate coincidence: 0 decision mismatches on
every line (924/924 A, 925/925 B). Both probes are the constant INSTALL
function reached by different routes — P-L2 deleted the conflict *rule*
(ev ≥ 5 always), P-A2 deleted the conflict *relation* (every adversarial
line lands in a virgin slot → first-impression install). The cross-variant
conflict bit **was** the gate's entire discrimination. Re-binning deletes
the only (fooled-vs-changed)-correlated statistic in the stream
(P(advC|match) 0.588/0.559 vs P(advC|differ) 0.423/0.348). The differ-block
flips en bloc: A recovers 44 true installs at the price of 60 new false
ones (**1.36 false installs per recovered truth**, net errors 77→93);
B: 31 for 55 (**1.77 each**, net 77→101). It is not 1:1 — the trade is
priced against the gate. The block-constant optimum (77 A / 73 B) is
attained by the frozen binding on A; no partition or reweighting of the
same inputs beats 77/73, and even a label-cheating empirical-Bayes ceiling
only reaches 74/69. The information that would let any binding win —
per-fixture fooled-vs-changed — lives in the unobserved
perturbation-truth mapping.

### 2.3 Rank 3 — L4, load-bearing and broken (W5 recomputation)

The frozen gate's only working mode is "sense fooled AND judgment changed"
(51 A / 37 B). Removing L4 raises the rate ~9pp on both approaches — it is
the gate's sole defense — and deletes the M3 cells exactly (44→0, 31→0):
it is also the sole author of the largest failure cell (23.9% of A).
"Load-bearing and broken" is not a contradiction; it is the signature of a
mechanism doing the wrong job well. The rule's hypothesis space contains
only "my sense was wrong" — it cannot represent "the world changed", so
every truth-change is misclassified as sense-error.

### 2.4 Rank 4 — Corroboration corroborates poison (W5 recomputation)

Wave-5's 35/35 defense was against transient spoofing of a *stable* truth.
KB4's adversary perturbs the *stimulus itself*, so there is no stable anchor:
it fools both channels correlatively on 50/184 (27.2%) adversarial
fixtures, and agree→install converts all 50 into poison installs. This
bounds the "add a second judgment channel" repair — the new channel must
be *causally* independent (different physical basis, analytic/causal check,
or human override), never a second ML judgment on the same pipeline.

### 2.5 Rank 5 — Confidence (W5 recomputation)

Wrong ≥ correct on both approaches, independently re-derived (exact match
with autopsy). B's 6 evidence-rule differ-installs (5 false) are the
measured cost (+2.4pp); A coincides exactly with the pure match rule, so
confidence never moved an A decision. Real error, minor rate contribution —
removing it changes no verdict.

### 2.6 Rank 6 — L8: the autopsy's story was wrong in a precise way (W3)

W3 reimplemented the gate in Python, reproducing all four frozen output
files byte-identically, then instrumented it. Two structural facts:
the CONSISTENT branch can *never* withhold (ev ≥ 15 even without L8 —
observed minimum 35), and on FIRST the L8 term is identically 0. The only
live boundary L8 can move is CONFLICT's `ev > eev`. On A, **zero** conflict
lines had prior>0 — L8's challenger-side +20 never fired once; all its
A-effect was incumbent fortification. 443/924 lines differ in the evidence
column only; **0 decision flips** — P-L1 is 924/924 decision-identical on
A. The M2 "consistent error" cell — which the autopsy pinned on L8 — is
100% amplifier on both approaches: every install was sealed at the primary
line with L8 contributing exactly 0 (traced: `colorconst/p018`,
`colordisc/p023`, `colordisc/p025` with exact line numbers and evidence
values). L8's real complicity is narrower: a **rejected-judgment attractor
channel** — on B, 6 conflict adversarial lines won only because the
*refused* noise-variant judgment sat in history earning +20 (all
shapetrans; 5 poison installs, 1 true install; one also flipped the global
`src_bad`). A: 0 attractor / 443 amplifier lines (+10,460 pure bonus).
B: 6 attractor / 429 amplifier (+10,280). So: L8 is complicit and
decorative on A, genuinely load-bearing (−2.4pp) on B, but never through
the mechanism the autopsy narrative described.

## 3. The minimal signal — and its honest limit (W2)

Cheapest genuine separator: the per-fixture truth-preservation bit T =
"did this perturbation change the ground truth?", carried realistically as
a **perturbation-class → truth-effect table** (6 task-level entries;
sense-independent — colorconst 0.00, colordisc 0.17, motiondir 0.90,
pitchdisc 0.57, shapetrans 0.55, timbredisc 0.77 — so learnable in
principle). With T known the identity breaks exactly
(T=0∧differ ⇒ fooled; T=1∧differ ⇒ changed stimulus). New ledger fact:
**M1 is 100% stale-on-changed-truth** — all 21 (A) / 16 (B) silent
failures have T=1: the truth moved under a sense that repeated the old
judgment; no match-rule can ever catch these. Cheaper candidates are inert:
variant flag 41.2%/46.5% (already implicit); noise re-presentation ~inert
(noise never changes truth, 0/369, and stability ≠ truth); confidence
deltas weak and sign-inconsistent across senses. The honest limit:
**brute force over all 16 binary rules on {(T,match)} proves no rule
reaches (≤15% ∧ ≥50 true installs) even with perfect T** — minimum rate at
≥50 true: 28.4% (A) / 42.2% (B); the binary fork is 14.0% DEGENERATE
(withhold T=1) vs 40.4% FAIL (install T=1), because T=1 judgments are
44/96 (A) / 39/97 (B) correct — worse than coin-flip — and their
correctness is invisible from the judgment stream. Residual falsifiers
under oracle-T: consistent error on preserved truth (7/16 — needs a
primary-correctness signal); changed-truth correctness fork (44/39 true
foregone vs 52/58 false under install); sense self-correction (4/5); class
ambiguity (74/75 fixtures in ~coin-flip classes; novel classes have no
entry — structural). The SUSPECT third state (or a causal/analytic channel
at rank 4, or a perturbation-effect forward model) is load-bearing, not
optional.

## 4. Corrections to AUTOPSY.md established by this swarm

1. **B has 185 paired adversarial fixtures, not 184** (W1, W5; the autopsy
   8-cell B table sums to 185 — the extra fixture is one of the 6 L4
   re-deliberation deviants).
2. **"L8 rewards M2 (+20 per repeat)" is true of the evidence numbers but
   decision-irrelevant** (W3): M2 installs were sealed at the primary line
   with L8 at 0. L8's actual decision-level complicity is the
   rejected-judgment attractor channel, exercised only by B.
3. **The binding trade is not 1:1** (W4): 1.36 (A) / 1.77 (B) false installs
   per recovered true install; total errors rise (+16/+24). The frozen
   binding bets the winning side of the only available bet on both
   approaches (differ-block base-rate ratios 0.73 A / 0.53 B favor withhold).
4. **The impossibility is algebraic, not a search gap** (W5): ≤15% forces
   α_m=α_d=0 (zero installs) on the whole policy simplex, both approaches —
   strengthening the autopsy's four-policy table. No stochastic
   judgment-only policy can pass either.
5. **"withhold all differs" / "install all differs" answered explicitly**
   (W5): A 41.25% DEGENERATE / 50.54% FAIL; B 44.09% FAIL / 54.59% FAIL.
6. **A's gate = the match rule exactly** (W1): 0/184 deviations, `src_bad`
   never flips, noise never changes the endorsed judgment. B's 6 deviants
   are all shapetrans L4 re-deliberation misfires at batch lines ≥ 432;
   5/6 installed poison (W1, W3).

## 5. What this report does NOT do

- It builds, tests, and freezes nothing. The SUSPECT-gate draft remains
  DRAFT/unsigned; no crew implemented any part of it.
- It modifies no frozen bar and no frozen rule.
- It collects no new data requiring architecture changes: all numbers are
  re-derivations from the frozen ledger (truth.json used as scorer oracle
  only, except in explicitly-marked oracle-ceiling simulations).
- One caveat carried from W5: the impossibility proofs are scoped to
  judgment-side inputs. If a future analysis finds a latent informative
  signal in the frozen ledger (noise-variant agreement was checked: 363/370
  A, 336/370 B — nearly constant, null), the bound needs re-derivation.

## 6. Reproducibility

Each crew's section (W1..W5 `.md` in `~/workspace/kb4-why/`) carries its
own reproduction commands and expected hashes; every analysis ran 3×
byte-identical with zero RNG. Key checks:

```bash
cd ~/workspace/kb4-why
python3 W1_identity.py            # → W1_identity_results.json, sha256 312ffcb0…
python3 w5_recompute.py > r.txt   # 3× byte-identical (cmp clean)
python3 w4_analysis.py            # 3× byte-identical, sha256 b39f7779…
# W3 exact gate model reproduces all frozen outputs byte-for-byte:
python3 w3_gate_model.py ~/workspace/tnn-lab/prose-learning/epistemic_wave/kb4_rerun/batch_A.txt 1 /tmp/x.txt
cmp /tmp/x.txt ~/workspace/tnn-lab/prose-learning/epistemic_wave/kb4_rerun/out_A_rep1.txt
diff ~/workspace/tnn-lab/prose-learning/epistemic_wave/kb4_rerun/kb4_gate.zag \
     ~/workspace/tnn-lab/kb/autopsy/probes/probe_pa2.zag   # IDENTICAL: P-A2 logic = frozen logic
```

**One-sentence verdict:** KB4 fails at a provable ceiling — the two
hypotheses the gate must separate are observationally identical on its
input (0.02–0.03 bits of ~1 needed), the frozen rule is already the
optimal judgment-only rule on A, and no rule, re-binning, or correlated
second channel can pass the joint bars (proven algebraically, not by
search); only new information — an independent observation of the
adversarial stimulus, a perturbation-truth model, or the unsigned SUSPECT
state — can break the identity.
