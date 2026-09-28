# REDTEAM — Methodology attacks on the TNN native lab (ranked)

**Date:** 2026-09-21/22. Crew: methodology skeptic (red team, Micah's order
"TNN almost seems too good to be true").
**Scope:** experimental DESIGN, not results. Every attack below is grounded in
the program's own committed artifacts (`docs/lab/` on `tnn-native-lab`).
Two attacks were tested empirically by this crew (see
`paraphrase_attack/`); the rest carry concrete test designs.

**Ranking rule (parent guidance):** an attack the program already found and
documented itself ranks WEAKER than one pointing at an untested gap.
**Honesty rule:** "COULD be an artifact" ≠ "IS an artifact." Each attack
carries the author's judgment of which it is.

---

## 1. The truth-gap: no "does it believe true things" instrument (Sol #2, untested part)

**Severity: SERIOUS.** **Status: IS a real gap (program-admitted), untested.**

The program's own noisy-teacher verdict (q1n, 10% leg) states it plainly:
"§B.7 stays 12/12 because the battery does not see semantic truth… A 'does it
believe true things' instrument does not exist in this battery," and
"**DECIDED, per standing rule:** the 12/12 battery score is NOT evidence of
truth-preservation under a noisy teacher." The learner absorbed 19/19, 49/49,
99/99 taught falsehoods — a verbatim mirror — while the headline battery
stayed 96/96.

