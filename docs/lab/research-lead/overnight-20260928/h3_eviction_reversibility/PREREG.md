# PREREG: H3-EVICTION-REVERSIBILITY (frozen)

Frozen 2026-10-03. This preregistration strictly precedes all
implementation and all runs in this lane. This prereg commit contains
ONLY PREREG.md and NAMECHECK.md. No kill bar below may be weakened
or reinterpreted after results are seen. VOID is terminal: it is
corrected only by fresh preregistration plus a fresh run, never by
salvage or amend-and-promote.

Worker: H3-EVICTION-REVERSIBILITY worker (non-ledger task; claim
minting paused). Lane:
`docs/lab/research-lead/overnight-20260928/h3_eviction_reversibility/`.
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

H3-SECOND-CONSOLIDATE achieved SECOND-CONSOLIDATE-PASS (S0..S5):
re-running the guarded consolidate after the post-release composite
install blocks re-release of the referenced candidates (W13 rel2=0)
but does NOT heal the already materialized hazard (hz2=8), and the
gate's predicate is stateless (W14 rel2=8, W15 rel2=4). The parent's
remaining open follow-up (c): evicting the post-release composite to
test hazard reversibility -- the one remaining untested self-heal
path, since re-consolidation is now proven not to heal.

The frozen question: evict the post-release composite (remove the
reference). Does eviction reverse the hazard (hz 8 -> 0)? Or is the
hazard irreversible even after eviction (materialized hazard
persists)? What is the reversibility condition (when does eviction
heal vs not)?

## The mechanism under test (frozen)

`h3_eviction_reversibility.zag` starts from the H3-SECOND-CONSOLIDATE
sealed source (`h3_second_consolidate/h3_second_consolidate.zag`)
and applies EXACTLY the following frozen delta. The guarded
consolidate itself is NOT modified (canonized; test only). Every
mechanism function (learner_consolidate, has_live_ref,
learner_unpin, install_composite, count_hazard, audit_releases,
count_a_released, lholds, mem_write, mem_read, relocate,
learner_revise_r, learner_scratch, learner_check, all teachers, and
all pre-existing runners run_cond / run_cond_h3 / run_sealed_wx /
run_guarded_wx / run_churn_wx / run_postrel_wx / run_seccon_wx) is
byte-identical.

Frozen delta:

1. File renamed `h3_eviction_reversibility.zag`; lane header comment
   and the `LANE=` tag string updated to H3-EVICTION-REVERSIBILITY.
