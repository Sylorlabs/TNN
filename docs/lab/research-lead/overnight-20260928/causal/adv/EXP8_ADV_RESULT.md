# H-EXP8 Red Team Report: X-E8-1..X-E8-4

**Date:** 2026-09-29
**Prereg:** causal/adv/PREREG_EXP8_ADV.md (commit f5b3f3a79,
frozen alone BEFORE any attack fixture, build, or execution;
strict ancestor of this report commit)
**Target:** committed exp_invent8.zag (byte-identical copy
verified via cmp before building; built with znc
2026.07.0-dev (edition 2026) in /tmp only, never committed)
**Purity:** Pure Zag. No Python anywhere (fixtures via shell
heredocs, comparison via cmp/diff/grep/md5sum).
**No em dashes in loop documentation.**

## Verdict: H-EXP8 DOWNGRADED (not killed)

One attack succeeds. H-EXP8's 5/5 frozen bars still pass
(X-E8-4 confirms byte-identical regression), the `*` flag
is deductively sound (X-E8-3), and the raw-range
distribution limit is as documented (X-E8-1). But X-E8-2
succeeds: the from-att "attempt denominator" silently
excludes episodes superseded by the inherited law-change
revision system, and the frozen documentation affirmatively
misdescribes the counts. This reintroduces the X-E7-2
hazard class (invisible attempts) through a path the repair
does not disclose. The X-E7-2 closure is incomplete.

## Methodology

1. Read PREREG_EXP8.md and EXP8_RESULT.md.
2. Read exp_invent8.zag: compute_transitions (change
   predicate, att/rmin/rmax/rdiff), emit_trans_cells and
   emit_transition_evidence (`*` flag, raw tag, from-att),
   episode parsing (all `T` episodes become EP_ACT).
3. Wrote PREREG_EXP8_ADV.md with frozen attacks and kill
   criteria; committed alone as f5b3f3a79.
4. Built the committed mechanism in /tmp; verified
   byte-identical to the repo copy via cmp.
5. Created 9 S1-based attack fixtures (shell heredocs).
6. Ran each fixture; compared outputs; investigated every
   anomaly in source.
7. Rebuilt and ran all 11 frozen fixtures 3x for X-E8-4.

## Attack X-E8-1 (raw range): FAILS as a kill; boundary confirmed; new limit found

### X-E8-1a: distribution hiding (documented limit confirmed)

- D1 = S1 + 9x `T 5 0 0 | 0 | 2 0 0` (raw 5->2,
  artifactual) + 1x `T 2 0 0 | 0 | 3 0 0` (raw 2->3,
  genuine). 90% artifactual.
- D2 = S1 + 1x `T 5 0 0 | 0 | 2 0 0` + 9x
  `T 2 0 0 | 0 | 3 0 0`. 10% artifactual.
- Both render the from-bucket identically:
  `2:10*(raw:2..5)`.
