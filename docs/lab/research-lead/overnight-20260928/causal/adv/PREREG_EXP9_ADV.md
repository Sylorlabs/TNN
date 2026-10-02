# PREREG_EXP9_ADV: H-EXP9 Independent Red Team (Adversary Preregistration)

**Date:** 2026-09-29
**Target:** H-EXP9 SURVIVES 5/5 (bounded L2), EXP9_RESULT.md, committed
  causal/adv/exp_invent9.zag
**Stance:** Assume the H-EXP9 repair claim is false. Attack it.
**Method:** Freeze this prereg alone BEFORE building any binary, creating any
  attack fixture, or running any attack. Then build from git-extracted source
  in /tmp only, create frozen attack fixtures via shell heredocs, run, and
  check the frozen kill criteria below.
**Purity:** Pure Zag throughout. No Python at any stage. Fixtures via shell
  heredocs and cat. Analysis via grep, sed, diff, cmp, md5sum, wc. No em dashes
  in loop documentation.

## Base fixture (pinned)

All attack fixtures are built as: committed
`causal/adv/d2_e8_adv.txt` (md5 `141baf5dc1117aacd7ed1125e0459ee9`, 21 T lines,
last touched by H-EXP8 red-team commit `af2d3affe`) PLUS the appended lines
listed verbatim per attack. The base is byte-identical (verified by md5 before
use). D2 is chosen because it is proven to emit RANKED EXPERIMENTS with
TRANSITION-EVIDENCE lines and one RESOLVE (action 0 state (2 0 0), 1 EP_SUP).

D2 already contains exactly 1 EP_SUP episode: `T 2 0 0 | 0 | 2 0 0`
(from (2,0,0)), superseded at the seq-14 RESOLVE. All hand derivations below
include it.

## Contest mechanics (from source, pre-execution analysis)

- `contest_feed` resolves when `(s0>=2 && s0>s1) || (s1>=2 && s1>s0)`, where
  s0/s1 count only episodes fed AFTER the contest opened (initialized 1,1).
- On RESOLVE, every non-SUP episode in the entry at the contest state whose
  outcome matches the loser outcome is set EP_SUP. EP_SUP is terminal (no
  reinstatement in source). Only two episode states exist (EP_ACT=0, EP_SUP=1).
- A contest opens only in an ACTIVE entry (`entry_ingest` returns early via
  `amb_update` for ST_AMBIG entries). D2's action-2 entry is AMBIGUOUS, so no
  new contests are attempted on action 2. All new contests use actions 0, 1, 3.
- Appended episodes arrive after D2's 21 lines, so D2's RESOLVE is unaffected.

## X-E9-1 (Boundary): supersession at entry boundaries, multi-episode loser sets

**Fixture E1** = D2 + these 23 appended lines (order frozen):

```
# X-E9-1a: action 0 at (0,0,0): 3 more loser-A + 5 winner-B; 4-episode loser set
T 0 0 0 | 0 | 1 0 0
T 0 0 0 | 0 | 1 0 0
T 0 0 0 | 0 | 1 0 0
T 0 0 0 | 0 | 2 0 0
T 0 0 0 | 0 | 2 0 0
T 0 0 0 | 0 | 2 0 0
T 0 0 0 | 0 | 2 0 0
T 0 0 0 | 0 | 2 0 0
# X-E9-1b: action 1 at (1,0,0): 3 more loser-A + 5 winner-B; 4-episode loser set
T 1 0 0 | 1 | 0 0 0
T 1 0 0 | 1 | 0 0 0
T 1 0 0 | 1 | 0 0 0
T 1 0 0 | 1 | 2 0 0
T 1 0 0 | 1 | 2 0 0
T 1 0 0 | 1 | 2 0 0
T 1 0 0 | 1 | 2 0 0
T 1 0 0 | 1 | 2 0 0
# X-E9-1c: action 3 at (2,2,2): 1 loser-A + 4 winner-B; single-episode loser set
T 2 2 2 | 3 | 2 2 2
T 2 2 2 | 3 | 2 2 1
T 2 2 2 | 3 | 2 2 1
T 2 2 2 | 3 | 2 2 1
T 2 2 2 | 3 | 2 2 1
# X-E9-1d: action 3 at (1,1,1): 1 A + 1 B; 1v1 tie, contest opens, NO resolve
T 1 1 1 | 3 | 1 1 1
T 1 1 1 | 3 | 1 1 2
```

