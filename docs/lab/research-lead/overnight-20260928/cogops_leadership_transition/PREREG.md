# PREREG: COGOPS-LEADERSHIP-TRANSITION (frozen)

Worker: COGOPS-LEADERSHIP-TRANSITION. Date: 2026-10-03.
Lane: `docs/lab/research-lead/overnight-20260928/cogops_leadership_transition/`
Non-ledger task (claim minting paused). Builds on
COGOPS-HEDGE-FREQUENCY (c19/c19h, BUILD-PASS 9/9).

## 1. Research question

COGOPS-HEDGE-FREQUENCY found 0/22 natural hedge firings and
attributed it to ANTI-tie selection dynamics: leaders get
picked, accrue matching records, and extend their leads, so
no leadership transition occurred in 22 selections and the
hedge's exact-tie precondition never arose. This worker
characterizes the PRECONDITION for hedge relevance: under
what world dynamics DO leadership transitions occur, and
when transitions are forced, how often do exact ties (and
hedge firings) arise at them?

## 2. Pre-prereg probe discovery (material context)

A pre-prereg probe (pure Zag, /tmp/probe, throwaway binary;
does not enter the evidence) found that c19's (3,615) block
(F17-F22) did NOT run on the world the world-file comments
describe. S4's retrieve episodes (ids 12-15) log rel 615
into the learner's ret coverage; S6B's specialize_ret runs
on world F, which has no 615 facts, so rel 615 gets an EMPTY
specialized bucket; setup_worldF_plus then adds the 615
facts WITHOUT re-specializing. Result: rel 615 is invisible
to the specialized RETRIEVE (ret_version=2, empty bucket),
so c19's kind-5 need1 was [] (not the 3-cycle) and kind-6
need1 was [] (not the 3-cycle). As-run: kind 5 was
PW-winnable-on-degenerate-constant (PW won at lag 2 via the
prior), kind 6 was all-fail-on-degenerate. The rebuild-from-
source check (byte-identical output) confirms this is the
committed behavior, not a stale binary. Consequence for
THIS worker: kinds 5/6 are not used; two new kinds (8, 9)
are defined below and their trajectories were validated by
the probe method before freezing this prereg.

## 3. Battery design (c20h: hedge-bearing + instrumented)

One binary only (c20h). No hedge-deleted variant: this study
measures the hedge's firing precondition, it does not
re-price deletion. Setup blocks S1A/S1B/S2/S4/S6L/S6B are
verbatim copies of c19's (K5 checks byte-identity).

- Block A (4 stages, context (3,613), kinds 2,1,2,1):
  reproduce the anti-tie baseline: NEED leads and extends.
- Block B (10 stages, context (3,613), kind 8): REGIME
  CHANGE to an unwinnable world. All four forms fail every
  stage; per-failure turn costs order WHOLE (1-2 CMP) <
  PW (2-3) < NEED (3-6 NCMP) < ALT (9+). The leader's
  failures are costlier than the challenger's, so the
  score race inverts: NEED's score rises at ~6*rb+ra per
  failure-use, WHOLE's at ~2*rb+ra. Hand-simulation of the
  exact score algebra (ledger (5,2) after A) predicts the
  NEED->WHOLE crossing at B6 (B6: NEED ~118 vs WHOLE
  ~114.9 in raw score units) and WHOLE keeping the lead
  thereafter (its asymptotic mean cost 2*rb+ra is the
  global minimum; no failure record can undercut it).
- Block C (12 stages, context (3,613), kinds 2,1
  alternating): REGIME RESTORED to NEED-winnable. WHOLE
  leads at C1, fails; NEED wins the rescue; per
  win/fail cycle NEED's score grows ~3*rb/use while
  WHOLE's grows ~(2*rb+ra)/use with ra/rb~4.6, so NEED
  retakes the lead mid-block (hand-sim: C4) and extends
  it (anti-tie reasserts).
- Block D1 (4 stages, context (4,613), kinds 4,3,4,3):
  establish NEED leadership in a second (4-need) context.
- Block D2 (10 stages, context (4,613), kind 9):
  replicate the Block-B dethroning in the second context.

Kind 8 (new, context (3,613)): needs [801:(601,621)],
[801:(613,770)] (NO self-link: constant [771] via generic
retrieve; 613 not in ret coverage), [801:(604,611)] with
kind-1 self-link (convergent drifter 612->618 via the
specialized 604 bucket, indexed at S6B from world-F
facts). Trajectory: [611],[771],[612+p]. PW/WHOLE fail
(drifter: whole never repeats); NEED fails (only the two
constant carriers match: trivial match set); ALT fails.
Kind 9 (new, context (4,613)): kind-8 shape plus need3
[801:(605,640)] (constant 8-subject record via generic
retrieve; 605 not in ret coverage). Same unwinnability
argument (need2 still drifts; NEED match set all-trivial).

