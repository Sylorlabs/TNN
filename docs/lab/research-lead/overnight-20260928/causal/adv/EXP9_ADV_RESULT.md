# H-EXP9 Independent Red-Team Report (Adversary)

**Date:** 2026-09-29
**Target:** H-EXP9 SURVIVES 5/5 (bounded L2), EXP9_RESULT.md
**Prereg:** causal/adv/PREREG_EXP9_ADV.md (commit `aee0521bb`, frozen alone
BEFORE any fixture creation, build, or run; verified strict ancestor)
**Source:** committed causal/adv/exp_invent9.zag, extracted from git HEAD
(byte-identical to worktree copy, cmp-verified), built with znc 2026.07.0-dev
(edition 2026) in /tmp only, never committed
**Attack fixtures:** causal/adv/exp9_adv_e1.txt, exp9_adv_e2.txt,
exp9_adv_e3.txt, exp9_adv_e3b.txt (created AFTER the prereg commit via shell
heredocs, exactly as frozen in the prereg)
**Raw evidence:** causal/adv/evidence/exp9adv_{e1,e2,e3,e3b}_raw.txt (first
runs); all attack fixtures verified 2/2 byte-identical (deterministic)
**Purity:** Pure Zag throughout. No Python at any stage. Fixtures via shell
heredocs and cat. All analysis via grep, cmp, diff, md5sum, wc. No em dashes
in loop documentation.

## Verdict: H-EXP9 SURVIVES (adversarially confirmed, bounded L2)

All four attacks were executed as preregistered. Every kill criterion whose
gate triggered HOLDS. The repair's core claims (sup-att accounting
correctness, complete-denominator completeness, raw-to record correctness)
withstood direct adversarial construction. Two sub-cases are INCONCLUSIVE due
to inherited H-EXP entry dynamics (ambiguity absorbing episodes before any
contest could open), not due to repair behavior; they are reported explicitly
and do not count as passes. No kill criterion failed. H-EXP9 is NOT killed
and NOT downgraded.

## Methodology

1. Read EXP9_RESULT.md, PREREG_EXP9.md, and exp_invent9.zag (R1/R2/R3 repair
   code, contest_feed, entry_ingest, emit_transition_evidence).
2. Wrote PREREG_EXP9_ADV.md with four attacks, frozen fixtures, hand-derived
   expectations, and explicit kill criteria; committed it alone as `aee0521bb`
   before any execution.
3. Extracted committed exp_invent9.zag from git, cmp-verified against worktree,
   built in /tmp/e9adv (znc 2026.07.0-dev, warnings only, same as builder).
4. Created E1/E2/E3/E3b via shell heredocs exactly as frozen; verified T-line
   counts (44/25/31/26).
5. Ran all four; checked the CONTEST/RESOLVE gate lines FIRST, then the
   frozen kill criteria.
6. Ran X-E9-4: rebuilt from git-extracted source, ran all 11 frozen fixtures
   plus D2/D3 2x each, cmp against committed evidence, grep-checked all five
   frozen bars.

## X-E9-1 (Boundary): supersession at entry boundaries. HOLDS.

**Gate (K-E9A-1):** Three of four designed contests triggered as predicted:

- `RESOLVE action 0 state (0 0 0) winner outcome 1 (2 0 0) support 2 at seq 26;
  loser SUPERSEDED` (X-E9-1a, 4-episode loser set). TRIGGERED.
- `RESOLVE action 1 state (1 0 0) winner outcome 1 (2 0 0) support 2 at seq 34;
  loser SUPERSEDED` (X-E9-1b, 4-episode loser set). TRIGGERED.
- `CONTEST action 3 state (1 1 1) ... opened at seq 44` with NO resolve
  (X-E9-1d, 1v1 tie). TRIGGERED AS DESIGNED (no supersession).
- X-E9-1c (action 3 at (2,2,2), single-episode loser): NO contest opened.
  The action-3 entry went `AMBIGUOUS action 3 [any] candidates={s0,s1,s2} at
  seq 38` when the fresh-state episode arrived, then `CONFLICTED at seq 39`.
  The B episode refuted ambiguity candidates instead of opening a contest.
  INCONCLUSIVE (entry dynamics did not cooperate; neither pass nor kill).

