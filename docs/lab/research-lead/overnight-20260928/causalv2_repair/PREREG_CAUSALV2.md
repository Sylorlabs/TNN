# Preregistration: H-CAUSALV2 (Causal Vocabulary Repair)

**Date:** 2026-09-29 (PDT)
**Status:** FROZEN (before any H-CAUSALV2 implementation)
**Researcher:** H-CAUSALV2 Repair Researcher (subagent)
**Branch:** tnn-native-lab
**Target:** H-CAUSALV DOWNGRADED (red team CV_ADV_RESULT.md, 2 attacks succeed).
This hypothesis repairs both downgrade findings.

## Background and failures being repaired

H-CAUSALV SURVIVES 8/8 (bounded L2) was DOWNGRADED by independent red team:

- **X-CV-2 (delay masks law change):** SUCCEEDED. In fixture
  cv_adv_mask_obs.txt, a positioned action-1 episode made
  delay_clean accept the spurious rule (cause a=1, delay d=1 ->
  s2 SET(0), support=1) for a genuine law-change flip. Zero contests
  opened. The bogus rule then mispredicted the harm probe
  (Q (0 0 1) | 1 -> (0 0 0), WRONG; action 1 is a no-op).
  Root cause: delay attribution is purely correlational at support=1,
  and delay-before-contest priority is preemptive, so a positioned
  confounder suppresses the contest machinery.

- **X-CV-3 (threshold tie-break load-bearing):** SUCCEEDED. K-CV2's
  "inequality invention" was decided by the amendment's THR-over-EQ
  tie-break, not by data. The split fired at seq 4 of obs3i with
  2 episodes where s0-EQ also had 2 cells (2-vs-2 tie). The noamend
  ablation (EQ enumerated first) produced three equality children
  with identical probe predictions. The "data-driven selection"
  framing for K-CV2 is weakened.

Revised classification stands: bounded L2 with unacknowledged
researcher biases. Not L3 (unchanged).

## Repairs (frozen mechanism specification)

### R1: Two-tier delay rules (provisional until confirmed)

The delay rule gains a lifecycle. Status codes: ST_ACT=1 (unchanged),
new ST_PROV=5 (provisional).

1. `dl_add_or_support`: a newly created delay rule starts as
   PROVISIONAL (not ACTIVE). Provenance emits
   `# PROVISIONAL-DELAY-RULE Rn: cause a=<xa> d=<d> -> s<v> SET(<nv>) support=1 (unconfirmed)`.
2. When an existing PROVISIONAL rule (matched on cause, delay,
   variable) receives a second supporting episode (support reaches 2),
   it is promoted to ACTIVE. Provenance emits
   `# delay rule Rn CONFIRMED at seq <s> support=2 (provisional -> active)`.
   Further supports increment as before.
3. The support-matching scan matches both PROVISIONAL and ACTIVE
   rules (previously ACTIVE only; otherwise a provisional rule could
   never be confirmed and duplicates would be created).
4. Only ACTIVE rules fire on probe predictions (the probe runner's
   existing `dl_st==ST_ACT` gate is unchanged; provisional rules are
   inert by construction).
5. Contest suppression is unchanged: a variable explained by delay
   attribution (provisional or active) does not open a contest.
   This preserves the genuine-delay behavior (K-CV3: no contest for
   the lamp flips) while making unconfirmed correlations harmless.
6. `emit_dl` provenance shows rule status honestly (PROV vs ACT).

Rationale: at support=1, genuine delay (obs3d seq 7) and masking
(cv_adv_mask_obs.txt seq 4) are indistinguishable. The safe posture
is to record the correlational hint without acting on it. Genuine
delays repeat (seq 11 confirms seq 7); positioned confounders do not.
The masking fixture's spurious rule therefore stays PROVISIONAL
forever and never corrupts a prediction.

### R2: Genuine threshold world (data-driven, tie-break not load-bearing)

A new inequality world 3i2 replaces obs3i/probe3i for the K-CV2'
bar. Law (environment only): depressurize is blocked iff temp>=2
(hot only; warm works).

Frozen obs3i2.txt (seq 1-8):
```
T 0 0 0 | 0 | 1 0 0    # 1: (cold,low,off) heat -> (warm,low,off)
T 1 0 0 | 0 | 2 0 0    # 2: (warm,low,off) heat -> (hot,low,off)
T 0 1 0 | 3 | 0 0 0    # 3: (cold,high,off) depressurize -> (cold,low,off) [works]
T 1 1 0 | 3 | 1 0 0    # 4: (warm,high,off) depressurize -> (warm,low,off) [works, no contradiction]
T 2 1 0 | 3 | 2 1 0    # 5: (hot,high,off) depressurize -> (hot,high,off) [BLOCKED: temp>=2]
T 0 1 1 | 3 | 0 0 1    # 6: (cold,high,on) depressurize -> (cold,low,on) [works; lamp irrelevant]
T 2 1 1 | 3 | 2 1 1    # 7: (hot,high,on) depressurize -> (hot,high,on) [BLOCKED, confirmation]
T 1 1 0 | 3 | 1 0 0    # 8: (warm,high,off) depressurize -> (warm,low,off) [works, confirmation]
```

Design verification (frozen analysis): the depressurize entry holds
seq 3, 4 at seq 5 arrival; seq 5 contradicts (pressure UNCH vs SET).
s0 takes three distinct values {0,1,2}:
- s0-EQ: 3 cells ({0}->SET(0), {1}->SET(0), {2}->UNCH), all resolved.
- s0-THR t=0: {<=0}->SET(0) resolved; {>0}={1,2} mixes SET/UNCH,
  unresolved. Fails.
