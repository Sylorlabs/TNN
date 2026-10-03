# SPEC-COMMIT-L: PREREG

**Lane:** docs/lab/research-lead/overnight-20260928/spec_commit_l/
**Date:** 2026-10-03
**Status:** Non-ledger (claim minting paused). Local commits only, never pushed.
**Parent:** SPEC-L-DISCIPLINE (BUILD-PASS K1-K9), which builds on
SPEC-FLIP-THRESHOLD (BUILD-PASS K1-K10).

## Parent result this builds on

SPEC-L-DISCIPLINE showed L is dead weight in the flip discipline:
both flip directions now run L-free (lazy bar `2*qhi < dlo` by fix2;
eager direction `phid > phin` by noeg, byte-identical to fix2 on all
cells). L survives in exactly two places: J accounting (by
definitional right: L IS the caller-stated refusal cost ratio) and
the untouched pre-shift commit rule, where it IS observably
load-bearing: on R = 120, cm = 0 / tc = 128 at L = 1/3 vs
cm = 2 / tc = 112 at L = 7/10, identical across adapt/fix2/noeg.
This lane asks the parent's frozen next question: is the commit
rule's L-dependence load-bearing, or can the commit rule also run
L-free? Quirk implications are examined explicitly.

## Where L enters the commit rule (frozen mechanism analysis)

The pre-shift commit rule is the `com == 0` branch of sld_checkpoint
(checkpoints e in {32,48,64,80,96,112,128}), inherited unchanged
through every SPEC lane:

```
dec = nr_decide(dh,qh,dlo,dhi,qlo,qhi,L)   // the FULL margin test
dec == 2 -> eager commit (cm = 2, sel = 1, specialize, restamp)
dec == 1 -> lazy commit  (cm = 1, sel = 0)
e == 128 undecided -> com = 2, cm = 0 (budget default, terminal)
```

nr_decide: eager-decisive iff `L*phid > phin`
(phid = max(qlo,1), phin = max(0,dhi-qlo)); lazy-decisive iff
`L*plod < plon` (plod = max(qhi,1), plon = max(0,dlo-qhi)).
The pol-4 minimum-data guard (SPEC-COLD-START) suppresses dec == 2
while (dh,ed) = (0,0) via the blk flag; pol 2/5/6/7/10 keep the
inherited zero-data eager commit (the quirk).

The quirk (SPEC-COLD-START, confirmed): with (dh,ed) = (0,0) the
price interval degenerates to {0}: dhi = 0 so phin = 0, phid >= 1,
so `L*phid > 0` fires for EVERY L >= 1: a zero-data eager commit at
e = 32 (tc = 32, cm = 2, Dc = 0, dh = dlo = dhi = phin = 0,
phid = 1). Dc = 0 at commit implies (dh,ed) = (0,0): no drift
arrived, so the drift EWMA and its deviation EWMA are both zero.
The quirk is therefore L-INVARIANT for all L >= 1: it fires under
L := 1 exactly as under L.

The commit rule's OBSERVED L-dependence is elsewhere: on R = 120
(D32 = 1, data present) the eager direction `L*phid > phin` fires
pre-shift at L = 7/10 (tc = 112, cm = 2) but never at L = 1/3
(cm = 0, tc = 128). The flip rule then rescues the L = 7/10
episodes to lazy at tf1 = 160 (fdir = -1): the L-driven eager
commit was wrong-direction pre-shift.

## The commit-rule question (frozen)

Q1. Is the commit rule's L-dependence load-bearing? I.e., does an
    L-free commit rule behave differently from the parent's
    L-bearing commit rule?
Q2. If it differs: was the L-driven behavior economically useful
    (under the caller-stated J = rb + rf*L), or dead weight like
    the flip discipline's L?
Q3. Quirk interaction: the quirk fires through the commit rule's
    eager direction and is L-invariant. Does an L-free commit rule
    preserve it, and what does killing it cost/save under the
    L-free (noeg) flip discipline?
Q4. Under an L-free commit, does the eager direction do any
    data-driven work at all, or is it purely the quirk channel?

## Design (frozen)

One binary, pure Zag, safebin-built. 88 episodes: 4 inherited regime
cells (R = 21/60/82/120, seeds and arrivals byte-identical to the
parent) x 22 arms: fixed lazy, fixed eager (L = -1), and pol in
{7,10,13,14,15} x L in {1,3,7,10}.

- pol 7 "fix2": parent control (L-bearing flip bar, L-bearing
  commit). Replication anchor.
- pol 10 "noeg": parent control (L-free flip discipline, L-bearing
  commit). Replication anchor and the behavioral baseline the new
  arms are compared against.
- pol 13 "coml1": noeg flip discipline + L-FREE commit
  (scl_commit_decide: nr_decide with L := 1, both directions).
  The quirk is preserved by construction.
- pol 14 "comlg": noeg flip + L-free commit + minimum-data guard
  (dec == 2 suppressed while (dh,ed) = (0,0), via the blk flag
  exactly as pol 4). Quirk blocked; data-driven eager kept.