**K-E9A-2 (sup-att values):** On the temp==2 TRANSITION-EVIDENCE line:

- `0: from {0:5,1:1,2:10*(raw:2..5)(raw-to:2..3)} (16/16)
  from-att {0:5,1:1,2:10} sup-att {0:4,1:0,2:1}`
  Expected (0,temp) sup-att {0:4,1:0,2:1}: 4 from (0,0,0) plus D2's 1 from
  (2,0,0), aggregated across two different contests. EXACT MATCH.
- `1: from {1:5} (5/5) from-att {0:1,1:5,2:1} sup-att {0:0,1:4,2:0}`
  Expected (1,temp) sup-att {0:0,1:4,2:0}: the 4-episode loser set. EXACT
  MATCH. (Also confirmed on the temp==1 line.)
- (3,*) sub-case: INCONCLUSIVE (precondition RESOLVE absent).

**K-E9A-3 (completeness invariant):** from-att + sup-att (absent = 0) equals
the fixture-text episode count per (a,v,oa), verified by hand against
grep-counted fixture lines:

- (0,temp): {0:5,1:1,2:10} + {0:4,1:0,2:1} = {0:9,1:1,2:11}. Fixture:
  action-0 temp-from 0: 9 (1 D2 + 3 A-SUP + 5 B); from 1: 1; from 2: 11
  (1 SUP + 1 raw-5 + 9 raw-2). HOLDS.
- (1,temp): {0:1,1:5,2:1} + {0:0,1:4,2:0} = {0:1,1:9,2:1}. Fixture:
  from 0: 1; from 1: 9 (1 D2-SUP + 3 A-SUP + 5 B); from 2: 1. HOLDS.
- (3,pressure): {0:0,1:3,2:5} + (no segment = 0). Fixture: from 0: 0;
  from 1: 3; from 2: 5; zero SUP. HOLDS (absence-means-zero confirmed).
- (3,lamp): {0:1,1:2,2:5} + 0. Fixture: from 0: 1; from 1: 2; from 2: 5.
  HOLDS.

**K-E9A-4 (single-episode loser):** INCONCLUSIVE (X-E9-1c did not trigger).
Note: D2's own pre-existing single EP_SUP episode (`T 2 0 0 | 0 | 2 0 0`,
counted as {0:0,1:0,2:1}) continues to be counted correctly in all runs,
so the single-episode boundary is covered by the frozen D2 evidence even
though the new single-episode attack did not trigger.

**K-E9A-5 (no spurious/missing segments):** All sup-att segments in E1 output
are {0:0,1:4,2:0} (action 1, temp) and {0:4,1:0,2:1} (action 0, temp).
No sup-att for action 2 (zero supersessions). No sup-att for action 3 (zero
supersessions; the unresolved contest correctly yields no marker). No
segment carries counts inconsistent with the 9 actual EP_SUP episodes
(1 D2 + 4 X-E9-1a + 4 X-E9-1b). HOLDS.

## X-E9-2 (Mixed): raw-to tag under mixed clamp/no-clamp cells. HOLDS.

**K-E9B-1:** On the temp==2 line for action 0:

`0: from {1:1,2:14*(raw:2..5)(raw-to:2..9)} (15/15)`

Expected `2:14*(raw:2..5)(raw-to:2..9)` exactly. The cell (0,temp,2,2)
contains 14 change episodes mixing clamped-from/unclamped-to (raw 5->2),
clamped-from/clamped-to (raw 5->9, 5->6), and unclamped-from/clamped-to
(raw 2->7, 2->3), with raw to-values {2,3,5,6,7,9}. The tag renders
(raw-to:2..9): the honest observed range over ALL change episodes in the
cell, including the ns==x episodes (raw 5->2, raw 2->2-class) that do not
themselves trigger the tag. EXACT MATCH. The raw-to record claim is
confirmed under adversarial mixing.

