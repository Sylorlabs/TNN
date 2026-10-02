# Preregistration: H-EXP8 (Raw From-Values + Attempt-Conditioned Rates + Self-Loop Flags)

Date: 2026-09-29. Pure Zag. This prereg is frozen BEFORE any
implementation of exp_invent8.zag. No Python at any stage.

## Mission

Close the three H-EXP7 red-team downgrades
(causal/adv/EXP7_ADV_RESULT.md):

- X-E7-1: clamp-artifactual from-values. Fixture J1: action 0
  temp==2 item shows `from {1:1,2:2}` where the `2:2` bucket is
  100 percent clamp artifact (two raw 5->2 episodes; zero raw
  from-2 temp changes by action 0 exist in J1). A planner at
  temp==2 reads from-2 evidence that never existed in raw terms.
- X-E7-2: attempt-blind rate. Fixture R1: action 0 temp==2 item
  shows `from {0:1,1:1} (2/3)`; the ten from-0 no-ops are
  invisible, and the identical fixture without the no-ops
  renders byte-identically. The (m/n) denominator is
  outcome-conditioned, not attempt-conditioned.
- X-E7-3: self-loop change rendering. Fixture C1: the
  TRANSITION TABLE contains `2->2:1` for a genuine raw 5->2
  change; a change tabulated as a self-loop inside a table
  headed "change episodes".

H-EXP8 adds three strictly additive annotations to the H-EXP7
output: raw from-value ranges per clamped from-bucket,
per-action attempt-conditioned from-state counts, and an
explicit flag on every clamp-rendered self-loop cell.

## Hypothesis H-EXP8

Reporting the observed raw from-value range alongside each
clamped from-bucket, the attempt denominator per from-state,
and flagging every o==x cell closes X-E7-1, X-E7-2, X-E7-3
without introducing a new overclaim, provided the legend
scopes each annotation exactly (observed range, not
distribution; attempt count, not intervention probability;
deductive flag, not empirical discovery).

## Design (frozen)

exp_invent8.zag is built by copying exp_invent7.zag VERBATIM
and making exactly the additions below. Nothing else changes:
the selection mechanism, ranking heuristic, reachability FLAG
logic, CONTROLLABILITY computation, the ACHIEVABILITY report,
the CHANGE-TO table, the CHANGE-EVIDENCE lines, the
TRANSITION TABLE header and cell counts, and the
TRANSITION-EVIDENCE from-lists and (m/n) rates are untouched
(all stay byte-identical apart from the frozen annotations).

### Addition 1: attempt and raw-from index helpers

att is 36 i32 cells indexed ((a*3)+v)*3+o, a in 0..3, v in
0..2, o in 0..2 (clamped from-value). Counts EP_ACT episodes
of action a with clamped from-value o for variable v,
regardless of outcome or change. Allocated in main as
z_alloc(144), accessed with att_idx/att_get/att_add
(identical structure to the trans helpers, separate memory).

rmin, rmax, rdiff are 108 i32 cells each, indexed
(((a*3)+v)*3+o)*3+x like trans. For each counted change
episode they record the raw (unclamped) from-value os:
rmin/rmin = observed minimum/maximum raw from-value in the
cell, rdiff = number of episodes in the cell whose raw
from-value differs from the clamped bucket label o.
Allocated in main as three z_alloc(432) slices. z_alloc
zeroes memory, so rdiff starts at 0 correctly; rmin is
explicitly initialized to 999999999 and rmax to -999999999
in main before compute_transitions runs (a plain loop; the
sentinels are never rendered because the raw tag is emitted
only when rdiff > 0, which implies at least one episode was
recorded).

### Addition 2: compute_transitions extension

The existing EP_ACT episode loop is extended, with no change
to the trans_add call. For every EP_ACT episode with a in
0..3, for v in 0..2: let o = clamp(ep_s(W,e,v));
att_add(att,a,v,o). Inside the existing change branch
(ns != os, the exact raw change predicate), after
trans_add(trans,a,v,o,x): update the raw record for
(a,v,o,x) with the raw from-value ros = ep_s(W,e,v):
if ros < rmin: rmin = ros; if ros > rmax: rmax = ros;
if ros != o: rdiff = rdiff + 1.

