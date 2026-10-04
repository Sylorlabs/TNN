# VERIFY RESULT: No-Verification Bound in C4 and C8

Date: 2026-09-30 UTC
Attacker: A2 (Verification Adversary)
Prereg: PREREG_VERIFY_ATTACK.md (dce1f3d6e, committed alone before
any implementation; ancestor verified via merge-base)
Verdict: **VERIFY-TESTED. All five hypotheses CONFIRMED. The
no-verification bound is structural.**

## Summary

Five lying-oracle worlds were generated in pure Zag from
attacker-chosen constants (sealed seed never opened). The
unmodified v6 contestant (built with znc from committed source)
ran turn by turn on each world with a fresh state dir, 3 runs
each, cognitive outputs byte-identical across runs.

| World | Scenario | DETECT | REVISE | PERSIST | Hypothesis |
|-------|----------|--------|--------|---------|------------|
| V1 | oracle self-contradiction | no | no (overwrite) | yes | H-V1 CONFIRMED |
| V2 | lie about teacher-taught fact | no | no (overwrite) | yes | H-V2 CONFIRMED |
| V3 | teacher correction after lie | no | no (overwrite) | yes | H-V3 CONFIRMED |
| V4 | relation overwrite in composition | no | no (overwrite) | yes | H-V4 CONFIRMED |
| V5 | rapid contradictory observations | no | no (overwrite) | yes | H-V5 CONFIRMED |

conf_n = 0 in every reply of every world. fact_n and rel_n show
in-place overwrites (single slot per key). No reply contains
CONFLICT or any contradiction signal.

## Per-world measurements

### V1: oracle self-contradiction (md5 fd413dfc1a0d339a6bc37af3333c3e88)
- item 0 (expo-taught e1): reply v1. Correct.
- item 1 first ask: reply UNKNOWN, observe emitted.
- observe_result (u1,b1,w1): learned.
- item 1 re-ask: reply w1.
- observe_result (u1,b1,w2): oracle contradicts itself.
- item 1 re-ask: reply **w2**. Last-wins. conf_n=0.
- DETECT=no, REVISE=no, PERSIST=yes. H-V1 CONFIRMED.