Also confirmed: from-att {0:1,1:1,2:14} + sup-att {0:0,1:0,2:1} = 15 =
total action-0 clamped-temp-from-2 episodes (14 EP_ACT + 1 SUP). The
invariant holds on the mixed fixture too.

## X-E9-3 (Multi): sup-att on multi-variable picks. HOLDS (2/3 shown).

**Gate (K-E9C-1):** `RESOLVE action 1 state (1 0 0) winner outcome 1 (2 0 0)
support 2 at seq 26; loser SUPERSEDED`. TRIGGERED. 4 EP_SUP episodes of
action 1, all from (1,0,0).

**K-E9C-2:** The same 4 superseded episodes are visible in two variables
with the correct per-variable from-distributions:

- (1,temp): `sup-att {0:0,1:4,2:0}` (on temp==1 and temp==2 lines for
  action 1). EXACT MATCH.
- (1,lamp): `sup-att {0:4,1:0,2:0}` (on three lamp==1 lines for action 1,
  via the visibility episode `T 0 0 2 | 1 | 0 0 1`). EXACT MATCH.
- (1,pressure): INCONCLUSIVE. Action 1 changed pressure to 1 (via
  `T 2 2 2 | 1 | 2 1 2`), but no ranked pick has pressure==1 as a target,
  so action 1 never appears for pressure and the segment is not shown.
  This is pick-coverage, not a mechanism failure; the (a,v)-gated display
  logic is as specified.

**K-E9C-3 (invariant):**

- (1,temp): {0:2,1:5,2:2} + {0:0,1:4,2:0} = {0:2,1:9,2:2}. Fixture:
  from 0: 2; from 1: 9 (4 SUP + 5 EP_ACT); from 2: 2. HOLDS.
- (1,lamp): {0:7,1:0,2:2} + {0:4,1:0,2:0} = {0:11,1:0,2:2}. Fixture:
  from 0: 11 (4 SUP + 7 EP_ACT); from 1: 0; from 2: 2. HOLDS.

## X-E9-3b (Boundary, exploratory): INCONCLUSIVE.

The designed contest at (3,(0,0,1)) did not open: the action-3 entry went
`AMBIGUOUS action 3 [any] candidates={s1,s2} at seq 22` on the fresh-state
episode, then `CONFLICTED at seq 24`. Zero EP_SUP for action 3. The output
correctly shows action 3 with from-att and no sup-att segment (absence
means zero, confirmed). The "action whose changes to a variable were all
superseded" scenario was not constructed; the boundary remains unprobed by
this red team. This is a limitation of the attack design (fresh states
trigger ambiguity, not contests, in the inherited H-EXP learner), not
evidence for or against the repair.

## X-E9-4 (Regression): all 5/5 behaviors verified, no silent changes.

**K-E9D-1:** Binary rebuilt from git-extracted committed source (not the
worktree copy). All 11 frozen fixtures plus D2/D3 run 2x each:

- 2/2 byte-identical per fixture (deterministic).
- All 13 outputs cmp-identical to the committed evidence
  (`evidence/exp9_*_raw.txt`, `exp9_adv_d2_raw.txt`, `exp9_adv_d3_raw.txt`).
- K-E9-1: `from-att {0:1,1:1,2:10} sup-att {0:0,1:0,2:1}` present on D2.
- K-E9-2: all frozen substrings present (J1, R1, ctrl, C1, G1, H1, F1 rows;
  the one apparent "MISSING" in the check loop was a shell bracket-escaping
  artifact, re-verified with grep -F).
- K-E9-3: `2:1*(raw:5..5)(raw-to:9..9)` on D3; zero `(raw-to:` tags in C1's
  TRANSITION-EVIDENCE temp from-list.
- K-E9-4: determinism confirmed (this run 2/2; builder's 3/3 stands).
- K-E9-5: change-set purity re-confirmed by byte-identity with the
  builder's committed evidence (the strip-diff itself was the builder's;
  this red team confirms the outputs it produced are reproducible from
  the committed source).

No regression. No silent change.

## Causal interpretation