**Hand-derived expectations (from source mechanics, before execution):**

- X-E9-1a: D2 already has 1x `T 0 0 0 | 0 | 1 0 0` (outcome A=(1,0,0)). After
  3 more A (total A=4) and 1st B=(2,0,0), contest opens (1,1). 2nd B feeds
  s1=2>1, s1>=2: RESOLVE, winner (2,0,0), loser (1,0,0). All 4 A-episodes
  (from (0,0,0)) become EP_SUP. Remaining 3 B added as EP_ACT.
- X-E9-1b: D2 already has 1x `T 1 0 0 | 1 | 0 0 0` (outcome A=(0,0,0)). After
  3 more A (total A=4) and 1st B=(2,0,0), contest opens (1,1). 2nd B: s1=2>1:
  RESOLVE, winner (2,0,0), loser (0,0,0). All 4 A-episodes (from (1,0,0))
  become EP_SUP.
- X-E9-1c: 1x A=(2,2,2), then 1st B=(2,2,1) opens contest (1,1). 2nd B:
  s1=2>1: RESOLVE. The single A-episode (from (2,2,2)) becomes EP_SUP.
  This is the single-episode loser boundary: the repair must count it.
- X-E9-1d: 1x A=(1,1,1), 1x B=(1,1,2): contest opens (1,1), no further
  episodes, NO resolve, zero EP_SUP. The repair must show no sup-att for
  these (absence means zero).

Total EP_SUP in E1: 1 (D2, action 0 from (2,0,0)) + 4 (action 0 from (0,0,0))
+ 4 (action 1 from (1,0,0)) + 1 (action 3 from (2,2,2)) = 10.

**Expected sup-att values (per (action,variable), aggregated over all
contests, clamped from-values):**

- (0,temp): {0:4,1:0,2:1}; (0,pressure): {0:5,1:0,2:0}; (0,lamp): {0:5,1:0,2:0}
- (1,temp): {0:0,1:4,2:0}; (1,pressure): {0:4,1:0,2:0}; (1,lamp): {0:4,1:0,2:0}
- (3,temp): {0:0,1:0,2:1}; (3,pressure): {0:0,1:0,2:1}; (3,lamp): {0:0,1:0,2:1}
- (2,*): zero superseded episodes; no sup-att segment may appear for action 2.

**Expected from-att (for invariant checks):**

- (0,temp): EP_ACT action-0 temp from-states: 5x B (from 0), 1x `T 1 0 0|0|2 0 0`
  (from 1), 1x `T 5 0 0|0|2 0 0` + 9x `T 2 0 0|0|3 0 0` (from 2) =
  {0:5,1:1,2:10}. Invariant: {0:5+4,1:1,2:10+1} = {0:9,1:1,2:11} equals the
  fixture-text count of action-0 episodes by clamped temp from-state.
- (1,temp): EP_ACT: 1x `T 0 0 0|1|0 0 0` (from 0), 5x B (from 1),
  1x `T 2 0 0|1|1 0 0` (from 2) = {0:1,1:5,2:1}; sup-att {0:0,1:4,2:0};
  invariant {0:1,1:9,2:1} matches fixture text.

**Kill criteria X-E9-1:**

- K-E9A-1 (gate): the output must contain RESOLVE lines for action 0 state
  (0 0 0), action 1 state (1 0 0), and action 3 state (2 2 2), plus a CONTEST
  line for action 3 state (1 1 1) with NO following RESOLVE. If any expected
  RESOLVE is absent, that sub-case is INCONCLUSIVE (entry dynamics did not
  cooperate) and is reported as such; it is neither a pass nor a kill.
- K-E9A-2: wherever (0,temp), (1,temp), (3,pressure), or (3,lamp) is shown
  with from-att, the sup-att segment must equal the hand-derived values
  above exactly. Any deviation in any shown cell: the accounting claim is
  falsified.
- K-E9A-3 (completeness invariant): for EVERY (a,v) shown with from-att,
  from-att + sup-att (absent segment = 0) must equal the fixture-text count
  of action-a episodes with clamped from-state oa for variable v (counted
  independently via grep). Any mismatch: the "complete observed attempt
  denominator" claim is falsified.
- K-E9A-4: the single-episode loser (X-E9-1c) must appear as the count-1
  entries in (3,*) sup-att. If it is missing while its RESOLVE is present,
  the counting is incomplete.
