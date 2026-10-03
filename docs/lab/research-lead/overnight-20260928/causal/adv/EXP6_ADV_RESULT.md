# H-EXP6 Red Team Result: H-EXP6 DOWNGRADED

**Date:** 2026-09-29
**Adversary prereg:** causal/adv/PREREG_EXP6_ADV.md (commit
efe82d454, frozen before any attack fixture, code, or
execution; strict ancestor of this result commit)
**Target:** causal/adv/exp_invent6.zag (committed source)
**Attack fixtures:** causal/adv/g1_e6_adv.txt (X-E6-1),
causal/adv/h1_e6_adv.txt (X-E6-2)
**Raw evidence:** causal/adv/evidence/exp6_adv_g1_raw.txt
(md5 441043679519989eb73d980fcec459c2),
causal/adv/evidence/exp6_adv_h1_raw.txt
(md5 461c7b13cc2944f8e7e682709a6b30a2)
**Toolchain:** znc 2026.07.0-dev (edition 2026)
**Purity:** Pure Zag. No Python anywhere (no generators,
verifiers, analysis, or scratch). Binaries built in /tmp
only, not committed.

## Verdict: H-EXP6 DOWNGRADED (claim-narrowing)

Two of four attacks succeeded. The frozen 4/4 bars
(K-E6-1 through K-E6-4) are NOT re-litigated: X-E5-1 and
X-E5-2 as literally stated remain closed. What is narrowed
is the broader claim that the CHANGE-EVIDENCE line is a
sufficient value-level hazard signal for setup planning.
The signal is from-blind (X-E6-1) and base-rate-blind
(X-E6-2). Classification remains bounded L2; nothing here
is L3-relevant.

## X-E6-1: SUCCEEDS (from-blindness)

**Prediction (prereg):** compute_change_to discards the
from-value os; the pick-level signal must lump change
evidence from different starting values with no
from-value distinction.

**Execution:** Fixture G1 = S1 plus 5 adversary episodes:
two more action-0 1->2 changes, two action-1 0->2 changes,
one action-0 from-0 no-change. Ran the rebuilt binary
(byte-identical to committed evidence on all 5 frozen
fixtures, see X-E6-3).

**Observed output** (evidence/exp6_adv_g1_raw.txt:38,
ranked pick requiring temp==2):

    CHANGE-EVIDENCE: temp==2 changed-to by action(s) {0,1} (5 eps); ...

CHANGE-TO TABLE confirms: CHGTO a0 temp[2:3], CHGTO a1
temp[2:2].

**Per-episode audit** (grep over g1_e6_adv.txt, no Python):

- Action 0 temp->2 changes (3, matching chgto): ALL are
  `T 1 0 0 | 0 | 2 0 0` (from temp==1). Zero from temp==0.
- Action 0 from temp==0 (2 episodes): `T 0 0 0 | 0 | 1 0 0`
  (yields 1) and `T 0 0 0 | 0 | 0 0 0` (yields 0). Action 0
  NEVER yields temp==2 from temp==0 in this fixture.
- Action 1 temp->2 changes (2): both `T 0 0 0 | 1 | 2 0 0`
  (from temp==0).

**Kill criterion check:** MET. The line lists {0,1} with no
from-value signal, although only action 1 ever effected the
0->2 transition and the fixture directly shows action 0
does not yield 2 from 0. A setup planner at temp==0 reading
"changed-to by {0,1}" cannot tell which action serves its
need. This is the X-E5-2 lumping complaint recurring along
a new axis: the repair added granularity over
change-vs-carryover but the signal remains coarse over the
from-value, which is material to the signal's stated
purpose. The base case already exists in committed S1
evidence (pick [2]: {0} (1 eps), the single change from
temp==1); G1 strengthens it to 3 from-1 episodes against a
competing from-0 action.

**Not covered by honest limits:** the prereg limits say
changed-to is "observed change, not proven capability" and
"the counts do not capture why the change occurred." The
from-value is not a why; it is a knowable-from-data
condition the mechanism possesses (ep_s) and discards in
aggregation. The legend does not warn that listed actions
may never have made the needed transition.

## X-E6-2: SUCCEEDS (hidden per-action base rate)

**Prediction (prereg):** emit_change_evidence prints the
change count m but no action-level outcome denominator; a
1-in-10 change renders identically to a 1-in-1 change at
the pick level.

**Execution:** Fixture H1 = S1 plus 10 adversary episodes:
nine action-0 temp==2 carryovers and one action-1 0->2
change with no carryover.

**Observed output** (evidence/exp6_adv_h1_raw.txt:34,
ranked pick requiring temp==2):

    CHANGE-EVIDENCE: temp==2 changed-to by action(s) {0,1} (2 eps); ...

TABLE confirms: CHGTO a0 temp[2:1], CHGTO a1 temp[2:1];
ACHV a0 temp[2:11], ACHV a1 temp[2:1].

**Per-episode audit** (grep over h1_e6_adv.txt):

