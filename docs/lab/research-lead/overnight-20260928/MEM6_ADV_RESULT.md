# ADV_MEM6_RESULT: H-MEM6 Red Team Report

**Date:** 2026-09-30
**Adversary verdict: H-MEM6 SURVIVES (all four attacks fail).**
**Frozen prereg:** `PREREG_MEM6_ADV.md` (commit `c52c1a60d`), committed
alone strictly before any adversary implementation or execution
(verified below: the prereg commit precedes the harness commit; no
amendments; no Python).
**Target:** `mem6_learn.zag` at the H-MEM6 result commit `266fbde85`
(H-MEM6 SURVIVES 6/6).
**Raw evidence:** `MEM6_ADV_RAW_OUTPUT.txt` (md5
`6661f2ad4ae01e8dbabf930f2ba26cd8`, 3 runs byte-identical via cmp,
exit 0, zero FAIL lines).
**Adversary harness:** `mem6_adv.zag` (mechanism region = lines 1..537
of the frozen `mem6_learn.zag`, cmp-verified byte-identical against
`git show 266fbde85:...`; only adversary fixture builders, CHECK
helpers, and `main` are new; no mechanism edits).
**Pure Zag. No Python in fixtures, harness, build, execution, or
analysis. No em dashes in any loop artifact.**

## Stance and scope

The repair claim R5 was assumed false. Four attacks were preregistered
with explicit frozen verdict rules before any implementation. All four
fail: no kill, no downgrade. The frozen H-MEM6 bars (K-M6-1 through
K-M6-6) are untouched by this report. The disclosed knife-edge at the
in-window 1-vs-2 threshold is confirmed as a real, measured boundary,
not softened.

## Adversary errors (owned before findings)

1. **Harness print bug, first build:** the initial `mem6_adv` binary
   segfaulted (exit 139) at the summary line. Cause: adversary error.
   `emit` is single-argument (`fn emit(s:[]u8)void`), and the harness
   passed a bare i32 (`emit(fail)`), reinterpreting it as a pointer.
   The mechanism idiom is `emit(i32s(x))`. Fixed by using `i32s()` in
   the summary and CHECK helpers. No frozen EXPECT was changed.
   All 54 CHECK lines had already printed PASS before the crash in the
   first run, and the fixed binary reproduced them identically.
2. **Compile-time arity error, second build:** an intermediate edit used
   multi-argument `emit(...)`; znc rejected it at compile time
   ("expected 1"). Reverted to the single-argument `i32s()` idiom.
   Neither defect touched any mechanism code or any expectation.

## Attack results

### X-M6-1 (in-window 1-vs-2 threshold): FAIL (boundary confirmed)

Paired fixtures identical except one recent query for slot7's
procedure (seq=105, nq=26, ev=11, win=20; slots 0..6 age-expired;
slot7 age-open prot=109). Frozen runs (3/3 byte-identical, exit 0):

```
X-M6-1a (2 in-window queries):
  [full counterfactual] protected: LFU victim=slot0(proc0) | unprotected: LFU victim=slot7(proc7)
  [selected-policy] protected-victim=slot0 unprotected-victim=slot7
  CHURN-FULL:1 (winner stable at LFU; eviction slot0(proc0)->slot7(proc7))
X-M6-1b (1 in-window query):
  [full counterfactual] protected: LFU victim=slot7(proc7) | unprotected: LFU victim=slot7(proc7)
  [selected-policy] protected-victim=slot7 unprotected-victim=slot7
  CHURN-FULL:0 (winner stable at LFU; eviction unchanged)
```

All 18 frozen CHECKs pass (9 per sub-fixture: winuses, elig,
wprot/vprot/cprot, wun/vun/cun, churn). The single added in-window
query flips the outcome from "evict newcomer at cost 1" to "shield a
cost-2 procedure and sacrifice a cost-9 procedure" (harm 7). Per the
frozen X-M6-1 verdict rule this is the builder-disclosed knife-edge
shape: the builder's own boundaries state "The in-window uses 1 versus
2 threshold remains a knife-edge" and "Shielding a cost-2 slot can
force eviction of a cost-3 slot". The observed harm is larger than the
disclosed cost-2-vs-cost-3 example (cost 2 vs 9 here), but the SHAPE
is the disclosed one, and churn_verdict reports it honestly
(CHURN-FULL:1 with the correct winner and slot pair). No structural
violation: slot7 is shielded at winuses=2 and evictable at
winuses=1, exactly as frozen. The attack fails.

### X-M6-2 (all-protected fallback): FAIL (boundary confirmed)

X-M6-2a (all 8 slots age-open with >=2 window queries each):
nelig=0, every protected-policy victim=-1, argmin_pol(protected)=0.
`pressure` emits FALLBACK-ALL-PROTECTED, sets st_fbf=1, and the
unprotected argmin selects LIFO victim slot7 cost 2 STRICT; proc8 is
stored at slot7 (has_proc(8)=1). Per-policy lines match the direct
victim()/replay_cost() calls exactly:
LFU/LRU/FIFO->slot0 cost 3, LIFO->slot7 cost 2, RANDOM->slot1 cost 3.
churn_verdict takes the fallback path and reports CHURN-FULL:0
(fallback path; protection not applied), return 0.

