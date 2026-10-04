# ADV_MEM4_RESULT: H-MEM4 Red Team Report

**Date:** 2026-09-29
**Adversary verdict: H-MEM4 DOWNGRADED (not killed).**
**Frozen prereg:** `PREREG_MEM4_ADV.md` (commit `b2681d2a4`), strictly before
any adversary implementation or execution (verified: prereg commit is an
ancestor of the harness and result commits; no amendments).
**Target:** `mem4_learn.zag` at `9b98d1fa9` (H-MEM4 SURVIVES 5/5).
**Raw evidence:** `MEM4_ADV_RAW_OUTPUT.txt` (md5
`2397df11915821f365bdd2d5fce89a3f`, 3 runs byte-identical via cmp)
**Adversary harness:** `mem4_adv.zag` (mechanism region = lines 1..500 of
the frozen `mem4_learn.zag`, byte-identical; only `main` replaced with
attack drivers; no mechanism edits)
**Pure Zag. No Python in fixtures, harness, build, execution, or analysis.**

## Stance and scope

The repair claim was assumed false. Four attacks were preregistered with
explicit frozen verdict rules before any implementation. Two succeed
(downgrade), one succeeds-as-boundary (builder disclosure confirmed), one
fails (no finding). The downgrade narrows R2; it does not touch R1 or R3.

## Attack results

### X-M4-1 (counterfactual soundness): FAIL (no finding)

Differential honesty check of `churn_verdict()` on three fixtures
(K-M4-1b flip, X-M4-2a state, X-M4-2b state): the verdict was recomputed
independently and the evicted procedure identity compared between the
protected and unprotected outcomes. Frozen kill rule: SUCCEED iff
(verdict==0 AND evicted procs differ) OR (verdict==1 AND winners same
AND evicted procs same).

Observed on all three fixtures: verdict=1 exactly when the winner
flipped (FIFO->LFU on K-M4-1b; LIFO->LFU on both harm states) and the
evicted proc differed (proc0->proc7; proc6->proc7). The verdict's
natural reading held on every fixture. The (winner, victim) pair is
exhaustive for the eviction outcome: same winner and same victim slot
implies the same evicted proc and the same replay cost by construction,
so a :0 verdict cannot hide an outcome change. R1 stands as stated.

### X-M4-2a (grace-window harm): SUCCEED -> DOWNGRADE

The exact X-M3-1b harm pattern recurs inside the 3-query grace window.
Fixture: slot7 holds a meritless newcomer (proc7, uses=0, age=2 < GRACE=3,
grace-protected); slots 0..6 hold procs 0..6 (uses 10..70); 20-query
window with proc7 absent. Frozen run:

- protected: LIFO evicts slot6 (proc6, uses=70) at replay cost 2
- unprotected: LFU evicts slot7 (proc7, uses=0) at replay cost 0
- `X-M4-2a HARM CONFIRMED: cost 0 -> 2; queried proc sacrificed for newcomer`

This is the X-M3-1b harm verbatim (cost 0 became cost 2; a queried
procedure with uses=70 is sacrificed to shield a never-queried newcomer),
recurring while the newcomer is inside grace. The mechanism's own
CHURN-FULL verdict honestly reports :1 (winner flips LIFO->LFU; eviction
slot6(proc6)->slot7(proc7)); the dishonesty is not in R1, it is in the
scope of R2. The builder's K-M4-2 bar used proc8 at age=9 (past grace),
so the frozen bar never covered the grace window. R2's natural reading
("a meritless slot is evictable") is false for the first 3 queries of a
newcomer's life, and the X-M3-1b harm is not closed there, only narrowed
to newcomers older than 3 queries.

### X-M4-2b (fig-leaf merit): SUCCEED -> DOWNGRADE

The same harm recurs past grace behind a single query of "merit".
Fixture: identical to X-M4-2a except slot7 has uses=1 (one stale query
outside the 20-query window), age=3 (past GRACE), within the PROB window,
therefore merit-protected (uses>0). Frozen run:

