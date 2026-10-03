# PREREG: H3-CHURN-INTERACTION (frozen)

Frozen 2026-10-03. This preregistration strictly precedes all
implementation and all runs in this lane. This prereg commit contains
ONLY PREREG.md and NAMECHECK.md. No kill bar below may be weakened
or reinterpreted after results are seen. VOID is terminal: it is
corrected only by fresh preregistration plus a fresh run, never by
salvage or amend-and-promote.

Worker: H3-CHURN-INTERACTION worker (non-ledger task; claim minting
paused). Lane:
`docs/lab/research-lead/overnight-20260928/h3_churn_interaction/`.
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

H3-GUARDED-SEALED canonized the guarded consolidate with the
caveat: "No churn phase in W5/W6 (deliberate isolation). Noted
hazard for future work: the churn value range (900001+j) overlaps
the reference-pattern range, so any future world mixing reason==2
with churn must re-derive the guard's interaction with
churn-displaced values." This lane resolves that hazard: it runs
reason==2 worlds WITH churn through the canonized guarded gate,
measures exactly how churn-displaced values interact with the
guard, and freezes the re-derived interaction.

## The mechanism under test (frozen)

`h3_churn_interaction.zag` starts from the H3-GUARDED-SEALED sealed
source (`h3_guarded_sealed/h3_guarded_sealed.zag`) and applies
EXACTLY the following frozen delta. The guarded consolidate itself
is NOT modified (canonized; test only). Every mechanism function
(learner_consolidate, has_live_ref, install_composite,
count_hazard, lholds, mem_write, relocate, learner_revise_r,
learner_scratch, learner_check, audit_releases, all teachers) is
byte-identical.

Frozen delta:

1. File renamed `h3_churn_interaction.zag`; lane header comment and
   the `LANE=` tag string updated to H3-CHURN-INTERACTION.
2. R scratch allocation 2048 -> 4096 bytes (room for 3 more
   40-byte guard rows).
3. New world driver `run_churn_wx` (harness only; see Worlds).
4. main: three new call sites `COND=CHURN-W7/W8/W9` at R offsets
   1928/1968/2008 (40-byte guard-row stride, same layout as
   W5/W6: cf, ev, drop, rel, av, ai, ar, lc, haz, trspack).
5. main: in-band C1..C4 checks and the
   `CHURN-INTERACTION-VERDICT=` line (C0 and C5 are external).

## Worlds (frozen)

All three worlds share the W5/W6 substrate setup: mem_zero,
pool_size=32, policy=8 (PIN-UNPIN), consent_mask=16,
learner_scratch, learner_revise_r with all 8 reasons = 2
(INCORPORATED), careful consolidate (verify=1) through the
canonized guarded gate. The 41 pre-existing conditions
(anchors + SEALED-W1..W4 + GUARDED-W5/W6) run verbatim as
regression anchors.

W7 CHURN-HAZARD: reason==2 + GENUINE references + churn. After
revise, install 8 reference composites (keys 8001..8008, values
905001..905008, install_composite), then natural churn
teach_churn(M,21), then consolidate. Tests whether the guard's
true positive survives churn.

W8 CHURN-COLLISION: reason==2 + churn debris in the COLLISION
BAND, no genuine references. After revise, collision-band churn:
9 writes mem_write(M,3999,905001+j,16) for j=0..8 (same churn key
3999, same owner 16, same conflict/displace mechanics as
teach_churn; values land on 900000+k for the candidate keys
5001..5008, i.e. the tail a wide natural churn would produce).
No composites installed. Then consolidate. Tests the re-derived
interaction: churn-displaced values value-matching candidate keys
fire the guard.

W9 CHURN-NOREF-CONTROL: reason==2 + NATURAL churn, no genuine
references, no collision. After revise, teach_churn(M,21), then
consolidate. Debris values 900001..900020 imply k in 1..20, which
cannot match candidate keys 5001..5008. Tests that churn per se
does not over-block.

## Derivation notes (frozen)