- pol 15 "comnoeg": noeg flip + L-free commit, eager direction
  DROPPED (lazy-decisive `plod < plon` only; dec == 2 impossible).
  Quirk channel closed by construction.

The delta on the parent lane's ld_spec.zag is minimal and marked
[CL-DELTA]: (1) new fn scl_commit_decide (dispatches the commit
decision; every pol outside {13,14,15} keeps the parent's
nr_decide(...,L) call verbatim); (2) the com == 0 branch calls it;
(3) blk flag also set for pol 14; (4) nr_decide_ft hoists lzmult = 1
and egl = 1 for pol 13/14/15 (the noeg flip discipline); (5)
nr_polname names; (6) apol/adap wiring for pol 13/14/15. The
parent's ld_spec.zag / ld_main.zag are superseded by copy-plus-delta
(cl_spec.zag), never edited. pol 3 (recheck) stays dormant.

Decomposition logic (mirrors the parent's noeg-vs-fix2 isolation):
- pol 10 vs pol 13 isolates L in the commit rule (Q1).
- pol 13 vs pol 14 isolates the quirk under L-free commit (Q3).
- pol 14 vs pol 15 isolates the data-driven eager direction under
  L-free commit (Q4).
- J / J' on R = 120 at L = 7/10 answers Q2.

## Frozen predictions (not bars; recorded before running)

P1. coml1 preserves the quirk exactly: on R = 21/60/82 at every L,
    tc = 32, cm = 2, Dc = 0 with the degenerate snapshot, because
    with (dh,ed) = (0,0), nr_decide(...,1) = nr_decide(...,L) = 2
    for every L >= 1.
P2. coml1 on R = 120 at every L is dynamically identical to the
    parent's frozen noeg L = 1 line on R = 120 (commit rule
    nr_decide(...,1) both; flip rule egl = 1 both; arrivals
    identical): cm = 0, tc = 128, flips = 0, rb = 11, rf = 11.
    Hence removing L changes L = 7/10 behavior there
    (cm = 2/tc = 112 -> cm = 0/tc = 128): the commit rule's L is
    observably load-bearing (Q1 = yes).
P3. comlg never binds its guard on R = 120 (dec == 2 never fires
    pre-shift under L := 1 there, proved by the parent's noeg L = 1
    cm = 0): comlg == coml1 there.
