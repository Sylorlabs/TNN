# H-EXP8 Result: Repair of the H-EXP7 Red-Team Downgrade

**Date:** 2026-09-29
**Prereg:** causal/adv/PREREG_EXP8.md (commit 98f650b2c, frozen
alone BEFORE any implementation of exp_invent8.zag; verified
strict ancestor of the implementation and result commits)
**Source:** causal/adv/exp_invent8.zag (built by copying
exp_invent7.zag verbatim, cmp-verified, then applying exactly
the six frozen additions)
**Control fixture:** causal/adv/r1_e8_ctrl.txt (R1 with the
ten `T 0 0 0 | 0 | 0 0 0` no-op lines removed)
**Target binary:** built from committed exp_invent8.zag with
znc 2026.07.0-dev (edition 2026), in /tmp only, not committed
**Raw evidence:** causal/adv/evidence/exp8_{j1,r1,c1,ctrl,s1,
s2,s0,a1,f1,g1,h1}_raw.txt; 3/3 byte-identical per fixture
**Purity:** Pure Zag. No Python anywhere (no generators,
verifiers, analysis, or scratch). No em dashes in loop
documentation.

## Verdict: H-EXP8 SURVIVES 5/5 (bounded L2)

All five frozen kill bars pass. The three H-EXP7 red-team
downgrades are closed by the repair:

1. **X-E7-1 closed (K-E8-1):** the clamp-artifactual
   from-bucket is flagged and its raw from-values are shown.
2. **X-E7-2 closed (K-E8-2):** the attempt-conditioned rate
   is visible; the two materially different realities no
   longer render identically (the from-0 attempt entry
   differs by exactly 10 between R1 and the no-no-op
   control).
3. **X-E7-3 closed (K-E8-3):** the clamp-rendered self-loop
   is explicitly flagged in both the TRANSITION TABLE and
   the from-bucket.
4. **No regression (K-E8-4):** all K-E7-1..K-E7-5 frozen
   checks still pass; diff of exp8 vs exp7 outputs shows
   ONLY the frozen additions.
5. **Determinism (K-E8-5):** 3/3 byte-identical per fixture
   on all 11 fixtures.

Classification remains bounded L2. H-EXP8 does not claim L3:
no new representation is invented; the vocabulary (actions,
variables, values) is given by the episode format.

## Methodology

1. Read EXP7_ADV_RESULT.md and PREREG_EXP7.md.
2. Built the committed exp_invent7.zag in /tmp and ran it on
   J1/R1/C1 to ground the exact current lines (analysis of
   existing code; no implementation before prereg).
3. Hand-verified the attempt counts from the fixture text
   (R1: S1 base contributes 1 action-0 temp-from-0 episode;
   R1 adds 1 change + 10 no-ops = 12 from-0 attempts;
   control = 2).
4. Wrote PREREG_EXP8.md with frozen kill bars and committed
   it alone as 98f650b2c before touching any implementation.
5. Copied exp_invent7.zag to exp_invent8.zag (cmp-verified
   byte-identical), then applied exactly the six frozen
   additions:
   - att (36 i32 cells) + rmin/rmax/rdiff (108 i32 cells
     each) helpers and allocations; rmin initialized to
     999999999, rmax to -999999999 (rdiff is zeroed by
     z_alloc).
   - compute_transitions extended: att_add for every EP_ACT
     episode per (action,variable,clamped from); raw
     from-value min/max/diff recorded per change cell.
   - emit_trans_cells: `*` appended to o==x cells.
   - emit_transition_evidence: `*` on o==x buckets,
     `(raw:lo..hi)` tag when rdiff > 0, and
     ` from-att {0:t0,1:t1,2:t2}` after each per-action
     (m/n) rate.
   - Three frozen legend sentences appended after the
     byte-identical H-EXP5/H-EXP6/H-EXP7 legend text.
6. Built with znc 2026.07.0-dev (edition 2026) in /tmp.
7. Ran all fixtures 3x; checked every frozen bar by grep;
   verified the exp7-vs-exp8 diff contains only the frozen
   additions (programmatic strip-and-diff check).

