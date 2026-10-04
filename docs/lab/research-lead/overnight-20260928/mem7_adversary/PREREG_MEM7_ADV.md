# PREREG_MEM7_ADV.md -- H-MEM7 red-team preregistration

Status: FROZEN. Written and committed ALONE before any adversary
implementation, build, or run exists. This document alone governs the
H-MEM7 red-team verdict. No em dashes are used in this file.

## Target

H-MEM7 builder verdict: SURVIVES (6/6). R6: decayed recency-weighted
merit; protection iff decmerit >= 25 (MTHRESH) within the age window.
Builder commit 60c3ba3a0. Prereg PREREG_MEM7.md. Result MEM7_RESULT.md.

The red team assumes the H-MEM7 claim is false and attacks four
surfaces the builder named as open boundaries.

## Attack X-M7-1: the 24-vs-25 margin (minimal pair)

Question: is the protection edge exactly at decmerit=25, and is a
one-query-position shift load-bearing (flips a real eviction)?

Fixture: the builder's own setup_m7pair (frozen in PREREG_MEM7.md),
two instantiations that differ by ONE query position:
- M25: setup_m7pair(W,ST,Q,17,18). proc7 at positions 17,18.
  Window = Q[6..26), lo=6, weight = pos-5.
  Hand derivation: weights 12+13 = 25. decmerit(slot7) = 25.
  slot7 age-open (seq=105 < prot=109), so protected: elig=0.
  slots 0..6 age-expired (prot=50), all eligible.
  LFU (min st_uses) protected: uses 10,20,30,40,50,60,70 ->
  victim slot0.
- M24: setup_m7pair(W,ST,Q,16,18). proc7 at positions 16,18.
  Hand derivation: weights 11+13 = 24. decmerit(slot7) = 24.
  slot7 age-open but 24 < 25, so evictable: elig=1.
  All 8 slots eligible. LFU protected: uses
  10,20,30,40,50,60,70,2 -> victim slot7 (uses=2).

Frozen CHECKs (X-M7-1):
1a. M25: decmerit(slot7) = 25.
1b. M25: elig(slot7, win=20, use_prot=1) = 0.
1c. M25: victim(W,Q,ST, LFU=0, ev=0, win=20, use_prot=1) = slot0.
1d. M24: decmerit(slot7) = 24.
1e. M24: elig(slot7, win=20, use_prot=1) = 1.
1f. M24: victim(W,Q,ST, LFU=0, ev=0, win=20, use_prot=1) = slot7.

Verdict rules for X-M7-1:
- KILL iff any of 1a..1f disagrees with the frozen spec
  (decmerit/elig/victim computed differently than hand-derived):
  the mechanism would not implement its own preregistered spec.
- DOWNGRADE iff the edge is load-bearing in a way that contradicts
  a frozen builder claim (none expected; the edge is disclosed).
- HOLD iff all of 1a..1f match: the 24-vs-25 knife-edge is exactly
  where the builder says, and one query position flips a real
  eviction. The disclosed boundary is confirmed, not broken.

## Attack X-M7-2: merit/harm inversion from the merit/harm split

Question: R6 protects by recency-mass (decmerit) but replay harm
stays count-based (winuses). Can R6 protect a strictly LOWER-harm
slot while exposing a strictly HIGHER-harm slot, both age-open?
Under R5 (merit = harm = count) this is impossible: protected
implies count >= 2, age-open evictable implies count <= 1, so a
protected slot never has lower harm than an age-open evictable one.

Hand-built fixture (frozen Q layout, nq=26, seq=105):
Q[0..26) =
 1,2,3,4,5,6,
 0,0,0,0,0,0,
 1,2,3,4,5,
 7,7,
 6,1,2,3,4,5,6.
(positions 0..25 in order.)
Window = Q[6..26), lo=6, weight = pos-5.
Hand-derived window masses and counts:
- pid0 (slot0): pos 6,7,8,9,10,11 -> weights 1,2,3,4,5,6 ->
  decmerit = 21, winuses = 6.
- pid7 (slot7): pos 17,18 -> weights 12,13 ->
  decmerit = 25, winuses = 2.
