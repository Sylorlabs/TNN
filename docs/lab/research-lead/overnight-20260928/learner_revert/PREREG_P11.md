# PREREG: Law-Revert Integration (P11 episode) FROZEN

Date: 2026-09-30 PDT. Worker: Law-Revert Integration Worker.
Status: FROZEN before any implementation exists. This prereg is committed
alone; the implementation follows only after the prereg commit.

## Goal

Port the C1 law-revert fix into the composed continuing learner
(LEARNER-INTEGRATION-PASS, d1305bd43) as a P11 episode: the learner must
survive a law change AND its revert inside one lifetime, in one binary,
one 32768-byte state, no resets. This is pure composition of frozen
pieces; no new mechanism is introduced.

## Frozen inputs (read, not modified)

1. Composed learner: integrate_learn.zag at d1305bd43 (1097 lines). P1-P8
   stress battery verbatim; P9 M1 causal episode (ADAPT, mode 2) with
   persistence as rule-store facts earned 3x to importance 31; P10
   pressure wave 3 + earn_guarded + delayed probes. DDES ledger is the
   slice W[16384..32768]; stress store is base 64, 36 slots.
2. R1 change-then-revert case: load_r1 (entry e5) at 00e9a766e, true
   phases G0,G1,G0. Passive observation per phase: Y(1) at t=2 is 1.
3. Frozen R1 traces at 00e9a766e (DDES_REVERT_RESULT.md):
   ADAPT: P0 winner=h0 rounds=1; P1 winner=h1 rounds=2; P2 winner=h0
   rounds=1 (re-derives h0 post-revert in 1 round); total rounds 4;
   dquery(e5,1,1)=1.
   STATIC: P0 RETIRE h1, RETIRE h2, winner=h0 rounds=1; P1 SINGLE
   winner=h0 rounds=0 (misresolve: true law G1); P2 SINGLE winner=h0
   rounds=0 (accidentally right). The C1-pathology signature is
   permanent cross-episode retirement with zero intervention rounds
   after the change.

## P11 design

P11 is appended in main() after emit_stage_hash(W,10) and before the
final "=== INTEGRATION COMPLETE ===" line. P1-P10 code is copied
verbatim from d1305bd43; nothing before P11 changes.

1. ADAPT episode (entry e5, already-zeroed ledger entry):
   load_r1(L); feed_ep(L,5,0, 1,2,1, 2); feed_ep(L,5,1, 1,2,1, 2);
   feed_ep(L,5,2, 1,2,1, 2).
   Read per-phase winners (eb+1068+ep*4), per-phase rounds
   (eb+1084+ep*4), total rounds (eb+1044), dquery(L,5,1,1).
2. STATIC control (entry e6, already-zeroed): load_r1b(L) is a verbatim
   copy of load_r1 writing entry 6 instead of 5 (the only new loader
   code; 15 lines, no semantic change). feed_ep(L,6,0, 1,2,1, 3);
   feed_ep(L,6,1, 1,2,1, 3); feed_ep(L,6,2, 1,2,1, 3).
   Read per-phase winners and per-phase rounds; the RETIRE lines are
   emitted by the writeback path and are part of the evidence.
3. Persistence (mirrors P9's encoding: winner, rounds, change-phase
   rounds): learn(W,910,1,0); 3x query; learn(W,911,1,4); 3x query;
   learn(W,912,1,2); 3x query. Each fact earned 3x immediately to
   importance 31, the same discipline that kept P10_CAUSAL 3/3.
4. Pressure wave: 20 junk items (subj 600..619, rel 99), unproven
   (importance 1), no earning.
5. Delayed probes: P11_CAUSAL (910/911/912), P11_FOUNDATION
   found_probe(W,8,180), P11_CORR (2,10)->8 and (5,11)->180.
6. emit_stage_hash(W,11).

## Frozen predictions

(a) No regression: the RUN output lines from "PHASE P1" through the
    "STATEHASH P10" line are byte-identical to INTEGRATION_RAW_OUTPUT.txt
    at d1305bd43 (verified by head+cmp on the prefix).
(b) ADAPT re-derives: P11_ADAPT_W0=0, W1=1, W2=0; per-phase rounds
    1,2,1; P11_ADAPT_ROUNDS=4; P11_ADAPT_Q (dquery 5,1,1)=1.
(c) STATIC pathology: P11_STATIC_W0=0, W1=0, W2=0; P1 rounds=0 and P2
    rounds=0 (zero intervention rounds after the change); P0 emits
    RETIRE h1 and RETIRE h2. P1 winner h0 is a misresolve (true law G1).
(d) Post-revert persistence: P11_CAUSAL 3/3; P11_FOUNDATION 8/8;
    P11_CORR 2/2 after the 20-item wave.

## Honest bars

P11-PASS requires all four of (a)-(d). P11-FAIL if any fails. The
STATIC control is expected to misresolve; if STATIC somehow resolves
correctly (winners 0,1,0), that is reported as written and the pathology
claim is withdrawn, not reinterpreted. Bounded L2; the candidate graphs
remain researcher-supplied, and the "one continuing learner" goal is
approached, not claimed.

## Determinism and purity

Pure Zag, zero Python (build pinned znc; analysis via shell/grep/awk/
cmp/sha256sum only). 3/3 byte-identical runs. No em dashes
(shell-only check_no_dash.sh). u8-backed cells only; no as *i32 slices
in functions.
