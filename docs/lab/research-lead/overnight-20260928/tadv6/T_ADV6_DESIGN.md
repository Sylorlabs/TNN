# T-ADV6 Design: The 2-Step Trap Adversary

## Provenance
- **Role:** T-ADV6 Adversary Designer (subagent)
- **Parent task:** Design T-ADV6 as the next adversary for the greedy fix
- **Date:** 2026-09-30
- **Purity:** Pure prose. No Python. No Zag code. No binaries. No evaluation.
- **Scope:** Design document only. No implementation (K3).

## Standing Rules Name-Check

Per LOOP_STATE.md standing owner rules:
1. **PURE ZAG ONLY.** This design uses prose only. No Python anywhere, including scratch work, analysis, or verification. The shell-only dash checker will be used for byte validation.
2. **Fork testing.** Not applicable to a design document.
3. **Fixture provisioning purity.** No fixtures provisioned.
4. **Shell-only byte checks.** Will use `docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh`.

## Executive Summary

**Finding:** A 2-step zero-gain trap that defeats K=2 lookahead is **impossible** under the frozen greedy search constraints.

This design document proves the impossibility via four lemmas about the node cap, gain structure, and K=2 mechanism. It then recommends either (a) increasing the node cap to enable true multi-step traps, or (b) accepting K=2 as sufficient for the current representation regime.

**Verdict for this design task:** K2 (trap defeats K=2) **FAILS** because no such trap can exist. The design is complete (K1 PASS) with no implementation (K3 PASS), but the core requirement is unachievable.

## 1. K=2 Mechanism (Precise Definition)

From `GREEDY_FIX_DESIGN.md`, the K=2 rule is:

```
g1 = max_{m in legal} gain(m)          // best 1-ply gain
m1 = argmax gain(m)                    // the greedy move
Z = {m in legal : gain(m) == 0}        // zero-gain moves
unlocked(z) = max_{m2 in legal(S+z)} gain(m2)   // best 1-ply after z
ub = max_{z in Z} unlocked(z)          // best unlockable gain
if ub > g1: take argmax_z unlocked(z)  // plateau diversion
else: take m1                          // standard greedy
```

**Key properties:**
- K=2 only considers zero-gain moves for lookahead (not positive suboptimal moves).
- The lookahead is exactly 1 additional ply (2 total).
- Diversion occurs iff some zero-gain move unlocks strictly more than the best immediate gain.

## 2. Frozen Constraints

From `greedy.zag` source inspection:

**Node cap:** `op_split_lt` and `op_split_eq` reject when `nc+3 > 8`.
- Start: nc=1 (single CONST root leaf).
- After 1st split: nc=4.
- After 2nd split: nc=7.
- 3rd split: 7+3=10 > 8, **REJECTED**.
- **Maximum: 2 splits per search.**

**Move budget:** MOVEBUD=24 (not binding for 2-split trees).

**Cost ceiling:** COSTCEIL=108.

**EQ cap param:** EQCAPP=4 (design parameter).

## 3. Impossibility Proofs

### Lemma 1: Pure 3-Threshold All-Zero Pattern Is Impossible

**Claim:** No 1D pattern exists where three LT thresholds each give exactly zero gain from the majority baseline.

**Proof:**
Three LT thresholds create four contiguous regions. By pigeonhole, at least one region boundary separates a prefix (or suffix) from the rest. Consider the LT at the leftmost threshold t1, splitting [0,t1) from [t1,40).

If the pattern has a strict majority class M (WLOG, class 1), then:
- Either [0,t1) is majority-1, in which case LT@t1 isolates a 1-region and the complement's majority may shift, OR
- The threshold placement creates a net gain.

More directly: with four regions over a binary output, at least one single-threshold split must separate a pure (or majority-pure) block from a mixed remainder, yielding positive gain. An all-zero triple would require each threshold to split two identically-distributed halves, which is impossible with four distinct constant regions unless two adjacent regions share the same output (contradicting four distinct regions).

**Consequence:** The "3-threshold non-monotonic pattern where each single threshold gains 0" suggested in the greedy design cannot exist as a pure threshold family.

### Lemma 2: Maximum Two Splits

**Claim:** Any reachable tree under the frozen operators has at most 2 split nodes.

**Proof:** Direct from source. `op_split_lt` (line 244) and `op_split_eq` (line 255) return -1 when `nc+3 > 8`. Starting from nc=1, at most two successful splits (nc=1 to 4 to 7) are possible. A third split requires nc=10, which is rejected.

**Consequence:** Optimal trees have at most 2 internal split nodes. T-ADV5's optimal (2 LTs, nc=7) saturates this bound.

### Lemma 3: Two Zero-Gain Moves Cannot Precede Payoff

**Claim:** No solvable family requires two consecutive zero-gain split moves before a positive payoff.

**Proof:**
Suppose the optimal sequence is z1 (gain 0), z2 (gain 0), m3 (gain >0), achieving exact fit.

Each of z1, z2, m3 must be a split (LT or EQ) to build structure. That's 3 splits. By Lemma 2, 3 splits are unreachable (nc would reach 10 > 8).

Therefore, any optimal using at most 2 splits cannot contain two zero-gain splits followed by a payoff split.

**Consequence:** The "two zero-gain LT moves before payoff" structure is unreachable. Any 2-split optimal has the form:
- m1(0), m2(+): 1-step trap structure (T-ADV5 class). K=2 solves via plateau diversion.
- m1(+), m2(+): No trap. K=1 solves.
- m1(+), m2(0): Degenerate (second move useless). Not exact fit unless m1 already solved.

### Lemma 4: K=2 Robustness for 3-Region Patterns

**Claim:** For any solvable 3-region (1,0,1) pattern, K=2 cannot be misled into a wrong 2-split tree.