- K-E9A-5: no sup-att segment may appear for action 2 (zero supersessions),
  and no sup-att segment may carry counts inconsistent with the 10 known
  EP_SUP episodes.

If K-E9A-2, K-E9A-3, K-E9A-4, or K-E9A-5 fails: H-EXP9 is DOWNGRADED (if the
failure is bounded to an edge case) or KILLED (if the core denominator claim
breaks). If all fail to trigger (all INCONCLUSIVE): the attack is void and
reported as such.

## X-E9-2 (Mixed): raw-to tag under mixed clamp/no-clamp cells

**Fixture E2** = D2 + these 4 appended lines (fresh states, no contests):

```
T 5 0 1 | 0 | 2 0 1
T 5 0 2 | 0 | 9 0 2
T 5 1 0 | 0 | 6 1 0
T 2 0 2 | 0 | 7 0 2
```

**Hand-derived expectations:** cell (a=0,v=temp,o=2,x=2) change episodes:

- D2: 9x (os=2,ns=3); 1x (os=5,ns=2).
- New: (os=5,ns=2), (os=5,ns=9), (os=5,ns=6), (os=2,ns=7).
- Count = 14. rmin=2, rmax=5, rdiff=4 (four os=5 episodes differ from o=2):
  tag `(raw:2..5)`. tomin=2, tomax=9, todiff=12 (all except the two ns=2
  episodes): tag `(raw-to:2..9)`.
- Expected bucket render on any temp==2 line for action 0:
  `2:14*(raw:2..5)(raw-to:2..9)`.
- This cell mixes: clamped-from/unclamped-to (5->2), clamped-from/clamped-to
  (5->9, 5->6), unclamped-from/clamped-to (2->7, 2->3). The raw-to range must
  span all change episodes including the ns==x ones (tomin/tomax update for
  every ns!=os episode per source).

**Kill criteria X-E9-2:**

- K-E9B-1: some TRANSITION-EVIDENCE temp==2 line must show action 0 with the
  o=2 bucket rendered EXACTLY as `2:14*(raw:2..5)(raw-to:2..9)`. If the
  raw-to range excludes any observed raw to-value (2,3,6,7,9), includes an
  unobserved value, is missing while todiff>0, or the count is not 14: the
  raw-to record claim is falsified.
- If action 0 appears in no temp==2 TRANSITION-EVIDENCE line: INCONCLUSIVE,
  reported as such.

## X-E9-3 (Multi): sup-att on multi-variable picks, one superseded from-state

**Fixture E3** = D2 + these 10 appended lines:

```
# contest: action 1 at (1,0,0): 3 more A + 5 B; 4-episode loser set, from=(1,0,0)
T 1 0 0 | 1 | 0 0 0
T 1 0 0 | 1 | 0 0 0
T 1 0 0 | 1 | 0 0 0
T 1 0 0 | 1 | 2 0 0
T 1 0 0 | 1 | 2 0 0
T 1 0 0 | 1 | 2 0 0
T 1 0 0 | 1 | 2 0 0
T 1 0 0 | 1 | 2 0 0
# visibility: action-1 EP_ACT changes on pressure and lamp (fresh states)
T 2 2 2 | 1 | 2 1 2
T 0 0 2 | 1 | 0 0 1
```

**Hand-derived expectations:** 4 EP_SUP episodes of action 1, all
`T 1 0 0 | 1 | 0 0 0` (1 from D2 + 3 new), from-state (1,0,0). The SAME 4
episodes must be visible in all three variables with different
from-distributions:

- (1,temp): sup-att {0:0,1:4,2:0} (shown wherever action 1 appears for temp).
- (1,pressure): sup-att {0:4,1:0,2:0} (action 1 appears for pressure==1 via
  `T 2 2 2 | 1 | 2 1 2`).
- (1,lamp): sup-att {0:4,1:0,2:0} (action 1 appears for lamp==1 via
  `T 0 0 2 | 1 | 0 0 1`).

**Kill criteria X-E9-3:**

- K-E9C-1 (gate): output must contain `RESOLVE action 1 state (1 0 0)`.
  If absent: INCONCLUSIVE.
- K-E9C-2: all three sup-att segments above must appear with exactly these
  values on lines showing (1,temp), (1,pressure), (1,lamp) respectively.
  Missing or wrong in any: the per-(a,v) accounting is broken.
- K-E9C-3: the completeness invariant (from-att + sup-att = fixture-text
  episode count per (a,v,oa)) must hold for (1,temp), (1,pressure),
  (1,lamp).