P4. comnoeg never commits pre-shift on R = 120 (its lazy test
    `plod < plon` is the L := 1 lazy test, which never fired on the
    parent's noeg L = 1 line): comnoeg == coml1 there. The commit
    rule's eager direction does no data-driven work on R = 120
    under L-free commit (Q4 answered there).
P5. Economics on R = 120 (from P2 + frozen parent data):
    J_coml1(120,L) = 11 + 11*L (22/44/88/121) vs J_noeg(120,7) = 78
    and J_noeg(120,10) = 93: the L-driven eager commit was
    J-beneficial at high L (Q2 = yes, under the caller-stated cost
    ratio). J'_coml1(120,L) = 22 flat vs J'_noeg(120,7/10) = 48:
    J-beneficial but J'-harmful; the tension is reported, not
    resolved here.
P6. Quirk scoreboard (findings): J_coml1 vs J_comlg vs J_comnoeg on
    R = 21/60/82 per L under the L-free flip discipline; not
    predictable in advance (depends on post-guard data arrivals).

## Kill bars (frozen)

- **K1.** Prereg commit strictly precedes the implementation commit
  (verified git log order on this lane directory). No implementation
  file (cl_spec.zag, cl_main.zag, cl_build.sh, cl_posthoc.sh,
  cl_full.zag, cl_bin, cl_run*.txt/err) may exist in the prereg commit.
- **K2.** Safebin mandatory: `which python3` and `which python` return
  nothing; pinned znc sha256
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
  (verified in-script).
- **K3.** znc builds the assembly clean (no `: error`, exit 0);
  cl_bin exits 0 on all 3 runs; stderr empty on all 3 runs; stdout 3/3
  byte-identical (cmp + sha256). Exactly 88 CELL lines per run
  (4 cells x 22 arms).
- **K4 (anchoring / replication).** (a) Per cell R in {21,60,82,120}:
  all 22 arms see identical (D, Q); lazy lines: answered = Q,
  kb = 2Q, refusals = rebuilds, rebuilds <= min(D, Q); eager lines:
  rebuilds = D, answered = Q, refusals = 0, kb = 2Q. (b) Arrival
  splits show the shift (lazy arm): R = 60 and R = 120: Dpost = 128
  exactly, Qpost < 32, Dpre < 32, Qpre < 32; R = 82: Qpost = 128
  exactly, Dpost < 32, Dpre < 32, Qpre < 32; R = 21: D < 48, Q < 48.
  (c) Structural accounting on all 80 adaptive lines (per cell:
  4 fix2 + 4 noeg + 4 coml1 + 4 comlg + 4 comnoeg): D = Dpre + Dpost,
  Q = Qpre + Qpost, answered = Q, kb = 2Q, rebuilds = od + rs,
  refusals = od; (pflips = 0) iff (tf1 = 0) iff (fdir = 0);
  pflips > 0 implies 128 < tf1 <= 256; flips >= pflips; lines with
  flips = 0 and cm in {0,1}: od/rf/rs field-equal to the lazy twin;
  lines with flips = 0 and cm = 2: rs = 1 + (D - Dc) and
  od <= min(Dc, Qc); lc = 0 everywhere (pol 3 dormant in this lane).
  (d) Exact replication: on all four cells, fix2 and noeg L in
  {1,3,7,10} CELL lines (32 lines) are byte-identical to the
  parent's frozen ld_run1.txt (sha256 36d63552...): the delta is
  surgical.
- **K5 (quirk: preserved / killed / dominated).** (a) Quirk preserved
  under L-free commit: on R in {21,60,82}, coml1 at L in {1,3,7,10}:
  tc = 32, cm = 2, Dc = 0, dh = dlo = dhi = phin = 0, phid = 1.
  (b) Quirk killed: no comlg line and no comnoeg line on
  R in {21,60,82} has cm = 2 AND Dc = 0; no comnoeg line has cm = 2
  at all pre-shift. (c) Quirk-dominated identity: on R in {21,60,82},
  L in {1,3,7,10}: the coml1 CELL line equals the noeg CELL line
  modulo the P= field (L-free commit changes nothing where the
  quirk dominates).
- **K6 (commit-rule L-dependence: the core question).** On R = 120,
  L in {1,3,7,10}: (a) the coml1 CELL line equals the parent's
  frozen noeg L = 1 R = 120 line modulo the P= and L= fields:
  cm = 0, tc = 128, flips = 0, rebuilds = 11, refusals = 11.
  (b) the comlg line equals the coml1 line modulo P= (guard never
  binds). (c) the comnoeg line equals the coml1 line modulo P=
  (no data-driven eager work under L-free commit on R = 120).
  K6a passing with the parent's L = 7/10 lines at cm = 2/tc = 112
  establishes Q1: the commit rule's L is observably load-bearing
  (removing it changes behavior).
- **K7 (economics).** (a) Exact J equalities on R = 120:
  J_coml1(120,L) = 11 + 11*L for L in {1,3,7,10} (22/44/88/121),
  vs the frozen J_noeg(120,7) = 78 and J_noeg(120,10) = 93: the
  L-driven eager commit was J-beneficial at high L (Q2).
  (b) Findings (reported, not barred): J'_coml1(120,L) = 22 flat vs
  J'_noeg(120,7/10) = 48; the J-beneficial / J'-harmful tension.
  (c) Findings: quirk scoreboard on R = 21/60/82 per L:
  J_coml1 vs J_comlg vs J_comnoeg (Q3's cost/benefit under the
  L-free flip discipline).
- **K8 (control integrity / eager-direction findings).** (a) Zero
  flips on R = 21/82 for coml1/comlg/comnoeg at every L (as in the
  parent). (b) Findings (reported, not barred): comlg vs comnoeg
  line identity on all cells/L: does `phid > phin` (L := 1) do
  data-driven eager work under L-free commit anywhere (Q4)?
  (c) Findings: R = 60 new-arm behavior (quirk + flip under L-free
  commit; tf1/fdir/sel per arm).
- **K9 (hygiene / governance).** ASCII-only lane sources; no world
  literals (901/902) in cl_spec.zag, cl_main.zag; exactly one
  `fn main` in cl_full.zag; reused sources byte-unmodified
  (`git diff --quiet` on the 9 grandparent sources plus the parent
  lane's ld_spec.zag / ld_main.zag); da_learn.zag in particular NOT
  modified (separate lane only); the parent lane's sources
  superseded by copy-plus-delta (cl_spec.zag carries [CL-DELTA]
  markers), never edited; commits local with explicit pathspecs,
  never pushed.

## What would falsify the lane

- K6a failing with coml1 diverging from the parent's noeg L = 1
  line on R = 120: would mean an L-entry in the episode dynamics
  outside the commit rule was missed, or a toolchain miscompile
  (K4d replication would likely fail first).
- K5a failing (quirk not preserved under L := 1): would falsify the
  frozen L-invariance analysis of the quirk.
- K5b failing (a comlg/comnoeg cm = 2 with Dc = 0): would mean the
  guard / eager-drop does not close the quirk channel as analyzed.
- K7a failing while K6a passes: an accounting defect (J is computed
  from the barred rb/rf fields).

## Non-goals (frozen)

- pol 3 (recheck) interaction with the new commit arms; multiple
  shifts; gradual drift; L = 0/15/20/30 tails; estimating L from
  data (L stays caller-stated); changing the flip discipline;
  adopting any arm as the working rule (governance decision, banked
  with the evidence).
- The stale-data facet of the degenerate interval (noted in
  SPEC-COLD-START, untested there and here).