## Frozen kill bars and raw results

### K-E8-1 (X-E7-1 closed): PASS

On J1, the raw output contains:

`TRANS a0 temp[0->1:1,1->2:1,2->2:2*] pressure[] lamp[]`

and the ranked pick requiring temp==2 contains:

`    TRANSITION-EVIDENCE: temp==2 transitions: 0: from {1:1,2:2*(raw:5..5)} (3/4) from-att {0:1,1:1,2:3}; pressure==0 transitions: 3: from {1:1} (1/1) from-att {0:0,1:1,2:0}; lamp==0 transitions: none`

The artifactual bucket is flagged (`*`) and its raw
from-values are shown (`(raw:5..5)`): the planner now sees
that the two from-2 temp changes were raw 5->2, with zero
raw from-2 exemplar. The from-att entry shows 3 from-2
attempts (1 genuine S1 no-change episode + 2 artifactual
changes).

### K-E8-2 (X-E7-2 closed): PASS

On R1, the ranked pick requiring temp==2 contains:

`    TRANSITION-EVIDENCE: temp==2 transitions: 0: from {0:1,1:1} (2/3) from-att {0:12,1:1,2:1}; pressure==0 transitions: 3: from {1:1} (1/1) from-att {0:0,1:1,2:0}; lamp==0 transitions: none`

On the control fixture r1_e8_ctrl.txt (the ten no-op lines
removed), the corresponding line contains:

`    TRANSITION-EVIDENCE: temp==2 transitions: 0: from {0:1,1:1} (2/3) from-att {0:2,1:1,2:1}; ...`

The from-0 attempt entry is 12 on R1 versus 2 on the
control: exactly the 10 hidden no-ops. The two materially
different realities (1 change in 12 from-0 attempts vs 1 in
2) no longer render identically. The outcome-conditioned
rate `(2/3)` is unchanged and still reported; the
attempt-conditioned denominator is now alongside it.

### K-E8-3 (X-E7-3 closed): PASS

On C1, the raw output contains:

`TRANS a0 temp[0->1:1,1->2:1,2->2:1*] pressure[] lamp[]`

and the ranked pick requiring temp==2 contains:

`    TRANSITION-EVIDENCE: temp==2 transitions: 0: from {1:1,2:1*(raw:5..5)} (2/3) from-att {0:1,1:1,2:2}; ...`

The genuine raw 5->2 change is explicitly flagged as a
clamp-rendered self-loop (`2->2:1*` in the table,
`2:1*(raw:5..5)` in the from-list). The flag is deductive:
every trans cell required raw ns != raw os, so an o==x cell
is always a genuine raw change rendered self-loop by
clamping.

### K-E8-4 (no regression): PASS

- (a) G1 contains `0: from {1:3} (3/4)` (2 occurrences:
  ranked pick and top pick) and `1: from {0:2} (2/2)`.
- (b) H1 contains `0: from {1:1} (1/11)` and
  `1: from {0:1} (1/1)`.
- (c) F1 contains
  `TRANS a0 temp[0->1:1,1->2:1] pressure[] lamp[1->0:1]`
  byte-identically (no clamping or self-loops in F1).
- (d) K-E6-1 passes on F1 (`lamp==1 changed-to by
  action(s) {} (0 eps)` and
  `carryover-only: action(s) {2} (1 eps)`); K-E6-2 passes
  on S1 (`temp==2 changed-to by action(s) {0} (1 eps)` and
  `carryover-only: action(s) {2} (2 eps)`).
- (e) Diff of exp8 vs exp7 raw outputs on
  S1,S2,S0,A1,F1,G1,H1: after stripping
  ` from-att {0:t0,1:t1,2:t2}` segments and the three new
  legend sentences, the diff is EMPTY on all 7 fixtures.
  No `*` and no `(raw:` tags appear in any data line of
  the 7 fixtures (their raw values are all within 0..2 and
  no o==x cells exist). The only output changes are the
  frozen additions.

### K-E8-5 (determinism): PASS

3/3 byte-identical per fixture. md5 of the frozen first
runs:

