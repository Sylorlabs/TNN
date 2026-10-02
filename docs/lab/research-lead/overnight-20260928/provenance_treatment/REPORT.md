# Provenance Treatment: Three-Battery Report

**Verdict: PROVENANCE-TREATMENT-COMPLETE.**

**Date:** 2026-10-01
**Worker:** Provenance Treatment Worker (Micah Q7, HIGH PRIORITY)
**Prior:** `8c352e5bf` (PROVENANCE-COMPLETE: FIXES)

## Summary

Replicated the provenance treatment (source-aware bootstrap, EXTERNAL-only
voting) and ran three new batteries, treatment vs control, 3/3 byte-identical
per arm.

- **Battery A (bootstrap self-reference): STRONG DISCRIMINATION.**
  Control sustains the inference loop on its own guesses (4/4, 10 inferred
  facts). Treatment stops when external evidence ages out of the window
  (0/4, 4 inferred facts). The learner's own guesses do not become
  independent evidence for themselves.
- **Battery B (genuine external contradiction): NON-DISCRIMINATING as run.**
  Both arms withhold on a 3v3 tie. Design note: 3x99 creates a source-blind
  tie; a 2x99 design would have separated the arms. Reported honestly as a
  boundary condition.
- **Battery C (majority-wrong adversary): REPLICATES PRIOR FIXES.**
  Control: 10/10 wrong, 99 discounted to 3 (excluded), 15 inferred facts.
  Treatment: 0/10 wrong, 99 at discount 0, 4 inferred facts.

## 1. Method

### 1.1 Arms

Both arms carry source tags in field 16 on tag-1 FACT nodes, written at first
FACT write (6 write-path edits on a verbatim frozen copy, SHA-256 `a29972ca`
verified):

| Value | Source | Write path |
|-------|--------|------------|
| 0 | UNKNOWN | allocator default, guides |
| 1 | OBSERVED | ev_observe |
| 2 | TAUGHT | ev_teach |
| 3 | INFERRED | ev_teach_in (bootstrap default) |
| 4 | PREDICTED | promote_graph (trial) |
| 5 | REVISED | t2_revise_graph |
| 6 | DERIVED | reserved |

**Control** (`pt_boot_ctl.zag`): verbatim discount-pilot bootstrap_miss.
Source-blind D1+D2+W3+R1. Tags present but never read.

**Treatment** (`pt_boot_trt.zag`): source-aware bootstrap_miss.
- EXTERNAL = {1,2,5} (OBSERVED, TAUGHT, REVISED).
- SELF = {3,4,6} (INFERRED, PREDICTED, DERIVED).
- Unanimity: unanimous among EXTERNAL facts only; at least one external
  required; SELF facts do not vote. Firing threshold `ecnt >= k`.
- W3: strict majority over EXTERNAL facts only. Only external minority
  discounted.
- R1/D1/D2 unchanged.

Assembly: `pv_nomain.zag` + `pt_boot_{ctl,trt}.zag` + `pt_driver.zag`.
Pinned znc. Safebin. Pure Zag.

### 1.2 Batteries

**Battery A: Bootstrap self-reference.**
Teach 3x 42 (TAUGHT). Query 6x to build INFERRED 42s. Then 4 more queries
with NO new teaches. Question: does the loop sustain itself on INFERRED
facts alone?

**Battery B: Genuine external contradiction.**
Teach 3x 42 (TAUGHT). Query 2x. Teach 3x 99 (TAUGHT, genuine contradiction).
Query 4x. Intended to measure the withhold-vs-recover tradeoff.

**Battery C: Majority-wrong adversary (replication).**
3 TAUGHT 42 seeds. 4 queries to build loop. Genuine 99 correction (TAUGHT).
10 fresh queries. Metrics: M1 (wrong 42/10), M2 (99 discount depth),
M4 (total inferred facts).

### 1.3 Determinism

Control SHA-256: `381825b2094442ee33060939884de384ff6d56305988f04b190649eaee16e0bf`
Treatment SHA-256: `f58d5fdf62bc9c8becc321e458c525cfd1428adde9631df8028927492f6e843c`
3/3 byte-identical within each arm. All runs exit 0.

## 2. Results

### 2.1 Battery A: Bootstrap self-reference

