# PREREG: L3-NIV2 Wave 4 (2S-CALR staged deepening)

Status: WAVE-4-PREREG-FROZEN 2026-10-02, before any wave-4 implementation
exists. This document is never edited after freezing. Any change requires
a new prereg. The frozen design prereg (affe2c3eb, PREREG.md) is untouched
and still governs; the wave-3 prereg (754f33d1c, PREREG_WAVE3.md) still
governs stage 1. This wave-4 prereg freezes only the staged-deepening
design, the diagnosis, the depth-4 target, and the wave-4 kill bars. K1
through K12 and KC0A through KC0D are not weakened. The 5-op ISA is not
widened. No beam quotas are introduced.

Commit-order self-check: the freeze commit contains PREREG_WAVE4.md and
the wave-4 Step 0 update to NAMECHECK.md ONLY. No wave-4 .zag source, no
binary, no run log exists at freeze time.

Worker: L3-NIV2 wave-4 worker (subagent, 2026-10-02). Replacement for the
completed wave-3 worker. Task: extend CALR beyond depth 3 (staged
deepening), the honest limitation recorded in REPORT_WAVE3.md section 8.

## 1. Background

Wave 1: PROCESS-FAIL (python3) plus BUILD-FAIL (select_beam panic).
Wave 2: panic fixed; BUILD-FAIL on search adequacy (beam pruned the
crucial prefix, rank 326/2109).
Wave 3 (e61c9c50c): CALR (Consequence-Anchored Lookahead Retention)
replaced the beam for base construction. Three phases, no beam, no
quotas, no pruning: Phase A harvests all 80 seeds and 6400 depth-2
prefixes through the consequence channel (building fhat, the
consequence-derived partial target map); Phase B computes 1-step
lookahead potential for all 6400 prefixes by local simulation (zero
TESTs); Phase C verifies prefixes in (potential, score, id) order
lazily through the channel, stopping at the first full acceptance.
T1 COMMITS on DEV-S1 ([CPY r1,r0][MUL r0,r0][ADD r0,r1], 6/6, 38,206
TESTs, 3/3 byte-identical). Verdict BUILD-PASS.

Honest limitation (REPORT_WAVE3.md section 8): CALR covers depth 3 only
(seeds to depth-2 prefixes to verified depth-3). Solutions of length 4
to 6 need staged deepening. That is this wave.

Baseline (wave-4 design time, current wave-3 code, T1 arm on DEV-S2,
y = x^2+x+1, depth-4 refprog
[CPY r1,r0][MUL r0,r0][ADD r0,r1][INC r0]): CALR-HARVEST 2 6400 7668
(fhat covers 2 inputs, 7,668 TESTs); CALR-RANK 433 1677 1497 2 2 (the
crucial depth-2 prefix [CPY r1,r0][MUL r0,r0], pool id 433, has
1-step-potential rank 1677 and score rank 1497 of 6400); CALR-DONE 0 495
50000 (0 accepted, 495 verifications, budget exhausted); ARM-END T1 FAIL
(DEFER). So the wave-3 mechanism, run to budget exhaustion, DEFERS on
the depth-4 target. The 495 verifications burned 42,332 TESTs on doomed
depth-3 candidates. Staged deepening must do better than burn-to-exhaust.

## 2. Diagnosis

### D1: 1-step potential is blind to 2-step latent utility

The depth-4 target DEV-S2 (y = x^2+x+1) has crucial depth-2 prefix P2 =
[CPY r1,r0][MUL r0,r0] (pool id 433, the same bytes as the wave-3
crucial prefix). Phase A yields fhat = {0->1, 1->3} (from [INC r0]
ACCEPT at x=0 and [INC r0][INC r0] ACCEPT at x=1; verified in the
baseline trace). P2's 1-step potential vs this fhat is 1 (best append
[INC r0] gives x^2+1, matching only x=0), while max 1-step potential
over all prefixes is 2. So P2 ranks 1677th by (potential, score, id):
1-step lookahead cannot see that P2 -> [ADD r0,r1] -> [INC r0] reaches
full fhat agreement in TWO steps. This is the exact wave-2 failure
shifted one level deeper: the crucial ancestor needs k-step lookahead
to be visible, and 1-step potential is the wrong k.

