# PREREG: L3-NIV2 Wave 3 (CALR)

Status: WAVE-3-PREREG-FROZEN 2026-10-02, before any wave-3 implementation
exists. This document is never edited after freezing. Any change requires
a new prereg. The frozen design prereg (affe2c3eb, PREREG.md) is untouched
and still governs; this wave-3 prereg freezes only the search-mechanism
fix, the diagnosis, and the wave-3 kill bars. K1 through K12 and KC0A
through KC0D are not weakened.

Commit-order self-check: the freeze commit contains PREREG_WAVE3.md and
the wave-3 Step 0 update to NAMECHECK.md ONLY. No wave-3 .zag source, no
binary, no run log exists at freeze time.

Worker: L3-NIV2 wave-3 worker (subagent, 2026-10-02). Replacement for the
completed wave-2 worker. Task: solve the wave-2 search-adequacy failure.

## 1. Background

Wave 1: PROCESS-FAIL (python3) plus BUILD-FAIL (select_beam panic).
Wave 2 (commit 4ea8b5fbe): panic root-caused to a worker bug (undersized
buffers in expand_level), fixed. T1 then runs clean (rc=0, no panic) but
DEFERS on DEV-S1 (y = x^2 + x, refprog
[CPY r1,r0][MUL r0,r0][ADD r0,r1], length 3).

Wave-2 search investigation: every length-3 solution must pass through the
score-1 prefix [CPY r1,r0][MUL r0,r0] (wave-2 pool id 913). Among 2109
distinct (first,second)-instruction pairs at score 1, it ranks 326 by
min-id. Four beam variants were tried (score-greedy, score-stratified,
syntactic (first,second) grouping, behavioral-signature grouping); ALL
DEFER. The 2109 to 80 cut (96 percent pruned) cannot retain a rank-326
prefix. Verdict: BUILD-FAIL on K1 (T1 must COMMIT). This is a
search-adequacy failure, not a bug.

## 2. Diagnosis

### D1: The scoring function is blind to latent register state

The construction search scores every candidate as a COMPLETE program: the
training ACCEPT count of its output register r0. The crucial prefix
P = [CPY r1,r0][MUL r0,r0] leaves r0 = x^2, which matches the target
y = x^2 + x only at x = 0, so P scores 1 of 6.

But P's value is not in r0. It is in the LATENT STATE: r1 = x is preserved
alongside r0 = x^2, so one further instruction ([ADD r0,r1]) completes the
solution. The scoring function observes only r0, so P is indistinguishable
from the other 2108 score-1 prefixes, most of which carry useless latent
state (for example [MUL r0,r0][MUL r0,r0] leaves r0 = x^4 with r1 = 0,
r2 = 0, r3 = 0: no register holds x, so no 1-step extension can reach the
target, yet it scores the same 1 of 6).

The rank 326 comes from min-id ordering among score-1 pairs, an artifact
of generation order that carries zero information about extendability.

### D2: Deceptive search, no score gradient toward P

Because score measures only output-register match, the fitness landscape
over prefixes has no gradient toward P: P's value becomes visible only
AFTER extension. Any retention criterion derived from score (all four
wave-2 variants) must prune P whenever the quota cuts below rank 326.

Wave-2 variant 4 (behavioral signatures) is the sharpest evidence for D1:
it groups candidates by r0-outputs on training inputs, so P collides with
programs like [MUL r0,r0][CPY r0,r0] (identical r0 = x^2 signature, but
latent r1 = 0 instead of r1 = x). The group keeps one representative by
id, not by latent-state utility. Output-behavior grouping is therefore
structurally incapable of seeing what makes P crucial.

### D3: What CAN see P

