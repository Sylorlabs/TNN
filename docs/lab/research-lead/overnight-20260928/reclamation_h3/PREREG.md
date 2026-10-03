# PREREG: RECLAMATION-H3 (learner-issued unpin)

Frozen 2026-10-03. This preregistration strictly precedes
implementation. This prereg commit contains ONLY PREREG.md and
NAMECHECK.md. No kill bar below may be weakened or reinterpreted after
results are seen. VOID is terminal: it is corrected only by fresh
preregistration plus a fresh run, never by salvage or amend-and-promote.

Worker: RECLAMATION-H3 worker (non-ledger task; claim minting paused).
Lane: `docs/lab/research-lead/overnight-20260928/reclamation_h3/`.
Commits local only, never pushed. Explicit pathspecs on every commit.
No `git reset`. Pure Zag for all scientific computation; shell only
for znc invocation, binary execution, git ops, sha256sum, cmp, and
file movement. Pinned compiler
`src/tools/toolchain/znc_linux_x86_64_abed8aa1`
(`znc 2026.07.0-dev (edition 2026)`).

## Objective

RECLAMATION_SYNTHESIS named H3 as the structurally distinct
hypothesis that relocates the death decision: reclamation may only
ever touch entries the learner has released. The learner emits unpin
when it judges an entry dead (here: it revised the belief the entry
recorded); the policy's only job is choosing among released entries;
it can never touch an entry the learner still holds. Capacity drop
then measures learner release behavior, not policy eviction.

This lane implements that relocation on the H1B substrate and tests
three preregistered predictions: (a) retention of learner-held
knowledge is 100 by construction (the mechanism cannot violate it);
(b) capacity is restored exactly to the extent the learner releases
entries, so drop is a function of learner releases; (c) the
adversarial cases are a learner that never releases (must degenerate
bit-for-bit to no-reclaim pinning) and a learner that releases
wrongly (the first honest measurement of learner judgment error under
pressure, with the white-box trace naming the invalid releases).

## Mechanism under test

Substrate identical to RECLAMATION-H1B (same header layout offsets
0..36, same 128-slot primary at 64, same 32-slot pool at 2112, same
touch side table at 2624, same conflict path, same owner-scoped
reads, same A family, same benign B writer, same single-owner churn,
same multi-owner churn modes 1/2/3, same adversarial inflation modes
4/5). Policies 0, 1, 3, 4, 5, 6, 7 and the anchor protocol are
carried verbatim so the full H1B 29-condition table reproduces
exactly (kill bars K1..K15). New code is additive only.

### H3 additions (frozen layout)

- Header 40: release_clock (monotonic release stamp). 44:
  unpin_issued (count of learner-issued releases). 48: trace_count.
  52: true revision-log count.
- Released flags: base 2752, 32 x 4 bytes. 0 = held (pinned); nonzero
  = release stamp. Written ONLY by learner_unpin. Read ONLY by the
  policy-8 reclamation branch.
- Release trace: base 2880, 32 entries x 24 bytes: 0 pool slot,
  4 key, 8 old_value, 12 reason, 16 episode, 20 claimed_new_value.
  Appended ONLY by learner_unpin. This is the white-box trace: what
  was released, when, on what evidence, citing which successor.