## X-E9-3b (Boundary, exploratory): action whose changes to a variable were all superseded

**Fixture E3b** = D2 + these 5 appended lines:

```
T 0 0 1 | 3 | 0 1 1
T 0 0 1 | 3 | 0 1 1
T 0 0 1 | 3 | 0 0 1
T 0 0 1 | 3 | 0 0 1
T 0 0 1 | 3 | 0 0 1
```

**Hand-derived expectations:** contest at (3,(0,0,1)): 2x A=(0,1,1), then
1st B=(0,0,1) opens (1,1), 2nd B resolves (s1=2>1). 2 EP_SUP episodes, both
`T 0 0 1 | 3 | 0 1 1` (lamp 0->1 changes). Action 3's EP_ACT episodes are
D2's `T 0 1 0 | 3 | 0 0 0` (pressure 1->0) plus 3x B (no changes), so
chgto(3,lamp,x)=0 for all x: action 3 NEVER appears on any lamp
TRANSITION-EVIDENCE line. The 2 superseded lamp-changing episodes are
therefore unmarked on lamp lines (they are marked on the pressure==0 line
for action 3 via sup-att (3,pressure)={0:2,1:0,2:0}, since action 3 changed
pressure to 0).

This is EXPLORATORY, not a kill bar: report exactly how the output surfaces
(or fails to surface) these 2 episodes, and assess the legend sentence
"absence of the sup-att segment means zero superseded episodes for that
action and variable" against the (3,lamp) case. If the output asserts
completeness for a SHOWN (a,v) that is false, that is a finding (downgrade
class); otherwise it is a documented boundary.

## X-E9-4 (Regression): verify all 5/5 H-EXP9 behaviors, no silent changes

- Extract committed `causal/adv/exp_invent9.zag` from git (not the worktree
  copy), build with znc 2026.07.0-dev (edition 2026) in /tmp only.
- Run the 11 frozen fixtures (S1,S2,S0,A1,F1,G1,H1,J1,R1,C1,r1_e8_ctrl) plus
  D2 and D3, 2x each; cmp every run against the committed evidence
  `causal/adv/evidence/exp9_*_raw.txt` and `exp9_adv_d2_raw.txt`,
  `exp9_adv_d3_raw.txt` (byte-identical required).
- Grep the five frozen bars: K-E9-1 (`from-att {0:1,1:1,2:10}
  sup-att {0:0,1:0,2:1}` on D2), K-E9-2 (all 16 K-E8-2 substrings),
  K-E9-3 (`2:1*(raw:5..5)(raw-to:9..9)` on D3, no `(raw-to:` tag on C1's
  temp from-list), K-E9-5 (exp9-vs-exp8 strip diff empty; re-verified via
  shell only).

**Kill criterion X-E9-4:** K-E9D-1: any byte mismatch with committed evidence
or any frozen-bar substring missing: REGRESSION, H-EXP9 DOWNGRADED (if
bounded) or KILLED (if a frozen bar no longer holds).

## Verdict mapping

- Any kill criterion above FAILS (excluding INCONCLUSIVE gates and the
  exploratory E3b): H-EXP9 is KILLED if a core repair claim is falsified
  (denominator completeness, sup-att correctness, raw-to correctness), or
  DOWNGRADED if the failure is bounded to an edge case or is
  documentation-class. The report will state which.
- All attacks FAIL to break the claim (all kill criteria hold, no
  INCONCLUSIVE on load-bearing sub-cases): H-EXP9 SURVIVES, adversarially
  confirmed at bounded L2.
- INCONCLUSIVE outcomes are reported explicitly with the reason (e.g.,
  contest did not trigger due to entry dynamics); they do not count as
  passes.

## Governance

- This prereg is committed ALONE before any fixture is created, any binary
  is built, or any attack is run. No amendments after execution begins; any
  correction requires a new dated prereg commit and the reason disclosed.
- Only owned paths will be staged: causal/adv/PREREG_EXP9_ADV.md (this
  file), causal/adv/EXP9_ADV_RESULT.md, causal/adv/exp9_adv_e{1,2,3,3b}.txt,
  causal/adv/evidence/exp9adv_*_raw.txt. No binaries committed. No broad
  git add. Concurrent workers' files untouched.
- On `.git/index.lock` contention: wait for live locks to clear, never
  remove.
- Pure Zag: no Python at any stage. No em dashes in loop documentation.