### D2: 2-step potential sees P2, and the final step is provably prunable

potential_2(P) = max over all 80x80 append pairs of fhat agreement,
computed by local simulation (zero TESTs). For P2, the pair
([ADD r0,r1],[INC r0]) yields x^2+x+1, matching all known fhat, so
potential_2(P2) = 2 = max. The 2-step lookahead sees what 1-step
cannot: P2's latent state (r0=x^2, r1=x) admits a 2-step completion.

The naive 6400-pair verification per prefix explodes (design-time probe:
49,452 TESTs for 9 prefixes, 59,868 total, over budget). The principled
prune: stage-1 Phase C is COMPLETE for depth-3 (theorem T1 below), so
when stage 2 begins, no depth-3 program fully accepts. Any depth-4
solution P+c1+c2 whose final instruction c2 does not write r0 has the
same outputs as the depth-3 program P+c1, which does not fully accept.
Therefore every depth-4 solution's final instruction writes r0 (d=0).
Restricting the nested descent's c2 to the 16 d=0 appends is a PROVABLE
prune, not a heuristic and not a quota. Design-time probe with this
prune: stage-2 uses 3,192 TESTs (9 prefixes to find), total 13,608.

### D3: The inter-stage rule is retention-by-default with
consequence-anchored ordering

Between stages, NOTHING is pruned by score or by quota. All 6400
depth-2 prefixes carry into stage 2 with their Phase-A scores and
locally recomputed potentials. The combinatorial explosion (512K
depth-3 programs) is handled by (a) zero-TEST-cost local potential
computation and (b) lazy budgeted verification in potential order,
exactly the CALR principle. What changes between stages is only the
lookahead horizon (1-step to 2-step) and the verification depth
(depth-3 to depth-4). The yield rule (section 4) is a completeness
theorem, not a quota: stage 1 yields if and only if its max-potential
level is exhausted, which proves no depth-3 solution exists.

## 3. Falsifiable predictions (from the design-time probe)

A pure-Zag probe (probe2.zag, /tmp/probe, design time only, not a
result) exactly simulates 2S-CALR on DEV-S2 using the unsealed fixture
target directly. It replicates Phase A (2-pass early-exit eval),
Phase B, Phase C1 with Y1, fhat growth, and stage 2 with the d=0
prune. It predicts:

P1 (rank): P2's rank by (potential_2 desc, score desc, id asc) is 149,
vs 1677 by (potential_1, score, id) and 1497 by (score, id). Prediction:
PR2 <= 200 in the real trace. Rationale: 2-step potential must rank the
crucial ancestor far better than 1-step potential or score.

P2 (diagnosis): In the real trace, P2 has potential_1 = 1 < 2 =
max_1 (stage-1 CALR-RANK) and potential_2 = 2 = max_2 (stage-2
CALR2-RANK). This is the wave-4 analogue of W3K3.

P3 (stage-1 cost): Stage-1 Phase C1 verifies exactly the 211
max_1-level prefixes, uses fewer than 5,000 TESTs, and finds nothing
(probe: 211 verifications, 2,748 TESTs, 0 found). Rationale: Y1 bounds
stage 1 to its complete depth-3 search; the baseline's 495
verifications were burn-to-exhaust, not Y1.

P4 (budget and commit): Stage 2 finds a depth-4 full-acceptance program
within 12 prefix expansions and total TESTs stay under 20,000 (probe:
9 expansions, 13,608 total). The probe found
[CPY r1,r0][INC r0][MUL r0,r1][INC r0] (x^2+x+1) via prefix pi=384
([CPY r1,r0][INC r0]), c1=[MUL r0,r1], c2=[INC r0]. Note this is a
valid depth-4 solution distinct from the refprog; the kill bar requires
a committing depth-4 program, not the refprog bytes.

## 4. Mechanism: 2S-CALR (two-stage CALR)

Stage 1 is wave-3 CALR VERBATIM (Phase A harvest, Phase B 1-step
potentials, Phase C ordered lazy verification), plus the Y1 yield rule:
Phase C verifies prefixes in (potential_1 desc, score desc, id asc)
bucket order and stops at the first full acceptance (COMMIT) or when
the next bucket's potential_1 drops below pmax_1 (YIELD to stage 2).
On DEV-S1 this behaves byte-identically to wave-3 (commit at
verification 229 precedes any yield).