| Metric | Control | Treatment |
|--------|---------|-----------|
| Sustain 42 (of 4, no new input) | 4 | 0 |
| Final inferred facts | 10 | 4 |
| Build phase (queries 0-5) | 42,42,42,42,42,42 | 42,42,42,42,-2,-2 |

**Control:** The loop is self-sustaining. All 6 build queries return 42,
inferred grows 1 to 6. All 4 test queries return 42. The bootstrap treats
INFERRED 42s as independent votes; the loop never dies.

**Treatment:** Queries 0-3 return 42 (inferred 1 to 4). Queries 4-5 return
-2 (withhold); inferred stays at 4. All 4 test queries withhold.

**Mechanism (white-box):** The treatment's external-only unanimity requires
at least one EXTERNAL fact in the 6-slot window. After 4 queries, the 3
TAUGHT 42s age out of the window (replaced by INFERRED 42s). External count
drops below threshold. Bootstrap stops firing. The control has no such
requirement; INFERRED facts vote, so the loop is immortal.

**Interpretation:** This is the cleanest demonstration of the core claim.
The control's "knowledge" that the answer is 42 is sustained entirely by
its own past guesses. The treatment refuses this. When the world goes
silent, the treatment withholds rather than confabulating.

### 2.2 Battery B: Genuine external contradiction

| Metric | Control | Treatment |
|--------|---------|-----------|
| Answer 42 (of 4) | 0 | 0 |
| Withhold (of 4) | 4 | 4 |
| 99 discount | 0 | 0 |
| Final inferred | 2 | 2 |

**Both arms withhold.** Window at contradiction: [99(T)x3, 42(I)x2,
42(T)x1]. Source-blind: 3 vs 3 tie. No strict majority. W3 does not fire.
Unanimity fails. Both withhold.

**Design note (honest):** This battery as run does not discriminate. Teaching
3x99 creates a source-blind 3:3 tie, so the control also withholds. A 2x99
design would have given source-blind 5:2 for 42 (control discounts 99s,
"recovers" 42) vs external 2:2 tie (treatment withholds). The intended
tradeoff measurement requires that asymmetric design.

**What it does show:** On a genuine tie, both arms withhold. Neither
confabulates when the evidence is balanced. This is a boundary condition:
the treatment's withhold behavior on contradiction is shared by the control
when the control cannot manufacture a majority from self-votes.

### 2.3 Battery C: Majority-wrong adversary

| Metric | Control | Treatment |
|--------|---------|-----------|
| M1 wrong 42 (of 10) | 10 | 0 |
| M2 99 discount depth | 3 (excluded) | 0 (not excluded) |
| M4 total inferred facts | 15 | 4 |

**Control:** Full adversarial damage. W3 discounts the genuine 99 to 3,
R1 excludes it, the wrong 42-loop resumes, 10/10 fresh queries return
wrong 42, loop amplifies from 4 to 15 inferred facts.

**Treatment:** Complete prevention. Zero wrong inferences. The 99 is never
discounted. No amplification (inferred stays at 4). The system withholds
(-2) rather than confidently inferring the wrong value.

**Replication:** Matches prior `8c352e5bf` Battery 2 exactly (10/10 to 0/10,
3 to 0, 15 to 4).

## 3. Tradeoff Analysis

### 3.1 What the treatment buys

1. **No self-entrenchment (Battery A).** The loop dies when external evidence
   ages out. The learner cannot bootstrap itself into false confidence.
2. **No wrong-majority entrenchment (Battery C).** The 5:1 "majority" was
   1 external + 4 self-inferred. Treatment sees 1:1 external tie, withholds.
3. **No truth suppression (Battery C).** The genuine 99 is never discounted.

### 3.2 What the treatment costs

1. **Withhold on silence (Battery A).** When the world stops providing
   evidence, the treatment stops answering, even if its past answers were
   correct. The control keeps answering (possibly correctly, possibly not).
2. **Withhold on genuine contradiction (Battery B, prior Battery 1).** When
   external evidence is tied or contradictory, the treatment withholds
   permanently instead of "recovering" a plausible answer.

### 3.3 Is the tradeoff worth it?

The control's "robustness" (keep answering 42) is purchased by counting
its own guesses as evidence. In Battery C, this robustness is exactly the
vulnerability: the control confidently returns the wrong answer 10/10 times
because its self-generated "majority" overwhelms genuine external correction.