- protected: LIFO evicts slot6 (proc6, uses=70) at replay cost 2
- unprotected: LFU evicts slot7 (proc7, uses=1) at replay cost 0
- `X-M4-2b HARM CONFIRMED: cost 0 -> 2; queried proc sacrificed for newcomer`

The merit gate is satisfied by a single query. A procedure queried once
and never again receives full age protection and can still displace a
heavily-used procedure at a cost increase of 0 -> 2. R2's "merit-gated"
claim is therefore narrowed to: gated by any single query (uses>0), not
by any substantive merit threshold. The X-M3-1b harm class is closed only
for the uses=0-past-grace instance, not in general.

### X-M4-3 (sub-majority targeting): SUCCEED-AS-BOUNDARY

A 10/20 (50 percent, non-strict-majority) future targeting the selected
policy's victim (proc6, selected LIFO): `fvp*2 > nf` is `20 > 20` =
false, so no ADVERSARIAL-TARGET fires. L1=16 >= 6 passes DIST-DIFFERS2.
Misses: LFU=4 LRU=4 FIFO=4 LIFO=10 RANDOM=3; selected LIFO uniquely
worst; `fut_score3` returns 0 (`K-M3-2 FAIL: selected not min`) with no
adversarial diagnosis. This confirms the builder's disclosed limit
("strict-majority screen misses sub-majority targeting") exactly as
disclosed: even exactly half the future concentrated on the victim is
missed by the screen. Boundary confirmed; no verdict change. Note the
bar itself behaves correctly (it FAILs rather than passing a bad
selection); what is missing is only the exonerating diagnosis.

### X-M4-4 (regression): FAIL (no finding)

`mem4_learn.zag` rebuilt unmodified: stdout md5
`7921b0f4bc917d9ccb3627aa41d1ca97` matches the frozen value exactly;
3 consecutive runs byte-identical; `ALL BARS PASS` printed; 0 FAIL
lines. All five K-M4 bars reproduce. Source audit: the mechanism region
(lines 1..500) contains no fixture literals (`setup_flip` is the
builder's own frozen K-M4-1b fixture, documented in PREREG_MEM4.md).
The builder's 5/5 stands as executed.

## Causal interpretation

The downgrade is a design-scope finding, not an implementation bug.
`elig()` implements exactly what the builder preregistered: absolute
protection for age < 3, then protection iff uses > 0. Both attacks use
the mechanism exactly as designed; the frozen arithmetic in
PREREG_MEM4_ADV.md reproduced on the first execution with no fixture
tuning. The X-M3-1b harm was therefore never fully closed by R2: it was
closed for one instance (uses=0, age=9) while remaining reachable through
two adjacent instances (uses=0 inside grace; uses=1 anywhere). A
substantive merit threshold (e.g. uses >= k for k > 1, or recency-weighted
merit) would be needed to close the class; that is a new hypothesis, not
a repair of this one.

## Verdict aggregation (per frozen rules)

- X-M4-1 FAIL, X-M4-4 FAIL: no findings; R1 and the 5/5 regression stand.
- X-M4-2a SUCCEED, X-M4-2b SUCCEED: H-MEM4 DOWNGRADED.
- X-M4-3 SUCCEED-AS-BOUNDARY: disclosed limit confirmed.

**H-MEM4 is DOWNGRADED, not killed.** Surviving claims: R1 full
counterfactual (verdict sound on all fixtures); R3 adversarial-target
screen within its disclosed strict-majority scope; all five K-M4 bars as
executed. Narrowed claims: R2 merit-gated probation (grace-window
exception; uses>0 fig-leaf threshold). H-MEM4 remains bounded L2; no L3
implication was claimed or affected.

## Governance disclosures

- Adversary harness reuses the frozen mechanism source verbatim
  (lines 1..500); only the driver `main` is new. No mechanism file was
  modified by the adversary.
- Prereg commit `b2681d2a4` strictly precedes all adversary
  implementation and execution; no amendments were made.
- All fixture arithmetic was hand-derived in the prereg and reproduced
  on first execution; no fixture was tuned after seeing output.
- No Python was used at any stage (fixtures, harness, build, execution,
  analysis, or editing).
- Determinism: 3/3 byte-identical adversary runs; 3/3 byte-identical
  regression rebuilds.