Pool accounting uses policy 8 (PIN-UNPIN): relocate scans for the
first free slot; when the pool is full and zero releases exist,
it is bit-for-bit no-reclaim pinning (drop++, destroy-in-place:
the old primary value is destroyed, not displaced).

- W7: 8 revise conflicts (cf=8). 8 composites installed, no
  conflicts, pool 8 -> 16. Natural churn: 21 writes on key 3999;
  j=0 allocates (fresh key), j=1..20 conflict -> 20 relocates,
  cf=28. Pool slots 16..31 take the first 16 debris (values
  900001..900016); the last 4 relocates hit the full pool under
  policy 8 with zero releases -> drop=4, ev=0. Consolidate:
  8 candidates (keys 5001..5008, reason 2); has_live_ref fires via
  the genuine composites (905001..905008 live in slots 8..15) ->
  all 8 blocked -> rel=0, av=0, ai=0. No releases -> haz=0,
  trs="-". lc=12 (learner_check reads 5001..5012, untouched by
  churn/composites).
- W8: 8 revise conflicts. Collision churn: 9 writes; j=0
  allocates, j=1..8 conflict -> 8 relocates, cf=16. Pool: 8
  revised-displaced (slots 0..7, values 600001..600008, outside
  the reference band) + 8 debris (slots 8..15, values
  905001..905008). 16 <= 32 -> ev=0, drop=0. Consolidate:
  8 candidates reason 2; has_live_ref(5000+i) fires via debris
  (value 905000+i in a used slot) for all 8 -> rel=0, av=0,
  ai=0, haz=0, lc=12, trs="-". This is the re-derived interaction
  made observable: debris, not genuine references, fires the
  guard (false positive under the guard's intended semantics,
  true positive under its value-based letter).
- W9: 8 revise conflicts + 20 churn conflicts -> cf=28. Pool:
  8 revised + 20 debris (slots 8..27, values 900001..900020);
  28 <= 32 -> ev=0, drop=0. Debris implies k in 1..20; no
  candidate key matches -> guard never fires -> rel=8, av=8,
  ai=0, haz=0, lc=12, trs=22222222 (trace reasons all 2).

## Frozen predictions

Guard rows (40-byte stride: cf, ev, drop, rel, av, ai, ar, lc,
haz, trspack). R offsets: W7 -> 1928, W8 -> 1968, W9 -> 2008.

| cond     | cf | ev | drop | rel | av | ai | ar | lc | haz | trs      |
|----------|----|----|------|-----|----|----|----|----|-----|----------|
| CHURN-W7 | 28 | 0  | 4    | 0   | 0  | 0  | 0  | 12 | 0   | -        |
| CHURN-W8 | 16 | 0  | 0    | 0   | 0  | 0  | 0  | 12 | 0   | -        |
| CHURN-W9 | 28 | 0  | 0    | 8   | 8  | 0  | 0  | 12 | 0   | 22222222 |

## Frozen kill bars

- C0 IDENTITY (external): the 41 pre-existing `^COND=` lines are
  byte-identical to h3_guarded_sealed/run1.txt, AND 3/3 runs are
  byte-identical (sha256 equal), AND `diff` of
  h3_churn_interaction.zag against
  h3_guarded_sealed/h3_guarded_sealed.zag shows ONLY the frozen
  delta (lane header/tag, R alloc bump, run_churn_wx driver, 3
  main call sites, C-bar checks, verdict line). Else VOID: the
  mechanism moved beyond the frozen delta or the build is
  nondeterministic; the churn test is invalid.
- C1 W7-HAZARD-BLOCKED-UNDER-CHURN: rel==0 AND haz==0 AND av==0
  AND ai==0 AND cf==28 AND ev==0 AND drop==4 AND lc==12. (The
  guard's true positive survives churn: genuine references
  installed before churn still block all 8 releases.)
- C2 W8-DEBRIS-BLOCKS: rel==0 AND haz==0 AND av==0 AND ai==0 AND
  cf==16 AND ev==0 AND drop==0 AND lc==12. (Re-derived
  interaction: collision-band churn debris fires the guard for
  all 8 candidates despite zero genuine references.)
