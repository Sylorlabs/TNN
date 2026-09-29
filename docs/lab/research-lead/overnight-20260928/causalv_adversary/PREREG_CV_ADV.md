# Preregistration: H-CAUSALV Red Team (X-CV-ADV)

**Date:** 2026-09-29 (PDT)
**Status:** FROZEN (before any attack execution)
**Researcher:** H-CAUSALV Red Team (independent subagent)
**Branch:** tnn-native-lab
**Target:** H-CAUSALV SURVIVES (bounded L2), 8/8 kill bars (RESULTS_CAUSALV.md, commit c98846c7e)

## Mission

Assume the H-CAUSALV claim is false. Attack it. Any successful attack
kills or downgrades H-CAUSALV. Report honestly, including failed attacks.

## Attack X-CV-1: Pair-uniqueness audit (conjunction)

**Question:** At the actual split point in obs3c, was (s0,s2) truly the
unique Phase-2 resolver, or did the implementation bypass the prereg's
"If two or more [pairs resolve], AMBIGUOUS" rule?

**Background:** The prereg's design verification claims "pairs involving
s1 are skipped (s1 has a single distinct value)". The authoritative trace
shows "# SPLIT-CONJ entry 2 by (s0,s2) pair into 5" with no AMBIGUOUS
line. The split fired at seq 9 (5 episodes in entry 2).

**Method (static + trace):** Independently recompute, by hand from the
frozen obs3c.txt, the Phase-1 and Phase-2 candidate tables for entry 2
(action 2) at seq 9 using the frozen fx_codes_f semantics (UNCH if all
nv==sv; else SET(sc) if all nv equal; else ADD(dd) if a single nonzero
delta fits all; else unresolved). Confirm: (a) Phase 1 yields zero
candidates; (b) exactly one pair resolves; (c) it is (s0,s2).

