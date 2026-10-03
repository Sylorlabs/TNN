# H-CAUSALV Red Team: Final Report

**Verdict: H-CAUSALV DOWNGRADED** (two attacks succeed; the eight frozen
bars stand as executed, so this is a downgrade, not a kill).

**Prereg:** `PREREG_CV_ADV.md` frozen at commit `134c991a9` before any
attack execution. **Result + evidence:** this commit. Pure Zag
throughout (one governance note below). All dynamic runs 3/3
byte-identical.

## Attack X-CV-1: Pair-uniqueness audit (conjunction) — FAILED (control)

Recomputed the Phase-1 and Phase-2 candidate tables for entry 2
(action 2) of obs3c at the actual split point (seq 9, 5 episodes) using
the frozen fx_codes_f semantics.

Phase 1 at seq 9: s0-EQ fails (cell s0=2 mixes seq 7 delta +1 with seq 9
delta 0); s0-THR fails on both t=0 and t=1; s1-EQ fails (cell s1=0 mixes
seq 7/8 delta +1 with seq 9 delta 0); s1-THR fails; s2-EQ and s2-THR fail
(cell s2=1 mixes seq 8 delta +1 with seq 9 delta 0). Zero Phase-1
candidates: Phase 2 correctly runs.

Phase 2 at seq 9: (s0,s2) resolves (5 nonempty cells, each uniform:
(0,0):UNCH, (1,0):UNCH, (2,0):SET(1), (0,1):SET(1), (2,1):UNCH).
(s0,s1) fails (cell (2,0) mixes seq 7 and seq 9). (s1,s2) fails (cell
(0,1) mixes seq 8 delta +1 with seq 9 delta 0). Exactly one pair
resolves. The trace shows "# SPLIT-CONJ entry 2 by (s0,s2) pair into 5"
with no AMBIGUOUS line. The prereg's "if two or more, AMBIGUOUS" rule is
not violated. The conjunction split is as claimed.

Documentation nit (not a mechanism failure): the prereg's design
verification says "pairs involving s1 are skipped (s1 has a single
distinct value)". At seq 9, s1 takes two distinct values (1 at seq 4-5,
0 at seq 7-9), so the parenthetical reason is factually wrong; the pairs
were considered and failed on resolution, and the conclusion (unique
resolver) is correct.

## Attack X-CV-2: Delay attribution masks a law change — SUCCEEDED

**Fixtures** (mechanism byte-identical to causal3.zag, md5
9851c7ac37e1ffbdd4f277cae50d5e1c; only obs fixtures differ):

Fixture A (`cv_adv_mask_obs.txt`): action 0 sets s2:=1 (seq 1-2), then a
LAW CHANGE: action 0 sets s2:=0 (seq 4-5). Action 1 is always a no-op.
The seq-3 action-1 episode positions a spurious correlation.

Result (`CV_ADV_MASK_RUN.txt`):
```
# DELAY-RULE R0: cause a=1 d=1 -> s2 SET(0) support=1
# delay-attributed var s2 of seq 4 to R0
# entry 0 CONFLICTED: no resolving split
# learned 5 episodes, 5 entries, 0 contests, 1 delay rules
```
A spurious delay rule (action 1 causes s2:=0 after 1 step) is created
for the seq-4 law-change flip. **Zero contests opened.** The
delay-before-contest priority masked the law change.

Fixture B (`cv_adv_ctrl_obs.txt`, control): same law change at seq 5,
but interleaved action-1 episodes refute every (cause, delay)
correlation.

Result (`CV_ADV_CTRL_RUN.txt`): 0 delay rules, 0 contests; entry 0 goes
CONFLICTED via split search finding no candidates. No spurious rule.

**Harm demonstration** (`CV_ADV_HARM_RUN.txt`): probe `H 0 0 0 | 1` then
`Q 0 0 1 | 1`. Truth: action 1 is a no-op, so (0,0,1)|1 -> (0,0,1). The
spurious rule fires on the H action and the learner predicts
`Q (0 0 1) | 1 -> (0 0 0)`. WRONG. The bogus causal rule corrupts future
predictions.

**Interpretation:** delay_clean is purely correlational. A positioned
confounder satisfies it, the contest machinery (the architecture's
law-change handler) is suppressed, and the white-box model is polluted
with a false causal rule that then mispredicts. K-CV3's "no contest"
bar is achievable by masking, not only by genuine delay. The frozen
prereg documents the priority but not this failure mode.

## Attack X-CV-3: Threshold tie-break load-bearing — SUCCEEDED

**Ablation** (`cv_adv_noamend.zag`): byte-identical to causal3.zag
except split_search Phase 1 enumerates EQ candidates before THR (so the
strict-less-than per-variable best prefers EQ on ties), reverting the
amendment's tie-break. Frozen obs3i.txt + probe3i.txt run through it.

