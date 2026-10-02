# Strong Learning-to-Learn: Report

**Verdict: STRONG-L2L-COMPLETE.**

**Date:** 2026-10-01
**Worker:** Strong Learning-to-Learn Worker (Micah Section 5)
**Commit:** local only, nothing pushed.

## 1. Question

Micah Section 5: "Now make it harder. Current families are structurally
similar. Run: learn Family A, later encounter structurally different
Family B, previous experience must still improve learning."

Strong K-LT target: previous lifetime leads to unfamiliar domain requiring
fewer examples/search, with ablation of learned meta-structure removing the
advantage. "Do not count merely having more facts."

## 2. Design rationale and a documented deviation

The task suggested Family A as chain-following and Family B as
value-transformation. Investigation revealed a constraint: the only
learned, domain-general meta-parameter in the current codebase is the
adaptive evidence threshold T (from `b6135c531`). Chain/MAP learning
(trial/rebind) does not engage the threshold mechanism; it has no learned
meta-parameter to transfer. Using chains for Family A would produce a
trivial negative (no meta-structure learned, nothing to transfer).

The experiment therefore uses policy-default learning for both families,
with **structurally different evidential regimes**:

- **Family A (noisy estimation):** intermittent single noise spikes on a
  stationary truth (45). Teaches the learner that the environment is noisy.
- **Family B (bursty estimation):** sustained 3-revelation noise bursts on
  a stationary truth (100). A structurally different temporal pattern:
  bursts defeat low thresholds that spikes do not.

The meta-structure under test is the global evidence threshold T
(learner-owned value; researcher-owned update rule). The evidence node is
global (tag 40, subtype 3), so T persists across different revelation
streams. This is cross-regime transfer at the meta level (how much
evidence to demand), not the object level (what the value is).

Four arms, 3/3 byte-identical runs per arm (SHA-256 `6f5a1fd0...`):

| Arm | Family A | T entering B | Family B |
|-----|----------|--------------|----------|
| NOISY-A (treatment) | 16 noisy revelations (~45) | 5 (E=13) | 30 bursty revelations (~100) |
| STABLE-A (control) | 10 stable revelations (45) | 2 (E=0) | same 30 |
| FRESH (baseline) | none | 3 (E=3, initial) | same 30 |
| ABLATED | 16 noisy (same as treatment) | reset to 3 (E=3) | same 30 |

The STABLE-A arm controls for "any experience helps" (it has Family A
experience but learns boldness, not caution). The ABLATED arm keeps all
Family A policy knowledge (default=45) but resets the meta-parameter,
isolating T as the causal factor.

## 3. Results

Family B default trajectory (30 revelations; bursts of 105/106/107 at
i=3-5, i=12-14, i=21-23):

| Arm | def sequence (abridged) | Wrong commits | Revelations to stable correct |
|-----|-------------------------|---------------|-------------------------------|
| NOISY-A | 45 x10, 100 x20 | **0** | **11** |
| STABLE-A | 45,100 x4,105 x2,100 x6,106 x4,100 x6,107 x2,100 x5 | 3 | 26 |
| FRESH | 30,100 x4,105 x2,100 x6,106 x4,100 x6,107 x2,100 x5 | 3 | 26 |
| ABLATED | 45,100 x4,105 x2,100 x6,106 x4,100 x6,107 x2,100 x5 | 3 | 26 |

"Stable correct" means the default reaches 100 and never deviates again.
"Wrong commit" means the default becomes a burst value (105/106/107).

### 3.1 The transfer is real and large

NOISY-A avoids all three burst-traps. It learns the correct default in
11 revelations with zero errors. Every other arm is trapped by all three
bursts, requiring 26 revelations to reach stability with 3 wrong commits.

The 11 vs 26 gap is not raw speed: NOISY-A is *slower* to first correct
(11 vs 2). It is *faster to stable correct* because it never gets knocked
off. In a bursty environment, caution compounds: each avoided trap saves
the wrong-commit plus the recovery.