P is distinguished by a counterfactual property: "does there exist a
1-step extension whose outputs match the consequence-derived target?"
That property is a function of the FULL register state, not of r0 alone.
The target itself is not given, but the learner can derive a partial
target map fhat from its own consequence history: whenever the learner's
own TEST(x, y) is ACCEPTed, the learner knows f(x) = y through the
consequence channel (learner commitment to world consequence to
learner-owned evaluation; this is the section 6 chain, and the C1 control
already harvests accepted (x, y) pairs the same way). No expected value
crosses the channel; fhat is computed inside the learner from ACCEPTs.

Potential(P) = max over the 80 appends of local agreement between the
extended program's outputs and fhat on known inputs. This is pure local
simulation (zero TEST cost). P's latent state (x, x^2) is exactly what
makes a 1-step full-fhat match possible; most other score-1 prefixes'
latent states do not admit one.

## 3. Falsifiable predictions

P1 (rank): Let SR be the rank of the crucial prefix (bytes
00 01 00 02 00 00, the wave-2 P) by (score desc, id asc) among all 6400
depth-2 append prefixes, and PR its rank by (potential desc, score desc,
id asc) over the same set. Prediction: PR <= SR/2 (integer division).
Rationale: if potential genuinely sees latent-state utility that score
cannot, it must rank P at least twice as well as score does. Both ranks
are computed and traced in the run.

P2 (efficiency): Phase C (ordered verification, section 4) reaches a
full-acceptance length-3 program after verifying fewer than 2000 prefix
candidates. Rationale: the mechanism must fit comfortably inside
B_CONSTRUCT = 50,000 TESTs (Phase A costs roughly 12K TESTs; 2000
candidates at roughly 9 TESTs each keeps the total under 31K).

## 4. Mechanism: CALR (Consequence-Anchored Lookahead Retention)

CALR replaces the beam for base construction (transfer = 0). It has three
stages and NO beam, NO level quotas, NO score stratification, and NO
pruning of prefixes by score.

Phase A (harvest, consequence channel): evaluate all 80 length-1 seeds and
all 6400 length-2 appends through the consequence channel (eval_prog,
with its existing early-exit). As a side effect, every ACCEPT records
fhat[input] = output (new cfg fields; gated by a flag set only during
CALR). No prefix is pruned: all 6480 stay in the pool with exact scores.

Phase B (potential, local, zero TESTs): for each of the 6400 depth-2
prefixes, simulate the full 4-register state on each training input
(local isa_regs, zero TEST cost), then compute potential = max over the
80 appends of agreement with fhat on known inputs.

Phase C (ordered verification, consequence channel): verify prefixes in
(potential desc, score desc, id asc) order with NO sort (bucket loops).
For each prefix, recompute its argmax extensions (the appends achieving
max potential, in byte order) and TEST each through the consequence
channel until one reaches full training acceptance or the argmax set is
exhausted, then move to the next prefix. Stop at the first full
acceptance (documented search-stop rule, section 8), or when the TEST
budget exhausts. Every promotion decision (full acceptance) is a training
ACCEPT count through the consequence channel, exactly as the frozen
prereg requires.

### Why CALR is not a fifth beam variant

