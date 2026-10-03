# PREREG: H3-SEALED (sealed post-freeze adversary worlds for H3 decision authority)

Frozen 2026-10-03. This preregistration strictly precedes all implementation
and all runs. This prereg commit contains ONLY PREREG.md and NAMECHECK.md.
No kill bar below may be weakened or reinterpreted after results are seen.
VOID is terminal: it is corrected only by fresh preregistration plus a fresh
run, never by salvage or amend-and-promote.

Worker: H3-SEALED worker (non-ledger task; claim minting paused).
Lane: `docs/lab/research-lead/overnight-20260928/h3_sealed/`.
Commits local only, never pushed. Explicit pathspecs on every commit.
No `git reset`. Pure Zag for all scientific computation; shell only for
binary execution, git ops, sha256sum, cmp, diff, grep, and file movement.
Pinned compiler `src/tools/toolchain/znc_linux_x86_64_abed8aa1`
(`znc 2026.07.0-dev (edition 2026)`), byte-identical to `~/safebin/znc`
(sha256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef,
verified 2026-10-03 before this prereg).

## Objective

RECLAMATION-H3B closed the H3 derivation error: VERDICT=PASS (22/22) on the
unchanged H3 binary. Still open from H3/H3B: "sealed post-freeze adversary
worlds" for H3's decision-authority claim. H3's adversaries were the frozen
H1B mechanism stressors, designed pre-freeze. This lane runs the independent
red-team test: an adversary designs worlds AFTER H3 froze, targeting the
learner-issued unpin mechanism, trying to break decision authority:

- (F1) fool the learner into releasing critical (A-family) entries, or
- (F2) fool the learner into never releasing (and the mechanism overriding
  the silence), or
- (F3) break the release/audit accounting across learner episodes.

## What "sealed" means in this lane

1. Post-freeze: the four worlds were designed after the H3 mechanism froze
   (H3B VERDICT=PASS 2026-10-03). No world existed when H3 was built.
2. Published-interface only (adversary hat): the world designs and attack
   hypotheses below were produced from the H3/H3B reports and preregs only:
   the protocol steps (teach A/B, scratch, revise, interfere, consolidate,
   churn drivers, post-test), the 10 published condition rows, and the
   claimed decision-authority statements. The adversary did not use the
   .zag source.
3. Frozen predictions: every kill bar is frozen here, before implementation
   and before any run.
4. Mechanism identity: the mechanism source is copied verbatim (see below);
   S0 proves behaviorally that the sealed binary reproduces all 39 frozen
   H3/H3B COND rows bit-for-bit. Any deviation voids the lane.

## The two-hat honesty statement

The adversary is this worker in a different hat: no second agent was
available (depth 2/2, cannot spawn). The information barrier actually
enforced:

- Hat 1 (adversary): designed W1..W4 and the attack hypotheses from the
  published reports/preregs only. Fixed before the source was consulted
  for implementation. Its information set is listed under each world.
- Hat 2 (builder): implements the worlds by copying the frozen mechanism
  source verbatim and adding only new world-driver functions plus new
  print/K-lines. Read the source before this prereg ONLY to validate
  interface assumptions (A1..A5 below). No world design was changed as a
  result; one exact count was refined (W2 cf 76 -> 84, see A2).

Provenance of every frozen number is labeled [A] (adversary, from published
claims) or [B] (builder, from validated interface assumptions). A bar that
fails is SEALED-FAIL regardless of provenance; the report will root-cause
whether the failure is a mechanism surprise or a derivation error, without
moving the bar.

## The mechanism under test (frozen, unchanged)

`unpin_h3.zag` from reclamation_h3b (binary sha256
a9759f7c4bd71b944a6e0e2da69264c6f2f192ba4edef4835c8ee9fdf747223c).
The sealed binary is built from a source file whose mechanism functions
(all fns except the new `run_sealed_w*` drivers and the extended `main`)
are byte-identical to that file. S0 verifies behavioral identity.