- True revision log: base 3648, 16 entries x 12 bytes: 0 key,
  4 old_value, 8 new_value. Appended ONLY by learner_revise (the
  learner's own revision episode). 3648 + 16*12 = 3840 <= 4096.

### The learner (frozen routines)

The simulated learner holds beliefs as owner-scoped readable entries
and runs cognitive episodes. Its key ranges (learner_holds): A-family
keys (1000+i*10+hop for i=1..10, hop=1..3; 2000+i for i=1..5) and its
own scratch keys 5001..5012. Churn keys (3997/3998/3999) are never
held: the learner never incorporated them, so they are never its
memories to release.

- learner_scratch (episode 1): creates 12 scratch beliefs, keys
  5001..5012, values 600000+i, owner 1. Fresh keys; no conflicts.
- learner_revise (episode 2): revises scratch beliefs i=1..8 to
  values 700000+i (owner 1). Each write conflicts and displaces the
  old value to the pool (8 conflicts, pool slots 20..27). Appends
  (key, old, new) to the TRUE revision log. This is the learner's own
  cognitive event; the log is learner state, not a researcher
  annotation of the pool.
- learner_interfere (episode 3, WRONG condition only): models learner
  fallibility (memory interference). Builds a corrupted log = the 8
  true entries plus 5 FALSE entries for A keys the learner never
  revised: (1062,614,999614), (1072,714,999714), (1082,814,999814),
  (1092,914,999914), (1102,1014,9991014). The old_values match the
  live pool entries; the new_values are fictions never written.
- learner_consolidate (episode 4): the belief-reconciliation episode.
  Scans pool slots 0..31. For each used slot with entry (k,v):
  release iff learner_holds(k) AND k is in the supplied log AND
  log.old_value == v AND (hasty mode OR careful mode's extra check).
  Careful mode (verify=1, aligned conditions): additionally requires
  the learner's CURRENT belief mem_read(k,15) != v, i.e. the entry
  genuinely contradicts what the learner now takes to be true. Hasty
  mode (verify=0, WRONG condition only): trusts the (corrupted) log
  without belief verification. Release calls learner_unpin with
  reason=1 (REVISED), episode=4, claimed_new_value = the belief (or
  the log's fiction in hasty mode).
- learner_check: reads back the 12 scratch beliefs (expecting new
  values for revised, old for unrevised); returns count correct.
  Verifies the learner's own knowledge survives its own memory
  management.

### The release rule (frozen)

The learner releases a pool entry iff the entry records a version of
a belief the learner itself revised away: the key is in the learner's
revision log, the entry's value equals the log's old value, and (in
careful mode) the learner's current belief for the key differs from
the entry's value. The 20 displaced A entries are NEVER released:
the learner's current belief for those keys (owner-scoped read, which
falls through to the pool) EQUALS the entry values -- they are its
live, cold-but-critical knowledge. A mechanism-level staleness rule
(pool entry stale iff primary holds the same key with a different
value) would flag all 20; the learner's belief-mediated judgment
protects all 20. This asymmetry is the K19/K20 discriminator.

### Policy 8: PIN-UNPIN (frozen)

On a full pool, the mechanism scans for used slots with nonzero
released flags and evicts the one with the oldest release stamp
(ties: lowest slot). It can never evict a held entry. With zero
releases it drops (destroy-in-place), exactly like no-reclaim
pinning. The ranking among released entries is arbitrary and frozen;
the death decision is entirely upstream of it.

### Policy 9: PIN-STALE (frozen control)

A mechanism-level staleness policy, for contrast: on a full pool,
evict the used slot whose key exists in primary with a different
value, oldest touch stamp first; drop if none is stale. This is what
"staleness" looks like when the mechanism computes it without the
learner's beliefs. It is the control that proves H3's protection of
cold knowledge comes from the decision authority and evidence basis,
not from ranking cleverness.

### The audit (frozen check code, not mechanism)

After consolidation and before churn, audit_releases verifies every
trace entry against ground truth: valid iff the key is in the TRUE
revision log AND trace.old_value == log.old_value AND the learner's
live belief mem_read(key,15) == log.new_value. Returns
(valid*64+invalid). The audit is experiment check code, not part of
the mechanism; it is the instrument that detects researcher-issued
releases wearing learner labels (none are expected in aligned
conditions; 5 are expected in the WRONG condition, where the
corrupted log is the modeled learner error).

## The anti-disguise design (frozen)

The honest risk, named in the synthesis, is that "learner-issued"
collapses to a researcher policy wearing a learner label. Three
frozen design decisions discriminate, and three kill bars test them:

1. Code-path authority: learner_unpin is callable only from
   learner_consolidate (the learner's reconciliation episode). The
   mechanism's reclamation path (relocate, policies 8/9) can read
   released flags but can never set them. K18 proves this
   behaviorally: policy 8 with a silent learner (scratch beliefs
   created, never revised, never consolidated: zero releases) must be
   bit-for-bit identical to policy 3 (no-reclaim pinning) in every
   numeric column, with ev=0 and the identical leak (drop=8). If
   policy 8 contained any mechanism-side auto-reclaim rule, K18
   fails.
2. Evidence basis: the learner's release cites its own beliefs and
   revision history; the mechanism cannot compute "my current belief
   for k" because beliefs are owner-scoped reads (the knower's
   perspective), not primary contents. K19/K20 prove the basis
   matters: under the identical protocol, learner-issued unpin
   releases zero A entries (a_released=0, ret=100) while
   mechanism-computed staleness destroys them (ret=20). A disguised
   policy could mimic either row alone; it cannot produce both rows
   from the two different authorities unless the authorities differ.
3. Per-release auditability: every release carries a trace triple
   (slot, key, old_value, reason, episode, claimed_new_value) checked
   against the true revision log. K21's WRONG condition shows the
   audit catching exactly the 5 invalid releases the corrupted log
   produced, with retention paying exactly for those 5.

What would falsify the H3 claim in this lane: K18 passing with ev>0
(the mechanism reclaims on its own); K19 failing with a_released>0
in aligned conditions (the learner releases what it holds); K20
passing with ret=100 (mechanism staleness protects cold knowledge
too, so authority adds nothing).

## Protocol

Per anchor condition (lphase=0, identical to H1B): on a freshly
zeroed workspace: 1. teach A family (multi). 2. pre-test (expect
35). 3. teach B benign FULL (20 conflicts, 20 A victims pinned in
pool slots 0..19, slots 20..31 free). 4. churn: single-owner key
3999 (w in {1,21,33}) or multi-owner mode 1/2/3 (w=21 per key).
5. post-test; retention = 100*post/pre. 6. record conflicts,
evictions, drop, B accuracy, rawA.

Per H3 condition: steps 1..2 identical; 3. teach B FULL (same 20
displacements); 3b. learner phase per lphase: lphase=1 (full):
learner_scratch, learner_revise (8 conflicts, pool slots 20..27),
careful learner_consolidate (true log), audit; lphase=2 (silent):
learner_scratch only (no revision, no consolidation, no audit);
lphase=3 (wrong): learner_scratch, learner_revise,
learner_interfere (corrupted log), hasty learner_consolidate
(corrupted log), audit; 4. churn (same drivers); 5. post-test,
learner_check, release/audit counters.

H3 conditions (10). Column order: pre, post, ret, cf, ev, drop,
bacc, rawA, releases, audit_valid, audit_invalid, lcheck,
a_released.

| cond           | pol | adv        | lphase | pre | post | ret | cf | ev | drop | bacc | rawA | rel | av | ai | lc | ar |
|----------------|-----|------------|--------|-----|------|-----|----|----|------|------|------|-----|----|----|----|----|
| UNPIN-B0       | 8   | single w1  | 1      | 35  | 35   | 100 | 28 | 0  | 0    | 20   | 35   | 8   | 8  | 0  | 12 | 0  |
| UNPIN-A20      | 8   | single w21 | 1      | 35  | 35   | 100 | 48 | 8  | 8    | 20   | 35   | 8   | 8  | 0  | 12 | 0  |
| UNPIN-A32      | 8   | single w33 | 1      | 35  | 35   | 100 | 60 | 8  | 20   | 20   | 35   | 8   | 8  | 0  | 12 | 0  |
| UNPIN-M2       | 8   | mode1      | 1      | 35  | 35   | 100 | 68 | 8  | 28   | 20   | 35   | 8   | 8  | 0  | 12 | 0  |
| UNPIN-M3       | 8   | mode2      | 1      | 35  | 35   | 100 | 88 | 8  | 48   | 20   | 35   | 8   | 8  | 0  | 12 | 0  |
| UNPIN-X2       | 8   | mode3      | 1      | 35  | 35   | 100 | 68 | 8  | 28   | 20   | 35   | 8   | 8  | 0  | 12 | 0  |
| UNPIN-SILENT   | 8   | single w21 | 2      | 35  | 35   | 100 | 40 | 0  | 8    | 20   | 35   | 0   | 0  | 0  | 12 | 0  |
| PINCTRL-SILENT | 3   | single w21 | 2      | 35  | 35   | 100 | 40 | 0  | 8    | 20   | 35   | 0   | 0  | 0  | 12 | 0  |
| UNPIN-WRONG    | 8   | single w21 | 3      | 35  | 25   | 71  | 48 | 13 | 3    | 20   | 30   | 13  | 8  | 5  | 12 | 5  |
| UNPINSTALE-A20 | 9   | single w21 | 1      | 35  | 7    | 20  | 48 | 16 | 0    | 20   | 19   | 8   | 8  | 0  | 12 | 0  |

Anchor conditions (29, lphase=0): the H1B table reproduced exactly
(IMPCON-B0/A20/A32, IMPPIN-M2/M3, IMPCON-M2/M3/X2, IMPPIN-X2,
IMPLIV-M2/M3/X2, IMPFIFO-B0/A20/A32, IMPPART-B0/A20/A32,
IMPLRU-B0/A20/A32, IMP-B0/A20/A32, IMP-M2/M3/X2, IMPADV-M2,
IMPADV3-M2 with the corrected K13 values ret=14, post=5, rawA=20).

## Derivation notes (frozen with the prereg)

Learner-phase pool layout (all H3 conditions): teach_B displaces
the 20 A entries into pool slots 0..19 (install stamps 1..20,
clock=20). learner_scratch writes 12 fresh keys to primary (no
conflicts). learner_revise writes 8 same-key new values: 8 conflicts
-> relocate finds free slots 20..27 (policy-independent free-slot
scan; pool not full) -> old scratch values installed with stamps
21..28 (clock=28). Slots 28..31 free.

Careful consolidation (lphase=1) scans slots 0..31. Slots 0..19:
learner_holds=1 but key not in the true revision log -> skipped with
no belief read (no touch-stamp disturbance). Slots 20..27: key in
log, log.old_value == entry value, and the learner's current belief
mem_read(k,15) hits primary with the NEW value != entry value ->
released with stamps 1..8 (release_clock, header 40; separate from
the touch clock). Slots 28..31: free. Result: exactly 8 releases,
all valid (audit 8/0), a_released=0. The 20 A entries stay pinned:
the learner's belief for those keys (owner-scoped read falling
through to the pool) equals the entry values, so they are live
knowledge, not stale versions.

UNPIN-B0: churn w=1 -> 1 write, 0 conflicts. cf=20+8+0=28. ev=0,
drop=0. ret=100, rawA=35, bacc=20, lcheck=12.

UNPIN-A20: churn w=21 -> 20 conflicts. 4 fills (slots 28..31, stamps
29..32); 16 relocations. Policy 8: the 8 released slots (20..27)
are evicted oldest-release-first (ev=8); the remaining 8 relocations
find no released slot -> drop=8. cf=20+8+20=48. All A entries
intact: ret=100, post=35, rawA=35, bacc=20. drop = relocations (16)
- releases (8) = 8: capacity exactly tracks learner releases.

UNPIN-A32: churn w=33 -> 32 conflicts = 4 fills + 28 relocations ->
8 evictions + 20 drops. cf=20+8+32=60. ret=100, rawA=35.

UNPIN-M2 (mode1, w=21): 40 churn conflicts = 4 fills + 36
relocations -> 8 evictions + 28 drops. cf=20+8+40=68. ret=100,
rawA=35. UNPIN-X2 (mode3): identical footprint: cf=68, ev=8,
drop=28. UNPIN-M3 (mode2): 60 churn conflicts = 4 fills + 56
relocations -> 8 evictions + 48 drops. cf=88. ret=100 x3.

UNPIN-SILENT / PINCTRL-SILENT (lphase=2): 12 scratch beliefs, no
revision (0 pool entries beyond the 20 A), no consolidation (0
releases). Churn w=21 -> 20 conflicts = 12 fills (slots 20..31) + 8
relocations. Policy 3: 8 drops. Policy 8: released-flag scan finds
none -> 8 drops. ev=0, drop=8, cf=40, ret=100, rawA=35, bacc=20,
releases=0, lcheck=12 (all 12 scratch beliefs unrevised, in
primary). Bit-for-bit identical across all 13 numeric columns: the
mechanism cannot reclaim what the learner never released.

UNPIN-WRONG (lphase=3): corrupted log = 8 true + 5 false entries.
Hasty consolidation (no belief verification): consolidation scans
slots 0..31; slots 11,13,15,17,19 hold (1062/1072/1082/1092/1102,
614/714/814/914/1014) matching the false log's old_values ->
released with release stamps 1..5; slots 20..27 (true revisions) ->
released with stamps 6..13. Total 13 releases. Audit (against the
TRUE log + live beliefs): the 5 false keys are not in the true log
-> invalid=5; the 8 true verify -> valid=8. a_released=5. Churn
w=21: 20 conflicts = 4 fills + 16 relocations -> all 13 released
slots evicted (ev=13), then 3 drops. The 5 evicted live A entries
are hop-2 keys i=6..10 (1062,1072,1082,1092,1102): post-test loop1
(owner 1) i=6..10 fail, loop2 (owner 2) i=6..10 fail, loop3
intact (5), loop4 intact (10): post=5+5+5+10=25,
ret=(100*25)/35=71. rawA: owner-1 hop2 loses 5 -> 30. bacc=20
(B primary intact). cf=48. The 3 evicted released scratch entries
were already dead; the learner's live scratch beliefs are in
primary: lcheck=12.

UNPINSTALE-A20 (policy 9, lphase=1): consolidation releases the same
8 scratch entries (policy 9 ignores released flags). Churn w=21 ->
20 conflicts = 4 fills (slots 28..31, stamps 29..32) + 16
relocations. Policy 9 stale set: slots 0..19 (A entries: primary
holds B's values for the same keys -> stale, stamps 1..20), slots
20..27 (scratch: primary holds new values -> stale, stamps 21..28).
The 16 relocations evict the 16 oldest-stale: slots 0..15 in order
(the churn fills in slots 28..31 are stale too but newest: stamps
29..32, never the oldest while A entries remain). Destroyed: hop-1
and hop-2 keys i=1..8. post: loop1 i=1..8 fail -> 2; loop2 i=1..8
fail -> 2; loop3 i=1..4 fail, i=5 passes -> 1; loop4 i=1..8 fail ->
2: post=7, ret=(100*7)/35=20. rawA: owner-1 hop1 2 + hop2 2 +
owner-2 hop3 10 + owner-4 5 = 19. ev=16, drop=0, cf=48, bacc=20,
lcheck=12. Mechanism-computed staleness destroys cold knowledge
(ret 20) that learner-issued unpin protects (ret 100): the evidence
basis, not the ranking, is the discriminator.

## Frozen kill bars

- K1 ANCHOR-CONSENT: IMPCON-B0/A20/A32 match the frozen
  CONSENT-MULTIOWNER consent rows exactly, every column
  (ret=[100,100,100], cf=[20,40,52], ev=[0,8,20], drop=[0,0,0],
  bacc=20, rawA=35). Else VOID: the substrate moved.
- K2 ANCHOR-PIN-MULTI: IMPPIN-M2/M3 match the frozen
  MULTI-OWNER-CHURN PIN rows exactly (ret=[100,100], cf=[60,80],
  ev=[0,0], drop=[28,48], bacc=20, rawA=35). Else VOID.
- K3 ANCHOR-CONSENT-MULTI: IMPCON-M2/M3/X2 match the frozen
  CONSENT-MULTIOWNER rows exactly (ret=100 x3, cf=[60,80,60],
  ev=[11,5,0], drop=[17,43,28], bacc=20, rawA=35); IMPPIN-X2 matches
  the frozen PIN-M2 row exactly. Else VOID.
- K4 ANCHOR-FIFO: IMPFIFO-B0/A20/A32 match the frozen
  EVICTION-POLICY-COMPARE FIFO rows exactly, every column
  (ret=[100,54,0], post=[35,19,0], cf=[20,40,52], ev=[0,8,20],
  drop=[0,0,0], bacc=20, rawA=[35,27,15]). Else VOID.
- K5 ANCHOR-PART: IMPPART-B0/A20/A32 match the frozen
  EVICTION-POLICY-COMPARE PART rows exactly, every column
  (ret=[77,77,77], post=27 x3, cf=[20,40,52], ev=[4,8,20],
  drop=[0,0,0], bacc=20, rawA=31 x3). Else VOID.
- K6 ANCHOR-LRU: IMPLRU-B0/A20/A32 are bit-for-bit equal to
  IMPFIFO-B0/A20/A32 in every column, and ret=[100,54,0].
- K7 ANCHOR-LIVENESS: IMPLIV-M2/M3/X2 match the frozen
  LIVENESS-SIGNAL liveness rows exactly (ret=0 x3, cf=[60,80,60],
  ev=[28,48,28], drop=[0,0,0], bacc=20, rawA=15 x3). Else VOID.
- K8 IMP-COLD-SAVED: IMP-B0/A20/A32 ret==100 x3; IMP-A20 ev==8,
  drop==0, rawA==35, post==35; IMP-A32 ev==20, drop==0, rawA==35,
  post==35.
- K9 IMP-MULTI-SAVED: IMP-M2/M3/X2 ret==100 x3; ev==[28,48,28];
  drop==0 x3; rawA==35 x3.
- K10 IMP-BEATS-LIVENESS: IMP-M2 ret (100) > IMPLIV-M2 ret (0) AND
  IMP-M2 ev (28) == IMPLIV-M2 ev (28) AND both drop==0.
- K11 IMP-BEATS-CONSENT-CAPACITY: IMP-M2 ev (28) > IMPCON-M2 ev (11)
  AND IMP-M2 drop (0) < IMPCON-M2 drop (17) AND IMP-M2 ret (100) ==
  IMPCON-M2 ret (100).
- K12 ADV-GAMED: IMPADV-M2 ret==71 AND post==25 AND rawA==30 AND
  ev==28 AND drop==0 AND cf==60 AND bacc==20.
- K13 ADV-DOSE (CORRECTED per H1B): IMPADV3-M2 ret==14 AND post==5
  AND rawA==20 AND ev==28 AND drop==0 AND cf==60.
- K14 ADV-FIXED: conflicts identical across policies per dose on
  anchors (40 at single w=21; 52 at single w=33; 60 at mode1/mode3/
  mode4/mode5; 80 at mode2).
- K15 DETERMINISM: 3/3 runs byte-identical (sha256 equal). Else
  VOID.
- K16 UNPIN-ALIGNED-CAPACITY: UNPIN-B0 ret==100, cf==28, ev==0,
  drop==0, releases==8, av==8, ai==0; UNPIN-A20 ret==100, post==35,
  cf==48, ev==8, drop==8, rawA==35, releases==8, av==8, ai==0;
  UNPIN-A32 ret==100, cf==60, ev==8, drop==20, rawA==35,
  releases==8. drop equals relocations minus releases exactly
  (16-8=8; 28-8=20): capacity is the learner's release behavior.
- K17 UNPIN-MULTI: UNPIN-M2 ret==100, cf==68, ev==8, drop==28,
  rawA==35, releases==8; UNPIN-M3 ret==100, cf==88, ev==8, drop==48,
  rawA==35, releases==8; UNPIN-X2 ret==100, cf==68, ev==8, drop==28,
  rawA==35, releases==8.
- K18 AUTHORITY: UNPIN-SILENT and PINCTRL-SILENT are bit-for-bit
  equal in all 13 numeric columns (pre, post, ret, cf, ev, drop,
  bacc, rawA, releases, av, ai, lcheck, a_released); ev==0 and
  drop==8 in both. Policy 8 with a silent learner IS no-reclaim
  pinning: the mechanism cannot reclaim on its own.
- K19 COLD-PROTECTED: a_released==0 in UNPIN-B0/A20/A32/M2/M3/X2.
  The learner's belief-mediated judgment releases zero A entries;
  all 20 cold entries stay pinned.
- K20 STALE-CONTROL: UNPINSTALE-A20 ret==20 AND post==7 AND
  rawA==19 AND ev==16 AND drop==0 AND cf==48 AND bacc==20.
  Mechanism-computed staleness destroys what learner-issued unpin
  protects (100 vs 20, identical protocol otherwise).
- K21 WRONG-RELEASE: UNPIN-WRONG ret==71 AND post==25 AND
  rawA==30 AND ev==13 AND drop==3 AND cf==48 AND releases==13 AND
  av==8 AND ai==5 AND a_released==5. The audit names exactly the 5
  invalid releases; retention pays exactly for them.
- K22 LEARNER-INTACT: lcheck==12 in all 10 H3 conditions.

Verdict: PASS iff K1..K22 all hold. Any kill-bar miss names the bar
and yields FAIL. K1, K2, K3, K4, K5, K7, or K15 failure yields VOID.
Thresholds are frozen; they are not moved after results.

## Discrimination design

- K1..K7 anchor all six baseline policies (a moved substrate or
  baseline invalidates the probe); K6 additionally checks the
  LRU==FIFO equivalence inside this run; K8..K13 carry H1B's
  importance-weighted results (the baseline H3 must beat on
  authority, not on the aligned adversary); K14 bars the
  stronger-adversary confound on anchors.
- K16/K17 test the headline prediction: retention 100 by
  construction, capacity exactly the learner's releases (drop =
  relocations - releases). If drop deviated from that arithmetic,
  the policy would be doing something the learner didn't authorize.
- K18 is the anti-disguise bar: a mechanism-side auto-reclaim rule
  hiding inside policy 8 would show ev>0 with a silent learner. The
  frozen prediction is ev=0 and bit-equality with policy 3.
- K19 vs K20 is the evidence-basis discriminator: the same
  "staleness" intuition implemented as learner judgment (belief +
  revision history) protects cold knowledge, while implemented as a
  mechanism rule (primary comparison) destroys it. If H3 were
  staleness-in-disguise, K19 and K20 could not hold simultaneously
  with opposite retention.
- K21 measures the failure locus: when releases are wrong, the audit
  (not the retention number alone) says which releases were invalid,
  and retention pays exactly for those. This is the honest
  measurement of learner judgment error the synthesis asked for.
- K22 guards against the learner destroying its own live knowledge.

## What this does NOT test (honest accounting)

- The learner is simulated. Its "judgment" is a staleness check over
  its own belief state and revision history -- a genuine cognitive
  operation (belief reconciliation), but a simple one. The
  structural claim tested here is decision-authority relocation (who
  emits the release, on what evidence, at whose episode time), not a
  new kind of intelligence. If the bars show policy 8 == "mechanism
  staleness with extra steps", the report must say so; K19/K20 are
  designed to discriminate exactly that.
- Only the REVISED reason is exercised. INCORPORATED ("content lives
  on in a successor structure") and SUPERSEDED ("procedure replaced")
  are the same unpin code path with different reason codes; the trace
  format supports them but this lane does not run them.
- No sealed post-freeze adversary-designed world: the adversaries
  are the frozen H1B mechanism stressors (single-owner ladder,
  multi-owner modes, importance inflation on anchors). What is tested
  is the authority relocation under those stressors, not a real
  continuing learner under a novel workload.
- The WRONG condition's corrupted log is harness-injected to model
  learner fallibility (memory interference). The honest measurement
  is the audit's detection (5 invalid named) and the exact retention
  price (71), not the realism of the corruption.
- Owner-scoped reads are retained, so the label-free routing caveat
  carries over from L2-INTERFERENCE2 unchanged: this is a mechanism
  check on decision authority in shared memory, not a claim about a
  full continuing learner.
- This lane proposes and canonizes no repair: the measured prices
  are evidence, not a work order for an H3-2.

## Commit order

PREREG.md + NAMECHECK.md commit strictly first, alone. Implementation
(unpin_h3.zag), the compiled binary (unpin_h3_bin), runs, and
REPORT.md only after. Commit-order self-check: this prereg commit
must be the first commit in this lane and must strictly precede the
implementation, the binary, the runs, and the report.
