# PREREG: H3-RELEASE-CHURN (frozen)

Frozen 2026-10-03. This preregistration strictly precedes all
implementation and all runs in this lane. This prereg commit contains
ONLY PREREG.md and NAMECHECK.md. No kill bar below may be weakened
or reinterpreted after results are seen. VOID is terminal: it is
corrected only by fresh preregistration plus a fresh run, never by
salvage or amend-and-promote.

Worker: H3-RELEASE-CHURN worker (non-ledger task; claim minting
paused). Lane:
`docs/lab/research-lead/overnight-20260928/h3_release_churn/`.
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

H3-CHURN-INTERACTION achieved CHURN-INTERACTION-PASS (C0..C5):
churn arriving BEFORE the consolidate decision is fully
characterized (W7: genuine pre-decision references still block;
W8: collision-band debris value-matches and blocks; W9: natural
churn per se is inert). The frozen interaction is: the guard is a
decision-time, provenance-blind value predicate (blocks a
reason==2 candidate k iff some USED pool slot holds exactly
900000+k at consolidate time). Left open: the RELEASE-THEN-CHURN
ordering. Churn arriving AFTER a guarded release decision was
already taken installs references to already-released entries,
which the decision-time guard never saw. This lane tests the
hazard definition against post-release reference installation:
does the hazard re-materialize, and what is the hazard definition
against post-release references?

## The mechanism under test (frozen)

`h3_release_churn.zag` starts from the H3-CHURN-INTERACTION sealed
source (`h3_churn_interaction/h3_churn_interaction.zag`) and applies
EXACTLY the following frozen delta. The guarded consolidate
itself is NOT modified (canonized; test only). Every mechanism
function (learner_consolidate, has_live_ref, install_composite,
count_hazard, lholds, mem_write, relocate, learner_revise_r,
learner_scratch, learner_check, audit_releases, all teachers) is
byte-identical.

Frozen delta:

1. File renamed `h3_release_churn.zag`; lane header comment and the
   `LANE=` tag string updated to H3-RELEASE-CHURN.
2. New world driver `run_postrel_wx` (harness only; see Worlds).
   R scratch allocation stays 4096 bytes (three new 40-byte guard
   rows at 2048/2088/2128 fit: max read 2128+36+4=2168 < 4096).
3. main: three new call sites `COND=POSTREL-W10/W11/W12` at R
   offsets 2048/2088/2128 (40-byte guard-row stride, same layout as
   W5..W9: cf, ev, drop, rel, av, ai, ar, lc, haz, trspack).
4. main: in-band R1..R4 checks and the `RELEASE-CHURN-VERDICT=`
   line (R0 and R5 are external). The in-band
   GUARDED-SEALED-VERDICT and CHURN-INTERACTION-VERDICT lines and
   their G/C checks remain verbatim as regression anchors.

## Worlds (frozen)

All three worlds share the W5/W6 substrate setup: mem_zero,
pool_size=32, policy=8 (PIN-UNPIN), consent_mask=16,
learner_scratch, learner_revise_r with all 8 reasons = 2
(INCORPORATED), careful consolidate (verify=1) through the
canonized guarded gate. The 45 pre-existing conditions
(anchors + SEALED-W1..W4 + GUARDED-W5/W6 + CHURN-W7/W8/W9) run
verbatim as regression anchors. The ONLY ordering change vs the
parent lane: consolidate runs BEFORE the churn phase, and
count_hazard is measured AFTER the churn phase.

W10 POSTREL-REF: release-then-churn with BAND-MATCHED references.
After revise, NO composites installed (no live references exist at
decision time), consolidate (guarded), then collision-band churn:
9 writes mem_write(M,3999,905001+j,16) for j=0..8 (same key,
owner, and conflict/displace mechanics as W8). The debris values
905001..905008 land on 900000+k for the just-released candidate
keys 5001..5008. Tests whether post-release reference
installation re-creates the hazard the guard was designed to
prevent.

W11 POSTREL-NOREF-CONTROL: release-then-churn with NATURAL churn.
Same as W10 through the consolidate decision (rel=8), then
teach_churn(M,21) (debris 900001..900020, implying k in 1..20).
Tests that post-release churn per se does not create the hazard;
only band-matched reference installation does.

W12 PREREL-REF-POSTCHURN: the ordering mirror of W7. Genuine
reference composites installed BEFORE consolidate (keys
8001..8008, values 905001..905008, install_composite), guard
blocks (rel=0), then teach_churn(M,21) arrives after the decision.
Tests that post-decision churn does not dislodge the guard's
block: blocked stays blocked.