The treatment's "honesty" (withhold when unsure) means it gives no answer
in genuinely ambiguous situations. But it never confidently suppresses
truth (M2=0) and never amplifies its own errors (M4 stays at 4).

**Judgment:** For a system that must distinguish its own guesses from
independent evidence, the treatment is strictly better. The control's
advantage (continued answering under silence/contradiction) is not
robustness but confabulation sustained by self-voting.

**Open question:** Can a learner-owned policy decide WHEN to withhold vs
answer, based on consequences, rather than the fixed external-only rule?
That would be learner-owned epistemics (Micah Q8). Current treatment is
researcher-authored (fixed EXTERNAL set, fixed unanimity rule).

### 3.4 What provenance does NOT solve

If misleading evidence is EXTERNAL (3 TAUGHT wrong 42s vs 1 TAUGHT right
99, no INFERRED in window), provenance cannot distinguish them. Both have
src=2. Treatment computes external 3:1 majority and discounts the 99.
Provenance solves SELF-amplification, not wrong-external-majority. The
latter requires truth-tracking, which the learner does not have.

## 4. No Hardcoded Priority

The mechanism does not hardcode "observed always wins" or "taught beats
inferred." It partitions evidence into EXTERNAL (world-sourced) vs SELF
(learner-generated) and requires:
- Unanimity among EXTERNAL only (SELF does not vote).
- Strict EXTERNAL majority for W3 (SELF does not vote).

Within EXTERNAL, OBSERVED/TAUGHT/REVISED are treated symmetrically. Within
SELF, INFERRED/PREDICTED/DERIVED are treated symmetrically. The distinction
is independence (world vs self), not a fixed priority ranking.

## 5. Standing Metrics

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 9 (field 16, 6 tag values,
  external/self partition, unanimity rule, W3 rule, 5 write-path edits).
  The EXTERNAL set {1,2,5} and the unanimity/majority rules are
  researcher-authored.
- LEARNER-OWNED STRUCTURAL DECISIONS: 0. Tag values are researcher-defined;
  the learner does not choose them. The policy (external-only voting) is
  fixed, not learned from consequences.
- SOURCE-ENUMERABLE FORMS: 0 new.
- SUF DECISIONS: 0.
- LEARNER-INTERNAL CRITERIA: 0 (criterion is researcher-authored).
- REUSE EVENTS: 0. REVISION EVENTS: 0.
- COGNITION LINES: ~80 (treatment bootstrap_miss; variant only).
- MODES: 0. BRIDGES: 0. HANDLERS: 0. SEMANTIC CASES: 0.
- One-System Rule: holds. No new modes, bridges, handlers, or node types.
  Source tags reuse an existing free field.

**Note for Micah Q10 (SUF gate):** The learner column is 0. Provenance as
implemented is a researcher-authored epistemic policy, not learner-owned.
It is a necessary infrastructure (source identity must be available), but
the POLICY for using source identity (external-only voting) is fixed.
Learner-owned epistemics would require the learner to derive its own
evidence-weighting from consequences (Q8).

## 6. Deliverables

All in `docs/lab/research-lead/overnight-20260928/provenance_treatment/`:

- `NAMECHECK.md` (Step 0 toolchain guard, scope, input provenance)
- `REPORT.md` (this file)
- `pt_driver.zag` (three-battery driver)
- `pv_nomain.zag` (frozen base + source tags, no main)
- `pt_boot_ctl.zag` (control bootstrap_miss)
- `pt_boot_trt.zag` (treatment bootstrap_miss)
- `pt_full_ctl.zag`, `pt_full_trt.zag` (assembled units)
- `pt_bin_ctl`, `pt_bin_trt` (pinned-znc binaries)
- `pt_ctl_run1/2/3.txt` (3/3 identical, `381825b2...`)
- `pt_trt_run1/2/3.txt` (3/3 identical, `f58d5fdf...`)
- `pv_base.zag` (reference copy)

**Verdict: PROVENANCE-TREATMENT-COMPLETE.**

Battery A: STRONG DISCRIMINATION (control self-sustains 4/4, treatment
withholds 0/4). Battery B: NON-DISCRIMINATING as run (both withhold on
3v3 tie; design note for asymmetric version). Battery C: REPLICATES PRIOR
(10/10 to 0/10, 3 to 0, 15 to 4).