## Builder interface assumptions (validated from source before prereg)

- A1 [B]: `mem_write` counts a conflict only on same-key different-value;
  same-value rewrites are no-ops (owner OR only). Needed for W2/W4 cf.
- A2 [B]: `learner_scratch`/`learner_revise` use FIXED keys 5001..5012
  (not allocator-fresh). A second episode re-scratches the same keys:
  scratch2 causes 8 conflicts (keys 5001..5008, values 70000i -> 60000i)
  and revise2 causes 8 conflicts. The true revision log appends (count at
  M[52] goes 8 -> 16); `audit_releases` uses first-match in the cumulative
  log. This refined W2 cf from the adversary's 76 to 84; the world design
  (two episodes) is unchanged and the probe is stronger for it.
- A3 [A+B]: mode-2 churn causes exactly 60 conflicts and disturbs neither
  scratch beliefs nor A entries (published UNPIN-M3 row: lcheck=12,
  ret=100, cf=88=20+8+60).
- A4 [B]: counters conflicts (M[4]), evict (M[8]), drop (M[28]), releases
  (M[44]) are cumulative per condition; release/audit/trace state persists
  across phases within one condition run.
- A5 [A]: the published K16 derivation ("the remaining 8 relocations find
  no released slot -> drop=8") implies a consumed release does not
  re-authorize eviction. W2's S4 tests exactly this implication across
  episodes; the builder did not verify it from the source.

## Sealed worlds

Notation: columns are the 13 numeric COND columns (pre, post, ret, cf, ev,
drop, bacc, rawA, releases, av, ai, lcheck, a_released). Policy 8
throughout. "Published claim" = the H3/H3B decision-authority statements.

### W1 SILENT-PRESSURE ("never releasing" under 3x pressure)

Protocol: teach A -> pre -> scratch -> teach B -> SILENT (no revise, no
consolidate, no audit) -> churn MULTI-OWNER MODE 2 (w=21) -> post-test.
Adversary information set: UNPIN-SILENT (silent -> 0 releases, ev=0 at
w=21), UNPIN-M3 (mode2 -> 60 conflicts), K18 (no auto-reclaim at w=21).
Attack hypothesis (F2): K18's no-auto-reclaim result holds only at low
pressure; under 60 conflicts the mechanism reclaims unreleased slots on
its own (ev>0), overriding the learner's silence.
Survival prediction [A]: the mechanism cannot reclaim without a learner
release at any pressure: ev==0, drop==48 (12 fills + 48 relocations, zero
released), cf==80 (20+0+60), releases==0, av==0, ai==0, a_released==0,
ret==100, post==35, rawA==35, bacc==20, lcheck==12, pre==35.

### W2 TWO-EPISODE (release-flag lifecycle across episodes)

Protocol: teach A -> pre -> scratch -> teach B -> revise -> careful
consolidate (episode 1: 8 releases) -> churn single w=21 (consumes the 8
releases) -> scratch -> revise -> careful consolidate (episode 2) ->
churn single w=21 -> post-test.
Adversary information set: the published 3-conjunct release rule, the K16
drop arithmetic, A2 [B].
Attack hypothesis (F3): release authorization is a single-episode artifact.
Across episodes the mechanism either double-spends (evicts live entries on
stale release flags: ev>8) or leaks (episode-2 consolidation re-releases or
mis-releases: releases != 8).
Survival prediction: episode 1 identical to UNPIN-A20 (8 releases, av=8,
ai=0); churn1 evicts exactly the 8 released slots (ev=8) and drops 8;
episode-2 revise displaces into a full pool (16 drops across scratch2 and
revise2: the old values never reach the pool); episode-2 consolidation
finds no pool entries for its log keys (0 releases); churn2 drops 20.
Cumulative [A+B]: cf==84 (20+8+20+8+8+20), ev==8, drop==36 (8+8+8+20... 
8 churn1 + 8 scratch2 + 8 revise2 + 20 churn2 = 44; see derivation),
releases==8, av==8, ai==0, a_released==0, ret==100, post==35, rawA==35,
bacc==20, lcheck==12, pre==35.

W2 drop derivation (frozen): churn1: 20 conflicts = 4 fills + 16 reloc ->
8 evict (released) + 8 drop. scratch2: 8 conflicts -> pool full ->
8 drops. revise2: 8 conflicts -> pool full -> 8 drops. churn2:
20 conflicts -> 20 reloc -> 0 released -> 20 drops. Total drop =
8+8+8+20 = 44. (An earlier draft wrote 36; the frozen value is 44:
churn1 contributes 8 drops, not 0.)

### W3 HASTY-FIRST (release dissociated from eviction; audit under reorder)

Protocol: teach A -> pre -> scratch -> teach B -> revise -> churn single
w=21 (BEFORE consolidation) -> interfere (corrupted log, same as WRONG) ->
hasty consolidate -> audit -> post-test.
Adversary information set: UNPIN-WRONG row (13 releases, av=8, ai=5,
a_released=5, ret=71 because post-consolidation churn evicted the released
A entries), the published release rule, A1 [B].
Attack hypothesis: a release is harmless until eviction acts on it; the
audit still names exactly the 5 invalid releases under the reordered
protocol. The adversary hopes ret<100 (release itself damages reads, which
would weaken the authority claim: the learner's judgment alone destroys
knowledge).
Survival prediction [A]: churn meets zero released slots -> ev==0,
drop==16 (4 fills + 16 reloc, all drops); consolidate releases the same 13
(5 false A entries at slots 11,13,15,17,19 + 8 true); av==8, ai==5,
a_released==5; released-but-present A entries still serve reads ->
ret==100, post==35, rawA==35; cf==48 (20+8+20), bacc==20, lcheck==12,
pre==35.

### W4 REVISE-AFTER-PRESSURE (no phantom releases)

Protocol: teach A -> pre -> scratch -> teach B -> SILENT (no revise) ->
churn mode 2 (pool fills: 12 fills + 48 drops) -> revise (8 conflicts ->
pool full -> 8 drops; the displaced old values never reach the pool) ->
careful consolidate -> post-test.
Adversary information set: W1's setup, the 3-conjunct release rule, A1 [B].
Attack hypothesis: consolidation releases on key-match alone (phantom
releases of slots whose entries do not match the log's old_value), or the
old_value conjunct misfires under the novel cause -> releases>0.
Survival prediction [A+B]: the old values were dropped, never installed,
so no pool entry matches (key + old_value) -> releases==0, av==0, ai==0;
cf==88 (20+60+8), ev==0, drop==56 (48+8), a_released==0, ret==100,
post==35, rawA==35, bacc==20, lcheck==12, pre==35.

### Considered and not run (honest negative attack surface)

- Fooling CAREFUL consolidation into releasing an A entry: the release
  gate's first conjunct is membership in the learner's own revision log,
  which no world step can write (only `learner_revise` appends, and only
  for the learner's scratch keys 5001..5008). From the published interface
  the adversary could not construct this attack; the log gate is not
  world-writable. Recorded as unattempted, not as passed.
- Churn-between-revise-and-consolidate (belief desync): fizzles on the
  published interface, because no churn driver addresses the learner's
  keyspace (single key 3999; multi-owner modes provably avoid scratch keys
  per UNPIN-M3's lcheck=12). The world cannot move the learner's beliefs.
- Double consolidation within one episode: degenerate learner pathology,
  outside the threat model (the frozen learner is trusted; the adversary
  attacks world-novelty, not learner self-sabotage).

## Frozen kill bars

R offsets: W1 -> 1568, W2 -> 1632, W3 -> 1696, W4 -> 1760 (64-byte stride,
same 13-column layout as run_cond_h3 rows). In-band S-lines compute
against these frozen values; the governing verdict is the external worker
check (same reading as H3B's K20 note).

- S0 IDENTITY (external): the 39 pre-existing COND lines are byte-identical
  to reclamation_h3b/run1.txt (first 39 `^COND=` lines), AND 3/3 runs are
  byte-identical (sha256 equal). Else VOID: the mechanism moved or the
  build is nondeterministic; the sealed test is invalid.
- S1 W1-NORECLAIM: ev==0 AND drop==48 AND cf==80.
- S2 W1-SILENCE: releases==0 AND av==0 AND ai==0 AND a_released==0.
- S3 W1-INTACT: pre==35 AND post==35 AND ret==100 AND rawA==35 AND
  bacc==20 AND lcheck==12.
- S4 W2-NODOUBLESPEND: ev==8 AND drop==44 AND cf==84.
- S5 W2-EPISODES: releases==8 AND av==8 AND ai==0 AND a_released==0.
- S6 W2-INTACT: pre==35 AND post==35 AND ret==100 AND rawA==35 AND
  bacc==20 AND lcheck==12.
- S7 W3-RELEASENOTDEATH: releases==13 AND av==8 AND ai==5 AND
  a_released==5 AND ev==0 AND drop==16 AND cf==48.
- S8 W3-INTACT: pre==35 AND post==35 AND ret==100 AND rawA==35 AND
  bacc==20 AND lcheck==12.
- S9 W4-NOPHANTOM: releases==0 AND av==0 AND ai==0 AND ev==0 AND
  drop==56 AND cf==88 AND a_released==0.
- S10 W4-INTACT: pre==35 AND post==35 AND ret==100 AND rawA==35 AND
  bacc==20 AND lcheck==12.

Verdict: SEALED-PASS iff S0..S10 all hold. S0 failure -> VOID (terminal).
Any S1..S10 failure names the bar and yields SEALED-FAIL: the adversary
wins that world, i.e. a published decision-authority claim did not
generalize to a sealed post-freeze world. Thresholds are frozen; they are
not moved after results.

## Discrimination design

- S0 bars the moved-mechanism confound and the nondeterminism confound
  (VOID, not FAIL).
- S1 is the pressure generalization of K18: a hidden auto-reclaim path
  would show ev>0 exactly here (48 drops with ev=0 is a strong, falsifiable
  shape).
- S4 is the flag-lifecycle probe H3 never ran: stale release flags would
  show ev=16 (double-spend) instead of 8; a leak would show releases != 8.
- S7 dissociates release from eviction for the first time: 5 critical
  entries released but present. If release damaged reads, ret<100.
- S9 tests the old_value conjunct under a novel cause (drops instead of
  installs). Phantom releases would show releases>0.
- S2/S3/S5/S6/S8/S10 are the intactness preconditions: if the world setup
  itself disturbed knowledge, the outcome bars would be vacuous.

## What this does NOT test (honest accounting)

- The adversary is the worker in a second hat (see honesty statement).
  The seal is procedural (post-freeze design, published-interface-only
  hypotheses, frozen predictions, mechanism identity proof), not a second
  mind.
- The learner remains simulated; only the release-decision authority is
  probed, not learner intelligence.
- INCORPORATED/SUPERSEDED reasons remain unexercised (same code path,
  reason codes 2/3 never emitted); the successful-episode importance
  source from the H1 follow-ups remains unrun.
- A bar failure caused by a builder derivation error (wrong [B] number)
  is still SEALED-FAIL per the frozen bars; the report must root-cause it
  as derivation error vs mechanism surprise, without moving the bar.

## Commit order

PREREG.md + NAMECHECK.md commit strictly first, alone. Implementation
(new source file with verbatim mechanism + new drivers), the runs
(run1/2/3.txt), and REPORT.md only after. Commit-order self-check: this
prereg commit must strictly precede the implementation commit and the runs.