- s0-THR t=1: {<=1}={0,1}->SET(0) resolved; {>1}={2}->UNCH resolved.
  2 cells. WINS 2-vs-3 on the fewest-cells preference.
s1 (all 1) and s2 (all 0 in entry) have single values: no candidates.
s0 is the unique winning variable. Expected: `# SPLIT-THR entry N
by s0 threshold 1 into 2` with children (s0<=1)->SET(0) and
(s0>1)->UNCH.

The amendment tie-break (THR enumerated before EQ) remains in the
code, disclosed, but is NOT load-bearing here: the margin is 2-vs-3,
not a tie. A tie-break ablation (EQ enumerated first) must produce
the identical THR split; this is frozen as a control.

Frozen probe3i2.txt:
- **I1':** `Q 2 1 0 | 3` -> expect `(2,1,0)`. Hot blocked by threshold.
- **I2':** `Q 0 1 1 | 3` -> expect `(0,0,1)`. Cold works.
- **I3':** `Q 1 1 0 | 3` -> expect `(1,0,0)`. Warm works. This is the
  boundary probe: the old temp>=1 law would predict (1,1,0). The
  learner must place the boundary at temp>=2, not temp>=1.
- **I4':** `Q 2 0 0 | 0` -> expect `(2,0,0)`. Heat saturates at hot;
  unseen state (beats memorization).

The old obs3i/probe3i/world3i are retained unchanged as a regression
(the amendment tie-break still governs there, honestly documented as
a representational preference, not data-driven invention).

## Learner

causalv2.zag: byte-copy of frozen causal3.zag (md5 recorded at
implementation commit) plus ONLY the R1 changes above. No other
mechanism change. The R2 change is fixtures only (new world/obs/probe
files); the split search code is untouched.

## Kill Bars (FROZEN, all must pass for H-CAUSALV2 to survive)

- **K-CV2-1 (masking regression):** cv_adv_mask_obs.txt (the exact
  X-CV-2 fixture, byte-identical) run through causalv2: NO ACTIVE
  delay rule is created for the seq-4 law-change flip (a PROVISIONAL
  rule may be recorded but must never become ACTIVE and must never
  fire). The harm probe (`H 0 0 0 | 1` then `Q 0 0 1 | 1`) must NOT
  predict `(0,0,0)`. (Truth: (0,0,1); action 1 is a no-op. WITHHOLD
  or (0,0,1) both pass; (0,0,0) fails.)
- **K-CV2-2 (genuine threshold):** obs3i2/probe3i2 through causalv2:
  I1' `(2,1,0)`, I2' `(0,0,1)`, I3' `(1,0,0)`, I4' `(2,0,0)` all
  correct AND provenance shows ACTIVE entries for action 3 with
  THRESHOLD conditions (s0<=1 with pressure SET(0); s0>1 with
  pressure UNCH), not three equality children, AND the trace shows
  the split selected with EQ at 3 cells vs THR at 2 cells (design
  verification above), AND the tie-break ablation (EQ enumerated
  before THR) produces the identical THR split.
- **K-CV2-3 (no regression on H-CAUSALV bars):** K-CV1, K-CV3, K-CV4,
  K-CV5, K-CV6, K-CV7, K-CV8 (as frozen in PREREG_CAUSALV.md,
  commit 82e877e47) all still PASS on the original fixtures through
  causalv2. Specifically: K-CV3's DELAY rule (cause 4, delay 2,
  target lamp, SET(1)) must be ACTIVE with support >= 2 and no
  contest opened for obs3d seq 7/11; K-CV1's conjunction must still
  split; K-CV7's grep must still return zero hits on causalv2.zag.
  Any bar that cannot pass must be explicitly SUPERSEDED with
  justification, not silently dropped.
- **K-CV2-4 (determinism):** Two full runs per world/fixture
  (obs+probe) are byte-identical (SHA-256 of stdout).

**Verdict rule:** H-CAUSALV2 SURVIVES iff K-CV2-1..K-CV2-4 all pass.
Any single failure kills H-CAUSALV2 as stated (may survive weakened,
documented explicitly).

## Scope and Non-Claims

- This experiment does NOT claim L3. It repairs two specific
  downgrade findings in a bounded-L2 mechanism.
- Provisional rules are never retracted in this design; an
  unconfirmed provisional rule is inert provenance, not a belief.
  Retraction on refutation is future work (documented boundary).
- A provisional rule that later confirms is promoted; a provisional
  rule for (xa1,d1) does not block a later active rule for
  (xa2,d2) on the same variable.
- The old inequality world (temp>=1) is superseded for the
  invention claim but retained as a regression fixture.
- Phase-2, ambiguity, contest, and baseline machinery are unchanged.

## Governance

- This prereg is committed ALONE before any causalv2.zag code or
  fixture. Commit order self-check: the prereg commit strictly
  precedes the first causalv2 implementation commit.
- Fixtures (world3i2.zag, obs3i2.txt, probe3i2.txt) are environment
  or frozen logs, committed after the prereg and before results.
- Implementation, results, and verdict in separate commits.
- Results must include raw stdout, SHA-256 determinism checks, the
  K-CV7 grep output on causalv2.zag, and the K-CV2-3 regression
  outputs.
- Pure Zag. No Python anywhere in this experiment.
- No em dashes in loop documentation.
- Only H-CAUSALV2-owned files are staged/committed. Concurrent
  agents' files are untouched.