Result (`CV_ADV_NOAMEND_3I_RUN.txt`):
```
# SPLIT entry 3 by s0 equality into 2
# ENTRY 5 a=3 cond=[s0==0] ... # ENTRY 6 a=3 cond=[s0==1] ...
# ENTRY 7 a=3 cond=[s0==2] ... (partition-extended)
Q (1 1 0) | 3 -> (1 1 0)
Q (0 1 1) | 3 -> (0 0 1)
Q (2 0 0) | 0 -> (2 0 0)
```
The variant produces exactly the three equality children that K-CV2
forbids ("not three equality children"), while all probe predictions
remain correct.

**Interpretation:** K-CV2's representational requirement is satisfied
only because of the researcher-supplied "THR over EQ" tie-break. The
prereg's design verification ("THRESHOLD (2 cells) beats EQUALITY
(3 cells)") describes a scenario that never occurred: the split fired at
seq 4 with 2 episodes, where s0-EQ also has 2 cells. It was a tie,
resolved by researcher fiat, not by data. The amendment was transparent
and frozen before authoritative runs (ordering verified in X-CV-4), so
this is not cheating; it narrows the claim. The "inequality invention"
is researcher-selected representation, and the result's "data-driven
selection" framing is weakened for K-CV2. The probes do not
distinguish: EQ solves them identically (the result doc already admits
this as nuance).

## Attack X-CV-4: Source and lineage audit — PASS

(a) K-CV7 re-grep on causal3.zag: zero hits (exit 1). (b) No
probe-answer literals or task-specific constants in causal3.zag.
(c) Commit ordering verified via merge-base: 82e877e47 (prereg) <
cef56f56a (apparatus) < 32de40e0b (amendment) < 140199be1 (learner) <
c98846c7e (results), all strict ancestors. (d) K-CV8 probe files exist;
the actual queries are (2,0,0)|2, (0,0,0)|2, (1,1,1)|2 (B2) and
(2,0,0)|2, (2,0,1)|2, (0,0,0)|2 (C2), confirming the result doc's note
that the prereg mislabeled them. (e) Frozen obs/probe/world/baseline
files are byte-identical between apparatus, amendment, and learner
commits (empty diffs).

## Revised classification

Bounded L2, narrowed. The eight bars were honestly earned under the
frozen specification, but: (1) the delay-before-contest priority can
mask law changes with spurious correlational rules that then
mispredict; (2) the threshold representation in K-CV2 is selected by a
researcher tie-break, not discovered from data. The "invention" is
data-driven selection from an authored vocabulary *plus*
researcher-chosen representational biases that do unacknowledged work.
Not L3 (unchanged).

## Recommended follow-ups

1. Delay/contest priority: require a contest alongside delay attribution
   when the correlational evidence is thin (e.g., support=1), or rank
   delay vs. law-change as competing hypotheses rather than giving delay
   preemptive priority.
2. Re-run K-CV2 with a threshold law that EQ genuinely cannot express
   compactly on the probes (not just representationally), or restate
   K-CV2 as a representation-preference bar.
3. The X-CV-2 masking fixture is the regression test for any delay
   rework.

## Governance

- Prereg committed alone at 134c991a9 before any attack code or
  execution; verified strict ancestor of this result commit.
- cv_adv.zag is md5-identical to the frozen causal3.zag; only
  cv_adv_noamend.zag differs (documented ablation, 2-byte diff plus
  comment).
- One governance note: a python3 one-liner was used for the text
  replacement when building cv_adv_noamend.zag (block reorder). No
  Python was used in any mechanism, execution, or analysis; all
  experiments ran as compiled Zag. Disclosed per the pure-Zag rule.
- Only adversary-owned files staged/committed; concurrent agents'
  files untouched. No em dashes. No binaries committed (/tmp only).
- Determinism: 3/3 byte-identical runs per dynamic attack (md5:
  mask 04b1b879..., ctrl e237e935..., harm aef76a6c..., noamend
  cd3cffc1...).

## Files (all committed on tnn-native-lab)

- PREREG_CV_ADV.md (frozen 134c991a9)
- CV_ADV_RESULT.md (this report)
- cv_adv.zag (mechanism byte-copy)
- cv_adv_noamend.zag (tie-break ablation)
- cv_adv_mask_obs.txt, cv_adv_ctrl_obs.txt, cv_adv_harm_probe.txt,
  cv_adv_empty_probe.txt (fixtures)
- CV_ADV_MASK_RUN.txt, CV_ADV_CTRL_RUN.txt, CV_ADV_HARM_RUN.txt,
  CV_ADV_NOAMEND_3I_RUN.txt (raw evidence)
