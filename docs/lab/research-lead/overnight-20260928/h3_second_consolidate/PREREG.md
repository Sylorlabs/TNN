# PREREG: H3-SECOND-CONSOLIDATE (frozen)

Frozen 2026-10-03. This preregistration strictly precedes all
implementation and all runs in this lane. This prereg commit contains
ONLY PREREG.md and NAMECHECK.md. No kill bar below may be weakened
or reinterpreted after results are seen. VOID is terminal: it is
corrected only by fresh preregistration plus a fresh run, never by
salvage or amend-and-promote.

Worker: H3-SECOND-CONSOLIDATE worker (non-ledger task; claim minting
paused). Lane:
`docs/lab/research-lead/overnight-20260928/h3_second_consolidate/`.
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

H3-POSTREL-COMPOSITE achieved POSTREL-COMPOSITE-PASS (P0..P5): a
genuine absorbing composite installed after the guarded release
decision re-creates the hazard (POSTCOMP-W10: rel=8, haz=8), and
the canonized guard (`learner_consolidate` + `has_live_ref`) is a
DECISION-TIME predicate that cannot see references installed
after the release decision. Suggested follow-up (b) from that
lane's report: a SECOND guarded consolidate after the
post-release composite install. The frozen question: does
re-running the guarded consolidate catch the post-release
references (the guard now sees them at decision time), is the
hazard permanent (already-released entries stay released), or
does the system self-heal (haz drops on the second pass)?

## The mechanism under test (frozen)

`h3_second_consolidate.zag` starts from the H3-POSTREL-COMPOSITE
sealed source (`h3_postrel_composite/h3_postrel_composite.zag`)
and applies EXACTLY the following frozen delta. The guarded
consolidate itself is NOT modified (canonized; test only). Every
mechanism function (learner_consolidate, has_live_ref,
install_composite, count_hazard, lholds, mem_write, relocate,
learner_revise_r, learner_scratch, learner_check, audit_releases,
all teachers, run_postrel_wx) is byte-identical.

Frozen delta:

1. File renamed `h3_second_consolidate.zag`; lane header comment
   and the `LANE=` tag string updated to H3-SECOND-CONSOLIDATE.