The H-EXP9 repair does what it claims, and the claims are now
adversarially load-bearing rather than merely asserted. The sup-att table
counts every EP_SUP episode exactly once per (action, variable, clamped
from-state), using the same index function and clamping as the from-att
table, so from-att + sup-att is arithmetically complete over the two
existing episode states; the red team verified this invariant on
multi-contest aggregation (X-E9-1a: two contests feeding one (a,v) cell),
on multi-episode loser sets (4 losers), and across variables (X-E9-3: one
episode set, three from-distributions). The raw-to tag records the honest
observed range over all change episodes in the cell under clamp/no-clamp
mixing (X-E9-2). The "absence means zero" legend sentence held everywhere
it was testable: actions with zero supersessions (action 2, action 3)
appear with from-att and no sup-att segment.

## Boundaries and honest limits (adversary-confirmed)

- Contests only open in ACTIVE entries at already-seen states. Fresh
  (action,state) pairs with divergent outcomes drive the inherited learner
  to AMBIGUOUS/CONFLICTED instead (observed twice: E1 seq 38, E3b seq 22).
  This bounds where supersessions (and hence sup-att data) can arise; it is
  inherited H-EXP behavior, not an H-EXP9 defect.
- sup-att visibility is gated on the action appearing for the variable in
  a ranked pick's TRANSITION-EVIDENCE line (chgto>0). An action with
  superseded episodes that never changes a shown variable-target has its
  exclusions disclosed globally by the legend but not per-(a,v) marked.
  The E3b probe intended to test this further but did not construct the
  scenario; the boundary stands as documented, unprobed.
- The single-episode loser set (X-E9-1c) and the third variable of X-E9-3
  ((1,pressure)) are unprobed for the reasons above; the D2 frozen evidence
  covers the single-episode case.
- Classification remains bounded L2, as claimed. Nothing in this red team
  suggests otherwise.

## Failures and negative evidence

- No kill criterion failed. The adversary could not falsify the
  denominator-completeness claim, the sup-att accounting, or the raw-to
  record on any triggered attack.
- Two sub-cases INCONCLUSIVE (X-E9-1c, E3b) and one partial ((1,pressure)
  not shown): all due to inherited entry/ambiguity dynamics or pick
  coverage, reported explicitly, not counted as passes.

## Governance disclosures

1. Pure Zag: no Python at any stage of this red team (fixtures, builds,
   runs, analysis). Shell only.
2. Prereg ordering: PREREG_EXP9_ADV.md committed alone as `aee0521bb`
   before any fixture was created, any binary built, or any attack run.
   Verified strict ancestor of this result commit via merge-base
   --is-ancestor before committing.
3. Only owned paths staged: causal/adv/PREREG_EXP9_ADV.md (already
   committed), causal/adv/EXP9_ADV_RESULT.md (this file),
   causal/adv/exp9_adv_e{1,2,3,3b}.txt,
   causal/adv/evidence/exp9adv_{e1,e2,e3,e3b}_raw.txt. No binaries committed
   (builds in /tmp/e9adv only). No broad git add. Concurrent workers' files
   untouched.
4. Hand derivations in the prereg were made from source reading before
   execution; the X-E9-1c/E3b expectations are VOID where their gate
   contests did not trigger (marked INCONCLUSIVE, not retrofitted).
5. No em dashes in loop documentation (checked).
6. Note for the record: the H-EXP9 builder's python3 scratch use (disclosed
   in EXP9_RESULT.md governance note 1) is outside this red team's scope;
   this red team used no Python and independently reproduced all 5/5 bars
   from the committed source.

## Commit lineage (branch tnn-native-lab, local only)

- `aee0521bb`: Prereg: H-EXP9 independent red team (PREREG_EXP9_ADV) FROZEN
  (alone; before any fixture, build, or run)
- this commit: causal/adv/EXP9_ADV_RESULT.md (this file),
  causal/adv/exp9_adv_e{1,2,3,3b}.txt,
  causal/adv/evidence/exp9adv_{e1,e2,e3,e3b}_raw.txt
- Ordering: prereg is a strict ancestor of this commit (verified via
  merge-base --is-ancestor before committing).