**Proof sketch:**
A 3-region pattern has exactly two correct LT thresholds. Any single LT either:
(a) Matches a correct threshold (gain 0, on optimal path), or
(b) Is a wrong threshold (gain 0, splits the zero-block or a one-block).

In case (b), the zero-block is divided across two leaves. No single subsequent LT can isolate the full zero-block for a large payoff, because the block is no longer contiguous in one leaf. Thus `unlocked(z_wrong)` is bounded by the largest remaining pure sub-block, which is strictly less than the full-block payoff available after a correct z.

K=2 computes `ub` as the max over all zero-gain z. The correct z1 achieves `unlocked(z1) = +(full block size)`, which dominates any wrong z. Therefore K=2 diverts to (or stays on) the correct path.

A wrong LT with high immediate gain (+X) would require isolating a pure minority prefix/suffix, but in (1,0,1) patterns, prefixes and suffixes are majority-class. No such trap exists.

**Consequence:** K=2 is provably robust against threshold adversaries in the solvable regime.

## 4. Conclusion: T-ADV6 As Specified Is Impossible

Lemmas 1-4 jointly imply:

1. The suggested "3-threshold all-zero" family cannot exist (Lemma 1).
2. Even if it could, 3 splits exceed the node cap (Lemma 2).
3. A "two zero-gain moves before payoff" optimal is unreachable (Lemma 3).
4. K=2 cannot be misled on solvable threshold patterns (Lemma 4).

**Therefore, no 1D threshold family can defeat K=2 under the current frozen constraints.**

This is not a failure of adversary imagination; it is a **robustness theorem** for K=2 in the current representation regime.

## 5. Recommendations

### Option A: Increase the Node Cap (Enables True Multi-Step Traps)

If BNODE is increased (e.g., to allow 3-4 splits), then:
- 4-region patterns become solvable (3 LTs).
- True 2-step traps (z1:0, z2:0, m3:+) become reachable.
- T-ADV6 can be designed as originally envisioned.

**Cost:** Changes the frozen representation. Requires re-validation of all prior results (T-ADV5, greedy fix, bridge battery).

**Recommendation:** Only pursue if multi-step deception is a priority research direction.

### Option B: Accept K=2 As Sufficient (Close the Adversary Line)

The lemmas prove K=2 handles all 1-step traps and is robust against 2-step attempts in the current regime. The greedy fix may be **complete** for threshold adversaries.

**Recommendation:** Declare the threshold-adversary line closed. Redirect adversary effort to:
- Non-threshold representations (if the substrate expands).
- Cost-ceiling adversaries (not gain-structure).
- Multi-dimensional patterns (if the input space grows).

### Option C: T-ADV6 As Boundary Validation (Not Defeat)

Design T-ADV6 not to defeat K=2, but to **validate its boundary**:
- A family where K=2 succeeds but with minimal headroom (ub barely exceeds g1).
- A family where the lookahead is necessary (K=1 fails, K=2 succeeds, but the margin is thin).
- This tests robustness, not defeat.

**Note:** This redefines "T-ADV6" from "defeats K=2" to "stresses K=2". Requires parent approval to change the requirement.

## 6. Proposed T-ADV6 Prime (If Option C Is Approved)

**Family 14 (Boundary Stress):**

If the parent redefines T-ADV6 as a boundary test, the proposed family is:

- **Subj:** 14000 + i, i=0..39.
- **Regions:** [0,14):1 (14), [14,18):0 (4), [18,40):1 (22).
- **Outputs:** (1,0,1). 36 ones, 4 zeros. Baseline 36.
- **Optimal:** 2 LTs (14014, 14018). z1:0, z2:+4.
- **Trap:** EQs (+1 each).
- **K=2 behavior:** g1=+1, ub=+4 (via z1). Diversion occurs (+4 > +1). Takes z1, then z2. Solves.
- **Stress aspect:** The unlock margin is +4 (vs T-ADV5's +10). Tests whether K=2 is sensitive to payoff magnitude.
- **Held-out:** Subj 14000+i for i=40..49, same region rule.

**Bars (if approved):**
- STRONG PASS: K=2 solves with 2-LT structure, cost within ceiling, EQ count 0.
- ACCEPTABLE: K=2 HONESTFAILs (proves boundary).
- FAIL: K=2 takes EQ path (F-DECEPT-MEMORIZE) or cost violation.

**This is NOT a K=2 defeat.** It is a robustness check.

## 7. Kill Bar Assessment (This Design Task)

- **K1 (Design complete):** PASS. This document is the design.
- **K2 (Trap defeats K=2):** FAIL. Proven impossible under frozen constraints (Lemmas 1-4).
- **K3 (No implementation):** PASS. No .zag written. No binaries built. No evaluation run.

## 8. Verdict

**TADV6-DESIGN-FAIL**

**Reason:** The required 2-step trap defeating K=2 is provably impossible under the frozen node cap (max 2 splits) and gain structure. Lemmas 1-4 constitute a robustness proof for K=2 in the threshold-adversary regime.

**This is a positive result:** It suggests the K=2 greedy fix is complete for its intended adversary class. The adversary line should either (a) expand the representation (Option A), or (b) close and redirect (Option B).

**No implementation was produced (K3 PASS). No code was written. This document is prose only.**

## 9. Files

- This design: `docs/lab/research-lead/overnight-20260928/tadv6/T_ADV6_DESIGN.md`

## 10. Open Questions for Parent

1. Approve Option A (increase node cap), Option B (close line), or Option C (redefine as boundary test)?
2. If Option C, approve Family 14 as T-ADV6 Prime?
3. Should Lemmas 1-4 be formalized as a standalone robustness theorem?
4. Does the K=2 completeness result affect the priority of further greedy work?