- S1 b85b6c7d7af8dcd38895f410e28d6fa2
- S2 132f2c88b13154dad8f98ca2d5973aaa
- S0 b5aecda78fc55fd214ea707ef93f4290
- A1 42bd21af1338e5e6cab56a68431acaa0
- F1 0638b5d1af979db341422cecd495676c
- G1 3e3a0e7b6cde30e6a4eded5a035d7c12
- H1 31bd91f3afa42b43b5c5d569bfdb2dd9
- J1 825d7a223b62b9b08874f2f98276b91c
- R1 42e934cd7f992173f85c3a65da000a2b
- C1 26611cb936cb56c2eb93697b7db34303
- control 2fcbad97f8de25e99d9677309c5e5fd1

## Causal interpretation

The repair closes exactly the three rendering hazards the
red team found, and nothing more. The mechanism still does
not invent a representation: raw from-values are reported
as an observed per-bucket range, not as a new state
vocabulary; the attempt count is an observed denominator,
not an intervention model; the self-loop flag is a
deductive consequence of the change predicate, not an
empirical discovery. The downgrade is repaired in the
narrow sense: a planner that reads the annotations as
documented can no longer mistake a clamp artifact for a
from-state observation, mistake an outcome-conditioned
rate for an attempt-conditioned one, or mistake a
clamp-rendered self-loop for a maintained state. A planner
that ignores the annotations is exactly as exposed as
under H-EXP7.

## Boundaries and honest limits

- The frozen honest limits from PREREG_EXP8 apply: the raw
  tag is a per-bucket observed range, not per-episode and
  not a distribution; from-att does not condition on other
  variables or episode order and is not a success
  probability under intervention; the `*` flag is
  deductive.
- Negative raw values remain untestable in fixtures
  (parse_int reads digits only); the symmetric bucket-0
  artifact path is covered by the legend but not probed.
- from-att counts EP_ACT episodes per clamped from-state;
  episodes of other actions or non-EP_ACT episodes are not
  attempts of this action.
- Classification: bounded L2 discriminating-state
  selection with honest transition-level reporting.
  Not L3.

## Failures and negative evidence

- None during implementation: the first build succeeded
  and all five bars passed on the first full run. No
  amendments were needed; the prereg's hand-verified
  strings matched the implementation output exactly on
  the first execution (J1 row, J1/R1/C1 pick segments,
  control delta of exactly 10).

## Governance disclosures

- Prereg PREREG_EXP8.md committed alone as 98f650b2c
  before the verbatim copy of exp_invent7.zag was made and
  before any implementation edit. Ordering verified:
  prereg is a strict ancestor of the implementation and
  result commits.
- exp_invent8.zag was produced by copying exp_invent7.zag
  verbatim (cmp-verified) and applying exactly the six
  frozen additions; no other line of the inherited
  mechanism was touched.
- Pure Zag throughout: fixtures are hand-written text,
  the binary was compiled with znc, outputs were compared
  with cmp/md5sum/grep/sed/diff. No Python at any stage.
- The control fixture r1_e8_ctrl.txt was derived from R1
  by deleting exactly the ten no-op lines; the deletion
  is documented in the fixture header.
- Only owned files staged: PREREG_EXP8.md (already
  committed), exp_invent8.zag, r1_e8_ctrl.txt,
  EXP8_RESULT.md (this file), and
  evidence/exp8_*.txt. Concurrent workers' files were not
  touched.
- The pre-prereg exp7 runs on J1/R1/C1 in /tmp were
  analysis of the existing committed mechanism only; no
  implementation existed at that point.

## Commit lineage (branch tnn-native-lab, local only)

- 98f650b2c: PREREG H-EXP8 FROZEN (alone; before any
  implementation)
- this commit: exp_invent8.zag, r1_e8_ctrl.txt,
  EXP8_RESULT.md (this file),
  evidence/exp8_{j1,r1,c1,ctrl,s1,s2,s0,a1,f1,g1,h1}_raw.txt
- Ordering: prereg is a strict ancestor of this commit
  (verified via merge-base --is-ancestor before
  committing).