X-M6-2b (near-twin: pid7 has exactly 1 in-window query, slot7
evictable): no fallback triggers (st_fbf=0); protected and
unprotected both select LFU victim slot7 cost 1; CHURN-FULL:0
(winner stable at LFU; eviction unchanged).

All 21 frozen CHECKs pass (12 in 2a, 9 in 2b). Per the frozen X-M6-2
verdict rule: fallback triggers exactly when all slots are protected,
never when one slot is evictable, and the trace reports both paths
honestly. The attack fails.

### X-M6-3 (window-edge and age-deadline interaction): FAIL (boundary confirmed)

X-M6-3a (merit straddle: the 2nd query for pid7 moves from Q[6],
inside the window, to Q[5], outside it): elig(slot7) flips 0->1 and
the protected LFU victim flips slot0->slot7 exactly at the frozen
step. Costs move 18->1 coherently.

X-M6-3b (age straddle: seq 108 vs 109 with full 20-query merit for
pid7): at seq=108 the slot is protected (elig=0, LFU->slot0 cost 0);
at seq=109 the slot is evictable (elig=1, LFU->slot7 cost 20).
Age expiration dominates full window merit, exactly as frozen.

All 15 frozen CHECKs pass. Per the frozen X-M6-3 verdict rule: no
off-by-one shields a window-absent slot, no merit is ignored while
the age interval is open, and merit/harm are computed over the same
window at every call site. The attack fails.

### X-M6-4 (regression and mechanism diff): FAIL (no finding)

- `mem6_learn.zag` rebuilt unmodified from the committed blob
  (`git show 266fbde85:...`); cmp-verified byte-identical to the
  worktree file before execution.
- Compiled with the pinned znc 2026.07.0-dev; 3 runs byte-identical
  (cmp), exit code 0, zero FAIL lines.
- md5 of run output `b505e265efe2a48d78d57be85c66a6ad`, matching the
  frozen builder raw md5 exactly.
- Mechanism diff (H-MEM5 -> H-MEM6) reviewed: the only behavioral
  changes are the preregistered R5 repair. `winuses()` is added;
  `elig`, `nelig`, `victim`, `replay_cost`, `argmin_pol`,
  `churn_verdict`, and `pressure` thread `(Q, win)` through;
  `replay_cost` delegates to the same `winuses` implementation that
  `elig` uses; `pressure` fixes win=20 at its call sites. All
  remaining diff hunks are comments and the new builder fixtures
  (`setup_flip3`, `setup_xm51`), outside the mechanism region.
  No undeclared behavioral change.

## Verdict

**H-MEM6 SURVIVES the red team.** All four attacks fail per their
frozen verdict rules; the regression passes 3/3 with the frozen md5.
The in-window 1-vs-2 threshold is a genuine knife-edge with real
protection-induced harm (measured cost 2->9 here), but it is the
disclosed shape, gated by the same window that measures the harm, and
reported honestly by churn_verdict. The all-protected fallback is
explicit and honest. The window-edge and age-deadline boundaries flip
exactly at their frozen steps with no off-by-one.

## Preserved negative evidence and open concerns (not findings)

- The red team could not construct a protection-induced harm that the
  mechanism misreports or that violates R5. The strongest confirmed
  boundary remains the builder's own disclosed concern: the fixed
  20-query window (a step function, not smooth decay) and the severity
  of the in-window knife-edge (harm scales with the cost gap; this
  report measured 7, larger than the builder's cost-2-vs-cost-3
  example).
- Future red teams should attack: smooth-decay vs fixed-window merit,
  larger cost gaps at the knife-edge, and interactions between the
  window edge and the RANDOM policy's deterministic pick.
- The stale-merit class (X-M5-1/X-M5-2) is closed at the mechanism
  level under R5: X-M6-1b demonstrates that st_uses=2 with only 1
  in-window query does not shield the slot.

## Governance appendix

- Prereg `PREREG_MEM6_ADV.md` committed alone at `c52c1a60d`
  (2026-09-30, before any adversary implementation or execution).
- Mechanism region lines 1..537 of `mem6_learn.zag` at `266fbde85`
  cmp-verified byte-identical into `mem6_adv.zag` before execution.
- Pure Zag throughout: no Python in fixtures, harness, build,
  execution, or analysis. (The two adversary errors above were caught
  and fixed inside Zag/znc; no Python was used at any point.)
- No em dashes in this report or any artifact.
- Determinism: adversary 3/3 byte-identical, exit 0; regression 3/3
  byte-identical, exit 0, md5 match.
- Owned paths in this red-team commit: `PREREG_MEM6_ADV.md`
  (committed alone earlier), `mem6_adv.zag`,
  `MEM6_ADV_RAW_OUTPUT.txt`, `MEM6_ADV_RESULT.md`.
