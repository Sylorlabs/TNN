# REPORT: Coverage-Directed vs Failure-Triggered Widening -- Verdict MIXED

Date: 2026-10-02. Worker: widen-comp (replacement for S1/S2 empty-mask worker).
Battery: 4 discriminating problems (D0, D1, D2, D3), 2 arms (F, C), pure Zag,
pinned znc. Prereg committed alone before implementation (cd2c750fd).

## Verdict: MIXED, with a stated boundary

All kill bars K1-K5 pass exactly as frozen, 3/3 byte-identical per arm. The
frozen verdict mapping therefore yields MIXED: coverage-directed selective
widening is not a pure speedup over failure-triggered blind widening. It
changes WHAT is tried and WHEN, and the direction of the change depends on
whether the coverage evidence is observable:

- D1 (observable evidence): C wins. Try-1 miss (X,out,1) selectively admits
  WADD=(0,1),(0,3); (X,Y) succeeds at try 2. F needs 7 tries and a blind retry
  of all rejected pairs. Same answer, narrower tried-set {X,(X,Y)} vs 7.
- D2 (genuine but non-diagnostic evidence): C pays a spurious cost. The miss
  (D,out,1) is real (D did produce a NODE), but the justified pairs (D,Q) and
  (D,W) both fail. C fires WIDEN=1 where F has none and costs 5 tries vs 3.
- D3 (unobservable evidence): C fails where F succeeds. X is rejected in all
  admission positions (its outmask={2} contradicts kout=1), so X is never
  executed, no miss is ever observable, and arm C has no widening path: ANS=-2
  at try 1. F's blind retry finds (X,Y) at try 2 (ANS=44, WIDEN=1, WTRIG=1).
- D0 (canonical sanity): both arms identical (2,3,0,0,34), no misses, no
  widening. The coverage machinery does not perturb the normal path.

Boundary statement (as frozen): coverage-directed selective widening dominates
exactly when the coverage evidence is observable inside the admitted trial
sequence, i.e. the misleading MAP gets executed. It costs spurious trials when
genuine misses are non-diagnostic, and it cannot fire when the misleading MAP
is never admitted. The blind failure-triggered retry is the exploration
backstop for unobservable coverage: evidence the filter needs can sit behind
the filter itself.

## The two mechanisms, precisely

Shared (w_base.zag, identical in both assemblies): S2-pinned admission (empty
kind-set reads as universal {1,2} in all three positions), ordered trial
execution (admitted singles in MAP-id order, then admitted pairs in (a,b) id
order) with end-to-end verification, Amendment-2 success-recording into the
contract masks.

Arm F (w_fail.zag): on exhaustive admitted failure, retry ALL filter-rejected
ordered pairs once in id order (WIDEN=1, WTRIG=1). Triggered solely by
learner-observed exhaustive failure. No ledger.

Arm C (w_cov.zag): maintains missbits[m][p], the kind bits observed at runtime
during the learner's own trial executions that are not covered by MAP m's
contract mask at position p in {in,out} (S2 reading: empty masks cannot miss).
Populated from failed trials only. On a failed trial adding a new miss bit,
immediately admit EVERY filter-rejected, untried ordered pair (x,y) with kin in
u_eff(x.in), kout in u_eff(y.out), and junction justification
(missbits[x][out] intersects u_eff(y.in), or missbits[y][in] intersects
u_eff(x.out)); log WIDEN=1 once per query, WTRIG=2, WADD=x,y per pair; try them
immediately in id order before resuming the admitted sequence. No blind retry
exists in arm C. Every input to the decision is learner-observed; no
researcher oracle.

## Kill bar results

Format: ANS / TRIES / WIDEN / WTRIG / INTER. All 3/3 byte-identical.

| Prob | F predicted | F observed | C predicted | C observed |
|------|-------------|------------|-------------|------------|
| D0 | 2/3/0/0/34 | 2/3/0/0/34 | 2/3/0/0/34 | 2/3/0/0/34 |
| D1 | 2/7/1/1/44 | 2/7/1/1/44 | 2/2/1/2/44 | 2/2/1/2/44 |
| D2 | 2/3/0/0/-1 | 2/3/0/0/-1 | 2/5/1/2/-1 | 2/5/1/2/-1 |
| D3 | 44/2/1/1/44 | 44/2/1/1/44 | -2/1/0/0/-1 | -2/1/0/0/-1 |

- K1 D0: PASS. Identical columns; no misses recorded; no widening.
- K2 D1: PASS. F: 6 admitted trials fail, WIDEN=1 (WTRIG=1), rejected (X,Y)
  succeeds at try 7 (INTER=44 trace: 41,41,41 then 44). C: try-1 single X
  fails with miss (X,out,1); WIDEN=1 (WTRIG=2); WADD=0,1 and WADD=0,3 admitted
  up front; (X,Y) succeeds at try 2; (X,D2) admitted but never tried.
  LEDGER m=0 in=0 out=1 on C; all-zero on F.
