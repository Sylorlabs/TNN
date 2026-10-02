# Greedy Search Fix Design: 2-Ply Plateau Lookahead

Status: DESIGN-COMPLETE. Design only. No implementation. No empirical claims.
Parent: T-ADV5 re-evaluation `83c02efff` (verdict TADV5-ACCEPTABLE).
Scope: `docs/lab/research-lead/overnight-20260928/greedy_fix/` only.

## 1. Problem statement

The T-ADV5 re-evaluation on the fixed bridge ended HONESTFAIL with cost 68.
The trace (3/3 byte-identical, md5 `036a3fcb334c66c43f6d6e73e662a978`):

```
BRIDGE MOVE li=0 op=2 p=13010 gain=1 nc=4
BRIDGE MOVE li=3 op=2 p=13011 gain=1 nc=7
INV SEARCH fam=13 n=40 built=0 nodes=7 scost=28
INV HONESTFAIL fam=13 n=40
```

The inventor fired on the full 40-point buffer (the D1-D3 protocol fix works),
but the greedy search applied two EQ isolations (gain +1 each) while every LT
split gained 0, then terminated without exact fit at nc=7. The optimal form
`IF(x<13010, 1, IF(x<13020, 0, 1))` (5 nodes, 0 EQ, per `T_ADV5_DESIGN.md`
section 2) is expressible with the four generic operators and within all
caps, but the search never built it.

## 2. Root cause: a positive-gain trap, not a plateau

`construct_search` (`bridge_fix_impl/bridge.zag`, line 391) is 1-ply greedy:
each iteration applies the admissible move with strictly largest immediate
gain (`if(g>best_gain)` from `best_gain=0`), then terminates when no
positive-gain move remains.

On the T-ADV5 buffer (outputs 1 on [13000,13010), 0 on [13010,13020),
1 on [13020,13040)), from the initial CONST(1) leaf (30/40 correct):

- EQ at any zero point (13010..13019): gain +1 (isolates one zero).
- LT at 13010: gain 0 (then-side all 1, else-side majority still 1).
- LT at 13020: gain 0 (same reasoning).

The trap is that the locally best move (EQ, +1) is globally wrong, and the
globally right first move (LT, 0) is never taken because a positive-gain
move exists. This is strictly harder than a zero-gain plateau: a
sideways-move policy ("allow zero-gain moves when no positive move exists")
does NOT fix T-ADV5, because a positive-gain move always exists at the
decision point. The C2 T3 limitation (strict net-progress forbids paths with
intermediate score decreases) is the same family of defect, one level
shallower.

After the two EQ moves, nc=7 and every further split is refused by the node
cap (`nc+3>8` in `op_split_lt`/`op_split_eq`), so the search terminates by
(cap-exhaustion AND zero admissible gain): HONESTFAIL.

## 3. Proposed fix: 2-ply plateau lookahead (PLATEAU-LOOKAHEAD, K=2)

### 3.1 Rule

Inside `construct_search` only, replace the move-selection step with:

1. Compute the best 1-ply admissible move as now: gain `g1`, move `m1`
   (admissible = within node cap, EQ promotion cap, move budget; same
   candidate enumeration in the same scan order).
2. Collect `Z` = {admissible moves with gain exactly 0}, in existing scan
   order (leaf index, then LT thresholds ascending, then EQ values
   ascending; the current enumeration order is unchanged).
3. For each `z` in `Z`: simulate `z` (same save/apply/evaluate/restore
   pattern the code already uses), then compute the best 1-ply follow-up
   gain `g2(z)` from the resulting state under the same admissibility
   rules. Define `unlocked(z) = g2(z)`.
4. Let `z*` = first `z` in scan order maximizing `unlocked(z)`.
5. If `Z` is nonempty and `unlocked(z*) > g1`, apply `z*`.
   Else if `g1 > 0`, apply `m1` (unchanged greedy behavior).
   Else terminate (unchanged HONESTFAIL path).

Total path outlook of `z` is `0 + unlocked(z)`; the rule applies the plateau
move only when its unlocked follow-up strictly beats every immediate move.

### 3.2 Worked example on T-ADV5

State S0: CONST(1), nc=1, cur_correct=30.

- 1-ply: `g1 = +1` (EQ at 13010; first of ten +1 EQ moves in scan order).
- `Z = {LT@13010, LT@13020}`, both gain 0.
- Simulate LT@13010 (nc=4, cur=30): best follow-up is LT@13020 on the
  else-leaf: then-side [13010,13020) all 0, else-side [13020,13040) all 1,
  total 10+10+20 = 40/40. `unlocked = +10`.
- Simulate LT@13020 (nc=4, cur=30): best follow-up is LT@13010 on the
  then-leaf: same 40/40. `unlocked = +10`.
- `+10 > +1`, so apply LT@13010 (first in scan order).

State S1: IF(x<13010, 1, else-leaf), nc=4, cur_correct=30.

- 1-ply: LT@13020 on else-leaf, gain +10 (`g1 = +10`). (EQ moves give +1;
  some LT moves give 0 or +1.)