- pid1: pos 12,20 -> weights 7,15 -> mass 22, count 2.
- pid2: pos 13,21 -> weights 8,16 -> mass 24, count 2.
- pid3: pos 14,22 -> weights 9,17 -> mass 26, count 2.
- pid4: pos 15,23 -> weights 10,18 -> mass 28, count 2.
- pid5: pos 16,24 -> weights 11,19 -> mass 30, count 2.
- pid6: pos 19,25 -> weights 14,20 -> mass 34, count 2.
Slots (frozen):
- slot0: used=1 pid=0 uses=3 lastq=91 sseq=0 prot=109 (age-open).
- slot1: used=1 pid=1 uses=110 lastq=92 sseq=1 prot=50 (expired).
- slot2: used=1 pid=2 uses=120 lastq=93 sseq=2 prot=50 (expired).
- slot3: used=1 pid=3 uses=130 lastq=94 sseq=3 prot=50 (expired).
- slot4: used=1 pid=4 uses=140 lastq=95 sseq=4 prot=50 (expired).
- slot5: used=1 pid=5 uses=150 lastq=96 sseq=5 prot=50 (expired).
- slot6: used=1 pid=6 uses=160 lastq=97 sseq=6 prot=50 (expired).
- slot7: used=1 pid=7 uses=2 lastq=101 sseq=7 prot=109 (age-open).
Hand-derived protection:
- slot7: age-open, mass 25 >= 25 -> protected, elig=0.
- slot0: age-open, mass 21 < 25 -> evictable, elig=1.
- slots 1..6: age-expired -> eligible regardless of mass.
Hand-derived LFU selection (min st_uses):
- protected (use_prot=1): eligible slots 0..6, uses 3,110,120,130,
  140,150,160 -> victim slot0. replay_cost(slot0) = winuses = 6.
- unprotected (use_prot=0): all 8 eligible, uses
  3,110,120,130,140,150,160,2 -> victim slot7.
  replay_cost(slot7) = 2.
So protection flips the LFU victim slot7->slot0 and the measured
harm 2->6: protection-induced harm = 4, with BOTH slots age-open.
Bound (frozen derivation): an age-open evictable slot has mass < 25,
hence count <= 6 (7 queries min mass 28); a protected slot has
count >= 2. So R6 admits protection-induced harm up to 4 between two
age-open slots. Under R5 this shape is impossible (harm <= -1).

Frozen CHECKs (X-M7-2):
2a. decmerit(slot7) = 25; elig(slot7,20,1) = 0; seq < prot (age-open).
2b. decmerit(slot0) = 21; elig(slot0,20,1) = 1; seq < prot (age-open).
2c. winuses(slot7) = 2 < winuses(slot0) = 6 (harm inversion).
2d. victim LFU protected = slot0; victim LFU unprotected = slot7.
2e. replay_cost(slot0) = 6; replay_cost(slot7) = 2.

Verdict rules for X-M7-2:
- DOWNGRADE iff all of 2a..2e match: R6 inverts the merit/harm
  ordering (protects the lower-harm slot, exposes the higher-harm
  slot, both age-open), a shape impossible under R5's unified
  count-based merit and harm. This narrows the "decayed merit is a
  strict improvement" reading: the merit/harm split has a concrete
  cost, and positive protection-induced harm now occurs between two
  age-open slots (up to 4), where R5 admitted none.
- KILL iff the mechanism violates its spec (not expected).
- HOLD iff the inversion does not materialize as hand-derived.

## Attack X-M7-3: decay calibration vs the age-window lemma

Question: the frozen age-window lemma says "any 2 queries since
learning protect (weights >= 12 each, lightest pair 12+13 = 25)",
hence "every R5 fresh-merit shape is preserved by construction".
The weights >= 12 step assumes a FULL window (nq >= 20, so
lo = nq-20). For nq < 20, lo = 0 and the newest weights are < 20.
Is the lemma false for nq < 20, in a real-run-reachable state?

Real-run construction (public API only, no hand-set seq/nq):
- store_init(W,ST). learn_stream(W,ST,0,7): pids 0..6 at slots 0..6,
  sseq 0..6, prot = 0+10 = 10 (seq=0, nq=0).