2. New harness test hook `evict_composite(M, ckey)` (NOT mechanism;
   test-only, sibling of the harness's install_composite). Clears
   the used flag (oo+12) of the first used pool slot whose key ==
   ckey, dropping the composite's reference. The released flags
   (2752+s*4) of the released scratch slots (0..7) are untouched;
   composite slots were never released. The hazard predicate is
   evaluated over the resulting pool state.
3. New harness runner `run_evrev_wx(M,OB,tag,R,ro,rsn,compmode,chw,evkind)`.
   Setup, reason vector, revise, guarded consolidate pass 1, and the
   post-decision composite installation (chw==3/4/5, copied verbatim
   from run_seccon_wx) are identical to run_seccon_wx. Then the
   frozen eviction sequence:
   - `rel1 = ig(M,44)` (releases from pass 1; frozen: 8)
   - `hz_live = count_hazard(M)` (hazard with the composites live,
     before eviction; frozen: 8)
   - eviction phase: `nev = 8`, except evkind==2 where `nev = 4`;
     `evict_composite(M, 8000+i)` for i=1..nev
   - `pre2 = ig(M,44)`
   - if evkind==3: `learner_consolidate(M,M,3648,ig(M,52),1)`
     (the canonized gate, byte-identical call, verify=1 careful)
   - `rel2 = ig(M,44) - pre2` (new releases fired by pass 2; 0 when
     no recheck runs)
   - `hz_post = count_hazard(M)` (hazard after eviction, and after
     the optional recheck)
   - `audit_releases(M)` over the full trace (pack/av/ai)
   - `lc = learner_check(M,8)`
   R layout per row (48-byte stride): 0 cf, 4 ev, 8 drop, 12 rel1,
   16 rel2, 20 av, 24 ai, 28 ar, 32 lc, 36 hz_live, 40 hz_post,
   44 trspack (first 8 trace-entry reasons packed, i32; capped at 8
   iterations so the pack cannot overflow i32 even when the trace
   grows past 8 entries; the COND print loop prints every entry's
   reason digit).
   COND line format:
   `COND=EVREV-W1x cf=.. ev=.. drop=.. rel1=.. rel2=..
   audit_valid=.. audit_invalid=.. a_released=.. lcheck=..
   hz_live=.. hz_post=.. trs=..`
4. main: three new call sites `COND=EVREV-W16/W17/W18` at R
   offsets 2432/2480/2528 (48-byte stride):
   `run_evrev_wx(M,OB,"COND=EVREV-W16",R,2432,2,0,3,1)`,
   `run_evrev_wx(M,OB,"COND=EVREV-W17",R,2480,2,0,3,2)`,
   `run_evrev_wx(M,OB,"COND=EVREV-W18",R,2528,2,0,3,3)`.
   (rsn=2, compmode=0, chw=3 matching POSTCOMP-W10; evkind=1
   evict-8, evkind=2 evict-4, evkind=3 evict-8+recheck.)
   R scratch stays 4096 bytes (max read 2528+44+4=2576 < 4096).
5. main: in-band E1..E4 checks and the
   `EVICTION-REVERSIBILITY-VERDICT=` line (E0 and E5 are external).
   All pre-existing anchors, GUARDED-SEALED, CHURN-INTERACTION,
   RELEASE-CHURN, POSTREL-COMPOSITE, and SECOND-CONSOLIDATE checks
   remain verbatim as regression anchors.

## Worlds (frozen)

All three worlds share the POSTCOMP-W10 substrate through the pass-1
consolidate decision: 8 revise conflicts (cf=8), pool_size=32,
policy=8 (PIN-UNPIN), consent_mask=16, all 8 reasons = 2
(INCORPORATED), careful consolidate (verify=1) through the canonized
guarded gate, rel1=8, no live references at decision time; then 8
genuine band-matched composites installed via install_composite
(keys 8001..8008, values 905001..905008, first-free slots 8..15;
cf stays 8, ev=0, drop=0). hz_live=8 in all three (the hazard
materializes before eviction, as in POSTCOMP-W10/SECCON-W13). The 51
pre-existing conditions plus SECCON-W13/W14/W15 run verbatim as
regression anchors.

W16 EVREV-FULL-EVICT: evict all 8 composites (keys 8001..8008),
no recheck. Tests whether eviction reverses the hazard:
hz_post=0 predicted (the hazard is a live-state predicate, not a
materialized event; removing the reference leg clears it).

W17 EVREV-PARTIAL-EVICT: evict only the first 4 composites (keys
8001..8004), no recheck. Tests the reversibility condition's
granularity: hz_post=4 predicted (exactly the 4 still-referenced
keys 5005..5008 keep their hazard; the 4 evicted keys 5001..5004
heal). Per-entry reversibility, not all-or-nothing.

W18 EVREV-EVICT-THEN-RECHECK: evict all 8 composites, then run the
second guarded consolidate (canonized gate, unmodified) over the
post-eviction state. Tests whether eviction restores the
no-reference decision landscape: with has_live_ref=0 for all 8
keys the guard blocks nothing and the 8 already-released
candidates re-release (rel2=8 predicted, trace 8->16, av=16,
hz_post=0) -- the row must equal SECCON-W14's row on every shared
field, proving eviction leaves no residue. Any field differing
from W14 is an eviction-residue signal.

## Derivation notes (frozen)

Pass 1 is the byte-identical POSTCOMP decision: 8 candidates
(keys 5001..5008, reason 2), has_live_ref fires on nothing ->
rel1=8, cf=8, lc=12, trs=22222222, ev=0, drop=0. The 8 displaced
scratch old values (600001..600008) sit in pool slots 0..7;
learner_unpin sets the released flags for slots 0..7 and appends 8
trace entries.

Composite install (chw=3): first-free slots 8..15 get keys
8001..8008, values 905001..905008. count_hazard: all 8 trace keys
referenced -> hz_live=8.

Eviction: evict_composite clears the used flag of the slot holding
the composite key. Released flags (slots 0..7) untouched; memory
cells untouched; the true revision log untouched; the trace
untouched.

- W16: all 8 composite slots cleared. has_live_ref(M,k)==0 for all
  trace keys -> hz_post=0. No pass 2 -> rel2=0, trace stays 8 ->
  av=8, ai=0, trs=22222222. ar=0 (trace keys >= 5000). lc=12
  (mem cells 5001..5012 untouched by install/evict).
- W17: composites 8001..8004 evicted; 8005..8008 (values
  905005..905008) still reference keys 5005..5008 -> hz_post=4.
  All else as W16.
- W18: all 8 evicted, then pass 2 re-scans slots 0..7 with the
  identical predicate. cand=1 (lholds=1), log match
  (oldv==v), verify=1 re-fires (mem_read(M,k,15)=700000+i !=
  600000+i, memory cells untouched by install/evict), blocked iff
  has_live_ref(M,k)==1 -- now 0 for all 8 keys. All 8 re-release
  -> rel2=8, trace 8->16. audit_releases over 16 entries:
  duplicates carry the same key/old_value and the live belief
  still equals log.new_value -> av=16, ai=0. count_hazard: no
  value match -> hz_post=0. trs pack capped at 8 entries ->
  22222222. Composite slots (8xxx keys) are never candidates
  (lholds=0, no log entries). This is the W14 decision landscape
  reached by eviction rather than by never installing references.

## Frozen predictions

R offsets: W16 -> 2432, W17 -> 2480, W18 -> 2528 (48-byte
stride: cf, ev, drop, rel1, rel2, av, ai, ar, lc, hz_live,
hz_post, trspack).

| cond      | cf | ev | drop | rel1 | rel2 | av | ai | ar | lc | hz_live | hz_post | trs      |
|-----------|----|----|------|------|------|----|----|----|----|---------|---------|----------|
| EVREV-W16 | 8  | 0  | 0    | 8    | 0    | 8  | 0  | 0  | 12 | 8       | 0       | 22222222 |
| EVREV-W17 | 8  | 0  | 0    | 8    | 0    | 8  | 0  | 0  | 12 | 8       | 4       | 22222222 |
| EVREV-W18 | 8  | 0  | 0    | 8    | 8    | 16 | 0  | 0  | 12 | 8       | 0       | 22222222 |

## Frozen kill bars

- E0 IDENTITY (external): every output line of run1.txt except
  the `LANE=` line, the 3 new `COND=EVREV-W1[678]` lines, the
  new E1..E4 in-band check lines, and the
  `EVICTION-REVERSIBILITY-VERDICT=` line is byte-identical to
  h3_second_consolidate/run1.txt, AND 3/3 runs are byte-identical
  (sha256 equal), AND `diff` of h3_eviction_reversibility.zag
  against h3_second_consolidate/h3_second_consolidate.zag shows ONLY
  the frozen delta (lane header/tag, new evict_composite harness
  hook, new run_evrev_wx runner, 3 main call sites, E-bar checks,
  verdict line). Else VOID: the mechanism moved beyond the frozen
  delta or the build is nondeterministic; the eviction
  reversibility test is invalid.
- E1 W16-FULL-REVERSAL (W16 @2432): rel1==8 AND rel2==0 AND
  hz_live==8 AND hz_post==0 AND av==8 AND ai==0 AND ar==0 AND
  cf==8 AND ev==0 AND drop==0 AND lc==12 AND trs==22222222.
  (Evicting all 8 post-release composites reverses the hazard:
  the hazard is a live-state predicate over pool state, not a
  materialized irreversible event. If hz_post stayed 8, the
  hazard would be irreversible even after eviction.)
- E2 W17-PARTIAL-REVERSAL (W17 @2480): rel1==8 AND rel2==0 AND
  hz_live==8 AND hz_post==4 AND av==8 AND ai==0 AND ar==0 AND
  cf==8 AND ev==0 AND drop==0 AND lc==12 AND trs==22222222.
  (Reversibility is per-entry: exactly the 4 still-referenced
  keys 5005..5008 keep their hazard. hz_post==8 would mean
  all-or-nothing (no heal unless everything evicted);
  hz_post==0 would mean over-heal beyond the evicted set.)
- E3 W18-EVICT-THEN-RECHECK (W18 @2528): rel1==8 AND rel2==8 AND
  hz_live==8 AND hz_post==0 AND av==16 AND ai==0 AND ar==0 AND
  cf==8 AND ev==0 AND drop==0 AND lc==12 AND trs==22222222.
  (After eviction the second consolidate behaves exactly as in
  the no-reference world: the row equals SECCON-W14's row on
  every shared field. Any field differing from W14's row is an
  eviction-residue signal -- eviction did not fully restore the
  no-reference decision landscape.)
- E4 CLEAN: ai==0 AND ar==0 in W16, W17, W18; lc==12 in all
  three.
- E5 DETERMINISM (external): 3/3 runs byte-identical (sha256).

Verdict: EVICTION-REVERSIBILITY-PASS iff E0..E5 all hold. E0
failure -> VOID (terminal). Any E1..E5 failure names the bar and
yields EVICTION-REVERSIBILITY-FAIL. Thresholds are frozen; they
are not moved after results.

## Discrimination design

- E1 discriminates "hazard is a reversible live-state predicate"
  (hz_post==0 frozen) from "hazard is a materialized irreversible
  event" (hz_post==8 would mean the hazard persists after its
  reference leg is removed). The SECCON lane proved
  re-consolidation does not heal; E1 tests the one remaining
  self-heal path.
