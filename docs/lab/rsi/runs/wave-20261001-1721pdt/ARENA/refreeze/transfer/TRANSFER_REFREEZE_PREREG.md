# FROZEN PREREG: Transfer refreeze against the REAL frozen TNN-2 binary

Status: FROZEN PREREG. Written before any implementation. Any change
requires a dated amendment written before the changed code runs.
Date: 2026-10-01 PDT
Worker: ARENA lane replacement worker, wave-20261001-1721pdt
Lane dir: docs/lab/rsi/runs/wave-20261001-1721pdt/ARENA/refreeze/transfer/

## 0. Discrepancy note (parent instruction governs)

PREREG_TRANSFER.md (wave-20261001-1421pdt, arena_transfer lane) defines its
learner as a minimal SIMULATED learner (checklist of four hypothesis
forms). Its kill bars K2 (checklist wipe) and K3 (verbatim-lookup storage
control) are mechanics of that simulated learner and cannot be literally
rerun against a different learner. The parent instruction for this lane
requires refreezing against the REAL frozen TNN-2 binary (hash-verified
below), BLOCKED rather than simulated substitution, and documentation of
the discrepancy where the protocol text conflicts. This prereg therefore
ports the transfer protocol (same worlds, same conditions structure, same
scoring, same kill-bar intent) to the real TNN-2 binary via its public
interface. The simulated-learner 0.3333 remains a protocol-validation
score with zero evidential weight for TNN-2.

## 1. Claim under test

Transfer, operationalized as: a structure learned by TNN-2 during a LEARN
phase on world A improves later cognition on world B, where A and B are
materially different (different surface form, different law family).
Behavioral probe of C0-D (cognitive reuse). Scoring: examples-to-criterion
on B with A-experience, divided by examples-to-criterion of a fresh
control. S = 1 - (T_B / F_B), clipped to [0, 1]. Positive means transfer
helped. This does not move the canonical 0.573. A positive result is a
CANDIDATE for TNN-2 only.

## 2. Frozen TNN-2 binary identity

- Path: docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2_bin
- SHA-256: 6044f91f8fe35e307e1d6f73a4ee73bffb930fa0a16a9c899048a086d0d5f77b
  (matches CORE_FREEZE_TNN2_PREREG.md frozen record; verified by this
  worker before any run)
- Driver: docs/lab/research-lead/overnight-20260928/core_freeze_tnn2_shim/freeze_shim2_bin
- SHA-256: 9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954
  (matches frozen shim record; zero-cognition transport per SHIM_REPORT.md)
- Invocation: freeze_shim2_bin <world.txt> <state.bin>; world events are
  OBSERVE s r o / QUERY s r e (ASCII integers, negatives allowed);
  output lines include ANSWER s r v; state is 110656 bytes, loaded when
  present, written after each successful run. Neither binary is modified.

## 3. Worlds (identical sequences to PREREG_TRANSFER.md, ported exactly)

World A (LEARN): 24 training + 12 held-out arithmetic progressions
t(n+1) = t(n) + c. Training (start, c, len):
(3,3,5) (14,3,6) (-5,3,7) (22,3,5) (40,3,6)
(2,7,5) (-11,7,6) (30,7,7) (8,7,5)
(20,-4,5) (5,-4,6) (-3,-4,7) (33,-4,5)
(1,12,5) (-20,12,6) (15,12,7)
(50,-9,5) (12,-9,6) (-15,-9,7)
(7,5,5) (-8,5,6) (19,5,7) (26,5,5) (13,5,6)
Held-out: (100,3,5) (-30,3,6) (45,7,5) (-25,7,6) (60,-4,5) (-40,-4,6)
(70,12,5) (-50,12,6) (90,-9,5) (-60,-9,6) (55,5,5) (-35,5,6)

World B (TRANSFER): 24 training + 12 held-out geometric progressions
t(n+1) = r * t(n). Training (start, r, len):
starts 2..12, r=2, len=5 (11 seqs); starts 2..6, r=2, len=6 (5 seqs);
starts 2..8, r=3, len=5 (7 seqs); (2,3,6) (1 seq).
Held-out: starts 13..18, r=2, len=5 (6); starts 7..8, r=2, len=6 (2);
starts 9..11, r=3, len=5 (3); (3,3,6) (1).

World A surface: decimal integer tokens. World B surface: letter-code
tokens per the briefing code table (base-26). The decoder is interface
machinery applied in the generator (identical to the original protocol);
TNN-2 receives decoded integers. Material difference is verified at the
raw-string level (K5a) and law level (K5b), same as the original.

## 4. Event encoding (frozen)

Relations (interface machinery, shared across worlds): P1=11, P2=12,
P3=13, P4=14, P5=15, P6=16 (position relations), NEXT=20.
Sequence ids: A-train 1001..1024, A-heldout 1101..1112,
B-train 2001..2024, B-heldout 2101..2112,
X-scrambled-A-train 3001..3024. All id ranges disjoint by construction.

Per training sequence (id S, terms t[0..L-1], L in 5..7):
  OBSERVE S P1 t0
  ...
  OBSERVE S P_{L-1} t_{L-2}
  QUERY S NEXT t_{L-1}
  OBSERVE S NEXT t_{L-1}     (teaching signal: the correct answer as experience)
Per held-out sequence (id S): same OBSERVEs and QUERY, but NO teaching
OBSERVE (query only, on a state checkpoint copy; main state untouched).