- Any zero-gain `z` can unlock at most the remaining 10 errors, so
  `unlocked(z) <= +10`, never strictly greater than `g1 = +10`. No
  diversion. Apply LT@13020.
- State S2: exact fit 40/40, nc=7. `tree_exact_fit` returns true; the
  promotion path proceeds as now.

Predicted outcome: exact fit with the 2-threshold form, nc=7, 0 promoted EQ
nodes, within all caps.

### 3.3 Cost accounting

Each simulated evaluation continues to cost 1 under the existing accounting
(`set32(cost,0,get32(cost,0)+1)` per `tree_correct` simulation). Estimated
search cost on T-ADV5: S0 about 12 (1-ply) + 2x11 (follow-ups) = 34; S1
about 12 + small follow-up set = ~20; total search ~55-70, plus unchanged
episode overhead. This is above the measured 68 but below COSTCEIL=108.
The ceiling remains the guard: if lookahead cost ever breaches it,
F-DECEPT-COST fires exactly as now. The design narrows cost headroom; this
is disclosed, not hidden.

### 3.4 Determinism and blast radius

- Deterministic: scan order and strict-`>` argmax are unchanged; the
  lookahead adds no randomness and no new tie-breaking.
- Blast radius is `construct_search` only. Unchanged: the four operators,
  `novelty_generic`, VERIFY/refit, `teval`, family specs, menu adoption,
  cost units, and all caps (8-node, EQCAPP=4, MOVEBUD=24, COSTCEIL=108).
- No op-code-specific logic anywhere in the rule: it keys only on
  behavioral gain computed by `teval` on the buffer. This keeps the M1-M4
  audit posture (no new semantic cases, no new `setnode` sites outside the
  four operators).

## 4. Rejected alternatives

- **Sideways moves only** (take zero-gain moves when no positive move
  exists): REJECTED as insufficient. T-ADV5's trap move has strictly
  positive gain, so plain greedy still takes the EQ first. This would fix
  plateaus but not traps.
- **Op-prioritized search** (prefer LT over EQ, or try LT first):
  REJECTED. Keying the search order on op identity is adjacent to a
  dedicated semantic case and risks the C0-A audit (M3/M4). The lookahead
  is behavioral: it prefers the LT only because the LT unlocks +10.
- **Random restarts / stochastic perturbation**: REJECTED. Breaks K3
  byte-identical determinism.
- **Full beam search over tree states** (width w): viable but heavier
  machinery (per-element state save/restore; the current code mutates one
  state in place). Recommended as the follow-up if a depth-2 adversary
  defeats K=2 (section 5), not as the first fix.

## 5. Honest boundary

K=2 lookahead defeats 1-step traps (one zero-gain move before payoff).
A 2-step trap (two consecutive zero-gain moves before any payoff) still
defeats it. This is the new disclosed boundary. The natural next adversary
is T-ADV6: a family whose optimal form requires two zero-gain LT moves
before payoff (e.g., a 3-threshold non-monotonic pattern where each single
threshold gains 0). If T-ADV6 defeats K=2, the honest responses are K=3
(with cubic simulation cost, likely breaching COSTCEIL) or the beam-search
follow-up from section 4.

## 6. Implementation prereg requirements

Any builder implementing this design must preregister (before code) with:

1. **Frozen-battery regression**: the BRIDGE-TESTED battery
   (`ebdc4fd3e` raw output) must re-run byte-identical, or any divergence
   must be carried by transparent amendment with per-family justification.
   Rationale: the lookahead diverts the search path whenever a plateau
   move unlocks strictly more than the best immediate move; on
   greedy-friendly families (G, H, K, T-ADV4) this could in principle
   change a currently passing trace.
2. **M1-M4 re-audit** on the modified source (no new semantic cases, no
   new construction operators, `teval` unchanged).
3. **K4 pure-Zag** (shell, znc, grep, diff only; zero Python at every
   stage), 3/3 byte-identical determinism, zero em/en-dash bytes in loop
   docs (use `worker_snippets/check_no_dash.sh`).
4. **T-ADV5 re-run** under the sealed re-eval protocol
   (`tadv5_reeval/PREREG_TADV5_REEVAL.md` as template): predicted outcome
   is exact fit with the 2-threshold form at cost <= 108. STRONG PASS bars
   apply as frozen in `T_ADV5_DESIGN.md` section 5.1.
5. **Cost ledger**: report per-iteration simulation counts so the narrowed
   headroom is measured, not assumed.

## 7. Kill bars for this design task

- K1 (design complete): PASS. Rule (3.1), worked example (3.2), cost (3.3),
  determinism/blast radius (3.4), rejected alternatives (4), honest
  boundary (5), and implementation prereg requirements (6) are specified.
- K2 (addresses myopia): PASS. The rule directly targets the diagnosed
  mechanism: a positive-gain trap move is overridden if and only if a
  zero-gain move unlocks a strictly larger follow-up gain. The T-ADV5
  worked example shows the exact trace flipping from EQ,EQ,HONESTFAIL to
  LT,LT,exact-fit.
- K3 (no implementation): PASS. No `.zag` written or modified; no binary
  built; no evaluation run.

Verdict: GREEDY-DESIGN-COMPLETE.