- This is EXACTLY the documented honest limit ("two
  buckets with the same range may hide different
  distributions"). The planner sees the range 2..5 and
  knows at least one raw-2 exemplar exists (rmin=2), but
  cannot recover the 9:1 vs 1:9 proportion.
- Attack FAILS as a kill. Recorded as CONFIRMED BOUNDARY.

### X-E8-1b: raw to-value invisibility (new honest limit)

- D3 = S1 + `T 5 0 0 | 0 | 9 0 0` (raw 5->9).
- C1 (frozen) = S1 + `T 5 0 0 | 0 | 2 0 0` (raw 5->2).
- Both render cell (0,temp,2,2) identically:
  `TRANS a0 temp[...2->2:1*]` and bucket `2:1*(raw:5..5)`.
- rmin/rmax/rdiff record raw FROM-values only. The raw
  OUTCOME (9 vs 2) is recorded nowhere in any table,
  tag, or legend.
- This does not falsify the repair's from-value claim.
  Recorded as NEW HONEST LIMIT (boundary), not a kill:
  the repair shows raw from-values but not raw to-values.

## Attack X-E8-2 (from-att): SUCCEEDS -> DOWNGRADED

### The finding

D1 and D2 (above) were designed to test the raw range,
but their from-att lines differ:

- D1: `0: from {1:1,2:10*(raw:2..5)} (11/12) from-att {0:1,1:1,2:11}`
- D2: `0: from {1:1,2:10*(raw:2..5)} (11/11) from-att {0:1,1:1,2:10}`

Both fixtures contain ELEVEN action-0 temp-from-2
episodes (verified by grep). D2's from-att shows 10.

Root cause, verified in source and output: D2's nine
`T 2 0 0 | 0 | 3 0 0` episodes triggered the inherited
law-change revision system:

`CONTEST action 0 state (2 0 0) outcomes (2 0 0)@seq3 vs (3 0 0)@seq13 opened at seq 13 (LAW-CHANGE suspected, WITHHOLD)`

`RESOLVE action 0 state (2 0 0) winner outcome 1 (3 0 0) support 2 at seq 14; loser SUPERSEDED (valid only before seq 3)`

The resolver (contest_feed, exp_invent8.zag line 648)
sets the losing episodes' status via
`ep_st_set(W,f,EP_SUP())`. Every H-EXP8 count
(compute_achievability, compute_change_to,
compute_transitions) gates on
`if(ep_st(W,e)==EP_ACT())`, so the superseded S1 base
episode (seq3, `T 2 0 0 | 0 | 2 0 0`) is SILENTLY
EXCLUDED from achv, chgto, trans, att, and rmin/rmax/
rdiff. D1's single conflicting episode opened a CONTEST
at seq21 but never resolved (insufficient support), so
all 11 episodes counted.

### Why this is a downgrade, not a documentation nit

1. The frozen H-EXP8 legend states: "from-att
   {0:t0,1:t1,2:t2} counts EP_ACT episodes of that action
   with clamped from-value 0/1/2 for the variable: the
   attempt denominator per from-state." It does not
   disclose that episodes are mutated from EP_ACT to
   EP_SUP by the revision system and excluded. A planner
   reading "10 attempts" does not know an 11th attempt
   existed and was superseded.

2. This is the X-E7-2 hazard class. X-E7-2 was "ten
   no-op failures can be invisible." H-EXP8 claimed "the
   attempt-conditioned rate is visible." But attempts
   that lose a law-change contest are invisible in
   from-att, in the (m/n) denominator (achv), and in the
   from-buckets (trans). The closure is incomplete: the
   repair makes attempts visible UNLESS the revision
   system superseded them, which is undisclosed.

3. The honest limit "from-att ... does not condition on
   other variables or episode order" is itself
   inaccurate. F1 vs F2 (X-E8-2b, same episode multiset,
   different order) render very differently:
   F1: `from-att {0:12,...}`, TRANS `0->1:1,0->2:1`;
   F2: `from-att {0:11,...}`, TRANS `0->2:1,1->2:1`,
   with different CONTEST/RESOLVE/SPLIT lines. The
   counts ARE order-sensitive via the revision system's
   supersession. The documentation claims otherwise.

### Scope of the downgrade

- The 5/5 frozen H-EXP8 bars still pass (X-E8-4). The
  R1/control K-E8-2 demonstration is unaffected (R1 does
  not trigger supersession).
- The annotations remain useful: from-att, raw tags, and
  `*` flags are correct for the non-superseded episode
  set, and CONTEST/RESOLVE lines do appear in the full
  output for a careful reader.
- The revision system's exclusion is arguably correct
  behavior (stale-law data); the defect is that H-EXP8's
  frozen documentation misdescribes the denominator and
  omits the interaction entirely.
- Verdict: DOWNGRADED (documentation-inaccurate,
  incomplete X-E7-2 closure), NOT KILLED. The mechanism
  does not fabricate; it under-reports without
  disclosure.

## Attack X-E8-3 (deductive `*` flag): FAILS (defense holds)

### X-E8-3a: flag audit

- G1 = S1 + six genuine raw changes with clamped
  (o=2,x=2): raw 2->3, 2->5, 2->9, 5->2, 5->6, 3->4.
- Result: `TRANS a0 temp[0->1:1,1->2:1,2->2:6*]`.
  All six are genuine raw changes (raw ns != raw os,
  verified per episode). Every `*` sits on a genuine
  change. No o==x cell lacks `*`.
- The two CONTESTs in G1 opened but never resolved; no
  episodes excluded; count is exactly 6.
- From-bucket: `2:6*(raw:2..5)` (rmin=2, rmax=5 over raw
  from-values 2,2,2,5,5,3; the raw 9 was a to-value and
  is correctly absent, consistent with X-E8-1b).

### X-E8-3b: non-change exclusion

- H1 = S1 + `T 2 0 0 | 0 | 2 0 0` (raw 2->2) +
  `T 5 0 0 | 0 | 5 0 0` (raw 5->5).
- Result: `TRANS a0 temp[0->1:1,1->2:1]`. NO `2->2`
  cell. Non-change episodes never create trans cells.
- The single trans_add call site is inside the
  `if(ns!=os)` raw-change branch (line 1252). Verified.

The deductive claim holds: o==x in a trans cell implies
raw ns != raw os (change predicate) and
clamp(os)==clamp(ns), i.e. a genuine raw change rendered
self-loop by clamping. Attack FAILS.

## Attack X-E8-4 (regression): PASSES

Rebuilt the committed exp_invent8.zag unmodified; ran
all 11 frozen fixtures (S1,S2,S0,A1,F1,G1,H1,J1,R1,C1,
r1_e8_ctrl) 3x each. All 33 runs byte-identical per
fixture (3/3 deterministic) and byte-identical to the
committed evidence files
(causal/adv/evidence/exp8_*.txt). No silent behavior
change. The 5/5 H-EXP8 bars are intact as executed.

## Causal interpretation

H-EXP8's annotations are honest about the episode set
they actually summarize, but the frozen documentation
describes a larger set ("EP_ACT episodes", "does not
condition on episode order") than the implementation
delivers. The gap is the inherited law-change revision
system (CONTEST/RESOLVE/EP_SUP), which H-EXP8's prereg
("Nothing else changes") and honest limits never
mention. A planner that reads only the annotated lines
as documented will undercount attempts whenever a
law-change contest resolved against some episodes, and
will not know the counts are order-sensitive. The
CONTEST/RESOLVE trace lines mitigate this for a reader
of the full output, but the annotated lines themselves
carry no marker of exclusion.

## Boundaries and honest limits (adversary-confirmed)

- Raw range hides distributions (X-E8-1a): confirmed as
  documented; D1/D2 render `2:10*(raw:2..5)` identically
  at 90% vs 10% artifactual.
- Raw to-values are never recorded (X-E8-1b): new
  boundary; raw 5->9 and raw 5->2 render identically.
- from-att excludes superseded episodes (X-E8-2):
  undocumented; downgrade driver.
- from-att is order-sensitive via the revision system
  (X-E8-2b): contradicts the frozen honest limit.
- `*` flag deductive (X-E8-3): holds; audited over six
  raw profiles plus non-change exclusion.
- Regression (X-E8-4): 11/11 fixtures byte-identical,
  3/3 deterministic.

## Failures and negative evidence

- X-E8-2a (raw attempt-profile invisibility) and X-E8-2b
  (order invisibility) as preregistered did not isolate
  their intended variables: the S1 base is "hot" and
  both fixture pairs triggered the revision system
  (CONTEST/RESOLVE/SPLIT), so the outputs differed for
  reasons outside the preregistered comparison. The
  contamination itself produced the X-E8-2 findings
  above; the original identical-rendering hypotheses for
  2a/2b are recorded as NOT TESTED (void), not as
  passed.
- No implementation or fixture bug was found in the
  H-EXP8 additions themselves (att/rmin/rmax/rdiff
  logic, `*` emission, raw-tag gating).

## Governance disclosures

- Prereg PREREG_EXP8_ADV.md committed alone as f5b3f3a79
  before any attack fixture, build, or execution.
  Ordering verified: prereg is a strict ancestor of this
  report commit.
- Attack fixtures were generated with shell heredocs
  from the committed S1 (causal/cum_B.txt); the
  "# ADVERSARY ADDITIONS" headers document provenance.
- The target binary was built from a cmp-verified
  byte-identical copy of the committed exp_invent8.zag,
  in /tmp only, never committed.
- Pure Zag throughout: no Python at any stage.
- Only adversary-owned paths staged: PREREG_EXP8_ADV.md
  (already committed), d1/d2/d3/e1/e2/f1/f2/g1/h1
  _e8_adv.txt fixtures, EXP8_ADV_RESULT.md (this file),
  evidence/exp8_adv_*.txt raw outputs.
- X-E8-2a/2b as preregistered are VOID (not tested due
  to revision-system contamination); the findings they
  produced are reported above instead.

## Commit lineage (branch tnn-native-lab, local only)

- f5b3f3a79: Prereg: H-EXP8 red team (X-E8-1..X-E8-4)
  FROZEN (alone; before any attack work)
- this commit: attack fixtures (9), EXP8_ADV_RESULT.md
  (this file), evidence/exp8_adv_*.txt
- Ordering: prereg is a strict ancestor of this commit
  (verified via merge-base --is-ancestor before
  committing).
