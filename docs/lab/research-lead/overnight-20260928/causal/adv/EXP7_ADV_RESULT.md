# H-EXP7 Adversary Report: H-EXP7 DOWNGRADED

**Date:** 2026-09-29
**Red team prereg:** causal/adv/PREREG_EXP7_ADV.md (commit
b046ce810, frozen alone BEFORE any attack fixture was written
or any attack executed; verified strict ancestor of this
commit)
**Attack fixtures:** causal/adv/j1_e7_adv.txt (X-E7-1),
causal/adv/r1_e7_adv.txt (X-E7-2), causal/adv/c1_e7_adv.txt
(X-E7-3), all S1-based per the frozen prereg
**Target binary:** built from committed
causal/adv/exp_invent7.zag (unmodified since 346ee4e98) with
znc 2026.07.0-dev (edition 2026), in /tmp only, not committed
**Raw evidence:** causal/adv/evidence/exp7adv_{j1,r1,c1}_raw.txt
(attack runs), causal/adv/evidence/exp7adv_reg_{s1,g1,h1}.txt
(regression runs); 3/3 byte-identical per fixture
**Purity:** Pure Zag. No Python anywhere (no generators,
verifiers, analysis, or scratch). No em dashes in loop
documentation.

## Verdict: H-EXP7 DOWNGRADED (not killed)

Three of four attacks succeed. The 5/5 frozen H-EXP7 kill
bars all still hold (X-E7-4 regression clean), so this is a
downgrade, not a kill. The TRANSITION-EVIDENCE signal is
accurate in its clamped ontology, but it misleads a planner
in material ways the frozen honest limits do not cover:

1. **Clamp-artifactual from-values (X-E7-1):** a from-bucket
   can be 100 percent clamp artifact with zero raw exemplar.
2. **Attempt-blind rate (X-E7-2):** the (m/n) denominator is
   outcome-conditioned, not attempt-conditioned; failed
   from-state attempts with a different outcome value are
   completely invisible, and materially different realities
   render identically.
3. **Self-loop change rendering (X-E7-3):** a genuine raw
   change renders as "2->2" inside a table headed "change
   episodes," which is self-contradictory in context.

Classification remains bounded L2. The downgrade narrows the
repair claim; it does not retract the 5/5 bars.

## Attack methodology

The red team assumed the H-EXP7 claim false and attacked the
repair's stated purpose: "A planner at temp==0 now sees that
only action 1 ever effected the 0->2 transition" and "The
1-in-11 change no longer renders identically to the 1-in-1
change." Each attack used a fixture the mechanism had never
seen, built on the S1 ambiguity structure so ranked picks
with TRANSITION-EVIDENCE lines are produced. Kill criteria
were frozen in PREREG_EXP7_ADV.md before execution.

## X-E7-1 (From-value): SUCCEEDS

**Fixture J1:** S1 plus two action-0 episodes
`T 5 0 0 | 0 | 2 0 0` (raw temp 5->2, twice). There are ZERO
raw from-2 temp changes by action 0 anywhere in J1.

**Observed output (evidence/exp7adv_j1_raw.txt):**

TRANS a0 temp[0->1:1,1->2:1,2->2:2] pressure[] lamp[]

TRANSITION-EVIDENCE (temp==2 pick):
`temp==2 transitions: 0: from {1:1,2:2} (3/4); ...`

**Finding:** Action 0's temp==2 item shows `from {1:1,2:2}`.
The `2:2` component is 100 percent clamp artifact: both
episodes were raw 5->2, and no raw from-2 temp change by
action 0 exists in the fixture. A planner at temp==2 reads
"action 0 changed temp to 2 twice from 2" and concludes
action 0 is relevant to its from-2 need. In raw terms, action
0 was never observed starting at 2 when it changed temp to 2.
The from-list mixes one genuine from-1 transition with two
artifactual from-2 transitions, and the planner cannot tell
which is which.

**Why the honest limits do not cover this:** The legend
discloses "from/to values are clamped to 0..2 like outcomes"
and the honest limits document "a raw transition like 5->2
renders as 2->2." Neither discloses that a from-bucket can be
ENTIRELY artifactual with no raw exemplar, nor that the
from-list can mix genuine and artifactual entries
indistinguishably. The repair's purpose was to cure
from-blindness; the from-value is clamp-blind in exactly the
cases where the planner most needs precision (boundary
values 0 and 2, where clamping merges). Note the middle
value 1 is exact under clamping (only raw 1 maps to 1); the
vulnerability is specific to buckets 0 and 2.