New instrumentation (log-only, behavior-neutral): at
initial selection (tried==0), after the argmin, log
DET-TIE (kind 12): best=<argmin> tm=<tie mask> rt=<rt>
rc=<rc>, where bit (1<<s) of tm is set iff strategy s has
uses>0 in this context AND its rescue-aware score exactly
equals the argmin (same cross-multiplication as the
hedge). Fresh-context sanity: tm==0, best==1 (K9).

A leadership transition is defined as a change in
DET-STRAT chosen between consecutive stages WITHIN one
block (initial selection only; intra-stage DET-SWITCH
rescue lines are not leadership).

## 4. Frozen predictions

- Selections: A2,A3,A4 = NEED(3); B10 = WHOLE(2);
  C12 = NEED(3); D1a2,a3,a4 = NEED(3); D2-10 = WHOLE(2).
- Transitions: >=1 in B (NEED->WHOLE), >=1 in C
  (WHOLE->NEED), >=1 in D2 (NEED->WHOLE); 0 in A after
  A1; 0 in D1 after D1a1. Total across B+C+D2 >= 3.
- Ties: exact-tie stages (popcount(tm)>=2) <= 3 of 38
  eligible. (Transitions jump over exact equality;
  knife-edge. Discriminates against "ties are common".)
- Hedge firings: counted and reported; every DET-HEDGE
  line satisfies dt1==0, dt3==0, ev>=1001, and its stage's
  DET-TIE tm has bits 1 and 3 set (cross-check).
- Q lines: 40/40 match c20_stages_predicted.txt
  (id, goal tag, how) in order.

## 5. Kill bars (all frozen; each can fail)

- K1: 40 DET-HGATE == 40 DET-STRAT == 40 DET-TIE lines;
  eligible (HGATE c1>0 AND c3>0) == 38 (all stages
  except A1, D1a1).
- K2: every DET-HEDGE line: dt1==0, dt3==0, ev>=1001;
  each firing stage's DET-TIE tm has bits 1 and 3 set.
  (Zero firings: vacuously PASS; the count is reported.)
- K3a: A2,A3,A4 DET-STRAT chosen=3; 0 transitions in A
  after A1.
- K3b: >=1 leadership transition in B; DET-STRAT on
  B10 = 2.
- K3c: >=1 leadership transition in C; DET-STRAT on
  C12 = 3.
- K3d: D1a2,a3,a4 DET-STRAT chosen=3; >=1 transition
  in D2; DET-STRAT on D2-10 = 2.
- K3e: total leadership transitions across B, C, D2
  >= 3.
- K4: tie stages (popcount(tm)>=2) <= 3 of 38
  eligible; tie frequency and hedge firing count
  reported with the rule-of-three upper bound.
- K5: setup blocks S1A/S1B/S2/S4/S6L/S6B byte-identical
  to c19h_run1.txt's.
- K6: 3/3 byte-identical runs (sha256 per run),
  stderr empty on all 3 runs.
- K7: 40/40 Q lines match c20_stages_predicted.txt
  (id, goal tag, how) in order.
- K8: toolchain + provenance: safebin PATH for every
  command; `which python3`/`which python` empty;
  pinned znc only; new Zag scanned for `while.*!(`
  (must be clean) and deep nesting; c20_base.zag
  cmp-identical to c19_base.zag; c20h_strat_additive.zag
  diff vs c19h_strat_additive.zag = exactly the
  DET-TIE instrumentation block; c20_world_add.zag diff
  vs c19_world_add.zag = exactly mk_goal8 + mk_goal9;
  c20_main.zag diff vs c19_main.zag = battery swap +
  kind-12 dump branch only.
- K9: A1 and D1a1 DET-TIE lines read best=1 tm=0
  (fresh-context instrument sanity).

## 6. Decision rules

- If K3b/K3d fail with 0 transitions: the "regime
  change breaks rich-get-richer" hypothesis is killed;
  report that leadership is unbreakable even under
  adversarial unwinnable regimes (strengthens the
  anti-tie finding).
- If K4 fails (>3 tie stages): exact ties are NOT
  knife-edge under transitions; the hedge's
  precondition is common when leadership moves --
  report the measured tie/firing rates as the
  characterization.
- If K3 passes and K4 passes with ~0 ties: the
  characterization is "transitions occur under
  failure-cost-asymmetric regime change, but exact
  ties remain knife-edge even at transitions" --
  the hedge's precondition stays rare.