## Derivation notes (frozen)

Pool accounting uses policy 8 (PIN-UNPIN): relocate scans for the
first free slot; when the pool is full and zero releases exist it
is bit-for-bit no-reclaim pinning (drop++, destroy-in-place).

- W10: 8 revise conflicts (cf=8); 8 old values (600001..600008,
  outside the reference band) displaced to pool slots 0..7.
  Consolidate: 8 candidates (keys 5001..5008, reason 2);
  has_live_ref fires on nothing (no pool value in [900000,910000))
  -> all 8 released -> rel=8, av=8, ai=0, trs=22222222, lc=12.
  Collision churn: 9 writes; j=0 allocates, j=1..8 conflict ->
  8 relocates, cf=16. Debris victims land in free slots 8..15
  (first-free scan; pool 16 <= 32) -> ev=0, drop=0. The released
  slots 0..7 are untouched (debris never needs the full-pool
  path). count_hazard AFTER churn: debris 905001..905008 gives
  has_live_ref(5000+i)=1 for all 8 trace keys -> haz=8. The
  released entries are now referenced by live pooled entries the
  guard never saw.
- W11: same through consolidate (rel=8, av=8, ai=0, trs=22222222,
  lc=12). Natural churn: 21 writes; j=0 allocates, j=1..20
  conflict -> 20 relocates, cf=28. Pool 8+20=28 <= 32 -> ev=0,
  drop=0. Debris 900001..900020 implies k in 1..20; no candidate
  key 5001..5008 matches -> haz=0.
- W12: 8 revise conflicts (cf=8). 8 genuine reference composites
  installed -> pool slots 8..15. Consolidate: all 8 candidates
  reason 2, has_live_ref fires via genuine references -> all 8
  blocked -> rel=0, av=0, ai=0, trs="-". Natural churn: 20
  relocates, cf=28. Pool 16 used; first 16 debris fill slots
  16..31; last 4 hit the full pool under policy 8 with zero
  releases -> drop=4, ev=0. No trace entries -> haz=0. lc=12.
  Predicted row is content-identical to CHURN-W7's frozen row
  (ordering invariance when the guard blocks): cf=28, ev=0,
  drop=4, rel=0, av=0, ai=0, ar=0, lc=12, haz=0, trs="-".

## Frozen predictions

Guard rows (40-byte stride: cf, ev, drop, rel, av, ai, ar, lc,
haz, trspack). R offsets: W10 -> 2048, W11 -> 2088, W12 -> 2128.

| cond      | cf | ev | drop | rel | av | ai | ar | lc | haz | trs      |
|-----------|----|----|------|-----|----|----|----|----|-----|----------|
| POSTREL-W10 | 16 | 0  | 0    | 8   | 8  | 0  | 0  | 12 | 8   | 22222222 |
| POSTREL-W11 | 28 | 0  | 0    | 8   | 8  | 0  | 0  | 12 | 0   | 22222222 |
| POSTREL-W12 | 28 | 0  | 4    | 0   | 0  | 0  | 0  | 12 | 0   | -        |

## Frozen kill bars

- R0 IDENTITY (external): the 45 pre-existing `^COND=` lines are
  byte-identical to h3_churn_interaction/run1.txt, AND 3/3 runs are
  byte-identical (sha256 equal), AND `diff` of h3_release_churn.zag
  against h3_churn_interaction/h3_churn_interaction.zag shows ONLY
  the frozen delta (lane header/tag, run_postrel_wx driver, 3 main
  call sites, R-bar checks, verdict line). Else VOID: the mechanism
  moved beyond the frozen delta or the build is nondeterministic;
  the release-then-churn test is invalid.
- R1 POSTREL-HAZARD-MATERIALIZES (W10 @2048): rel==8 AND haz==8
  AND av==8 AND ai==0 AND cf==16 AND ev==0 AND drop==0 AND lc==12
  AND trs==22222222. (Post-release reference installation
  re-creates the hazard: the guard released all 8 correctly per
  its decision-time precondition, and references installed after
  the decision now point at released memory.)
- R2 POSTREL-NOREF-SAFE (W11 @2088): rel==8 AND haz==0 AND av==8
  AND ai==0 AND cf==28 AND ev==0 AND drop==0 AND lc==12 AND
  trs==22222222. (Post-release churn per se does not create the
  hazard: without value collision the hazard definition stays
  silent.)