## X-E7-2 (Rate): SUCCEEDS (on the substantive criterion)

**Fixture R1:** S1 plus one action-0 `T 0 0 0 | 0 | 2 0 0`
(0->2 change) and ten action-0 `T 0 0 0 | 0 | 0 0 0` (0->0
no-ops), all from temp==0. True from-0 0->2 success rate:
1 change in 12 from-0 episodes (1/12). The 10 no-ops have
outcome temp==0, so they do not enter the (m/n) denominator
for x=2.

**Observed output (evidence/exp7adv_r1_raw.txt):**

TRANS a0 temp[0->1:1,0->2:1,1->2:1] pressure[] lamp[]

TRANSITION-EVIDENCE (temp==2 pick):
`temp==2 transitions: 0: from {0:1,1:1} (2/3); ...`

**Finding:** The temp==2 item shows `(2/3)` and nowhere
reflects the 10 failed from-0 attempts. Control check: the
identical fixture WITHOUT the 10 no-ops produces the
byte-identical temp==2 item `from {0:1,1:1} (2/3)` (verified
by removing the no-op lines; chgto and achv for x=2 are
unchanged because the no-ops have outcome temp==0). Two
materially different realities, 1 success in 2 from-0
attempts versus 1 success in 12, render IDENTICALLY. This is
the exact "renders identically" pattern of the H-EXP6 X-E6-2
attack that H-EXP7 was built to close. The (m/n) rate is
change-per-outcome, not change-per-attempt; attempt-
conditioned base rates remain hidden whenever failures carry
a different outcome value than the required one.

**Frozen-criterion note (honest):** The prereg's literal
operationalization expected the string `from {0:1} (1/1)`.
The S1 base already contains an action-0 1->2 change and two
temp==2 outcomes, so the observed item is `from {0:1,1:1}
(2/3)`, not `(1/1)`. The letter of the criterion was foiled
by this fixture-design error. The attack is judged SUCCEEDS
on the frozen substantive criterion (the planner-misleading
criterion: a strong-looking rate hiding the true from-state
rate, an active-misleading hazard the honest limits do not
cover as such). The "does not measure robustness" honest
limit is a passive scope statement; it does not disclose
that the rate is specifically blind to cross-outcome
failures or that distinct attempt histories render
identically.

## X-E7-3 (Clamp): SUCCEEDS (low severity)

**Fixture C1:** S1 plus one action-0 `T 5 0 0 | 0 | 2 0 0`
(raw temp 5->2, a genuine raw change since 5 != 2).

**Observed output (evidence/exp7adv_c1_raw.txt):**

TRANS a0 temp[0->1:1,1->2:1,2->2:1] pressure[] lamp[]

TRANSITION-EVIDENCE (temp==2 pick):
`temp==2 transitions: 0: from {1:1,2:1} (2/3); ...`

**Finding:** The TRANSITION TABLE, headed "change episodes
per action/variable/from-value/to-value," contains the cell
`2->2:1`: a change tabulated as a self-loop. The from-list
contains `2:1` with o==x for a genuine raw change. The
rendering is accurate in the clamped ontology but
self-contradictory in context: a reader sees a "2->2
transition" in a change table and cannot know whether it
means "maintained 2" or "changed 5->2." Severity is low
(confusing rendering, not a false claim); it is recorded
because the frozen criterion was met and the honest limit
documents the convention without addressing the
self-contradiction.

## X-E7-4 (Regression): SUCCEEDS (clean)

All five frozen H-EXP7 kill bars reproduce byte-identically
on the committed binary:

- K-E7-1: G1 contains `0: from {1:3} (3/4)` (2 occurrences:
  ranked pick and top pick) and `1: from {0:2} (2/2)`.
- K-E7-2: H1 contains `0: from {1:1} (1/11)` and
  `1: from {0:1} (1/1)`.
- K-E7-3: K-E6-1/K-E6-2/K-E6-4 checks reproduce (inherited
  from the EXP7_RESULT verification; binary built from the
  identical committed source).