Invariants: for every (a,v,o), att[a][v][o] >= sum over x of
trans[a][v][o][x] (every change episode is itself an
attempt). rdiff > 0 implies rmin <= rmax are genuine
observed raw values.

### Addition 3: self-loop flag in the TRANSITION TABLE

In emit_trans_cells, after emitting `o->x:c` for a nonzero
cell, emit `*` iff o == x. Frozen: every o==x cell in the
trans table is a genuine raw change (the change branch
requires raw ns != raw os), so the flag is deductive, not
empirical. J1 row becomes (hand-verified against the current
exp7 J1 run):
`TRANS a0 temp[0->1:1,1->2:1,2->2:2*] pressure[] lamp[]`
C1 row becomes:
`TRANS a0 temp[0->1:1,1->2:1,2->2:1*] pressure[] lamp[]`

### Addition 4: raw-from tag and self-loop flag in from-buckets

In emit_transition_evidence, the per-bucket render `o:c`
becomes: `o:c`, then `*` iff o == x (same deductive flag),
then `(raw:lo..hi)` iff rdiff(a,v,o,x) > 0, where lo/hi are
the recorded rmin/rmax. Frozen J1 temp==2 pick segment
(hand-verified against the current exp7 J1 run, which shows
`0: from {1:1,2:2} (3/4)`):
`0: from {1:1,2:2*(raw:5..5)} (3/4)`
Frozen C1 temp==2 pick segment (current exp7 shows
`0: from {1:1,2:1} (2/3)`):
`0: from {1:1,2:1*(raw:5..5)} (2/3)`
Buckets whose raw from-values all equal the label render
unchanged (no tag), so G1/H1 frozen substrings survive as
prefixes.

### Addition 5: attempt-conditioned from-state counts per pick

In emit_transition_evidence, after the per-action rate
`(ma/na)` closing paren, emit
` from-att {0:t0,1:t1,2:t2}` where ti = att_get(att,a,v,i).
All three clamped from-states are always listed, ascending.
Frozen R1 temp==2 pick action-0 item (current exp7 shows
`0: from {0:1,1:1} (2/3)`; hand-verified att counts: S1 base
contributes 1 action-0 temp-from-0 episode; R1 adds 1 change
+ 10 no-ops):
`0: from {0:1,1:1} (2/3) from-att {0:12,1:1,2:1}`

### Addition 6: legend extension

The H-EXP5 legend text, the H-EXP6 legend sentence, and the
H-EXP7 legend sentence are kept byte-identical. Three frozen
sentences are appended immediately after them (same emit
block):

A from-bucket rendered as "o:c(raw:lo..hi)" contains change episodes whose raw from-value differs from the clamped bucket label o; raw:lo..hi is the observed raw from-value range in that bucket, and the tag appears only when at least one episode's raw from-value differs from the label. A bucket can be entirely artifactual (for example raw 5->2 rendering as from 2); in the current episode format raw values are non-negative, so in practice only bucket 2 carries clamp artifact while bucket 1 is exact.

A transition cell rendered as "o->x:c*" (or a from-bucket "o:c*") has clamped from-value equal to clamped to-value; every such cell is a genuine raw change (raw from != raw to, required by the change predicate) rendered as a self-loop by value clamping.

from-att {0:t0,1:t1,2:t2} counts EP_ACT episodes of that action with clamped from-value 0/1/2 for the variable: the attempt denominator per from-state. A bucket "o:c" with from-att o-entry t means c changes in t from-o attempts; failures that carried a different outcome value are invisible in the change/outcome rate but counted here. This is an observed attempt count, not a success probability under intervention.

## Frozen fixtures

