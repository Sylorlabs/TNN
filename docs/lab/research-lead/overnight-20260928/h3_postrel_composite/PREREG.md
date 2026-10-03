# PREREG: H3-POSTREL-COMPOSITE (frozen)

Frozen 2026-10-03. This preregistration strictly precedes all
implementation and all runs in this lane. This prereg commit contains
ONLY PREREG.md and NAMECHECK.md. No kill bar below may be weakened
or reinterpreted after results are seen. VOID is terminal: it is
corrected only by fresh preregistration plus a fresh run, never by
salvage or amend-and-promote.

Worker: H3-POSTREL-COMPOSITE worker (non-ledger task; claim minting
paused). Lane:
`docs/lab/research-lead/overnight-20260928/h3_postrel_composite/`.
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

H3-RELEASE-CHURN achieved RELEASE-CHURN-PASS (R0..R5):
post-release reference installation re-creates the hazard (W10:
rel=8, haz=8), but the reference installation path in W10 was
churn debris: collision-band mem_write values that conflict,
displace, and relocate into free pool slots. Left open, as the
suggested next probe: post-release reference installation via a
GENUINE absorbing composite (`install_composite` after the release
decision) -- the closest analog of a real structure referencing
released memory. Two questions are frozen here: (1) does a real
structure referencing released memory re-create the hazard, or is
debris special? (2) what is the hazard definition against genuine
post-release references?

## The mechanism under test (frozen)

`h3_postrel_composite.zag` starts from the H3-RELEASE-CHURN sealed
source (`h3_release_churn/h3_release_churn.zag`) and applies
EXACTLY the following frozen delta. The guarded consolidate
itself is NOT modified (canonized; test only). Every mechanism
function (learner_consolidate, has_live_ref, install_composite,
count_hazard, lholds, mem_write, relocate, learner_revise_r,
learner_scratch, learner_check, audit_releases, all teachers) is
byte-identical.

Frozen delta:

1. File renamed `h3_postrel_composite.zag`; lane header comment and
   the `LANE=` tag string updated to H3-POSTREL-COMPOSITE.
2. `run_postrel_wx` gains three new `chw` modes (harness only;
   post-decision composite installation via install_composite, no
   mem_write, no conflicts):
   - chw==3: `i=1; while(i<=8){ install_composite(M,8000+i,900000+5000+i); i=i+1; }`
     (keys 8001..8008, values 905001..905008: band-matched to the
     just-released candidate keys 5001..5008).
   - chw==4: `i=1; while(i<=8){ install_composite(M,8010+i,900000+5020+i); i=i+1; }`
     (keys 8011..8018, values 905021..905028: implying k in
     5021..5028; no candidate key 5001..5008 matches).
   - chw==5: `i=1; while(i<=4){ install_composite(M,8000+i,900000+5000+i); i=i+1; }`
     (keys 8001..8004, values 905001..905004: band-matched to the
     first 4 released keys only).
   R scratch allocation stays 4096 bytes (three new 40-byte guard
   rows at 2168/2208/2248 fit: max read 2248+36+4=2288 < 4096).
3. main: three new call sites `COND=POSTCOMP-W10/W11/W12` at R
   offsets 2168/2208/2248 (40-byte guard-row stride, same layout as
   W5..W12: cf, ev, drop, rel, av, ai, ar, lc, haz, trspack):
   `run_postrel_wx(M,OB,"COND=POSTCOMP-W10",R,2168,2,0,3)`,
   `run_postrel_wx(M,OB,"COND=POSTCOMP-W11",R,2208,2,0,4)`,
   `run_postrel_wx(M,OB,"COND=POSTCOMP-W12",R,2248,2,0,5)`.
4. main: in-band P1..P4 checks and the `POSTREL-COMPOSITE-VERDICT=`
   line (P0 and P5 are external). The in-band
   GUARDED-SEALED-VERDICT, CHURN-INTERACTION-VERDICT, and
   RELEASE-CHURN-VERDICT lines and their G/C/R checks remain
   verbatim as regression anchors.

## Worlds (frozen)

All three worlds share the parent W10/W11 substrate setup:
mem_zero, pool_size=32, policy=8 (PIN-UNPIN), consent_mask=16,
learner_scratch, learner_revise_r with all 8 reasons = 2
(INCORPORATED), careful consolidate (verify=1) through the
canonized guarded gate. The 48 pre-existing conditions
(anchors + SEALED-W1..W4 + GUARDED-W5/W6 + CHURN-W7/W8/W9 +
POSTREL-W10/W11/W12) run verbatim as regression anchors. The
ordering is the same as the parent lane: consolidate runs FIRST
(no composites installed before the decision), and
count_hazard is measured AFTER the post-decision composite
installation.