Theorem T1 (stage-1 completeness for depth-3): if a depth-3 program S3
= P+c fully accepts on training, then potential_1(P) = nk (S3
witnesses max agreement), so P is verified in Phase C1, c is in P's
argmax set (agree = nk = max), and S3 is TESTed. Contrapositive: Y1
yield implies no depth-3 solution exists. (fhat growth during C1 does
not break this: S3 agrees with grown fhat too, so its argmax
membership persists.)

Inter-stage rule: all 6400 depth-2 prefixes, their Phase-A scores, and
the grown fhat carry into stage 2. No prefix is pruned, no quota is
applied. This is the principled retention rule: consequence-anchored
ORDERING replaces pruning.

Stage 2:
- Phase B2: recompute potential_2 for all 6400 prefixes by local
  simulation (zero TESTs) vs current fhat. If pmax_2 < nk, DEFER
  immediately (no 2-step extension matches all known consequences, so
  no depth-4 solution exists; principled early stop).
- Phase C2: verify prefixes in (potential_2 desc, score desc, id asc)
  bucket order. For each prefix P at the max_2 level: nested complete
  descent. Compute p1d0(c1) = max over the 16 d=0 appends of fhat
  agreement for P+c1 (local, vs current fhat); let maxc1 be the max.
  For each c1 (byte order) with p1d0(c1) == maxc1, for each d=0 c2
  (byte order) with agreement == maxc1: TEST P+c1+c2 through the
  consequence channel. Stop at the first full acceptance (COMMIT) or
  when the max_2 level is exhausted (DEFER).
- The d=0 restriction is the D2 provable prune (any solution's final
  instruction writes r0, else stage-1 completeness is contradicted).

Theorem T2 (stage-2 completeness for depth-4): if S4 = P+c1*+c2* fully
accepts, then potential_2(P) = nk (S4 witnesses it), so P is processed;
p1d0(c1*) = nk (c2* has d=0 and witnesses it), so maxc1 = nk and c1* is
expanded; c2* is in the d=0 argmax, so S4 is TESTed. Contrapositive:
max_2-level exhaustion implies no depth-4 solution exists.

### Why 2S-CALR is not a beam

There are no level quotas, no retained sets, no score stratification.
Every depth-2 prefix survives every stage; potential only ORDERS the
lazy verification sequence. The d=0 restriction is a provable prune
from staged completeness (D2), not a ranking cut. The Y1 yield is a
completeness theorem (T1), not a budget quota. Verification remains
lazy (stops at first full acceptance) and every promotion is a
training ACCEPT count through the consequence channel.

## 5. Frozen design-prereg compliance

- 4(a): 0 new opcodes, 0 new semantic cases, 0 new modes/bridges/
  handlers. isa_regs and the nested simulator are local execution of
  the frozen 5-op ISA (zero TEST cost), the same class as wave-3.
- 4(c): propose-and-test over COMPLETE candidates; promotion solely by
  training ACCEPT count through the consequence channel (eval_prog).
  potential_1/potential_2/p1d0 are ordering heuristics, never
  promotion scores. Operators in T1 construction: APPEND only (as
  wave-3). No per-step gain requirement anywhere.
- A1/firewall: fhat is derived inside the learner from its own
  TEST/ACCEPT history (plus the fharv_on re-enable for stage-2
  dynamic fhat, same channel, same derivation). No expected value
  crosses the channel.
- V2: satisfied by construction (T1/T2 of section 4); the old lh2
  rescue is superseded by staged lookahead over all prefixes.
- KC0B: Phase A still evaluates all length-2 programs (disclosed for
  K10 as in wave-3). No length-3 or length-4 program is ever
  enumerated: stage-1 verifies depth-3 lazily (211 of 6400 prefixes'
  argmax sets), stage-2 verifies depth-4 lazily (probe: 9 prefixes'
  nested descents). The trace records exactly what was verified.
- Budgets: B_CONSTRUCT = 50,000 TESTs unchanged, enforced by the
  existing do_test guard (shared across both stages).
- Determinism: all loops fixed-order, no RNG; 3/3 byte-identical logs
  required (W4K2).