- Action 0: 11 temp==2 outcomes = 1 change
  (`T 1 0 0 | 0 | 2 0 0`) + 10 carryovers
  (`T 2 0 0 | 0 | 2 0 0`). Change rate 1-in-11.
- Action 1: 1 temp==2 outcome = 1 change
  (`T 0 1 0 | 1 | 2 1 0`), 0 carryovers. Change rate 1-in-1.

**Kill criterion check:** MET. The pick-level line shows
{0,1} (2 eps) with no per-action denominator, presenting
action 0's 1-in-11 change identically to action 1's 1-in-1
change. The denominators exist in the ACHV TABLE but are
not surfaced in the pick annotation, which is the
value-level hazard signal itself. The base case already
exists in committed S1 evidence (pick [2]: {0} (1 eps)
while action 0 had 2 temp==2 outcomes: 1 change +
1 carryover). A consumer reading only the pick line cannot
assess whether the change evidence is representative or a
lone episode. Note chgto does not feed ranking, so the
mechanism does not itself overweight the lone episode;
the gap is in the signal presented to consumers.

## X-E6-3: FAILS (regression holds)

- Rebuilt exp_invent6.zag from committed source with
  znc 2026.07.0-dev (warnings only, no errors).
- All 5 frozen fixtures, 3 runs each: byte-identical
  (cmp clean). md5s match committed evidence exactly:
  S1 3c8ad4a2a507cbe5f818d7ad2a47a901,
  S2 521fb312f4092f913c0562d1b2b10dad,
  S0 4ae8ecfabf44d5b7fb7a8ba21628a69e,
  A1 71c971adf7faf0769f54a9725d2632aa,
  F1 d11ad7f3f47dfeb26f14f0ba74ecbe7c.
- K-E6-1 strings present in fresh F1 output (3 occurrences
  each of the two frozen substrings); K-E6-2 strings
  present in fresh S1 output.
- Built exp_invent5.zag from committed source; diff of
  exp6 vs exp5 outputs on all 5 fixtures with added lines
  excluded: clean (strictly additive, no changed or
  removed pre-existing lines).
- First build attempt exited 2 with truncated output; retry
  succeeded. No source change between attempts; treated as
  transient toolchain behavior, disclosed here.

## X-E6-4: FAILS (source audit clean)

- (a) chgto_idx formula `((a*3)+v)*3+x` identical to
  achv_idx. Buffer 144 bytes = 36 cells * 4; max index 35.
- (b) compute_change_to has the same EP_ACT filter and
  a-in-0..3 guard as compute_achievability.
- (c) Change predicate `ns != os` on raw values matches
  compute_controllable exactly.
- (d) Both emit_achievability call sites (lines 1577,
  1600) are immediately followed by emit_change_evidence
  (lines 1580, 1602). No other achievability call sites.
- (e) No fixture-specific literals in the four added
  functions; no test-answer hardcoding.
- (f) diff exp_invent5.zag vs exp_invent6.zag: 136 added
  lines, 0 removed, in 7 hunks mapping exactly to the 4
  preregistered additions (compute_change_to + helpers,
  emit_chg_table + row, emit_change_evidence, main wiring,
  legend extension, 2 call sites).

## Causal interpretation

The two successful attacks share one root cause: the
(a,v,x) aggregation is a lossy projection of the episode
data, and the CHANGE-EVIDENCE line projects further. The
first projection drops the from-value; the second drops
the per-action outcome denominator. Both dropped dimensions
are material to the signal's consumer (a setup planner
assessing which action can bring about a required value
from the current state, and how representative the change
evidence is). The honest-limits text covers stochasticity
("not proven capability") and coincidence ("not causal
attribution") but not these two systematic information
losses. The natural repair, if pursued, is a further
narrowing of the claim plus optionally a transition-level
(from,to) table; whether that repair is worth the
complexity is the parent's call.

## What this does NOT show

- The frozen bars K-E6-1..K-E6-4 are intact; the builder's
  4/4 result reproduces exactly.
- X-E5-1 and X-E5-2 as literally frozen remain closed:
  carryover-only is machine-readable and change vs
  carryover actions are distinguished.
- No integrity failure: evidence reproduces from source,
  outputs are deterministic, the diff is additive-only,
  the audit is clean.
- Not L3-relevant in either direction.

## Commit lineage (branch tnn-native-lab, local only)

- efe82d454: PREREG_EXP6_ADV FROZEN (alone; before any
  attack execution)
- this commit: EXP6_ADV_RESULT.md (this file),
  g1_e6_adv.txt, h1_e6_adv.txt,
  evidence/exp6_adv_g1_raw.txt,
  evidence/exp6_adv_h1_raw.txt (only owned files staged)

## Suggested follow-up for parent

H-EXP6 is now DOWNGRADED (narrowed), not killed. If a
repair is authorized (H-EXP7), the preregistered attack
fixtures G1 and H1 are the natural regression tests, plus
a from-value audit of any new transition-level signal.