W10 POSTCOMP-GENUINE-REF: release-then-composite with
BAND-MATCHED genuine references. After revise, NO composites
installed (no live references exist at decision time),
consolidate (guarded), then 8 genuine composites installed via
install_composite: keys 8001..8008, values 905001..905008, which
are exactly 900000+k for the just-released candidate keys
5001..5008. Tests whether a REAL structure referencing released
memory re-creates the hazard (or whether the parent's W10 result
was debris-specific).

W11 POSTCOMP-NOREF-CONTROL: release-then-composite with
NON-COLLIDING genuine references. Same as W10 through the
consolidate decision (rel=8), then 8 genuine composites with
values 905021..905028 (implying k in 5021..5028; no released key
matches). Tests that genuine composite installation per se does
not create the hazard; only value collision does.

W12 POSTCOMP-PARTIAL-REF: release-then-composite with genuine
references targeting only the first 4 released keys (values
905001..905004, keys 8001..8004). Tests the hazard definition's
granularity: it should count exactly the referenced trace
entries (haz=4), proving the hazard is per-entry value matching
rather than systemic contamination from any composite install.

## Derivation notes (frozen)

Pool accounting uses policy 8 (PIN-UNPIN); install_composite
installs directly into the first free pool slot (no mem_write, no
conflict, no relocate, no drop/evict path).

- W10: 8 revise conflicts (cf=8); 8 old values (600001..600008,
  outside the reference band) displaced to pool slots 0..7.
  Consolidate: 8 candidates (keys 5001..5008, reason 2);
  has_live_ref fires on nothing (no pool value in [900000,910000))
  -> all 8 released -> rel=8, av=8, ai=0, trs=22222222, lc=12.
  Post-decision: 8 install_composite calls; cf stays 8 (no
  mem_write). The composites land in first-free slots 8..15
  (pool 16 <= 32 -> ev=0, drop=0); released slots 0..7
  untouched. count_hazard AFTER: values 905001..905008 give
  has_live_ref(5000+i)=1 for all 8 trace keys -> haz=8.
- W11: same through consolidate (rel=8, av=8, ai=0, trs=22222222,
  lc=12). 8 composites with values 905021..905028 land in slots
  8..15; cf=8, ev=0, drop=0. No value matches trace keys
  5001..5008 -> haz=0.
- W12: same through consolidate (rel=8, av=8, ai=0, trs=22222222,
  lc=12). 4 composites with values 905001..905004 land in slots
  8..11; cf=8, ev=0, drop=0. has_live_ref fires for trace keys
  5001..5004 only; 5005..5008 unreferenced -> haz=4.

## Frozen predictions

Guard rows (40-byte stride: cf, ev, drop, rel, av, ai, ar, lc,
haz, trspack). R offsets: W10 -> 2168, W11 -> 2208, W12 -> 2248.

| cond         | cf | ev | drop | rel | av | ai | ar | lc | haz | trs      |
|--------------|----|----|------|-----|----|----|----|----|-----|----------|
| POSTCOMP-W10 | 8  | 0  | 0    | 8   | 8  | 0  | 0  | 12 | 8   | 22222222 |
| POSTCOMP-W11 | 8  | 0  | 0    | 8   | 8  | 0  | 0  | 12 | 0   | 22222222 |
| POSTCOMP-W12 | 8  | 0  | 0    | 8   | 8  | 0  | 0  | 12 | 4   | 22222222 |

## Frozen kill bars

- P0 IDENTITY (external): every output line of run1.txt except
  the `LANE=` line, the 3 new `COND=POSTCOMP-W1[012]` lines, the
  new P1..P4 in-band check lines, and the
  `POSTREL-COMPOSITE-VERDICT=` line is byte-identical to
  h3_release_churn/run1.txt, AND 3/3 runs are byte-identical
  (sha256 equal), AND `diff` of h3_postrel_composite.zag against
  h3_release_churn/h3_release_churn.zag shows ONLY the frozen
  delta (lane header/tag, 3 new chw modes in run_postrel_wx, 3 main
  call sites, P-bar checks, verdict line). Else VOID: the
  mechanism moved beyond the frozen delta or the build is
  nondeterministic; the genuine-composite test is invalid.
- P1 GENUINE-POSTREL-HAZARD (W10 @2168): rel==8 AND haz==8 AND
  av==8 AND ai==0 AND cf==8 AND ev==0 AND drop==0 AND lc==12 AND
  trs==22222222. (A genuine absorbing composite installed after
  the release decision re-creates the hazard: the guard released
  all 8 correctly per its decision-time precondition, and a real
  structure installed after the decision now references the
  released memory.)
- P2 GENUINE-NOREF-SAFE (W11 @2208): rel==8 AND haz==0 AND av==8
  AND ai==0 AND cf==8 AND ev==0 AND drop==0 AND lc==12 AND
  trs==22222222. (Genuine composite installation per se does not
  create the hazard: without value collision the hazard
  definition stays silent.)