- R3 PREREL-BLOCK-SURVIVES-POSTCHURN (W12 @2128): rel==0 AND
  haz==0 AND av==0 AND ai==0 AND cf==28 AND ev==0 AND drop==4 AND
  lc==12. (The guard's pre-decision block is not dislodged by
  post-decision churn: blocked stays blocked.)
- R4 CLEAN: ai==0 AND ar==0 in W10, W11, W12; lc==12 in all three;
  av==rel in W10 and W11.
- R5 DETERMINISM (external): 3/3 runs byte-identical (sha256).

Verdict: RELEASE-CHURN-PASS iff R0..R5 all hold. R0 failure ->
VOID (terminal). Any R1..R5 failure names the bar and yields
RELEASE-CHURN-FAIL. Thresholds are frozen; they are not moved
after results.

## Discrimination design

- R0 bars the moved-mechanism confound (diff limited to the frozen
  delta) and the nondeterminism confound (VOID, not FAIL); the
  45-anchor check additionally bars substrate drift.
- R1 vs W7 (parent, frozen CHURN-W7 row) isolates ORDERING as the
  single variable: same reference values (905001..905008 targeting
  keys 5001..5008), same candidate keys, same reason==2. References
  BEFORE the decision -> blocked (rel=0, haz=0); references AFTER
  the decision -> released then referenced (rel=8, haz=8). If R1
  held at haz=0, the hazard definition would be decision-time and
  the guard's protection would be total; haz=8 proves the hazard
  definition is a state property that outlives the decision.
- R1 vs R2 discriminate reference installation from churn per se:
  identical post-release ordering, identical candidates, identical
  churn mechanics; the only difference is debris values (collision
  band vs natural band) -> haz=8 vs haz=0. If both held at haz=8,
  the hazard would be attributable to churn, not to the value
  overlap.
- R3 bars the "post-decision churn dislodges the block"
  alternative: R1's rel=8 must be attributable to the ordering of
  reference installation vs the decision, not to churn arriving
  late per se. R3 also closes the ordering matrix: pre-decision
  references stay blocked regardless of later churn (row
  content-identical to W7, checked externally).
- R2 vs W9 (parent, frozen CHURN-W9 row) checks the ordering is
  inert for the safe case: natural churn before the decision and
  natural churn after the decision both yield rel=8, haz=0.

## The hazard definition under test (frozen question)

The canonized guard (`learner_consolidate` + `has_live_ref`) is a
DECISION-TIME predicate: it blocks a reason==2 release candidate
iff a live reference exists at consolidate time. `count_hazard`
is a STATE predicate evaluated after the world runs: it fires for
any trace entry whose key is referenced by a live pooled entry at
measurement time, regardless of when the reference was installed
relative to the release decision. This lane freezes the
consequence: if W10 measures haz=8, the hazard definition covers
post-release reference installation and the guard's protection is
decision-time only. A future substrate needing post-release
safety would have to re-check at use time, pin released entries
against reference installation, or track references genuinely
(provenance) rather than decision-time value-sniffing; no such
change is proposed here (test only; the canonized gate is not
modified).

## What this does NOT test (honest accounting)

- The adversary is the worker in a second hat (same procedural
  seal as the parent lane), not a second mind. W10/W11/W12 were
  specified here before implementation.
- The learner remains simulated; reason codes are harness-written.
- W10's collision-band churn is a targeted probe: same churn key
  (3999), owner (16), and conflict/displace mechanics as
  teach_churn, with values in the collision band (the tail a wide
  natural churn would produce). It is not a natural
  teach_churn(M,w) run; per the parent lane's clause 4, natural
  churn cannot activate the overlap against the frozen keys under
  policy 8 at any width. The post-release ordering does not change
  that: natural post-release churn (W11) stays inert.
- A bar failure caused by a builder derivation error (wrong frozen
  number) is still RELEASE-CHURN-FAIL per the frozen bars; the
  report must root-cause it as derivation error vs mechanism
  surprise, without moving the bar.

## Amendments

(none yet; any amendment lands here before implementation and
before any results are seen, with its own commit.)

## Commit order

PREREG.md + NAMECHECK.md commit strictly first, alone.
Implementation (h3_release_churn.zag), the build, the runs
(run1/2/3.txt), and REPORT.md only after. Commit-order self-check:
this prereg commit must strictly precede the implementation commit
and the runs.