- st_learn(W,ST,7): slot7, pid7, sseq=7, prot=10.
- 7 filler queries: st_query pid 0,1,2,3,4,5,6 in order.
  seq=7, nq=7, Q[0..7) = [0,1,2,3,4,5,6].
- 2 queries: st_query pid 7, st_query pid 7.
  seq=9, nq=9, Q[7]=7, Q[8]=7.
Hand derivation:
- slot7: uses=2, lastq=9, sseq=7, prot=10. seq=9 < 10: age-open.
  Both queries are since learning (sseq=7 at seq=0).
- decmerit(slot7): nq=9, lo = max(0, 9-20) = 0. pid7 at
  positions 7,8 -> weights 8,9 -> mass 17 < 25.
- winuses(slot7) = 2 >= MERITK (2): under R5 this slot PROTECTS.
- elig(slot7, win=20, use_prot=1): age-open, 17 < 25 -> 1
  (evictable under R6).
So a canonical R5 fresh-merit shape (2 queries since learning,
age-open) is EVICTABLE under R6 when nq < 20. The lemma's lightest
pair is 12+13 = 25 only for nq >= 20; for nq <= 19 the two newest
queries weigh at most (nq-1)+nq = 2nq-1 < 25, and for nq <= 12 even
the two newest possible queries cannot reach 25.

Frozen CHECKs (X-M7-3):
3a. st_nq(ST) = 9; st_seq(ST) = 9.
3b. decmerit(slot7) = 17.
3c. winuses(slot7) = 2.
3d. st_seq(ST) = 9 < st_prot(W,7) = 10 (age-open, as constructed).
3e. elig(slot7, win=20, use_prot=1) = 1 (evictable under R6).

Verdict rules for X-M7-3:
- DOWNGRADE iff all of 3a..3e match: the frozen age-window lemma
  ("any 2 queries since learning protect") is FALSE, and "every R5
  fresh-merit shape is preserved by construction" must be narrowed
  to full windows (nq >= 20). For nq < 20, R6 evicts fresh-merit
  slots that R5 protects: the preservation claim is regime-bound,
  not by construction.
- KILL iff the mechanism violates its spec (not expected).
- HOLD iff slot7 is protected (the hand derivation is wrong; the
  red team owns the error).

## Attack X-M7-4: regression (rebuild and diff audit)

Question: does the committed mem7_learn.zag rebuild byte-identical,
and is the mem6->mem7 diff exactly the preregistered R6 change set
(no silent behavior changes)?

Procedure (frozen):
4a. Extract the frozen mem7_learn.zag blob at builder commit
    60c3ba3a0; cmp against the worktree file (must be identical).
4b. Build with znc 2026.07.0-dev and run 3 consecutive times;
    md5 of each stdout must equal the frozen MEM7_RAW_OUTPUT.txt
    md5 79fdc6eea90c8ed9c019e6893e693bba.
4c. Diff the frozen mem6_learn.zag blob against the frozen
    mem7_learn.zag blob; every hunk must fall in the preregistered
    R6 categories: decmerit(), MTHRESH(), elig() rewritten on
    decmerit, MERITK retained for lineage, F-M7-3c fixture replacing
    F-M6-3c, K-M7-1a/1b/2 fixtures and checks, K-M7-4/K-M7-5/K-M7-6
    checks, comments. No hunk may change preserved-fixture asserted
    behavior.

Verdict rules for X-M7-4:
- KILL iff 4a, 4b, or 4c fails: non-reproducible build or a silent
  behavior change outside the preregistered R6 set.
- HOLD iff all pass.

## Overall verdict

- KILL if any attack's KILL criterion fires.
- Else DOWNGRADE if any attack's DOWNGRADE criterion fires.
- Else SURVIVES (all HOLD).

## Governance

- Pure Zag: no Python anywhere (editing, generators, verifiers,
  analysis, harnesses, scratch). Shell diff/cmp/md5sum only.
- This prereg is committed alone before any adversary code exists.
- No frozen bar may be weakened after results.
- Commits local on tnn-native-lab; only explicitly owned paths;
  never broad-stage; never remove a live .git/index.lock.
- No em dashes in loop documentation (byte-verified).
- Classification: bounded L2. Nothing here establishes L3.