A QUERY passes the expected answer per the frozen shim protocol
(ev_query verification semantics); the scored value is TNN-2's returned
ANSWER. A miss returns the -2 sentinel and counts as wrong.

## 5. Online protocol and criterion (frozen)

Training sequences arrive one at a time, each as one shim invocation on
the persistent state file. After each step: if ANSWER equals the target,
consecutive++. Else consecutive = 0. When consecutive reaches V = 3:
copy the state file to a checkpoint; run the 12 held-out queries against
the checkpoint copy (fresh held-out ids each check); if 12/12 correct,
criterion met, examples-to-criterion = steps consumed; else consecutive =
0 and training continues on the main state. Cap: 24 training steps; if the
cap is hit without criterion, examples-to-criterion = 24 and met = 0.
V = 3, caps 24/24, identical to the original protocol.

## 6. Conditions (frozen)

- T (transfer): A phase with the criterion protocol on state_T; then B
  phase with the criterion protocol on the SAME state_T (persistent
  learner state across the phase boundary). Measure T_B (B examples) and
  T_met. Also record T_A / T_A_met.
- F (fresh): B phase with the criterion protocol on a fresh state_F.
  Measure F_B, F_met.
- X (ablated exposure): A phase on SCRAMBLED A (same 24 A surfaces, terms
  within each sequence permuted by the fixed deterministic permutation
  p(i) = (3*i+1) mod L, which destroys the arithmetic law; law-rejection
  verified in K5c), 24 steps, observe/query/teach exactly as T's A phase
  but with NO criterion check (pure exposure), on state_X; then B phase
  with the criterion protocol on the same state_X. Measure X_B, X_met.
  Rationale: X isolates law-learning from mere exposure/interface warmup.
  X always runs the full 24 scrambled steps; if T_A < 24 this gives X more
  exposure, which is conservative for K2 (more exposure can only help X).

The original M (storage) condition is not ported: it tested the simulated
learner's verbatim-lookup failure mode. For TNN-2, verbatim
cross-condition retrieval is impossible by construction (disjoint seq ids,
disjoint surfaces per K5), so anti-memorization is verified structurally
in K3/K5 instead of by a separate degenerate-learner condition.

## 7. Scoring (frozen)

S = 1 - (T_B / F_B), reported x10000 as an integer, clipped to [0, 1]
(negative clipped to 0). Identical to the original protocol.

## 8. Frozen kill bars

- K1 TRANSFER GAIN: S >= 0.25.
- K2 ABLATION ATTRIBUTION: |X_B - F_B| / F_B <= 0.10 AND X_B > T_B.
- K3 ANTI-MEMORIZATION: structural. All A/B/X seq id ranges disjoint;
  A-train and B-train raw surfaces share zero tokens (K5a); therefore no
  correct B prediction can be a verbatim retrieval of an A observation.
  Verified in the generator and reported.
- K4 DETERMINISM: 3/3 full runs (all conditions) byte-identical full logs
  (cmp). The shim/TNN-2 path is deterministic per the freeze eval record.
- K5 MATERIAL DIFFERENCE: (a) zero shared tokens between A-train and
  B-train raw surface strings, verified in-run; (b) the A-law (constant
  differences) rejected on all 36 B sequences and the B-law (constant
  exact integer ratios) rejected on all 36 A sequences, verified in-run;
  (c) the A-law rejected on all 24 scrambled-A sequences (scramble
  validity), verified in-run.
- K6 CRITERION VALIDITY: T_A met within 24 AND F_B met within 24;
  otherwise the comparison is VOID (no learned A structure, or no valid
  fresh baseline).
- K7 PURE ZAG: generator and scorer are znc-compiled Zag; bash only
  sequences shim invocations and parses logs; no python/python3 or any
  other interpreter anywhere in the lane; no .py files in the lane.
- K8 NO-CONFOUND: identical B briefing, B training order, and B held-out
  set across T/F/X; the only difference entering B is the A-phase
  experience in the persistent state.

Verdict mapping: K1..K8 all PASS gives a CANDIDATE transfer score S for
TNN-2 (does not move the canonical 0.573). Any bar FAIL gives per-bar
FAIL. K6 FAIL gives VOID.

## 9. Architecture accounting (frozen expectations)

- TNN-2 source touched: none. Shim untouched (hash-verified).
- Cognition source lines added: generator + scorer (a few hundred lines),
  all inside this lane directory, evaluator-only.
- New hardcoded semantic cases: 0. New modes: 0. New bridges: 0.
- New routers: 0. New task-specific handlers: 0.
- Learner-state structures created: whatever TNN-2 itself constructs in
  its 110656-byte workspace during the phases (evaluator creates none).

## 10. Honest boundaries

- This ports the transfer measurement to TNN-2's public
  OBSERVE/QUERY interface. If TNN-2 cannot perform next-term prediction
  on these sequence families at all, K6 yields VOID; that is an
  informative negative (no transfer measurable), not a failure of the
  apparatus, and it would independently corroborate the
  TRANSFER_ANALYSIS.md finding (no demonstrated C0-D reuse).
- The decoder (letter-code to integer) is briefing interface machinery,
  identical across conditions, never counted as learned.
- No L3 claim is made or implied by any outcome here.

FROZEN 2026-10-01 PDT. Implementation begins only after this file is written.