**Kill criterion:** If the recomputation shows two or more pairs resolve
at seq 9 (i.e., the prereg's AMBIGUOUS rule was violated), or Phase 1
had a winner (i.e., Phase 2 should never have run), then the conjunction
split contradicts the frozen search specification -> DOWNGRADE
(mechanism deviates from prereg; K-CV1's provenance is not as claimed).

**Expected:** FAIL (no violation; preliminary hand computation shows
(s0,s2) unique: (s1,s2) fails on cell (s1=0,s2=1) mixing seq 8
delta +1 with seq 9 delta 0; (s0,s1) fails on cell (s0=2,s1=0) mixing
seq 7 delta +1 with seq 9 delta 0). This attack is a control.

## Attack X-CV-2: Delay attribution masks a law change

**Question:** The prereg freezes "delayed-cause attribution as an
alternative to contest opening" with delay tried BEFORE contest on every
exact-state contradiction. Can a spurious correlational delay match
suppress the contest machinery on a genuine law change?

**Method (dynamic):** Two fixtures, identical law change, different
action histories. The mechanism (byte-copy of causal3.zag, only fixtures
differ) is run on both.

Fixture A (masking), file cv_adv_mask_obs.txt:
```
T 0 0 0 | 0 | 0 0 1
T 0 0 0 | 0 | 0 0 1
T 0 0 0 | 1 | 0 0 0
T 0 0 0 | 0 | 0 0 0
T 0 0 0 | 0 | 0 0 0
```
True dynamics: action 0 sets s2:=1 (seq 1-2), then a LAW CHANGE: action 0
sets s2:=0 (seq 4-5). Action 1 is always a no-op. The action-1 episode at
seq 3 is positioned so that (cause a=1, delay d=1) is "clean" per
delay_clean for the seq-4 flip: positives (seq 4 only, seq>1) have
action 1 at t-1; negatives with history (seq 2: action at t-1 is action 0
at seq 1) do not.

Fixture B (control), file cv_adv_ctrl_obs.txt:
```
T 0 0 0 | 0 | 0 0 1
T 0 0 0 | 1 | 0 0 0
T 0 0 0 | 0 | 0 0 1
T 0 0 0 | 1 | 0 0 0
T 0 0 0 | 0 | 0 0 0
```
Same law change at seq 5, but interleaved action-1 episodes refute every
(cause, delay) correlation (each candidate is vetoed by a negative with
the cause action at t-d).

**Kill criterion:** If Fixture A produces a DELAY-RULE for the seq-4 flip
with ZERO contests opened for it, while Fixture B opens a contest (or at
minimum creates no delay rule) for its law-change flip, then the
delay-before-contest priority is demonstrated unsafe: a spurious
correlation masks a law change and suppresses the competing-hypothesis
machinery -> DOWNGRADE (the delay/contest priority claim is narrowed;
K-CV3's "no contest" bar is shown to be achievable by masking, not only
by genuine delay).

**Expected:** SUCCEED (preliminary trace-through predicts a spurious
(a=1,d=1 -> s2 SET(0)) rule in Fixture A and no rule + contest in B).

## Attack X-CV-3: Threshold tie-break load-bearing (ablation)

**Question:** K-CV2 requires THRESHOLD conditions "not three equality
children". The prereg's design verification describes THR winning by
fewest cells (2 vs 3), but the split actually fired at seq 4 of obs3i
with 2 episodes, where s0-EQ also has 2 cells: a tie broken only by the
amendment's "THR over EQ" rule. Is the inequality representation
data-driven, or researcher-selected via the tie-break?

**Method (dynamic ablation):** Build cv_adv_noamend.zag, a copy of
causal3.zag differing ONLY in split_search Phase 1 enumeration order
(EQ candidates added before THR candidates, so ties prefer EQ; the
strict-less-than per-variable best then selects EQ on ties). Run the
frozen obs3i.txt + probe3i.txt through it. Compare the provenance
(THRESHOLD vs EQUALITY children) and the probe predictions.

**Kill criterion:** If the no-amendment variant produces equality
children for action 3 (instead of the threshold pair) while the probe
predictions remain correct, then K-CV2's representational requirement is
satisfied only because of the researcher-supplied tie-break, and the
prereg's design verification (2-vs-3-cell win) describes a scenario that
never occurred -> DOWNGRADE (the "inequality invention" claim is
narrowed to "researcher tie-break selects the threshold representation";
the result's classification as data-driven selection is weakened for
K-CV2).

**Expected:** SUCCEED.

## Attack X-CV-4: Source and lineage audit (static)

**Method:**
(a) Re-run the K-CV7 forbidden-word grep on causal3.zag at the frozen
commit; must return zero hits.
(b) Search causal3.zag for probe-answer literals or task-specific
constants (e.g., hardcoded probe predictions, the values 2,0,1 as an
answer tuple outside generic machinery).
(c) Verify commit ordering via git: prereg (82e877e47) strictly before
apparatus (cef56f56a) strictly before amendment (32de40e0b) strictly
before learner (140199be1) strictly before results (c98846c7e).
(d) Verify the K-CV8 probe files contain the queries actually run and
that all predictions match the original learner (spot-check the
byte-identity claim on probe_B2/probe_C2 if the original binary is
available; otherwise verify the claim's evidence files exist).
(e) Check that the amendment did not alter any frozen observation,
probe, or baseline file (git diff of those files between 82e877e47 and
32de40e0b must be empty).

**Kill criterion:** Any hardcoding, any ordering violation, or any
frozen-file alteration -> KILL (if the bars were not honestly earned)
or DOWNGRADE (if documentation-only). Expected: PASS.

## Verdict rule

- Any kill criterion met -> corresponding verdict (KILL or DOWNGRADE).
- X-CV-1 is a control; its failure strengthens the result.
- Pure Zag. No Python anywhere. No em dashes.
- Prereg committed ALONE before any attack code or execution.
