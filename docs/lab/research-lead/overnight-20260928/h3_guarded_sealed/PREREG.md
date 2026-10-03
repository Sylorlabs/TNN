# PREREG: H3-GUARDED-SEALED (frozen)

Frozen 2026-10-03. This preregistration strictly precedes all
implementation and all runs in this lane. This prereg commit contains
ONLY PREREG.md and NAMECHECK.md. No kill bar below may be weakened
or reinterpreted after results are seen. VOID is terminal: it is
corrected only by fresh preregistration plus a fresh run, never by
salvage or amend-and-promote.

Worker: H3-GUARDED-SEALED worker (non-ledger task; claim minting
paused). Lane:
`docs/lab/research-lead/overnight-20260928/h3_guarded_sealed/`.
Commits local only, never pushed. Explicit pathspecs on every
commit. No `git reset`. Pure Zag for all scientific computation;
shell only for binary execution, git ops, sha256sum, cmp, diff,
grep, and file movement. Pinned compiler
`src/tools/toolchain/znc_linux_x86_64_abed8aa1`
(`znc 2026.07.0-dev (edition 2026)`), byte-identical to
`~/safebin/znc` (sha256
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef,
verified 2026-10-03 before this prereg).

## Why this lane exists

H3-INCORPORATED achieved 9/9 hold with the caveat: "the guarded
consolidate is proposed, not canonized: it modifies the
H3-SEALED-B-sealed gate and needs its own sealed lane before
adoption." This lane is that sealed lane. It seals the GUARDED
gate: the H3-SEALED-B mechanism plus exactly the guarded
consolidate delta, run through the same four sealed worlds W1-W4
plus a hazard test.

## The mechanism under test (frozen)

`h3_guarded_sealed.zag` starts from the H3-SEALED-B sealed source
(`h3_sealed_b/unpin_h3sealed.zag`, sha256 to be recorded in the
implementation commit) and applies EXACTLY the following frozen
delta, which is the H3-INCORPORATED guarded consolidate with the
guard hardwired ON (the gate IS the guarded gate; there is no
guard=0 mode in this lane). Nothing else in the mechanism may
change; world-driver call sites change only where the frozen delta
forces a signature change.

Frozen delta (from H3-INCORPORATED, deltas 1-4, guard hardwired):

1. Revision log entries are 16 bytes (key, old_value, new_value,
   reason) instead of 12. Reason codes: 1=REVISED, 2=INCORPORATED,
   3=SUPERSEDED. `log_find`, `audit_releases`, and
   `learner_interfere` use stride 16.
2. `learner_revise` becomes `learner_revise_r(M, RB)` taking a
   reason vector (8 i32s); the reason is written into the log
   entry. A `revise1(M)` adapter supplies an all-1 vector at the
   existing call sites (run_cond_h3, run_sealed_w2 x2,
   run_sealed_w3, run_sealed_w4).
3. `learner_consolidate` reads the reason from the log entry and
   passes it to `learner_unpin` (release trace) verbatim, replacing
   the hardcoded reason=1. Its signature is unchanged, so all
   existing call sites are byte-identical.
4. Guard (hardwired ON): a release candidate with reason==2 is
   additionally released only if no live pooled entry references
   its key (`has_live_ref`, frozen reference pattern from
   H3-INCORPORATED: used slot AND 900000<=value<910000 AND
   value-900000==key). Reasons 1 and 3 are unaffected by
   construction: the `blocked` conjunct can only fire for rsn==2.

Supporting harness functions carried verbatim from
H3-INCORPORATED: `has_live_ref`, `install_composite` (direct
composite install into the first free pool slot, no mem_write, no
conflicts), `count_hazard` (released entries still referenced by a
live pooled entry).