- C3 W9-NO-OVERBLOCK: rel==8 AND haz==0 AND av==8 AND ai==0 AND
  cf==28 AND ev==0 AND drop==0 AND lc==12 AND trs==22222222.
  (Churn per se does not block: without value collision the
  guard stays inert.)
- C4 CLEAN: ai==0 AND ar==0 in W7, W8, W9; lc==12 in all three;
  av==rel in W9.
- C5 DETERMINISM (external): 3/3 runs byte-identical (sha256).

Verdict: CHURN-INTERACTION-PASS iff C0..C5 all hold. C0 failure
-> VOID (terminal). Any C1..C5 failure names the bar and yields
CHURN-INTERACTION-FAIL. Thresholds are frozen; they are not moved
after results.

## Discrimination design

- C0 bars the moved-mechanism confound (diff limited to the frozen
  delta) and the nondeterminism confound (VOID, not FAIL); the
  41-anchor check additionally bars substrate drift.
- C1 fails (rel=8 or haz>0) if churn dislodges the guard's true
  positive: evicted/crowded-out genuine references, or the guard
  misfiring under churn. This is the "blocks hazard" half.
- C2 fails (rel=8) if the overlap analysis is wrong, i.e. if
  churn-displaced values do NOT fire the guard. A hold documents
  the overlap's false-positive consequence exactly.
- C3 fails (rel<8) if churn per se over-blocks reason==2 entries.
  This is the "doesn't over-block" half.
- C2 vs C3 discriminate the VALUE-BAND interaction from churn
  itself: identical candidate keys, identical reasons, identical
  churn mechanics; the only difference is debris values
  (collision band vs natural band) -> 0 vs 8 releases. If both
  held at rel=0, the block would be attributable to churn, not
  to the value overlap.
- C1 vs C2 discriminate provenance: genuine references (W7) vs
  debris only (W8) both yield rel=0, proving the guard is
  provenance-blind: it cannot distinguish a genuine absorbing
  reference from churn debris that value-matches.

## What this does NOT test (honest accounting)

- The adversary is the worker in a second hat (same procedural
  seal as H3-GUARDED-SEALED), not a second mind. W7/W8/W9 were
  specified here before implementation.
- The learner remains simulated; reason codes are harness-written.
  The claim is about the gate's behavior given reasons, not about
  a real learner producing them.
- W8's collision-band churn is a targeted probe: same churn key,
  owner, and conflict/displace mechanics as teach_churn, with
  values in the collision band (the tail a wide natural churn
  would produce). It is not a natural teach_churn(M,w) run.
  Natural churn cannot reach the frozen candidate keys
  (5001..5008 would need w >= 5002), and under policy 8's
  no-reclaim pinning a wide natural churn destroys old displaced
  values in place once the pool fills (drop++), so the colliding
  old debris would never survive to consolidate time anyway.
  The overlap is therefore LATENT under natural churn with the
  frozen keys, and ACTIVE exactly when debris values land on
  900000+k for a reason==2 candidate key k (W8 by construction;
  small candidate keys or adversarial churn in general).
- install_composite silently no-ops when the pool is full
  (harness limitation, verbatim H3-INCORPORATED). W7 avoids it by
  installing before the churn phase; a world installing
  composites after pool-full churn would measure rel=8 for the
  wrong reason (references never installed).
- A bar failure caused by a builder derivation error (wrong frozen
  number) is still CHURN-INTERACTION-FAIL per the frozen bars;
  the report must root-cause it as derivation error vs mechanism
  surprise, without moving the bar.

## Amendments

(none yet; any amendment lands here before implementation and
before any results are seen, with its own commit.)

## Commit order

PREREG.md + NAMECHECK.md commit strictly first, alone.
Implementation (h3_churn_interaction.zag), the build, the runs
(run1/2/3.txt), and REPORT.md only after. Commit-order self-check:
this prereg commit must strictly precede the implementation commit
and the runs.