What exists: truth-grounded tests are thin — info-source (live web as ground
truth, 22 facts, 12/12 caught) and principle-detection (43 hand-built items,
13/13). What does not exist anywhere: provenance-sensitive scoring (does the
learner know WHERE a belief came from?), an abstention option ("I don't
know" scored for calibration), corruption placement the harness didn't choose
deterministically (`id % 10 == 0` is pattern-learnable in principle), or any
deletion/revision battery (see attack #7).

This doesn't refute the flaw battery — the program doesn't claim it measures
truth. It bounds the HEADLINE: every "96/96" citation in `FINDINGS_2026-09-21.md`
should carry the q1n qualifier, and currently the qualifier lives in the trial
doc while the number headlines. Sol's "consistency-with-oracle, not truth"
overlaps here and is WEAKER where it overlaps (the program found it first);
the UNTESTED part — provenance, abstention, unknown corruption — is the live
ammunition.

**Test design (concrete):** freeze a truth battery where (a) the teacher's
corruption schedule is chosen by an independent author AFTER the learner is
frozen, from real-world facts verifiable against two independent sources;
(b) probes offer explicit ABSTAIN, scored: correct=1, abstain=0.25,
wrong=−1 (calibration matters); (c) every installed belief carries a
source tag and probes score source-conditional recall ("what did the
low-trust source claim about X?"). Pure Zag, zero RNG, 5/5 byte-identical.
Kill bar: abstention-calibrated score ≥ 0.8 AND provenance accuracy ≥ 0.9.

---

## 2. Test-generation coupling (Sol #1) — CONFIRMED IN PART, by experiment

**Severity: SERIOUS (for v1 headlines).** **Status: IS an artifact of the v1
battery design — measured, not just hypothesized.**

This crew ran Sol's demanded test: 48 clean facts × 3 probe tiers through the
frozen v1 pipeline (battery predates scoring; pipeline predates the battery —
Sol's "unknown until frozen" condition satisfied). Results
(`paraphrase_attack/VERDICT.md`):

- Novel syntax, same vocabulary (mild): **Δ = 0.000** vs generator probes on
  both sources. Syntax costs nothing.
- Disjoint concept vocabulary (adversarial): sol 0.9375→**0.6875**,
  grok 0.7917→**0.5625** (−23 to −25pp). Misc-count family **collapses to
  0.167/0.250** — no unique entity token + replaced concept words → 0-overlap
  tie soup → lowest-id winner. Pub-year holds 1.000 on sol only because
  "Hamlet"/"Moby-Dick" are unique tokens (one shared token beats 240 zeros).

The v1 prereg's claim — "the test measures generalization across wordings,
not template memorization" — is weakened to: generalization across *the
generator's template inventory*, which shares vocabulary by construction. Note
the tell inside the frozen spec itself: the stemmer rules (`ication→ish`,
`ished→ish`) exist precisely to bridge the generator's train/probe template
pairs. The program's own v2 PARA result (0.26–0.63 single-exposure, 48/48 only
with dense 3-phrasing exposure) corroborates: phrasing brittleness is real.

**What it doesn't overturn:** the quality refutation WITHIN the generator's
distribution (Q=+0.0022 used identical coupled probes per source — the
comparison was fair); TNN-the-architecture's ceiling (v2/v3 are the
admittedly-shallow pipeline's successors). This battery was ADVERSARIAL by
design (worst case, not natural paraphrase).

**Test design (next):** natural-paraphrase battery by an independent author
who has never seen the pipeline code, blind to mechanism, scored frozen —
estimates the average case between mild (1.0×) and adversarial (0.6–0.7×).

---

## 3. "Exactly 4.000 ops/fact" is a tautology; "92 B/fact" is 2/3 hardcoded (Sol #3, untested part)

**Severity: SERIOUS (efficiency headline) / MINOR (actual science).**
**Status: IS an accounting artifact — verified in the driver source.**

Audit of `scale/driver/scale_learner.zag`:
- The ops counter increments exactly once per instrumented step: one `find`
  (dupe check), one `add`, one `verify`, one `audit` per taught fact. 4.000
  is **4 by construction**. Uncounted: the SHA-256 inside one "audit op,"
  all eval/probe-path finds (`sc_recall` doesn't touch the counter), corpus
  generation, the flaw battery's own work.
- `SCALE_MEM` prints `bpf_slot=24` and `bpf_idx=4` as **hardcoded literals**;
  only `bpf_audit` is computed from the run. "92 B/fact" is asserted, not
  measured, for 28 of 92 bytes.

The honest numbers survive: 4.2 µs/fact wall-clock (whole-binary user CPU)
and — the actual finding — **constancy** (no superlinear term; the hash
table doesn't degrade to 6.58M). But "exactly 4.000 ops/fact at every scale"
reads as a measurement and isn't one; the interesting empirical claim was
always "constant," not "4."

**Test design (concrete):** full-cost audit — rerun the scale driver with
counters on EVERY indexed operation including eval probes, corpus
generation, and verifier passes; replace the hardcoded 24/4 with measured
high-water-mark bytes per fact (allocator-aware). Report wall-clock per
phase. Kill bar: total measured ops/fact ≤ 2× the reported 4.000 (else the
headline is off by more than 2×).

---

## 4. RSI "exact reproduction" is vacuous on binary batteries

**Severity: SERIOUS (headline framing).** **Status: IS a design artifact —
the program's own verdict half-admits it.**

"+10000pp predicted → +10000 actual, 3/3 reproduced EXACTLY." The verifying
batteries are BINARY (single-probe fail→pass: F45 withhold, 2-domain spoof,
paraphrase recall). On a binary battery, ANY effective fix reproduces
"exactly" — the precision is in the design, not the prediction. Moreover the
predictions were derived from the same lab data the variants re-implemented;
the verdict says so: "the predictions reproduced exactly partly because they
were derived from the same mechanisms they targeted; that is honest
calibration, not a miracle," and grades the loop "B+ as an engineering loop;
'not yet' as autonomous invention."

The underlying loop result (diagnose→rank→predict→verify→refuse, 3 traps
refused with a working negative control) is real. The headline "reproduced
EXACTLY" overclaims relative to the verdict's own B+. This is the program's
recurring pattern (see #8): the trial doc is honest, the headline isn't.

**Test design (concrete):** RSI-1b — rerun with GRADED verifying batteries
(e.g., paraphrase recall over 48 items, not pass/fail) and require
|predicted − actual| ≤ 25% of predicted on the graded scale, with the
prediction registered before the variant is built and the variant built by
an author who hasn't seen the prediction.

---

## 5. Kill bars are tripwires, not discriminators — "all bars held" is weak confirmation

**Severity: SERIOUS (methodological).** **Status: IS true of the bar set —
quantified below; the program's HONORING of tripped bars is genuine.**

Sampled slack (observed vs bar):
- self-test KB-ST-OVERHEAD: bar 2.0, observed 0.0127 (**157× slack**).
- RSI KB2-CORRECT: bar ≥1/3 reproduced, observed 3/3 (on binary batteries).
- principle-detection KB-PD-DET: bar ≥90% on n=13 (allows a miss), observed 13/13.
- info-source KB-CATCH-RATE: bar ≥10/12, observed 12/12.
- The most devastating result in the program (q1n: 19/19 falsehoods absorbed)
  had **no kill bar at all** — measurement only.

Counter-evidence (honesty): when bars DO bind, the program honors them —
KB-PROSE-VIABLE tripped on all four sources → reported, v2/v3 dispatched, no
re-tuning; Track A J1 died by its own kill criterion; the R0 fork-exhaustion
recommendations were confirmed unchanged rather than "improved." The
disclosure norm is real. But it means "PASS" certifies "not catastrophically
broken," not "strongly confirmed" — and the absence of noise (parent's
"real science has noise") is fully explained: deterministic system +
synthetic batteries + wide bars ⇒ perfect scores are the EXPECTED outcome of
a correct implementation, not a miracle. The "too good to be true" feeling
dissolves into "bars too loose to be informative."

**Test design (concrete):** bar-sensitivity audit — for each trial, recompute
verdicts with bars tightened to 50% of observed slack; report which
headlines survive. Going forward: preregister bars at ≤2× the pilot
observation, not at round numbers.

---

## 6. Mid-run corrections: disclosed, pre-score — but battery edits are the ones to watch

**Severity: MINOR as practiced; SERIOUS if the norm slips.**
**Status: COULD be "retest until pass" — the evidence says it ISN'T, yet.**

Counted mid-run corrections: info-source A1 (distractor "300,000 km/s" →
"150,000 km/s" — the original wasn't actually false), info-source C3
(same-domain → two distinct domains), info-source hash-convention generator
fix, prose v1 test_grok.jsonl checksum re-freeze (Micah-signed), self-test
competition-implementation rewrite (pre-scored-run), Track B harness repairs
(ZNC-005/006/007).

All are disclosed in verdict "build notes," timed pre-score, and the
battery-CONTENT edits (A1, C3, checksum re-freeze) each moved the battery
TOWARD the prereg's stated intent with dated amendments — two of them
Micah-signed. That's the deliberate-repair culture working as designed, and
the alternative (abandon on first bug) would be wasteful. The residual risk:
there is no INDEPENDENT check that a "fix" didn't also make the battery
easier; disclosure + pre-score timing is the entire control. One control,
no redundancy.

**Test design (concrete):** re-freeze audit — an independent crew re-verifies
every committed battery SHA against its prereg SHA across all trials,
flags every amendment, and re-scores one trial per battery from the
PRE-amendment battery to quantify amendment effect size. (This crew verified
the paraphrase battery's own freeze: `f6189f4b…22fad`, pre-score.)

---

## 7. No deletion/revision battery exists (Sol #3, untested)

**Severity: SERIOUS (capability gap) / MINOR (as an attack on current claims).**
**Status: IS an untested gap.**

Everything is install-only. Principle-detection's "refinement" is
logged-not-applied (verdict: "deliberate principle revision is future work").
Strength-trial ruling 4 (overwrite semantics: direct write vs literal add
path) is still parked awaiting Micah. No battery tests: unlearning a false
belief, correcting a taught falsehood after install, or withdrawing a claim.
A memory system that can only add is half a memory system — and the
noisy-teacher result (19/19 absorbed) makes revision load-bearing: without
it, every absorbed falsehood is permanent.

Not an attack on any current claim (the program doesn't claim revision
works). It IS the largest untested capability adjacent to the program's
core thesis.

**Test design (concrete):** teach A (trust 50) → teach ¬A (trust 90) → probe:
expect WITHDRAW of A, install of ¬A, audit shows both. Then: deliberate
DELETE directive on a fact → probe must miss; then re-teach → probe hits.
Kill bars: revision correctness ≥ 95%, no residue (probe-after-delete = 0%),
5/5 byte-identical. Pure Zag, zero RNG.

---

## 8. Headline-vs-fine-print framing asymmetry (parent #5/#6, Sol overlap)

**Severity: MINOR (the disclosure record is unusually good).**
**Status: COULD be selection bias — the evidence mostly says it ISN'T,
with one surviving kernel.**

The program reports negatives you wouldn't expect from a hype operation:
prose v1's bar trip on all four sources, senses qualitative-percepts kill
(54.0% vs 72.6%, both under the false-install ceiling), J1 dead by its own
criterion, SWE behaviorally banned, hy3/GLM dropped, the model-quality
hypothesis ABANDONED after two refutations, q1n's "verbatim mirror"
devastation published plainly. `FINDINGS_2026-09-21.md` includes nulls.

The surviving kernel is FRAMING, not suppression: nulls are narrated as
findings ("two nulls that are actually the finding"); the trial docs carry
honest B+ grades and "not a miracle" qualifiers while headlines cite
"3/3 reproduced EXACTLY" and "96/96"; the q1n qualifier ("NOT evidence of
truth-preservation") lives in the trial doc while 96/96 headlines. With the
"test both" culture running dozens of preregistered experiments, the
headlines will always be drawable from the passes. The defense is real too:
preregistration + mechanical bars + committed logs make the full record
auditable — which is exactly what this redteam did.

**Test design (concrete):** headline audit — for each claim in
`FINDINGS_2026-09-21.md`, check the linked verdict's caveats/limits section
is faithfully summarized in one sentence next to the number. Publish the
diff.

---

## 9. "Frozen prereg written by the experimenters" (parent #1)

**Severity: MINOR.** **Status: COULD be self-dealing — mitigations are real
but single-layered.**

True: the crew writes the prereg, builds the binary, and (via an "independent"
oracle) checks it. Mitigations: oracles share no code with the binary; bars
are applied mechanically; amendments are dated; content changes are
Micah-signed; logs are byte-identical and re-runnable. The residual, admitted
by the self-test verdict itself: "a subtler adjudication bug (wrong bar
constant shared by a misread prereg) would need prereg-vs-code review" —
oracle and binary share the SPEC AUTHOR's interpretation. 400/400
verdict/oracle agreement is agreement between two implementations of one
author's reading.

**Test design (concrete):** adversarial oracle — a second author who has not
seen the implementation reimplements the scorer from the prereg TEXT alone;
any verdict disagreement is investigated as spec ambiguity, not
implementation bug.

---

## 10. "Byte-identical" is determinism, not intelligence (parent #3)

**Severity: MINOR as a standalone attack.** **Status: attacks a claim nobody
makes — useful only as a lens on #2.**

Determinism is Micah's LAW (a constraint on the substrate), never presented
as the intelligence evidence. The intelligence evidence is the generalization
battery set — whose strength is exactly what's at issue in #1 and #2. Where
generalization is genuinely external (info-source live web 12/12;
principle-derivation 13/13 with no second claim present), the lookup-table
objection fails outright. Where the battery is generator-coupled (v1 prose),
the objection bites — and attack #2 measured the bite (misc-family 0.167).
A lookup table with Jaccard addressing is byte-identical too; byte-identity
distinguishes implementations, never capabilities. Not separately testable
beyond #1/#2.

---

## Synthesis: what survives contact with the evidence

**Strongest validated attacks:** #2 (measured: vocabulary-coupled
"generalization," −25pp adversarial, misc collapse to 0.167), #3 (measured:
4.000-by-construction, 92B 2/3 hardcoded), #4 (binary batteries make "exact"
reproduction vacuous), #5 (bars are tripwires; perfect scores are the expected
outcome, not a miracle).

**Real untested gaps (ranked above self-found issues per guidance):** #1
(truth/provenance/abstention instrument), #7 (deletion/revision battery).

**Weak or redundant:** #8 (disclosure record is genuinely good; only the
framing kernel survives), #9 (mitigations real, single-layered), #10
(attacks an unmade claim).

**What the skeptic concedes:** the program's disclosure norms — dated
amendments, build-notes sections, honored tripwires (v1, J1), published
devastations (q1n), self-graded B+s, Micah-signing for content changes —
are better than most labs'. The attacks above are mostly about what the
headlines IMPLY beyond what the trial docs SUPPORT, plus two genuinely
untested capabilities. The program is not fabricating; it is, in places,
overclaiming the inferential reach of synthetic, wide-barred, generator-
coupled batteries. The fix is not less testing — it's tighter bars (#5),
independent batteries (#2, #9), truth instruments (#1), and revision (#7).

## Artifacts

- `paraphrase_attack/` — PREREG.md (frozen pre-score), paraphrases.py,
  paraphrase_battery.jsonl (sha256 `f6189f4b…22fad`), score_paraphrase.py,
  results.json, VERDICT.md.
- This file: `RANKED_ATTACKS_2026-09-21.md`.