`learner_interfere` (W3's corrupted log): copies the 8 true
16-byte entries verbatim (reasons carried) and appends the same 5
false entries as the sealed source, each with reason=1 (matching
the sealed source's hardcoded trace reason=1, preserving sealed
behavior exactly).

## Worlds (frozen)

W1 SILENT-PRESSURE, W2 TWO-EPISODE, W3 HASTY-FIRST, W4
REVISE-AFTER-PRESSURE: protocols, adversary information sets, and
world-driver code are exactly as in H3-SEALED-B (verbatim, except
the `revise1` call-site adapter forced by frozen delta 2). All
revision reasons are 1 (REVISED): the guard's precondition cannot
fire, so any deviation from the sealed rows is a regression
attributable to the delta.

W5 GUARDED-HAZARD (new): the H3-INCORPORATED RSN-INCREF-GUARD
protocol on the sealed substrate: learner_scratch ->
learner_revise_r (reasons all 2) -> 8 composites installed as
REFERENCES (keys 8001..8008, values 905001..905008, referencing
absorbed keys 5001..5008) -> careful consolidate (verify=1, guard
hardwired ON). No churn (same isolation rationale as
H3-INCORPORATED: this world isolates the release gate).

W6 GUARDED-NOREF (new): the H3-INCORPORATED RSN-INCORPORATED
protocol on the sealed substrate: same as W5 but composites
installed as COPIES (keys 8001..8008, values 600001..600008; not
the reference pattern), reasons all 2, guard hardwired ON. The
guard must NOT fire: this world discriminates over-blocking.

## Derivation notes (frozen)

- W1-W4: every release candidate carries reason==1, so the
  `blocked` conjunct is identically false and the gate reduces to
  the sealed gate term by term. Frozen rows are therefore the
  H3-SEALED-B frozen values exactly (S1..S10 values, [B]
  provenance inherited from H3-SEALED-B's corrected derivation).
- W5: cf=8 (revise's 8 conflicting writes); pool never fills
  (8 displaced + 8 composites = 16/32), so ev=0, drop=0. All 8
  candidates have reason==2 with a live reference -> blocked ->
  releases=0 -> av=0, ai=0, hazard=0 (no trace entries to be
  referenced), lc=12 (learner_check reads 5001..5012; composites
  use disjoint keys), trs="-" (no releases). This is the
  H3-INCORPORATED RSN-INCREF-GUARD row, transplanted onto the
  sealed substrate.
- W6: copies are not references (600001..600008 outside
  900000..910000), so has_live_ref=0 for all 8 candidates ->
  releases=8, trace reasons all 2 -> trs=22222222. Audit: keys
  5001..5008 in the true log, old matches, live belief equals
  log.new -> av=8, ai=0. hazard=0 (no references exist). lc=12,
  cf=8, ev=0, drop=0. This is the H3-INCORPORATED RSN-INCORPORATED
  row with the guard ON (the guard is inert here by construction).

## Frozen predictions

Sealed rows (64-byte stride, same layout as H3-SEALED-B):

| cond      | pre | post | ret | cf | ev | drop | bacc | rawA | rel | av | ai | lc | ar |
|-----------|-----|------|-----|----|----|------|------|------|-----|----|----|----|----|
| SEALED-W1 | 35  | 35   | 100 | 80 | 0  | 48   | 20   | 35   | 0   | 0  | 0  | 12 | 0  |
| SEALED-W2 | 35  | 35   | 100 | 85 | 8  | 45   | 20   | 35   | 8   | 8  | 0  | 12 | 0  |
| SEALED-W3 | 35  | 35   | 100 | 48 | 0  | 16   | 20   | 35   | 13  | 8  | 5  | 12 | 5  |
| SEALED-W4 | 35  | 35   | 100 | 88 | 0  | 56   | 20   | 35   | 0   | 0  | 0  | 12 | 0  |

Guard rows (40-byte stride: cf, ev, drop, rel, av, ai, ar, lc,
haz, trspack):

| cond       | cf | ev | drop | rel | av | ai | ar | lc | haz | trs      |
|------------|----|----|------|-----|----|----|----|----|-----|----------|
| GUARDED-W5 | 8  | 0  | 0    | 0   | 0  | 0  | 0  | 12 | 0   | -        |
| GUARDED-W6 | 8  | 0  | 0    | 8   | 8  | 0  | 0  | 12 | 0   | 22222222 |

R offsets: W1 -> 1568, W2 -> 1632, W3 -> 1696, W4 -> 1760,
W5 -> 1824, W6 -> 1888.

## Frozen kill bars

- G0 IDENTITY (external): the 39 pre-existing COND lines are
  byte-identical to h3_sealed_b/run1.txt (first 39 `^COND=` lines:
  all anchors use reasons==1 paths or no learner phase, so the
  frozen delta must not move them), AND 3/3 runs are byte-identical
  (sha256 equal), AND `diff` of h3_guarded_sealed.zag against
  h3_sealed_b/unpin_h3sealed.zag shows ONLY the frozen delta (log
  stride 12->16, learner_revise_r + revise1 adapter, reason
  read-through in consolidate, guard conjunct, has_live_ref /
  install_composite / count_hazard additions, W5/W6 world drivers,
  main extensions, G-bar checks). Else VOID: the mechanism moved
  beyond the frozen delta or the build is nondeterministic; the
  sealed test is invalid.
- G1 W1-NORECLAIM: ev==0 AND drop==48 AND cf==80.
- G2 W1-SILENCE: releases==0 AND av==0 AND ai==0 AND
  a_released==0.
- G3 W1-INTACT: pre==35 AND post==35 AND ret==100 AND rawA==35 AND
  bacc==20 AND lcheck==12.
- G4 W2-NODOUBLESPEND: ev==8 AND drop==45 AND cf==85.
- G5 W2-EPISODES: releases==8 AND av==8 AND ai==0 AND
  a_released==0.
- G6 W2-INTACT: pre==35 AND post==35 AND ret==100 AND rawA==35 AND
  bacc==20 AND lcheck==12.
- G7 W3-RELEASENOTDEATH: releases==13 AND av==8 AND ai==5 AND
  a_released==5 AND ev==0 AND drop==16 AND cf==48.
- G8 W3-INTACT: pre==35 AND post==35 AND ret==100 AND rawA==35 AND
  bacc==20 AND lcheck==12.
- G9 W4-NOPHANTOM: releases==0 AND av==0 AND ai==0 AND ev==0 AND
  drop==56 AND cf==88 AND a_released==0.
- G10 W4-INTACT: pre==35 AND post==35 AND ret==100 AND rawA==35 AND
  bacc==20 AND lcheck==12.
- G11 HAZARD-BLOCKED (W5): releases==0 AND hazard==0 AND av==0 AND
  ai==0 AND lcheck==12 AND cf==8. (The guarded gate fixes the
  INCORPORATED hazard on the sealed substrate.)
- G12 NO-OVERBLOCK (W6): releases==8 AND hazard==0 AND av==8 AND
  ai==0 AND lcheck==12 AND cf==8 AND trs==22222222. (The guard
  does not block reason-2 entries without live references.)
- G13 DETERMINISM (external): 3/3 runs byte-identical (sha256).
- G14 CLEAN: ai==0 AND ar==0 in all 6 rows; av==releases wherever
  releases>0.

Verdict: GUARDED-SEALED-PASS iff G0..G14 all hold. G0 failure ->
VOID (terminal). Any G1..G14 failure names the bar and yields
GUARDED-SEALED-FAIL: either the guard regressed a sealed world
(G1..G10), the hazard fix did not survive transplantation
(G11), or the guard over-blocks (G12). Thresholds are frozen;
they are not moved after results.

## Discrimination design

- G0 bars the moved-mechanism confound (diff limited to the frozen
  delta) and the nondeterminism confound (VOID, not FAIL); the
  39-anchor check additionally bars substrate drift.
- G1..G10 are the no-regression proof: the guarded gate must
  reproduce all four sealed worlds exactly, since reason==1
  entries can never trigger the guard. A leak of the guard into
  the reason-1 path fails here, not in the guard worlds.
- G11 fails if the guard is absent or inert on the sealed
  substrate (would measure releases=8, hazard=8).
- G12 fails if the guard is a blanket reason==2 block rather than
  a no-live-reference precondition (would measure releases=0).
- G11 and G12 together discriminate the exact proposed semantics:
  block iff (reason==2 AND live reference).
- G2/G3/G5/G6/G8/G10 are the intactness preconditions: if a world
  setup itself disturbed knowledge, the outcome bars would be
  vacuous.

## What this does NOT test (honest accounting)

- The adversary is the worker in a second hat (same procedural
  seal as H3-SEALED: post-freeze designs from the published
  interface, frozen predictions, mechanism identity proof), not a
  second mind. W1-W4 designs are inherited from H3-SEALED's sealed
  set; W5/W6 are specified here before implementation.
- The learner remains simulated; only the release-gate behavior
  is probed. Reason codes are harness-written.
- The reference pattern (900000+k) is a harness convention
  modeling "the absorbing structure references the absorbed
  entry," inherited from H3-INCORPORATED. A real substrate needs
  genuine reference tracking; this lane seals the decision logic,
  not the tracking.
- No churn phase in W5/W6: downstream retention/capacity behavior
  of the guarded gate under churn is untested here (isolated
  deliberately, as in H3-INCORPORATED).
- The churn value range (900001+j) overlaps the reference-pattern
  range; W2's pool therefore contains pattern-matching values, but
  all W2 entries are reason==1 so the guard cannot fire there.
  Any future world mixing reason==2 with churn must re-derive the
  guard's interaction with churn-displaced values.
- A bar failure caused by a builder derivation error (wrong [B]
  number) is still GUARDED-SEALED-FAIL per the frozen bars; the
  report must root-cause it as derivation error vs mechanism
  surprise, without moving the bar.

## Commit order

PREREG.md + NAMECHECK.md commit strictly first, alone.
Implementation (h3_guarded_sealed.zag), the build, the runs
(run1/2/3.txt), and REPORT.md only after. Commit-order self-check:
this prereg commit must strictly precede the implementation commit
and the runs.