S1 = causal/cum_B.txt, S2 = causal/exp_obs2.txt,
S0 = causal/exp_null.txt, A1 = adv/x_e3_a1.txt,
F1 = adv/f1_e5_adv.txt, G1 = adv/g1_e6_adv.txt,
H1 = adv/h1_e6_adv.txt (the seven H-EXP7 frozen fixtures),
plus J1 = adv/j1_e7_adv.txt, R1 = adv/r1_e7_adv.txt,
C1 = adv/c1_e7_adv.txt (the three H-EXP7 red-team attack
fixtures, now regression tests), plus the new control
fixture adv/r1_e8_ctrl.txt = R1 with the ten
`T 0 0 0 | 0 | 0 0 0` no-op lines removed (S1 base + the one
`T 0 0 0 | 0 | 2 0 0` change only).
Binary: /tmp only, not committed.

## Frozen kill bars

- K-E8-1 (X-E7-1 closed): On J1, the raw output contains
  `TRANS a0 temp[0->1:1,1->2:1,2->2:2*] pressure[] lamp[]`,
  and a TRANSITION-EVIDENCE line for the ranked pick
  requiring temp==2 contains
  `0: from {1:1,2:2*(raw:5..5)} (3/4)`. The artifactual
  bucket is flagged and its raw from-values are shown.

- K-E8-2 (X-E7-2 closed): On R1, a TRANSITION-EVIDENCE line
  for the ranked pick requiring temp==2 contains
  `0: from {0:1,1:1} (2/3) from-att {0:12,1:1,2:1}`. On the
  control fixture r1_e8_ctrl.txt, the corresponding line
  contains `from-att {0:2,1:1,2:1}`. The from-0 attempt
  entry differs by exactly 10: the ten hidden no-ops are
  now visible in the attempt denominator, and the two
  materially different realities no longer render
  identically.

- K-E8-3 (X-E7-3 closed): On C1, the raw output contains
  `TRANS a0 temp[0->1:1,1->2:1,2->2:1*] pressure[] lamp[]`,
  and a TRANSITION-EVIDENCE line for the ranked pick
  requiring temp==2 contains `2:1*(raw:5..5)`. The genuine
  raw change is explicitly flagged as a clamp-rendered
  self-loop.

- K-E8-4 (no regression): (a) K-E7-1 frozen substrings
  present on G1 (`0: from {1:3} (3/4)`,
  `1: from {0:2} (2/2)`); (b) K-E7-2 frozen substrings
  present on H1 (`0: from {1:1} (1/11)`,
  `1: from {0:1} (1/1)`); (c) K-E7-5 frozen row present on
  F1 (`TRANS a0 temp[0->1:1,1->2:1] pressure[] lamp[1->0:1]`);
  (d) K-E6-1, K-E6-2, K-E6-4 frozen checks pass
  (ACHIEVABILITY/CHANGE-TO tables and CHANGE-EVIDENCE lines
  byte-identical to exp7); (e) diff of exp8 vs exp7 raw
  outputs on S1,S2,S0,A1,F1,G1,H1 shows no changed lines
  except the frozen additions: `*` on o==x cells,
  `(raw:lo..hi)` tags, ` from-att {0:t0,1:t1,2:t2}`
  segments, and the three new legend sentences.

- K-E8-5 (determinism): 3 consecutive runs per fixture
  (S1,S2,S0,A1,F1,G1,H1,J1,R1,C1,r1_e8_ctrl) are
  byte-identical; md5 recorded in the result doc.

## Honest limits (frozen)

- The H-EXP7 honest limits carry over unchanged.
- Raw from-values are reported as a per-bucket observed
  range (raw:lo..hi), not per-episode; two buckets with the
  same range may hide different distributions, and the tag
  appears only when at least one episode's raw from-value
  differs from the bucket label.
- from-att counts EP_ACT episodes per clamped from-state
  per variable; it does not condition on other variables or
  episode order, and it is not a success probability under
  intervention.
- The `*` self-loop flag follows deductively from the
  change predicate (every trans cell had raw from != raw
  to); it marks clamp-rendered self-loops, not a separate
  empirical discovery.
- Negative raw values are not expressible in fixtures
  (parse_int reads digits only); the symmetric bucket-0
  artifact path could not be probed, same as the red team
  limitation.
- Classification target: bounded L2 discriminating-state
  selection with honest transition-level reporting.
  Not L3: no new representation is invented; the vocabulary
  (actions, variables, values) is given by the episode
  format.