A beam variant keeps the level-by-level generate, rank, quota-cut
structure and changes only the ranking key. CALR has no levels, no
ranking cut, and no retained set: every depth-2 prefix survives to Phase
C; potential only ORDERS the verification sequence, and verification is
lazy (stops at first success). The structural difference is
prune-then-extend (beam) versus keep-all, order-by-lookahead,
verify-lazily (CALR). The anti-V2 mandate in the frozen prereg ("the
construction loop must retain zero- or negative-immediate-gain extensions
whenever bounded lookahead shows eventual full acceptance") is what CALR
implements: the old lh2 rescue applied lookahead to 5 hand-picked
children; CALR applies 1-step lookahead to all 6400 prefixes and verifies
in lookahead order.

## 5. Frozen design-prereg compliance

- 4(a): 0 new opcodes, 0 new semantic cases, 0 new modes/bridges/handlers.
  isa_regs is a local simulator over the frozen 5-op ISA, the same class
  of zero-TEST-cost local execution wave-2 already used (prog_sig6).
- 4(c): propose-and-test over COMPLETE candidates; scoring is the training
  ACCEPT count through the consequence channel (eval_prog). Potential is
  an ordering heuristic for retention, not a promotion score; no
  per-step positive-gain requirement appears anywhere (nothing is pruned
  by score at all). Operators used in T1 construction: APPEND. SUBSTITUTE
  and TRUNCATE remain the revision operators (revise, unchanged). Every
  length-2 program is already an append-child, so SUBSTITUTE adds no new
  depth-2 prefix; this is recorded for red-team review under K10.
- A1/firewall: fhat is derived inside the learner from its own
  TEST/ACCEPT history. The protocol log shows only TEST/ACCEPT/REJECT;
  no expected value crosses the channel. Audit A-INFO remains satisfiable
  by protocol-log plus source inspection.
- V2: satisfied by construction (see section 4, final paragraph).
- KC0B: Phase A evaluates (not just generates) all length-2 programs.
  This is disclosed: C4 (exhaustive length-2 enumeration) is the control
  that must FAIL, and it does fail here (no length-2 program fully
  accepts, per G1a). The SOLUTION (length 3) is never enumerated: Phase C
  verifies length-3 programs lazily in potential order and stops at the
  first full acceptance, typically after a small fraction. Whether this
  satisfies "the construction enumerates no candidate family" is left for
  the K10 red team to adjudicate; the trace records exactly what was
  enumerated, evaluated, and verified.
- Budgets: B_CONSTRUCT = 50,000 TESTs unchanged; the existing do_test
  budget guard enforces it. Determinism: all loops are fixed-order, no
  RNG; 3 of 3 byte-identical logs required (W3K2).
- arm_t1 is unchanged except that construct() dispatches to CALR when
  transfer = 0. Transfer mode (T4) and revise (T3) keep the existing beam
  path (known limitation, section 8).

## 6. Frozen kill bars (wave 3)

- W3K1: T1 COMMITS on DEV-S1 (the frozen K1). The committed program must
  reach the commit step via the CALR path with a full CONSTRUCT event
  chain in the trace.
- W3K2: 3 of 3 byte-identical run logs for the T1 arm (sha256).
- W3K3 (diagnosis bar): PR <= SR/2 for the wave-2 crucial prefix (bytes
  00 01 00 02 00 00), both ranks traced as CALR-RANK. If W3K1 passes but
  W3K3 fails, the mechanism worked for the wrong reason (potential did
  not discriminate; the lazy scan did).

## 7. Verdict logic

- W3K1, W3K2, W3K3 all green: BUILD-PASS. Diagnosis supported.
- W3K1 red: BUILD-FAIL (search still inadequate). Report where CALR
  stopped (Phase A cost, fhat coverage, PR/SR, verifications used).
- W3K1 green, W3K3 red: DIAGNOSIS-FALSIFIED. Report honestly; the
  mechanism is kept as an engineering result but the D1/D3 explanation
  is rejected.
- W3K2 red: DETERMINISM-FAIL; investigate before any verdict.

## 8. Known limitations (honest)

- CALR as implemented covers depth 3 only (seeds to depth-2 prefixes to
  verified depth-3). Solutions of length 4 to 6 (allowed by the battery)
  need staged deepening; that is wave-4 work. T5a/T5b/C5 are not
  re-validated this wave.
- Phase C stops at the first full-acceptance program rather than
  collecting the full hypothesis set. For T1 this satisfies the commit
  path; the interaction with the section 6 sole-survivor rule under
  genuine ambiguity (T5b) is deferred to wave 4.
- T4 (transfer) still uses the old beam construct; T3 revise is unchanged.
- If fhat is empty (no ACCEPT in Phase A), potential is 0 for all and
  Phase C degrades to a score-ordered scan bounded only by the TEST
  budget. For DEV-S1, seeds alone guarantee fhat covers x = 0 and x = 1.