- arm_t1 unchanged; construct dispatches to 2S-CALR when transfer=0.
  T4 (transfer=1) keeps construct_beam; T3 revise unchanged (known
  limitations).

## 6. Target fixture (frozen before implementation)

DEV-S2 (existing unsealed dev fixture, dev/DEV-S2.key): y = x^2+x+1,
train x = 0..5, held-out 6..11. Refprog
[CPY r1,r0][MUL r0,r0][ADD r0,r1][INC r0] (length 4).

Why depth 3 cannot solve it: computing x^2+x+1 needs four ingredients:
preserve x (CPY before any MUL clobbers r0), form x^2 (MUL), add x
(ADD), add 1 (INC or SET1+ADD). Three instructions cannot supply all
four: any depth-3 program either loses x before the MUL, or lacks the
+1, or lacks the +x. (Exhaustively: the only way to form x^2 is MUL
r0,r0 or MUL r0,r1 after CPY; both consume 2 instructions with the
CPY, leaving 1 instruction which can add x OR add 1 but not both;
INC/SET1-first variants give (x+1)^2 = x^2+2x+1, and no SUB exists to
correct.) The baseline confirms empirically: 495 depth-3 verifications,
0 full acceptances.

## 7. Frozen kill bars (wave 4)

- W4K1: T1 (transfer=0) COMMITS on DEV-S2 with a depth-4 program that
  reaches full training acceptance via the stage-2 path (CALR2-FOUND
  in the trace), then scores 6/6 on held-out (SCORE PASS).
- W4K2: 3 of 3 byte-identical run logs for the T1-on-DEV-S2 arm
  (sha256).
- W4K3: total TESTs within B_CONSTRUCT = 50,000 (probe predicts
  ~13.6K).
- W4K4 (no-regression): T1 on DEV-S1 still COMMITS via the stage-1
  wave-3 path; the run log is byte-identical to the wave-3 canonical
  log (sha256 5221c529905ee07d80e573ece060722fc743896b7385575d7e85e6577d1c1f02).
- W4K5 (diagnosis bar): the trace shows P2 (bytes 00 01 00 02 00 00)
  with potential_1 = 1 < 2 = max_1 (stage-1 CALR-RANK) and
  potential_2 = 2 = max_2 (stage-2 CALR2-RANK). If W4K1 passes but
  W4K5 fails, the mechanism worked for the wrong reason
  (DIAGNOSIS-FALSIFIED, not BUILD-PASS).

## 8. Verdict logic

- W4K1, W4K2, W4K3, W4K4, W4K5 all green: BUILD-PASS. Staged deepening
  works; CALR extends beyond depth 3.
- W4K1 red: BUILD-FAIL (staged deepening inadequate). Report precisely
  where it stopped using the traces: stage-1 cost vs probe (harvest
  explosion?), P2's potential_2 rank (potential computation?), max_2
  level size and nested TESTs per prefix (verification budget?).
  That diagnosis constrains wave 5.
- W4K1 green, W4K5 red: DIAGNOSIS-FALSIFIED. Report honestly; the
  engineering result stands but the D1/D2 explanation is rejected.
- W4K2 red: DETERMINISM-FAIL; investigate before any verdict.
- W4K4 red: REGRESSION-FAIL; stage-1 behavior changed. Investigate
  before any verdict.

## 9. Known limitations (honest)

- 2S-CALR covers depth 4 only. Length 5-6 solutions need a third
  stage (3-step potential); that is wave-5 work. The max_2 < nk early
  DEFER is honest about this boundary.
- The d=0 prune is complete only because stage-1 C1 is complete for
  depth-3; it does not generalize to deeper stages without the
  corresponding completeness argument.
- Stage-2's nested descent is still TEST-hungry per prefix (probe:
  ~350 TESTs per prefix); if the solution's prefix ranks deep in the
  potential_2 order on a future target, the budget binds. fhat
  strengthening is the principled fix; deferred to wave 5.
- T4 (transfer) still uses the wave-2 beam engine via the dispatcher;
  T3 revise unchanged. KC0B adjudication stays with the K10 red team.
- Phase C1's dynamic argmax (recomputed vs grown fhat per prefix) is
  retained from wave-3; the Y1 yield level is fixed from Phase-B
  potentials. This asymmetry is disclosed.