- K3 D2: PASS. F: D,Q fail, W succeeds at try 3, no widening (WIDEN=0). C:
  try-1 miss (D,out,1) fires SPURIOUS widening (WTRIG=2, WADD=0,1 and 0,2);
  both justified pairs fail (INTER=44 traces); Q fails; W succeeds at try 5.
  LEDGER m=0 in=0 out=1 on C; all-zero on F.
- K4 D3: PASS. F: Y fails, exhaustive admitted failure, WIDEN=1 (WTRIG=1),
  blind retry finds (X,Y) at try 2, ANS=44, INTER=44. C: Y fails with no miss
  (its kinds are covered), no widening rule exists to fire, ANS=-2 at try 1.
  Both ledgers empty.
- K5 LEDGER: PASS. C D1/D2 show `LEDGER m=0 in=0 out=1`; every F ledger line
  and every C D0/D3 ledger line shows in=0 out=0.
- K6 DETERMINISM: PASS. 3/3 byte-identical per arm (digests below).
- K7 NO-MODE AUDIT: PASS. Each arm implements exactly one widening rule,
  always on. No identifier selecting widening policies at runtime exists in
  either arm source (grep for widen_arm/policy/mode: zero hits). The F vs C
  difference is the experimental manipulation (two separately assembled
  binaries sharing one base file), never a learner-selected mode. Disclosed:
  w_cov.zag's c_try_pair/c_try_single take a wom call-site constant (1 from
  the main trial sequence, 0 from inside widening) to prevent nested widening
  triggers; it is structural, not learner state.
- K8 HYGIENE: PASS. Zero em/en dash bytes (byte-verified); safebin guard
  attested in NAMECHECK.md Step 0; pure Zag; pinned znc.

## Faster vs different (the required bar)

D1 alone would read as "coverage-directed is faster" (7 tries to 2). D2 and
D3 are the bars that distinguish faster from different, and both fire: D2
shows a WIDEN event and try-count difference in the opposite direction
(C slower, C widens where F does not), and D3 shows an outcome difference
(C fails where F succeeds). A verdict of COVERAGE-DIRECTED WINS would have
required C to match or beat F on every problem; a verdict of
FAILURE-TRIGGERED SUFFICES would have required identical columns. Neither
obtained. The differences are in what is tried, when widening fires, and
whether the query can succeed at all: that is "different", not "faster".

## Why the boundary is principled, not an artifact

The three discriminating regimes follow from one fact about the design: a
coverage miss can only be observed by executing the MAP that exhibits the
uncovered kind.

- Observable (D1): the misleading MAP X is admitted as a single (its contract
  is compatible with the goal kinds), so execution surfaces the miss early and
  selective widening beats blind retry.
- Non-diagnostic (D2): the miss is genuine evidence about D, but the
  junction-justified pairs happen to be wrong. Selectivity does not imply
  correctness; the evidence underdetermines which pair works.
- Unobservable (D3): the misleading MAP X contradicts the goal kinds in its
  contract, so the filter never admits it anywhere and the evidence needed to
  correct the filter is behind the filter. Only unconditioned exploration
  (the blind retry) crosses this.

This is the same coverage boundary the C319 prereg Section 7 predicted, now
with the mechanism's own fallback policy as the variable under test.

## Architecture accounting

- Cognition lines added: ~330 (w_base.zag) + ~90 (w_fail.zag) + ~150
  (w_cov.zag). Shared base is identical by construction across arms.
- New hardcoded semantic cases: 0. Modes/bridges/handlers: 0.
- Researcher-owned: behavior implementations, world facts/teaching, the two
  widening rules (the variable under test).
- Learner-owned: kind-set contracts, missbits ledger, admitted/widened/tried
  sets per query, grown contracts on success.

## Honest limitations

- Four problems discriminate the widening policy; they do not establish
  generality of either policy.
- missbits is per-query; cross-query learning uses only the shared
  success-recording. A persistent coverage ledger is untested.
- Arm C was tested in its pure form (no blind backstop) as the strongest
  test; the hybrid (coverage-selective first, failure-triggered blind as
  backstop) is the recommended follow-up, not a claim of this battery.
- Expected-answer verification still used (canonical boundary).
- During implementation, the first C build admitted widened pairs lazily
  (one at a time, stopping at success), which under-logged WADD against the
  frozen "admit every justified pair up front" semantics; the composer was
  corrected to admit-all-then-try-in-order before any runs were recorded, and
  the corrected build reproduces every frozen prediction. No prereg text was
  changed after the freeze.

## Recommended follow-ups

1. Hybrid arm: coverage-selective widening on first new miss, failure-
   triggered blind retry as backstop on miss-less exhaustion. Predicted to
   match C on D1/D2 and F on D3; the battery discriminates whether the hybrid
   inherits only the wins.
2. Persistent missbits across queries: does the ledger become learner-owned
   long-term knowledge that changes admission on later queries (P5-style
   growth battery for the ledger)?
3. Adversarial worlds where the miss systematically misleads (D2 generalized):
   characterize when selectivity helps vs hurts as a function of contract
  ...[truncated 1333 chars]