- K-E7-4: 3/3 byte-identical runs per fixture; md5s match
  the frozen values exactly: S1
  fffd7b90df92bd818425faeafcb39879, S2
  cfcd78710ea1fd4fc11a1efcba6b23bd, S0
  166126b807aa5f3d1ec3f389d80463df, A1
  330eff81a35ad932f2eb894017983139, F1
  f182d8a6a0523d04d531367bde0fd866, G1
  4b7e445a19f28b5d05d41363b96ed9fd, H1
  2151589e50be604cd0d92f039c2e3d86.
- K-E7-5: F1 contains
  `TRANS a0 temp[0->1:1,1->2:1] pressure[] lamp[1->0:1]`.

No silent change from exp6 behavior outside the 5 frozen
additions. Attack-run determinism: J1
e88e34f195126981a160a0f8c93ff5c3, R1
a85eb6cd0587d5139038e235caffa617, C1
36b1c3485b9780d017eb9f2c00d33b3e (3/3 each).

## Causal interpretation

The downgrade does not show the mechanism is useless; it
shows the repair claim was broader than the signal. The
TRANSITION-EVIDENCE does decompose change-to claims by
from-value and per-action outcome rate, and the 5/5 frozen
bars (including the original X-E6-1/X-E6-2 closures on G1/H1)
stand. What it does NOT do:

- It does not report raw from-values, so boundary-bucket
  from entries (0, 2) can be artifactual.
- It does not report attempt-conditioned rates, so the
  planner cannot see failures that carried other outcomes.
- It does not flag self-loop renderings of genuine changes.

A planner that treats "from {2:c}" as "observed starting at
2" or "(m/n)" as "reliability" will be misled. The honest
limits warn against causal reading but not against these
specific rendering hazards.

## Limitations of this red team

- Negative raw values are not expressible in fixtures
  (parse_int reads digits only); clamp-artifact attacks used
  raw > 2 only. The symmetric bucket-0 artifact (raw < 0)
  could not be probed.
- Cross-variable confounding was explicitly out of scope
  (disclosed as "not causal attribution").
- Single-episode non-reproducibility was out of scope
  (already disclosed).
- The R1 letter-criterion operationalization was flawed by
  S1 base contamination (documented above); the substantive
  probe nevertheless succeeded.

## Governance disclosures

- Prereg PREREG_EXP7_ADV.md committed alone as b046ce810
  before any attack fixture was written or executed.
- Pure Zag throughout: fixtures are hand-written text, the
  binary was compiled with znc, outputs were compared with
  cmp/md5sum/grep. No Python at any stage.
- Only owned files staged: PREREG_EXP7_ADV.md,
  j1_e7_adv.txt, r1_e7_adv.txt, c1_e7_adv.txt,
  EXP7_ADV_RESULT.md (this file), and
  evidence/exp7adv_*.txt. Concurrent workers' files were not
  touched.
- The X-E7-2 fixture-design error (S1 contamination of the
  intended 1/1) is disclosed above rather than hidden; the
  verdict rests on the substantive criterion.

## Commit lineage (branch tnn-native-lab, local only)

- b046ce810: PREREG H-EXP7 red team FROZEN (alone; before
  any attack fixture or execution)
- this commit: PREREG_EXP7_ADV.md already committed;
  j1_e7_adv.txt, r1_e7_adv.txt, c1_e7_adv.txt,
  EXP7_ADV_RESULT.md (this file),
  evidence/exp7adv_{j1,r1,c1,reg_s1,reg_g1,reg_h1}_raw.txt
- Ordering: prereg is a strict ancestor of this commit
  (verified via merge-base --is-ancestor before committing).

## Suggested follow-up for parent

H-EXP7 is DOWNGRADED: the 5/5 bars stand, but the repair
claim must be narrowed to "decomposes change-to claims by
clamped from-value and per-action outcome rate," with the
three rendering hazards (artifactual boundary from-buckets,
attempt-blind rate, self-loop change rendering) documented
as known limitations. A repair lane (H-EXP8) could: report
raw from-values alongside clamped buckets, add an
attempt-conditioned rate (changes per from-state episode),
and flag o==x renderings. The research paper's NQ3 line
should read H-EXP7 DOWNGRADED (5/5 bars hold; 3 red-team
findings).