- E2 discriminates per-entry reversibility (hz_post==4 frozen)
  from all-or-nothing behavior: hz_post==8 would mean eviction
  heals nothing unless every reference is gone; hz_post==0 would
  mean eviction over-heals beyond the evicted set. Both
  alternatives name a different reversibility condition and both
  fail the bar.
- E3 discriminates "eviction restores the no-reference decision
  landscape" (row == SECCON-W14's row, reached by a different
  path) from "eviction leaves residue" (any field differing).
  It also re-exposes the stateless gate under eviction: rel2==8
  is the frozen non-idempotent re-fire, now after reference
  removal.
- E0 bars the moved-mechanism confound (diff limited to the
  frozen delta) and the nondeterminism confound (VOID, not FAIL);
  the 51+3-anchor check additionally bars substrate drift.

## What this does NOT test (honest accounting)

- The adversary is the worker in a second hat (same procedural
  seal as the parent lane), not a second mind. W16/W17/W18 were
  specified here before implementation.
- The learner remains simulated; reason codes are harness-written.
- The composite values are harness-written (worker in a second
  hat), not learner-created. "Genuine" means the canonical
  install_composite path, as in the parent lane.
- The eviction is a harness-issued reference removal (the
  evict_composite hook), not a learner-initiated composite drop.
  Whether the learner itself would ever evict its composite is not
  tested.
- The eviction clears the pool slot's used flag only; it does not
  touch released flags, the trace, the true revision log, or
  memory cells. A substrate whose eviction path also rewrites
  those would need its own test.
- A bar failure caused by a builder derivation error (wrong
  frozen number) is still EVICTION-REVERSIBILITY-FAIL per the
  frozen bars; the report must root-cause it as derivation error
  vs mechanism surprise, without moving the bar.

## Amendments

(none yet; any amendment lands here before implementation and
before any results are seen, with its own commit.)

## Commit order

PREREG.md + NAMECHECK.md commit strictly first, alone.
Implementation (h3_eviction_reversibility.zag), the build, the
runs (run1/2/3.txt), and REPORT.md only after. Commit-order
self-check: this prereg commit must strictly precede the
implementation commit and the runs.