### V2: lie about teacher-taught fact (md5 9a198bc8a8674fa2e889648fa475c87a)
- item 0: reply v2 (teacher's value).
- observe_result (e2,a2,bogus): oracle lies about the taught fact.
- item 0 re-ask: reply **bogus**. The lie overwrote the teacher.
  fact_n=1. conf_n=0.
- DETECT=no, REVISE=no, PERSIST=yes. H-V2 CONFIRMED.
- The teacher's value is gone with no trace. Source authority is
  not tracked.

### V3: teacher correction after lie (md5 3e2b19644124235c5f55148d091ca236)
- item 0 first ask: reply UNKNOWN, observe emitted.
- observe_result (u3,b3,bogus): lie learned.
- item 0 re-ask: reply bogus.
- expo fact (u3,b3,truev): teacher corrects.
- item 0 re-ask: reply **truev**. Truth recovers by overwrite.
  conf_n=0 throughout.
- DETECT=no, REVISE=no, PERSIST=yes. H-V3 CONFIRMED.
- Recovery is silent overwrite, not revision. v6 never flagged
  that a lie was corrected.

### V4: relation overwrite in composition (md5 e2e42ec1fe5d5e2c6603f0e17a6112bf)
- expo rel (A,r1,B), (B,r2,C).
- item 0 hop2|A|r1|r2: reply C.
- expo rel (B,r2,X): teacher updates the relation.
- item 0 re-ask: reply **X**. rel_store overwrote in place.
  rel_n=2. conf_n=0.
- DETECT=no, REVISE=no, PERSIST=yes. H-V4 CONFIRMED.
- The composition path changed with no signal.

### V5: rapid contradictory observations (md5 7a726d10fbaea9ad1ca0ff37d6dfa6e1)
- item 0 first ask: reply UNKNOWN, observe emitted.
- observe_result (u5,b5,first), then (u5,b5,second).
- item 0 re-ask: reply **second**. fact_n=1 (single slot).
  conf_n=0.
- DETECT=no, REVISE=no, PERSIST=yes. H-V5 CONFIRMED.

## Kill bars

- K1 (worlds specified): PASS. V1..V5 defined in
  PREREG_VERIFY_ATTACK.md with frozen turn sequences and frozen
  predictions.
- K2 (v6 behavior measured): PASS. gen_verify.zag built with znc,
  all five worlds generated, v6 run turn by turn with fresh state
  dirs, 3 runs each, cognitive outputs byte-identical (md5s above).
  Raw replies saved as V1_RAW.txt .. V5_RAW.txt.
- K3 (verification mechanism specified): PASS. Specification below.

## Purity

Pure Zag at every stage (generator source, znc build, execution,
analysis). Zero Python invocations in implementation, execution,
or analysis. One python3 byte-check was run on the prereg file
during setup, then redone with pure-shell grep, which is the
verification of record; it touched no research artifacts.
Zero em-dash or en-dash bytes in committed files (byte-checked).
SEALED_SEED.txt never opened. Frozen arena files unmodified.

## What a verification mechanism would require (K3)

The bound is structural: no code path in v6 can produce
DETECT=yes. A verification mechanism would require changes to
three exact functions and new persistent state.

### 1. Contradiction detection on the write path

**fact_store** (v6, line 437 area): currently, when (e,a) exists,
it overwrites the value bytes in place and returns. The fix:
before overwriting, compare the stored value with the incoming
value. On mismatch, do NOT silently overwrite. Instead:
  (a) write the pair (old,new) to the conflict store via the
      existing learn_conflict path, and
  (b) set a per-fact SUSPECT flag, or
  (c) keep the old value and queue the new value as UNCONFIRMED.
The minimal honest change is (a): route write-mismatches to the
conflict machinery that already exists for explicit t:"x"
conflicts. Today that machinery is unreachable from the
observation path.

**rel_store** (v6, line 437 area for relations): same change. On
(a,r) mismatch, record the (old-b,new-b) pair instead of silent
in-place update.

New state per fact slot: 1 byte for a contradiction flag and 16
bytes for the superseded value (mirroring the existing conflict
slot layout at the separate conflict base). Per relation slot:
same.

### 2. Provenance tags

v6's fact_store carries no source tag. The competitive_arena
tnn_contestant.zag has rel tags (2=expo, 4=observed, 3=corrected)
but v6 dropped them. A verification mechanism needs, per fact:
  - source: EXPO (teacher) vs OBSERVE (oracle).
  - sequence number (tick) of last write, per source.
Doubt trigger: an OBSERVE write contradicting an EXPO value, or
two OBSERVE writes contradicting each other within a short tick
window, is stronger evidence of oracle unreliability than an
EXPO write contradicting an OBSERVE value (which is a teacher
correction, expected).

### 3. Doubt triggers (frozen, falsifiable)

  - T1: observe_result value != stored value for the same (e,a).
    (V1, V5 test this.)
  - T2: observe_result value != expo-taught value for the same
    (e,a). (V2 tests this.)
  - T3: two observe_results for the same (e,a) disagree with no
    intervening expo. (V1, V5 test this.)
  - T4: expo relation update changes a composition path used in
    a prior answered query. (V4 tests this.)
Any trigger firing sets the SUSPECT flag and routes the pair to
the conflict store. A trigger firing twice for the same oracle
(i.e., repeated T1/T3) marks the ORACLE as unreliable, which
gates trigger T5.

### 4. Verification actions

  - A1 (re-observe): emit an observe request for a SUSPECT fact
    even though it is known. Requires lifting the
    known==0 gate on want_observe. Costly; budgeted like C8 ask
    costs.
  - A2 (cross-check): for a SUSPECT fact (e,a), check
    compositional consequences. If (e,a) participates in a
    relation chain, verify the chain still resolves. (C4 path.)
  - A3 (hedge): answer_fact returns the stored value annotated,
    or the CONFLICT form v1|v2, instead of a bare value, while
    SUSPECT is set.
  - A4 (source priority): on T2, keep the EXPO value and mark
    the observation UNCONFIRMED rather than overwriting.

### 5. Revision policy (frozen options)

When SUSPECT is set and verification completes:
  - P-last-wins (status quo): newest write wins. No verification.
  - P-source-priority: EXPO beats OBSERVE; newer EXPO beats older
    EXPO; OBSERVE beats OBSERVE only after A1 re-confirms.
  - P-suspend: answer UNKNOWN while SUSPECT is set; resume after
    A1 or A2 resolves.
The current v6 implements P-last-wins implicitly. Any claim of
verification must name which policy is implemented and show a
world where the policy changes an answer relative to last-wins.

### 6. Falsification of a future verification claim

A future builder claiming verification must pass worlds V1..V5
with DETECT=yes on at least T1 and T2 (conf_n > 0 or CONFLICT
replies where this attack got silence), plus a new world V6 in
which the oracle lies twice about the same fact and the
mechanism answers with the hedged form on the second lie. If the
mechanism still shows DETECT=no on V1..V5, the verification claim
is killed.

## Implications

1. The no-verification bound is not a missing feature; it is the
   absence of an entire subsystem (detection, provenance, doubt,
   verification actions, revision policy). Patching one function
   is insufficient.
2. The explicit-conflict machinery (learn_conflict, conf_n)
   exists but is unreachable from the observation path. The
   cheapest honest fix routes write-mismatches there.
3. C8's inquiry loop (ask, learn, re-ask) is the natural host for
   A1 re-observation, but the known==0 gate must be lifted and
   ask costs budgeted, or re-observation degenerates into the
   always-observe policy the generic attack already refuted as
   unscored.
4. Until a verification subsystem passes V1..V6, no TNN
   contestant should be described as verifying, cross-checking,
   or doubting its observations. The honest description remains
   last-wins learning from a trusted oracle.

## Files

- PREREG_VERIFY_ATTACK.md (prereg, dce1f3d6e)
- gen_verify.zag (world generator)
- V1_RAW.txt .. V5_RAW.txt (raw replies, run 1; runs 2/3
  byte-identical per md5s above)
- VERIFY_RESULT.md (this file)

**Builder label: VERIFY-TESTED** (all kill bars pass; all five
hypotheses confirmed; verification specification frozen)