- P3 PARTIAL-REFERENCE-GRANULARITY (W12 @2248): rel==8 AND haz==4
  AND av==8 AND ai==0 AND cf==8 AND ev==0 AND drop==0 AND lc==12
  AND trs==22222222. (The hazard counts exactly the referenced
  trace entries: per-entry value matching, not systemic
  contamination.)
- P4 CLEAN: ai==0 AND ar==0 in W10, W11, W12; lc==12 in all three;
  av==rel in W10, W11, W12.
- P5 DETERMINISM (external): 3/3 runs byte-identical (sha256).

Verdict: POSTREL-COMPOSITE-PASS iff P0..P5 all hold. P0 failure ->
VOID (terminal). Any P1..P5 failure names the bar and yields
POSTREL-COMPOSITE-FAIL. Thresholds are frozen; they are not moved
after results.

## Discrimination design

- P0 bars the moved-mechanism confound (diff limited to the frozen
  delta) and the nondeterminism confound (VOID, not FAIL); the
  48-anchor check additionally bars substrate drift.
- P1 vs the parent's POSTREL-W10 (frozen row: rel=8, haz=8, cf=16)
  isolates the INSTALLATION PATH as the single variable: same
  reference values (905001..905008 targeting keys 5001..5008),
  same candidate keys, same reason==2, same post-decision
  ordering. Debris (mem_write conflict/displace, cf=16) ->
  haz=8; genuine composite (install_composite direct slot write,
  cf=8) -> haz=8 predicted. If P1 held at haz=8, debris is not
  special: the hazard definition is installation-path-blind. If
  P1 measured haz=0 while W10 held haz=8, the hazard would be
  debris-specific (installation-path-dependent), and the report
  must say so. Note P1's cf=8: the reference arrives with zero
  conflict/churn mechanics at all -- the purest possible
  post-release reference.
- P2 vs P1 discriminate value collision from composite
  installation per se: identical post-decision genuine-composite
  installation, the only difference is composite values
  (collision band vs non-colliding band) -> haz=8 vs haz=0. If
  both held at haz=8, the hazard would be attributable to
  installing composites after release, not to the value overlap.
- P3 discriminates per-entry value matching from systemic
  contamination: 4 references installed, 4 released keys
  referenced. haz=4 predicted. haz=8 would mean contamination
  spreads beyond value match; haz=0 would mean genuine
  composites are hazard-inert.
- P1 vs the parent's CHURN-W7 (genuine pre-decision references ->
  rel=0) additionally closes the ordering matrix for genuine
  composites: genuine references BEFORE the decision block
  (rel=0); genuine references AFTER the decision re-create the
  hazard (rel=8, haz=8). Ordering is the only variable.

## The hazard definition under test (frozen question)

The canonized guard (`learner_consolidate` + `has_live_ref`) is a
DECISION-TIME predicate: it blocks a reason==2 release candidate
iff a live reference exists at consolidate time. `count_hazard`
is a STATE predicate evaluated after the world runs: it fires for
any trace entry whose key is value-matched by a live pooled entry
at measurement time. This lane freezes the consequence against
GENUINE post-release references: if W10 measures haz=8, then
debris was never special -- any live pooled entry
value-matching a released key re-creates the hazard, regardless
of whether the entry arrived as churn debris or as a genuine
absorbing composite. The frozen consequence from the parent lane
stands: the guard's protection is decision-time only; any future
substrate that needs post-release safety must re-check at use
time, pin released entries against reference installation, or
track references genuinely (provenance). No such change is
proposed here (test only; the canonized gate is not modified).

## What this does NOT test (honest accounting)

- The adversary is the worker in a second hat (same procedural
  seal as the parent lane), not a second mind. W10/W11/W12 were
  specified here before implementation.
- The learner remains simulated; reason codes are harness-written.
- The composite values are harness-written (worker in a second
  hat), not learner-created. "Genuine" here means the canonical
  install_composite path (first-free-slot pooled entry, same as
  the parent's W7/W12 genuine references) rather than churn
  debris mechanics; the reference intent is still adversarially
  assigned, not learned.
- A bar failure caused by a builder derivation error (wrong frozen
  number) is still POSTREL-COMPOSITE-FAIL per the frozen bars; the
  report must root-cause it as derivation error vs mechanism
  surprise, without moving the bar.

## Amendments

(none yet; any amendment lands here before implementation and
before any results are seen, with its own commit.)

## Commit order

PREREG.md + NAMECHECK.md commit strictly first, alone.
Implementation (h3_postrel_composite.zag), the build, the runs
(run1/2/3.txt), and REPORT.md only after. Commit-order self-check:
this prereg commit must strictly precede the implementation commit
and the runs.