2. New harness runner `run_seccon_wx` (s = second consolidate).
   Setup, reason vector, revise, guarded consolidate pass 1, and
   the post-decision composite installation (chw==3/4/5, copied
   verbatim from run_postrel_wx) are identical to run_postrel_wx.
   Then the frozen second-pass sequence:
   - `rel1 = ig(M,44)` (releases from pass 1; frozen: 8)
   - `hz_post = count_hazard(M)` (hazard after the post-decision
     composite install, before pass 2)
   - `pre2 = ig(M,44)`
   - `learner_consolidate(M,M,3648,ig(M,52),1)` (the canonized
     gate, byte-identical call, verify=1 careful)
   - `rel2 = ig(M,44) - pre2` (new releases fired by pass 2)
   - `audit_releases(M)` over the full trace (pack/av/ai)
   - `hz2 = count_hazard(M)` (hazard after pass 2)
   - `lc = learner_check(M,8)`
   R layout per row (48-byte stride): 0 cf, 4 ev, 8 drop,
   12 rel1, 16 rel2, 20 av, 24 ai, 28 ar, 32 lc, 36 hz_post,
   40 hz2, 44 trspack (first 8 trace-entry reasons packed, i32;
   capped at 8 iterations so the pack cannot overflow i32 even
   when the trace grows past 8 entries; the COND print loop
   prints every entry's reason digit).
   COND line format:
   `COND=SECCON-W1x cf=.. ev=.. drop=.. rel1=.. rel2=..
   audit_valid=.. audit_invalid=.. a_released=.. lcheck=..
   hz_post=.. hz2=.. trs=..`
3. main: three new call sites `COND=SECCON-W13/W14/W15` at R
   offsets 2288/2336/2384 (48-byte stride):
   `run_seccon_wx(M,OB,"COND=SECCON-W13",R,2288,2,0,3)`,
   `run_seccon_wx(M,OB,"COND=SECCON-W14",R,2336,2,0,4)`,
   `run_seccon_wx(M,OB,"COND=SECCON-W15",R,2384,2,0,5)`.
   (rsn=2, compmode=0, chw=3/4/5 matching POSTCOMP-W10/W11/W12.)
   R scratch stays 4096 bytes (max read 2384+44+4=2432 < 4096).
4. main: in-band S1..S4 checks and the
   `SECOND-CONSOLIDATE-VERDICT=` line (S0 and S5 are external).
   All pre-existing anchors, GUARDED-SEALED, CHURN-INTERACTION,
   RELEASE-CHURN, and POSTREL-COMPOSITE checks remain verbatim as
   regression anchors.

## Worlds (frozen)

All three worlds share the POSTCOMP-W10/W11/W12 substrate through
the pass-1 consolidate decision: 8 revise conflicts (cf=8),
pool_size=32, policy=8 (PIN-UNPIN), consent_mask=16, all 8 reasons
= 2 (INCORPORATED), careful consolidate (verify=1) through the
canonized guarded gate, rel1=8, no live references at decision
time. The 51 pre-existing conditions run verbatim as regression
anchors.

W13 SECCON-BANDMATCH-SECONDPASS: after the pass-1 release (rel1=8),
8 genuine band-matched composites installed via install_composite
(keys 8001..8008, values 905001..905008, first-free slots 8..15;
cf stays 8, ev=0, drop=0), then the SECOND guarded consolidate.
Tests whether the guard catches the now-live post-release
references on a later decision (rel2=0 predicted: all 8
re-release candidates blocked), and whether the already
materialized hazard heals (hz2=8 predicted: permanent, no
self-heal).

W14 SECCON-NOREF-SECONDPASS: same through pass 1 (rel1=8), then 8
genuine NON-COLLIDING composites (keys 8011..8018, values
905021..905028, implying k in 5021..5028; slots 8..15), then the
second guarded consolidate. Control: with no value match, the
guard has nothing to block on pass 2. Tests whether pass 2 is a
no-op or re-fires the release decision (rel2=8 predicted: the
guard predicate is stateless w.r.t. past decisions --
learner_unpin does not clear slot candidacy, so the 8
already-released candidates re-release; trace grows 8->16, all
entries still audit-valid).

W15 SECCON-PARTIAL-SECONDPASS: same through pass 1 (rel1=8), then
4 genuine composites matching only the first 4 released keys
(keys 8001..8004, values 905001..905004, slots 8..11), then the
second guarded consolidate. Tests per-key granularity of the
second decision (rel2=4 predicted: exactly the 4 unreferenced
keys 5005..5008 re-release; the 4 referenced keys 5001..5004 are
blocked; trace grows 8->12).

## Derivation notes (frozen)

Pass 1 is the byte-identical POSTCOMP decision: 8 candidates
(keys 5001..5008, reason 2), has_live_ref fires on nothing ->
rel1=8, av=8, ai=0, trs=22222222, lc=12, cf=8 (8 revise
conflicts; install_composite and learner_consolidate add none),
ev=0, drop=0. learner_unpin sets the released flag
(2752+s*4) and appends the trace entry; it does NOT clear the
pool slot's used flag (oo+12 stays 1), key, or value.

Pass 2 re-scans pool slots 0..31 with the identical predicate.
For slots 0..7 (keys 5001..5008, values 600001..600008):
cand=1 (lholds=1), log match (oldv==v), verify=1 re-fires
(mem_read(M,k,15)=700000+i != 600000+i, memory cells untouched
by install_composite), so rel=1 for each; blocked iff
has_live_ref(M,k)==1.

- W13: composites values 905001..905008 give has_live_ref=1 for
  all 8 keys -> blocked=1 for all 8 -> rel2=0. Trace unchanged
  (8 entries) -> av=8, ai=0, trs=22222222. count_hazard over the
  8 trace entries: all 8 referenced -> hz_post=8, hz2=8.
- W14: composites values 905021..905028 imply k in 5021..5028;
  has_live_ref=0 for keys 5001..5008 -> blocked=0 for all 8 ->
  all 8 re-release -> rel2=8, trace 8->16. audit_releases over
  16 entries: duplicates carry the same key/old_value and the
  live belief still equals log.new_value -> av=16, ai=0.
  count_hazard: no value match -> hz_post=0, hz2=0.
  trs pack capped at 8 entries -> 22222222; the printed trs=
  digits loop shows all 16 entry reasons.
- W15: composites values 905001..905004 -> has_live_ref=1 for
  keys 5001..5004 (blocked), 0 for 5005..5008 (re-released) ->
  rel2=4, trace 8->12 (new entries: keys 5005..5008). av=12,
  ai=0. count_hazard: original entries 5001..5004 fire (4);
  original 5005..5008 and new 5005..5008 do not -> hz_post=4,
  hz2=4.

Composite slots (keys 8001..8008 / 8011..8018 / 8001..8004) are
never candidates on pass 2: lholds is 0 for the 8xxx range, and
the revision log has no entries for them. lc=12 all three
(learner_check reads mem cells 5001..5012, untouched by the
second pass). ar=0 all three (trace keys are 5001..5008, not
A keys).

## Frozen predictions

R offsets: W13 -> 2288, W14 -> 2336, W15 -> 2384 (48-byte
stride: cf, ev, drop, rel1, rel2, av, ai, ar, lc, hz_post, hz2,
trspack).

| cond      | cf | ev | drop | rel1 | rel2 | av | ai | ar | lc | hz_post | hz2 | trs      |
|-----------|----|----|------|------|------|----|----|----|----|---------|-----|----------|
| SECCON-W13| 8  | 0  | 0    | 8    | 0    | 8  | 0  | 0  | 12 | 8       | 8   | 22222222 |
| SECCON-W14| 8  | 0  | 0    | 8    | 8    | 16 | 0  | 0  | 12 | 0       | 0   | 22222222 |
| SECCON-W15| 8  | 0  | 0    | 8    | 4    | 12 | 0  | 0  | 12 | 4       | 4   | 22222222 |

## Frozen kill bars

- S0 IDENTITY (external): every output line of run1.txt except
  the `LANE=` line, the 3 new `COND=SECCON-W1[345]` lines, the
  new S1..S4 in-band check lines, and the
  `SECOND-CONSOLIDATE-VERDICT=` line is byte-identical to
  h3_postrel_composite/run1.txt, AND 3/3 runs are byte-identical
  (sha256 equal), AND `diff` of h3_second_consolidate.zag against
  h3_postrel_composite/h3_postrel_composite.zag shows ONLY the
  frozen delta (lane header/tag, new run_seccon_wx runner, 3 main
  call sites, S-bar checks, verdict line). Else VOID: the
  mechanism moved beyond the frozen delta or the build is
  nondeterministic; the second-consolidate test is invalid.
- S1 W13-BLOCK-BUT-NO-HEAL (W13 @2288): rel1==8 AND rel2==0 AND
  hz_post==8 AND hz2==8 AND av==8 AND ai==0 AND cf==8 AND ev==0
  AND drop==0 AND lc==12 AND trs==22222222. (The guard on the
  second pass sees the now-live post-release references and
  blocks all 8 re-releases -- the guard is decision-time-correct
  on re-check -- but the already materialized hazard is NOT
  healed: hz2==hz_post==8. No self-heal.)
- S2 W14-NOREF-DOUBLE-RELEASE (W14 @2336): rel1==8 AND rel2==8
  AND hz_post==0 AND hz2==0 AND av==16 AND ai==0 AND cf==8 AND
  ev==0 AND drop==0 AND lc==12 AND trs==22222222. (With no value
  match the guard blocks nothing on pass 2 and the
  already-released candidates re-release: the guard predicate is
  stateless w.r.t. past decisions -- no idempotency memory --
  so re-running consolidate re-fires the release decision. This
  proves the W13 block is value-match-specific, not
  pass-2-inert.)
- S3 W15-PARTIAL-BLOCK (W15 @2384): rel1==8 AND rel2==4 AND
  hz_post==4 AND hz2==4 AND av==12 AND ai==0 AND cf==8 AND ev==0
  AND drop==0 AND lc==12 AND trs==22222222. (Exactly the 4
  unreferenced keys re-release on pass 2; the 4 referenced keys
  are blocked. Per-key granularity of the second decision.)
- S4 CLEAN: ai==0 AND ar==0 in W13, W14, W15; lc==12 in all
  three.
- S5 DETERMINISM (external): 3/3 runs byte-identical (sha256).

Verdict: SECOND-CONSOLIDATE-PASS iff S0..S5 all hold. S0 failure
-> VOID (terminal). Any S1..S5 failure names the bar and yields
SECOND-CONSOLIDATE-FAIL. Thresholds are frozen; they are not
moved after results.

## Discrimination design

- S1 discriminates "guard re-catches references on pass 2"
  (rel2==0 frozen) from "guard blind even on re-check"
  (rel2==8 would mean the second decision did not see the live
  references); and "hazard permanent" (hz2==8 frozen) from
  "self-heal" (hz2<8 would mean re-running consolidate somehow
  clears or re-protects the hazard).
- S2 vs S1 discriminate the W13 block as value-match-specific
  from pass-2-inertness: if pass 2 were simply inert, W14 would
  also show rel2==0; frozen rel2==8 proves the guard re-fires
  the release decision and blocks only on live value match.
  S2 additionally exposes the stateless (non-idempotent)
  consolidate: re-running re-releases unreferenced candidates
  (av==16, trace grows 8->16, all entries audit-valid). If S2
  measured rel2==0, consolidate would be idempotent,
  contradicting the stateless-predicate reading -- the report
  must root-cause without moving the bar.
- S3 discriminates per-key granularity on pass 2 from
  all-or-nothing behavior: rel2==4 frozen; rel2==0 would mean
  the block is systemic, rel2==8 would mean the partial
  references were not seen.
- S0 bars the moved-mechanism confound (diff limited to the
  frozen delta) and the nondeterminism confound (VOID, not
  FAIL); the 51-anchor check additionally bars substrate drift.

## What this does NOT test (honest accounting)

- The adversary is the worker in a second hat (same procedural
  seal as the parent lane), not a second mind. W13/W14/W15 were
  specified here before implementation.
- The learner remains simulated; reason codes are harness-written.
- The composite values are harness-written (worker in a second
  hat), not learner-created. "Genuine" means the canonical
  install_composite path, as in the parent lane.
- The second consolidate is a harness-issued re-decision, not a
  learner-initiated re-check. Whether the learner itself would
  ever re-consolidate is not tested.
- A bar failure caused by a builder derivation error (wrong
  frozen number) is still SECOND-CONSOLIDATE-FAIL per the frozen
  bars; the report must root-cause it as derivation error vs
  mechanism surprise, without moving the bar.

## Amendments

(none yet; any amendment lands here before implementation and
before any results are seen, with its own commit.)

## Commit order

PREREG.md + NAMECHECK.md commit strictly first, alone.
Implementation (h3_second_consolidate.zag), the build, the runs
(run1/2/3.txt), and REPORT.md only after. Commit-order self-check:
this prereg commit must strictly precede the implementation commit
and the runs.