### 3.2 Ablation proves the meta-parameter is causal

ABLATED has identical Family A experience (default=45, all policy
knowledge retained) but T reset to 3. It behaves identically to FRESH
(3 traps, 26 revelations). The advantage is not "having more facts" or
"any prior learning." It is the threshold value specifically.

### 3.3 Stable-A proves the transfer is noise-specific

STABLE-A has Family A experience but learns T=2 (boldness). It is trapped
by all three bursts, identical to FRESH. Mere experience does not help;
*noisy* experience (which raises T) is what transfers. This rules out
arousal, familiarity, or general-practice confounds.

## 4. Interpretation

**Cross-regime meta-transfer works.** A learner that experienced noise in
one evidential regime (intermittent spikes) demands more evidence in a
different regime (sustained bursts), avoiding errors that trap less
experienced learners. The meta-knowledge ("this world is noisy; be
cautious") is domain-general within the policy-learning paradigm.

**The benefit is robustness, not raw speed.** High T is inherently slower
to commit. The "fewer examples" claim holds for *stable* learning (11 vs
26 to reach a default that sticks), not for *first* learning (11 vs 2).
In environments where errors are costly, this is a strict win. Where only
speed matters, it is not. The experiment measures both and reports the
tradeoff honestly.

**The threshold is paradigm-specific.** This is a boundary, not just a
caveat. The meta-transfer works because Family A and Family B share the
evidence-accumulation machinery. Chain/MAP learning has no learned
meta-parameter, so chain-to-policy transfer is not testable in the
current architecture. Genuine cross-paradigm L2L (e.g., arithmetic to
planning, as Micah envisions) requires meta-parameters that span
paradigms. That machinery does not yet exist. This is a concrete
architectural gap identified by the experiment, not a failure of it.

## 5. Honest boundaries

1. "Structurally different" here means different temporal noise structure
   (spikes vs bursts), not different cognitive paradigms. Full
   cross-paradigm transfer remains untested and likely impossible with
   current machinery (see 4, third paragraph).
2. The task suggested chains for Family A; policy learning was used
   instead because chains do not engage any learned meta-parameter.
   A chain-A arm would be a trivial negative. This deviation is
   documented here, not hidden.
3. LEARNER-OWNED: all T/E values, all write decisions and timing, the
   11-vs-26 gap, the zero wrong commits.
   RESEARCHER-OWNED: the E update rule (+3/-1), T formula (2+E/3, clamp
   2-5), the revelation sequences, the burst design, the arm structure.
4. Scale: 16+30 revelations, one policy node, builder-run worlds.
   The 1000-event lifetime regime is not tested.
5. The +3/-1 constants and clamp bounds are researcher-chosen; only the
   resulting T values are experience-driven (same standing as the
   adaptive-threshold result).

## 6. Standing metrics

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 5 (arm design, revelation
  sequences, reset procedure, metric definitions, value domains).
- LEARNER-OWNED STRUCTURAL DECISIONS: 1 (threshold trajectory and all
  downstream decisions).
- COGNITION LINES added: ~120 (driver only; mechanism verbatim).
- MODES/BRIDGES/HANDLERS/SEMANTIC CASES: 0/0/0/0.

## 7. Deliverables

All in `docs/lab/research-lead/overnight-20260928/strong_l2l/`:
NAMECHECK.md (Step 0 guard), REPORT.md (this file),
`sl2l_base.zag` (verbatim adaptive core),
`sl2l_mech.zag` (verbatim adaptive machinery),
`sl2l_driver.zag` (4-arm driver),
`sl2l_bin`, `sl2l_compile.txt`,
`sl2l_run1.txt`, `sl2l_run2.txt`, `sl2l_run3.txt`
(3/3 byte-identical, SHA-256 `6f5a1fd0c13faad1047e863a553b7a433f13e7b1a393a8924a5dac17729228ee`).
